from typing import List, Dict, Set, Tuple
from datetime import date, timedelta
from src.data.models import TaxLot
from src.optimiser.tax_lot_manager import TaxLotManager

class TaxOptimiser:
    def __init__(self, 
                 tax_lot_manager: TaxLotManager,
                 wash_sale_window_days: int = 30,
                 short_term_tax_rate: float = 0.30,
                 long_term_tax_rate: float = 0.15):
        self.tax_lot_manager = tax_lot_manager
        self.wash_sale_window_days = wash_sale_window_days
        self.short_term_tax_rate = short_term_tax_rate
        self.long_term_tax_rate = long_term_tax_rate
        
        # Keep track of recent realized losses: Portfolio -> Ticker -> Date of loss
        self.recent_losses: Dict[str, Dict[str, date]] = {}
        
    def record_realized_loss(self, portfolio_id: str, ticker: str, loss_date: date):
        """Record a realized loss for wash-sale tracking."""
        if portfolio_id not in self.recent_losses:
            self.recent_losses[portfolio_id] = {}
        self.recent_losses[portfolio_id][ticker] = loss_date
        
    def check_wash_sale_violation(self, portfolio_id: str, ticker: str, target_trade_shares: float, current_date: date) -> bool:
        """
        Check if a proposed BUY trade violates the wash sale rule.
        Returns True if there's a violation (meaning we should block the trade).
        """
        if target_trade_shares <= 0:
            return False # Only buys can trigger wash sale on a prior loss
            
        recent_loss_date = self.recent_losses.get(portfolio_id, {}).get(ticker)
        if recent_loss_date:
            days_since_loss = (current_date - recent_loss_date).days
            if days_since_loss <= self.wash_sale_window_days:
                return True
        return False
        
    def block_pending_target_buys(self, portfolio_id: str, proposed_trades: Dict[str, float], current_date: date) -> List[str]:
        """
        Given proposed trades (positive for buys, negative for sells), identify buys that 
        are blocked by wash-sale rules.
        """
        blocked_tickers = []
        for ticker, shares in proposed_trades.items():
            if self.check_wash_sale_violation(portfolio_id, ticker, shares, current_date):
                blocked_tickers.append(ticker)
        return blocked_tickers
        
    def calculate_tax_impact(self, portfolio_id: str, ticker: str, shares_to_sell: float, current_price: float, current_date: date) -> Tuple[float, float, List[Tuple[TaxLot, float]]]:
        """
        Simulate selling shares using HIFO and calculate the tax impact.
        Returns:
            tax_liability (float): The total tax liability (negative if net loss)
            realized_gains (float): The gross realized gains (or loss)
            sold_lots (List): The lots that would be sold
        """
        # Execute HIFO sell
        sold_lots = self.tax_lot_manager.allocate_sell_hifo(portfolio_id, ticker, shares_to_sell)
        
        total_tax = 0.0
        total_gain = 0.0
        
        for lot, shares in sold_lots:
            proceeds = shares * current_price
            cost = shares * lot.cost_basis
            gain = proceeds - cost
            
            total_gain += gain
            
            if gain > 0:
                is_long_term = self.tax_lot_manager.is_long_term(lot, current_date)
                tax_rate = self.long_term_tax_rate if is_long_term else self.short_term_tax_rate
                total_tax += gain * tax_rate
            else:
                # Capital loss - assume it offsets gains at short-term rate for max tax shield value
                total_tax += gain * self.short_term_tax_rate
                
            # Record the loss for wash sale tracking
            if gain < 0:
                self.record_realized_loss(portfolio_id, ticker, current_date)
                
        return total_tax, total_gain, sold_lots
