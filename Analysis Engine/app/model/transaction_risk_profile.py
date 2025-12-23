from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy import Column, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

    
@dataclass
class TransactionRiskProfile(Base):
    __tablename__ = "transaction_risk_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column()
    time_window_1hr: Mapped[float] = mapped_column()
    time_window_24hr: Mapped[float] = mapped_column()
    time_window_7days: Mapped[float] = mapped_column()
    variance_24hr: Mapped[float] = mapped_column()
    variance_7days: Mapped[float] = mapped_column()
    z_score_individual: Mapped[float] = mapped_column()
    z_score_branch: Mapped[float] = mapped_column()
    z_score_population: Mapped[float] = mapped_column()
    percentile_branch: Mapped[float] = mapped_column()
    percentile_transaction_type: Mapped[float] = mapped_column()
    frequency_1hr: Mapped[int] = mapped_column()
    frequency_24hr: Mapped[int] = mapped_column()
    frequency_7days: Mapped[int] = mapped_column()
    turnover_ratio_24hr: Mapped[float] = mapped_column()
    turnover_ratio_7days: Mapped[float] = mapped_column()
    leading_digit_distribution: Mapped[str] = mapped_column()
    round_number_hoarding: Mapped[float] = mapped_column()
    transaction_geography_risk: Mapped[float] = mapped_column()
    overall_risk_score: Mapped[Optional[float]] = mapped_column()
    risk_level: Mapped[Optional[str]] = mapped_column()
    reason_codes: Mapped[Optional[str]] = mapped_column()

    from_account : Mapped[str] = mapped_column()
    from_name : Mapped[str] = mapped_column()
    to_account : Mapped[str] = mapped_column()
    to_name : Mapped[str] = mapped_column()
    amount : Mapped[float] = mapped_column()
    transaction_type : Mapped[str] = mapped_column()
    transaction_time : Mapped[str] = mapped_column()


    generated_at: datetime = Column(DateTime, default=datetime.now)
