from typing import List, Dict, Tuple
from datetime import date
from src.data.models import TaxLot
import pandas as pd

class TaxLotManager:
    """Manages inventory of tax lots, defaults to HIFO (Highest In, First Out) accounting."""
    
    def __init__(self, long_term_holding_days: int = 365):
        self.long_term_holding_days = long_term_holding_days
        # Portfolio -> Ticker -> List of TaxLot
        self.portfolios_lots: Dict[str, Dict[str, List[TaxLot]]] = {}
    
    def load_lots(self, lots_df: pd.DataFrame):
        """Loads tax lots from a dataframe containing portfolio_id, security_ticker, shares, cost_basis, acquisition_date."""
        for _, row in lots_df.iterrows():
            self.add_lot(
                row['portfolio_id'], 
                row['security_ticker'], 
                TaxLot(
                    security_ticker=row['security_ticker'],
                    shares=row['shares'],
                    cost_basis=row['cost_basis'],
                    acquisition_date=row['acquisition_date'] # Assumes this is a date or datetime object
                )
            )

    def add_lot(self, portfolio_id: str, ticker: str, lot: TaxLot):
        """Add a single lot to the manager."""
        if portfolio_id not in self.portfolios_lots:
            self.portfolios_lots[portfolio_id] = {}
        if ticker not in self.portfolios_lots[portfolio_id]:
            self.portfolios_lots[portfolio_id][ticker] = []
        self.portfolios_lots[portfolio_id][ticker].append(lot)
        
    def get_lots(self, portfolio_id: str, ticker: str) -> List[TaxLot]:
        """Get all lots for a specific portfolio and security."""
        return self.portfolios_lots.get(portfolio_id, {}).get(ticker, [])
        
    def is_long_term(self, lot: TaxLot, current_date: date) -> bool:
        """Determines if a tax lot is long-term."""
        holding_period = (current_date - lot.acquisition_date).days
        return holding_period >= self.long_term_holding_days

    def allocate_sell_hifo(self, portfolio_id: str, ticker: str, shares_to_sell: float) -> List[Tuple[TaxLot, float]]:
        """
        Allocate a sell order across available tax lots using HIFO.
        Returns a list of tuples: (Lot, shares_sold_from_lot)
        """
        lots = self.get_lots(portfolio_id, ticker)
        if not lots:
            raise ValueError(f"No tax lots found for {portfolio_id} - {ticker}")
            
        total_available = sum(lot.shares for lot in lots)
        if shares_to_sell > total_available + 1e-6: # Numerical tolerance
            raise ValueError(f"Cannot sell {shares_to_sell} shares; only {total_available} available.")
            
        # Sort HIFO: Highest cost basis first
        # In case of tie on cost basis, it naturally maintains list order, but we could add secondary sort if needed.
        sorted_lots = sorted(lots, key=lambda x: x.cost_basis, reverse=True)
        
        sold_lots = []
        remaining_to_sell = shares_to_sell
        
        for lot in sorted_lots:
            if remaining_to_sell <= 1e-6:
                break
                
            if lot.shares > 0:
                shares_taken = min(lot.shares, remaining_to_sell)
                sold_lots.append((lot, shares_taken))
                
                # Deduct from inventory
                lot.shares -= shares_taken
                remaining_to_sell -= shares_taken
                
        return sold_lots
