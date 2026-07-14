from typing import List, Dict
from datetime import date
from src.optimiser.tax_lot_manager import TaxLotManager

class TaxHarvestingScanner:
    """Proactively identifies harvestable losses to trigger out-of-cycle rebalances."""
    
    def __init__(self, 
                 tax_lot_manager: TaxLotManager, 
                 min_harvestable_loss_usd: float = 500.0, 
                 min_harvestable_loss_pct: float = 0.03):
        self.tax_lot_manager = tax_lot_manager
        self.min_harvestable_loss_usd = min_harvestable_loss_usd
        self.min_harvestable_loss_pct = min_harvestable_loss_pct
        
    def scan_portfolio(self, portfolio_id: str, current_prices: Dict[str, float]) -> List[Dict]:
        """
        Scans a single portfolio for harvestable losses.
        Returns a list of opportunities.
        """
        opportunities = []
        lots_by_ticker = self.tax_lot_manager.portfolios_lots.get(portfolio_id, {})
        
        for ticker, lots in lots_by_ticker.items():
            if ticker not in current_prices:
                continue
                
            current_price = current_prices[ticker]
            for lot in lots:
                if lot.shares <= 0:
                    continue
                    
                proceeds = lot.shares * current_price
                cost = lot.shares * lot.cost_basis
                gain = proceeds - cost
                
                # Check for loss
                if gain < 0:
                    loss_amount = abs(gain)
                    loss_pct = loss_amount / cost if cost > 0 else 0
                    
                    if loss_amount >= self.min_harvestable_loss_usd and loss_pct >= self.min_harvestable_loss_pct:
                        opportunities.append({
                            "portfolio_id": portfolio_id,
                            "ticker": ticker,
                            "lot": lot,
                            "loss_amount": loss_amount,
                            "loss_pct": loss_pct,
                            "suggested_action": "SELL_FOR_TAX_LOSS"
                        })
                        
        return opportunities
