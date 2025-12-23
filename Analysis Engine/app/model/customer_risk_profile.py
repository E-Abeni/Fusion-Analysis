from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

@dataclass
class CustomerRiskProfile(Base):
    __tablename__ = 'customer_risk_profiles'

    Profile_ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Customer_ID: Mapped[Optional[int]] = mapped_column()             
    Account_No: Mapped[str] = mapped_column()  
    Full_Name: Mapped[str] = mapped_column()
    PEER_PROFILE_OCCUPATION: Mapped[str] = mapped_column()
    PEER_PROFILE_REGION: Mapped[str] = mapped_column()
    PEER_PROFILE_ACCOUNT_AGE: Mapped[str] = mapped_column()
    TIME_SERIES_GAP: Mapped[str] = mapped_column()
    KYC_INTEGRITY_UNIQUENESS: Mapped[str] = mapped_column()   
    KYC_INTEGRITY_COMPLETENESS_RATIO: Mapped[float] = mapped_column()        
    DEMOGRAPHICS_RISK: Mapped[str] = mapped_column()
    SANCTION_HITS: Mapped[str] = mapped_column()
    WATCHLIST_HITS: Mapped[str] = mapped_column()
    PEP_HITS: Mapped[str] = mapped_column()
    RISK_SCORE: Mapped[Optional[float]] = mapped_column()            
    RISK_LEVEL: Mapped[Optional[str]] = mapped_column()             
    REVIEW_FREQUENCY_DAYS: Mapped[int] = mapped_column()  
    LAST_REVIEW_DATE: Mapped[str] = mapped_column()         
    NEXT_REVIEW_DATE: Mapped[str] = mapped_column()       
    REASON_CODES_JSON: Mapped[str] = mapped_column()      
    STATUS: Mapped[str] = mapped_column()          
    CREATED_AT: Mapped[str] = mapped_column()
    UPDATED_AT: Mapped[str] = mapped_column()

    account_age: Mapped[str] = mapped_column()
    occupation: Mapped[str] = mapped_column() 
    region: Mapped[str] = mapped_column()

    