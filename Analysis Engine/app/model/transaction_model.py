from dataclasses import dataclass, asdict
from typing import Optional, List
import pandas as pd

# This dataclass mirrors the 56 fields defined in your generate_data.py script,
# providing strong typing and a clean way to represent a database record in Python.

@dataclass
class Transaction:
    """
    Represents a single transaction record from the 'transactions' table.
    The types reflect the SQLite types: INTEGER (int), REAL (float), TEXT (str).
    Optional is used for fields that might be NULL (e.g., CLOSEDDATE).
    """
    TRANSACTIONID: int
    REPORTNO: str
    REPORTDATE: str
    BRANCHID: int
    BRANCHNAME: str
    TRANSACTIONDATE: str
    TRANSACTIONTIME: str
    TRANSACTIONTYPE: str
    CONDUCTINGMANNER: str
    CURRENCYTYPE: str
    AMOUNTINBIRR: float
    AMOUNTINCURRENCY: float
    FULL_NAME: str
    OTHERNAME: str
    SEX: str
    BIRTHDATE: str
    IDCARDNO: str
    PASSPORTNO: Optional[str] # Made optional as these might sometimes be missing
    PASSPORTISSUEDBY: Optional[str]
    RESIDENCECOUNTRY: str
    ORIGINCOUNTRY: str
    OCCUPATION: str
    COUNTRY: str
    REGION: str
    CITY: str
    SUBCITY: str
    WOREDA: str
    HOUSENO: str
    POSTALCODE: Optional[str]
    BUSINESSMOBILENO: Optional[str]
    BUSSINESSTELNO: Optional[str]
    BUSINESSFAXNO: Optional[str]
    RESIDENCETELNO: Optional[str]
    EMAILADDRESS: str
    ACCOUNTNO: str
    ACCHOLDERBRANCH: str
    ACCOWNERNAME: str
    ACCOUNTTYPE: str
    OPENEDDATE: str
    BALANCEHELD: float
    BALANCEHELDDATE: str
    CLOSEDDATE: Optional[str]
    BENFULLNAME: str
    BENACCOUNTNO: str
    BENBRANCHID: int
    BENBRANCHNAME: str
    BENOWNERENTITY: Optional[str]
    BENCOUNTRY: str
    BENREGION: str
    BENCITY: str
    BENZONE: str
    BENWOREDA: str
    BENHOUSENO: str
    BENTELNO: str
    BENISENTITY: int

    # Class method to convert a database row (tuple or Row object) into a Transaction object
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Transaction':
        """Converts a tuple of row data into a Transaction dataclass instance."""
        # The order of fields must exactly match the column order in the DB and the dataclass definition
        return cls(*row)
    
    @classmethod
    def generate_transactions_dataframe(cls, transactions: List['Transaction']) -> pd.DataFrame:
        
        data_list = [asdict(t) for t in transactions]

        df = pd.DataFrame(data_list)

        return df
    
    def get_timestamp(self) -> pd.Timestamp:
        """Combines TRANSACTIONDATE and TRANSACTIONTIME into a single pd.Timestamp."""
        return pd.to_datetime(f"{self.TRANSACTIONDATE} {self.TRANSACTIONTIME}")