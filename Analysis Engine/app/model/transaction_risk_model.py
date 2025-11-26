from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
import time
    
    
@dataclass
class TransactionRiskResult:
    """The final calculated risk and details for a single transaction."""
    transaction_id: str
    overall_risk_score: float
    risk_level: str  # e.g., 'Low', 'Medium', 'High'
    # Velocity: Score based on transaction frequency in a short time frame
    velocity_score: int
    # Geographical: Score based on distance/mismatch from usual location
    geographical_anomaly: int
    # Amount Deviation: Score based on deviation from user's typical amount profile
    amount_deviation: int
    generated_at: datetime = field(default_factory=datetime.now)
