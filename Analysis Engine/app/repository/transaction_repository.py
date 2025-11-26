import sqlite3
import pandas as pd
from typing import Optional, List
from app.model.transaction_model import Transaction
from app.config import test_database, test_data_limit, transactions_data_limit

class TransactionRepository:
    """
    Manages database operations for the Transaction model.
    This class is responsible for all interaction with the SQLite database.
    """
    def __init__(self, db_path: str):
        """Initializes the repository with the path to the database file."""
        self.db_path = db_path
        self.table_name = 'transactions'
        
        # Get the ordered list of column names from the model
        self.columns = [field.name for field in Transaction.__dataclass_fields__.values()]
        self.column_names = ", ".join(self.columns)
        
        # Set row factory for easy access by column name
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.dict_factory = dict_factory

    def _connect(self) -> sqlite3.Connection:
        """Establishes and returns a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            # Ensure the connection is set to return column names in results for better error checking
            # We use default tuple factory here, relying on the 'from_db_row' for conversion
            return conn
        except sqlite3.Error as e:
            # Handle connection errors gracefully
            print(f"Database connection error at {self.db_path}: {e}")
            raise

    def get_all_transactions(self, limit: int = transactions_data_limit) -> List[Transaction]:
        """Fetches a limited number of all transactions."""
        sql = f"SELECT {self.column_names} FROM {self.table_name} LIMIT ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (limit,))
                rows = cursor.fetchall()
                return [Transaction.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Error fetching all transactions: {e}")
            return []
            
    def find_by_transaction_id(self, transaction_id: int) -> Optional[Transaction]:
        """Finds a transaction by its primary key (TRANSACTIONID)."""
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE TRANSACTIONID = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (transaction_id,))
                row = cursor.fetchone()
                if row:
                    return Transaction.from_db_row(row)
                return None
        except Exception as e:
            print(f"Error finding transaction by ID {transaction_id}: {e}")
            return None

    def find_by_account_no(self, account_no: str) -> List[Transaction]:
        """Finds all transactions associated with a specific ACCOUNTNO."""
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE ACCOUNTNO = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (account_no,))
                rows = cursor.fetchall()
                return [Transaction.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Error finding transactions by Account No {account_no}: {e}")
            return []

    # Example of a simple write operation (demonstrating the pattern)
    def update_transaction_type(self, transaction_id: int, new_type: str) -> bool:
        """Updates the TRANSACTIONTYPE for a given ID."""
        sql = f"UPDATE {self.table_name} SET TRANSACTIONTYPE = ? WHERE TRANSACTIONID = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (new_type, transaction_id))
                conn.commit()
                return cursor.rowcount > 0 # Returns True if a row was updated
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return False
    
    def get_pandas_df(self, limit=transactions_data_limit):
        """Fetches transactions as a pandas DataFrame."""
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table_name} LIMIT ?"
        try:
            with self._connect() as conn:
                df = pd.read_sql_query(sql, conn, params=(limit,))
                return df
        except Exception as e:
            print(f"Error fetching transactions as DataFrame: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error


    # This is often the logic you would use in a dedicated test file:
    @classmethod
    def setup_in_memory_db(cls, schema: str):
        """Helper to create an in-memory database connection for testing."""
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        conn.executescript(schema)
        conn.commit()
        return conn

# --- Example Usage (requires running generate_data.py first) ---

if __name__ == '__main__':
    # NOTE: Run 'python generate_data.py' once to create transactions.db
    
    DB_FILE = test_database
    
    # 1. Initialize the Repository
    repo = TransactionRepository(DB_FILE)
    
    print("--- Testing Repository Access ---")
    
    # 2. Test fetching all (a sample)
    all_txns = repo.get_all_transactions(limit=test_data_limit)
    print(f"Found {len(all_txns)} sample transactions.")
    if all_txns:
        sample_txn = all_txns[0]
        print(f"Sample Transaction ID: {sample_txn.TRANSACTIONID}, Type: {sample_txn.TRANSACTIONTYPE}")

        # 3. Test finding by ID
        found_txn = repo.find_by_transaction_id(sample_txn.TRANSACTIONID)
        if found_txn:
            print(f"Found Transaction by ID {found_txn.TRANSACTIONID}. Full Name: {found_txn.FULL_NAME}")
            
            # 4. Test updating a record
            original_type = found_txn.TRANSACTIONTYPE
            new_type = "TEST_UPDATE"
            if repo.update_transaction_type(found_txn.TRANSACTIONID, new_type):
                print(f"Updated Transaction ID {found_txn.TRANSACTIONID} type to '{new_type}'.")
                
                # 5. Verify the update
                verified_txn = repo.find_by_transaction_id(found_txn.TRANSACTIONID)
                if verified_txn and verified_txn.TRANSACTIONTYPE == new_type:
                    print(f"Verification successful: Type is now '{verified_txn.TRANSACTIONTYPE}'.")
                    # Clean up: set it back to original type (or close connection if only reading)
                    repo.update_transaction_type(found_txn.TRANSACTIONID, original_type)
        else:
            print(f"Could not find transaction with ID {sample_txn.TRANSACTIONID} for testing.")
    else:
        print("No transactions found. Did you run 'generate_data.py'?")