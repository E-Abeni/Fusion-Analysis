from app.database.database import Base
from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, Text, Boolean

@dataclass
class WatchListEntry(Base):
    __tablename__ = 'watch_list'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    Entry_Type: Mapped[str] = mapped_column(String(50))
    FirstName: Mapped[str] = mapped_column(String(100))
    LastName: Mapped[str] = mapped_column(String(100))
    DateOfBirth: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    PlaceOfBirth: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    Nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    PassportNumber: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    EntityName: Mapped[str] = mapped_column(String(255))
    RegistrationCountry: Mapped[str] = mapped_column(String(100))
    RegistrationID: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    Address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    Industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    FormerName: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    DesignationDate: Mapped[Date] = mapped_column(Date)
    LastUpdatedDate: Mapped[Date] = mapped_column(Date, nullable=True)
    ReasonSummary: Mapped[str] = mapped_column(Text, nullable=True)
    IsActive: Mapped[bool] = mapped_column(Boolean, default=True)