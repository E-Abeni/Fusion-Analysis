from dataclasses import dataclass, asdict
from typing import Optional, List
import pandas as pd
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.configuration.connections_configuration import get_database_connection_settings

@dataclass
class Transaction(Base):
    __tablename__ = get_database_connection_settings().get('table_name', 'transactions')
        
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    TRANSACTIONID: Mapped[int] = mapped_column()
    REPORTNO: Mapped[Optional[str]] = mapped_column()
    REPORTDATE: Mapped[Optional[str]] = mapped_column()
    BRANCHID: Mapped[int] = mapped_column()
    BRANCHNAME: Mapped[str] = mapped_column()
    TRANSACTIONDATE: Mapped[str] = mapped_column()
    TRANSACTIONTIME: Mapped[str] = mapped_column()
    TRANSACTIONTYPE: Mapped[str] = mapped_column()
    CONDUCTINGMANNER: Mapped[str] = mapped_column()
    CURRENCYTYPE: Mapped[Optional[str]] = mapped_column()
    AMOUNTINBIRR: Mapped[float] = mapped_column()
    AMOUNTINCURRENCY: Mapped[Optional[float]] = mapped_column()
    FULL_NAME: Mapped[str] = mapped_column()
    OTHERNAME: Mapped[Optional[str]] = mapped_column()
    SEX: Mapped[str] = mapped_column()
    BIRTHDATE: Mapped[Optional[str]] = mapped_column()
    IDCARDNO: Mapped[Optional[str]] = mapped_column()
    PASSPORTNO: Mapped[Optional[str]] = mapped_column()
    PASSPORTISSUEDBY: Mapped[Optional[str]] = mapped_column()
    RESIDENCECOUNTRY: Mapped[Optional[str]] = mapped_column()
    ORIGINCOUNTRY: Mapped[Optional[str]] = mapped_column()
    OCCUPATION: Mapped[str] = mapped_column()
    COUNTRY: Mapped[str] = mapped_column()
    REGION: Mapped[str] = mapped_column()
    CITY: Mapped[str] = mapped_column()
    SUBCITY: Mapped[Optional[str]] = mapped_column()
    WOREDA: Mapped[Optional[str]] = mapped_column()
    HOUSENO: Mapped[Optional[str]] = mapped_column()
    POSTALCODE: Mapped[Optional[str]] = mapped_column()
    BUSINESSMOBILENO: Mapped[Optional[str]] = mapped_column()
    BUSSINESSTELNO: Mapped[Optional[str]] = mapped_column()
    BUSINESSFAXNO: Mapped[Optional[str]] = mapped_column()
    RESIDENCETELNO: Mapped[Optional[str]] = mapped_column()
    EMAILADDRESS: Mapped[Optional[str]] = mapped_column()
    ACCOUNTNO: Mapped[str] = mapped_column()
    ACCHOLDERBRANCH: Mapped[str] = mapped_column()
    ACCOWNERNAME: Mapped[str] = mapped_column()
    ACCOUNTTYPE: Mapped[str] = mapped_column()
    OPENEDDATE: Mapped[str] = mapped_column()
    BALANCEHELD: Mapped[float] = mapped_column()
    BALANCEHELDDATE: Mapped[str] = mapped_column()
    CLOSEDDATE: Mapped[Optional[str]] = mapped_column()
    BENFULLNAME: Mapped[str] = mapped_column()
    BENACCOUNTNO: Mapped[str] = mapped_column()
    BENBRANCHID: Mapped[Optional[int]] = mapped_column()
    BENBRANCHNAME: Mapped[Optional[str]] = mapped_column()
    BENOWNERENTITY: Mapped[Optional[str]] = mapped_column()
    BENCOUNTRY: Mapped[str] = mapped_column()
    BENREGION: Mapped[str] = mapped_column()
    BENCITY: Mapped[str] = mapped_column()
    BENZONE: Mapped[Optional[str]] = mapped_column()
    BENWOREDA: Mapped[Optional[str]] = mapped_column()
    BENHOUSENO: Mapped[Optional[str]] = mapped_column()
    BENTELNO: Mapped[Optional[str]] = mapped_column()
    BENISENTITY: Mapped[int] = mapped_column()
    
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Transaction':
        return cls(*row)
    

    @classmethod
    def generate_transactions_dataframe(cls, transactions: List['Transaction']) -> pd.DataFrame:
        data_list = [asdict(t) for t in transactions]
        df = pd.DataFrame(data_list)
        return df
    

    def get_timestamp(self) -> pd.Timestamp:
        return pd.to_datetime(f"{self.TRANSACTIONDATE} {self.TRANSACTIONTIME}")