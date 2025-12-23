from app.configuration.schema_configuration import get_schema_configuration_settings
from app.repository.transaction_repository import get_all_transactions
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def preprocessing(df):
        if df is None or df.empty:
            return pd.DataFrame() 

        if 'TRANSACTIONDATE' in df.columns and 'TRANSACTIONTIME' in df.columns:
            combined_series = df['TRANSACTIONDATE'].astype(str) + ' ' + df['TRANSACTIONTIME'].astype(str)
            df['TIMESTAMP'] = pd.to_datetime(combined_series, errors='coerce', utc=True)
        
        for col in ['TRANSACTIONDATE', 'TRANSACTIONTIME', 'BIRTHDATE', 'OPENEDDATE', 'CLOSEDDATE']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)

        if 'TIMESTAMP' in df.columns:
            df.sort_values(by='TIMESTAMP', inplace=True)
            df.reset_index(drop=True, inplace=True)

        if 'AMOUNTINBIRR' in df.columns:
            df['BRENTFORDIGIT'] = df['AMOUNTINBIRR'].astype(str).str[0].astype(int, errors='ignore')

        now = pd.Timestamp.now(tz="UTC")
	
        if 'BIRTHDATE' in df.columns:
            pass #df['AGE'] = (now - df['BIRTHDATE']).dt.days // 365
	
        if 'OPENEDDATE' in df.columns:
            df['ACCOUNT_AGE_DAYS'] = (now - df['OPENEDDATE']).dt.days

        df['ACCOUNTNO'] = df['ACCOUNTNO'].astype(str)

        return df

def get_processed_data():

    schema = get_schema_configuration_settings()
    reversed_schema = {v: k for k, v in schema.items()}

    transactions = get_all_transactions(pandas_df=True)
    transactions.columns = [reversed_schema.get(name, name) for name in transactions.columns]
    
    transactions = preprocessing(transactions)

    usage = transactions.memory_usage(deep=True)
    usage_mb = usage / 1024**2
    """
    logging.info("-------------------MEMORY USAGE OF ALL TRANSACTION DF BY COLUMN--------------------------")
    logging.info(usage_mb.sort_values(ascending=False).head(5))
    logging.info(f"SUM OF SELECTED COLUMNS: {float(usage_mb.sort_values(ascending=False)[selected_columns].sum())}")
    """
    logging.info(f"-------------------TOTAL MEMORY USAGE OF ALL TRANSACTION {transactions.shape}---------------------------------")
    logging.info(f"Total size: {usage.sum() / 1024**2:.2f} MB")
    logging.info("-----------------------------------------------------------------------------------------")

    return transactions


if __name__ == "__main__":
    transactions = get_processed_data()