from app.model.transaction import Transaction
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData, select, Column
from sqlalchemy.exc import NoSuchTableError
from app.database.database import get_central_db_engine
import pandas as pd
from app.configuration.connections_configuration import get_database_connection_settings
from app.configuration.schema_configuration import get_schema_configuration_settings

engine = get_central_db_engine()
METADATA = MetaData()
table_name = get_database_connection_settings().get('database_table_name', 'transactions')
schema = get_schema_configuration_settings()

selected_columns = [
        'TRANSACTIONDATE', 'TRANSACTIONTIME', 'BIRTHDATE', 'OPENEDDATE', 'CLOSEDDATE', 'AMOUNTINBIRR', 'ACCOUNTNO',
        'BRANCHNAME', 'TRANSACTIONTYPE', 'BENACCOUNTNO', 'BENREGION', "IDCARDNO", "PASSPORTNO", "OCCUPATION",
        "REGION", "FULL_NAME", "BENFULLNAME"
    ]
reverse_selected_columns = [schema.get(column_name, column_name) for column_name in selected_columns]


try:
    table = Table(table_name, METADATA, autoload_with=engine)
    cols_to_select = [table.c[col] for col in reverse_selected_columns if col in table.c]
    print(f"[Transaction Repository] Table '{table_name}' metadata loaded successfully.")
    
except NoSuchTableError:
    print(f"[Transaction Repository] Error: Table '{table_name}' does not exist in the database.")

def get_all_transactions(pandas_df=False):
    with Session(engine) as session:
        #transactions = session.query(Transaction).all()
        stmt = select(*cols_to_select)
        result = session.execute(stmt)
        columns = result.keys()
        transactions = result.all()
    if pandas_df:
        df = pd.DataFrame(transactions, columns=columns)
        return df
    return (transactions, columns)


def get_transaction_by_column(column_name, value, all=True, pandas_df=False):
    with Session(engine) as session:
        search_column: Column = table.columns[schema.get(column_name, column_name)]
        stmt = select(table).where( search_column == value)
        
        result = session.execute(stmt)
        columns = result.keys()
        
        transactions = result.fetchall()
        #transaction = session.query(Transaction).filter(Transaction.TRANSACTIONID == transaction_id).first()
    if pandas_df:
        df = pd.DataFrame(transactions, columns=columns)
        if all:
            return df
        return df.iloc[0]
    
    if all:
        return transactions, columns
    return transactions[0], columns

def insert_transaction(transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()

def update_transaction(transaction):
    with Session(engine) as session:
        existing_transaction = session.query(Transaction).filter(Transaction.TRANSACTIONID == transaction.TRANSACTIONID).first()
        if existing_transaction:
            for key, value in transaction.__dict__.items():
                setattr(existing_transaction, key, value)
            session.commit()

def delete_transaction(transaction_id):
    with Session(engine) as session:
        transaction = session.query(Transaction).filter(Transaction.TRANSACTIONID == transaction_id).first()
        if transaction:
            session.delete(transaction)
            session.commit()

def insert_transactions_bulk(transactions):
    with Session(engine) as session:
        session.bulk_save_objects(transactions)
        session.commit()

def get_transactions_by_account(account_no):
    with Session(engine) as session:
        transactions = session.query(Transaction).filter(Transaction.ACCOUNTNO == account_no).all()
    return transactions

def get_transactions_in_time_range(start_time, end_time):
    with Session(engine) as session:
        transactions = session.query(Transaction).filter(
            Transaction.TRANSACTIONDATE >= start_time,
            Transaction.TRANSACTIONDATE <= end_time
        ).all()
    return transactions



if __name__ == "__main__":
    print(reverse_selected_columns)