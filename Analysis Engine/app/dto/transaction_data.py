from dataclasses import dataclass, asdict
from typing import Optional, List
import pandas as pd

@dataclass
class TransactionDataDTO:
    #ID: Optional[int] = None
    TRANSACTIONID: str
    REPORTNO: Optional[str]
    REPORTDATE: Optional[str]
    BRANCHID: str
    BRANCHNAME: str
    TRANSACTIONDATE: str
    TRANSACTIONTIME: str
    TRANSACTIONTYPE: str
    CONDUCTINGMANNER: str
    CURRENCYTYPE: Optional[str]
    AMOUNTINBIRR: float
    AMOUNTINCURRENCY: Optional[float]
    FULL_NAME: str
    OTHERNAME: Optional[str]
    SEX: str
    BIRTHDATE: Optional[str]
    IDCARDNO: Optional[str]
    PASSPORTNO: Optional[str]
    PASSPORTISSUEDBY: Optional[str]
    RESIDENCECOUNTRY: Optional[str]
    ORIGINCOUNTRY: Optional[str]
    OCCUPATION: str
    COUNTRY: str
    REGION: str
    CITY: str
    SUBCITY: Optional[str]
    WOREDA: Optional[str]
    HOUSENO: Optional[str]
    POSTALCODE: Optional[str]
    BUSINESSMOBILENO: Optional[str]
    BUSSINESSTELNO: Optional[str]
    BUSINESSFAXNO: Optional[str]
    RESIDENCETELNO: Optional[str]
    EMAILADDRESS: Optional[str]
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
    BENBRANCHID: Optional[str]
    BENBRANCHNAME: Optional[str]
    BENOWNERENTITY: Optional[str]
    BENCOUNTRY: str
    BENREGION: str
    BENCITY: str
    BENZONE: Optional[str]
    BENWOREDA: Optional[str]
    BENHOUSENO: Optional[str]
    BENTELNO: Optional[str]
    BENISENTITY: str

    @classmethod
    def generate_transactions_dataframe(cls, transactions: List['TransactionDataDTO']) -> pd.DataFrame:
        data_list = [asdict(t) for t in transactions]
        df = pd.DataFrame(data_list)
        return df
    
    def generate_transaction_series(cls, transaction: TransactionDataDTO) -> pd.Series:
        data = asdict(transaction)
        ps = pd.Series(data)

        return ps

    def get_timestamp(self) -> pd.Timestamp:
        return pd.to_datetime(f"{self.TRANSACTIONDATE} {self.TRANSACTIONTIME}")