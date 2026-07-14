from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date

class Security(BaseModel):
    ticker: str
    asset_class: str
    sub_asset_class: str
    sector: str
    geography: str
    current_price: float
    volatility: float
    expected_return: float

class TaxLot(BaseModel):
    security_ticker: str
    shares: float
    cost_basis: float
    acquisition_date: date

class Position(BaseModel):
    security_ticker: str
    total_shares: float
    current_value: float
    tax_lots: List[TaxLot]

class ClientProfile(BaseModel):
    client_id: str
    risk_category: str
    tax_bracket: float
    restricted_securities: List[str] = Field(default_factory=list)
    esg_screen: bool = False
    target_allocations: Dict[str, float]
    drift_band: float

class Portfolio(BaseModel):
    portfolio_id: str
    client: ClientProfile
    positions: List[Position]
    cash_balance: float
    total_value: float

    def get_allocation(self) -> Dict[str, float]:
        # Returns current weights across asset classes
        allocs = {"Cash": self.cash_balance / self.total_value}
        # In a real system, this would join with the Security Master to aggregate by asset_class
        return allocs

class MarketData(BaseModel):
    date: date
    prices: Dict[str, float]
    vix_level: float
