import sqlite3
import pandas as pd
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from app.model.transaction_risk_model import TransactionRiskResult
from app.config import transaction_risk_results_table_name, test_database

class TransactionRiskRepository:
    """
    Manages database operations for the TransactionRiskResult model.
    Stores and retrieves the output of the transaction monitoring model.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.table_name = transaction_risk_results_table_name
        
        # NOTE: Columns list must include the flattened RiskBreakdown fields 
        # for a simple flat table structure
        self.columns = [
            'transaction_id', 'overall_risk_score', 'risk_level', 
            'velocity_score', 'geographical_anomaly', 'amount_deviation',
            'generated_at'
        ]
        self.column_names = ", ".join(self.columns)
        
    def _connect(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error at {self.db_path}: {e}")
            raise

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            transaction_id TEXT PRIMARY KEY,
            overall_risk_score REAL,
            risk_level TEXT,
            velocity_score INTEGER,
            geographical_anomaly INTEGER,
            amount_deviation INTEGER,
            generated_at TEXT
        )
        """
        try:
            with self._connect() as conn:
                conn.execute(sql)
                conn.commit()
        except Exception as e:
            print(f"Error creating table {self.table_name}: {e}")
            raise

    def insert_result(self, result: TransactionRiskResult) -> bool:
        sql = f"""
        INSERT INTO {self.table_name} ({self.column_names})
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(transaction_id) DO UPDATE SET
            overall_risk_score=excluded.overall_risk_score,
            risk_level=excluded.risk_level,
            velocity_score=excluded.velocity_score,
            geographical_anomaly=excluded.geographical_anomaly,
            amount_deviation=excluded.amount_deviation,
            generated_at=excluded.generated_at
        """
        values = (
            result.transaction_id,
            result.overall_risk_score,
            result.risk_level,
            result.velocity_score,
            result.geographical_anomaly,
            result.amount_deviation,
            result.generated_at.isoformat()
        )
        try:
            with self._connect() as conn:
                conn.execute(sql, values)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting risk result for {result.transaction_id}: {e}")
            return False

    def get_result_by_id(self, transaction_id: str) -> Optional[TransactionRiskResult]:
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE transaction_id = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (transaction_id,))
                row = cursor.fetchone()
                if row:
                    # Map the flat row back to the nested dataclass structure
                    (
                        tx_id, overall_score, level, 
                        vel, geo, amt, generated
                    ) = row
                                           
                    
                    return TransactionRiskResult(
                        transaction_id=tx_id,
                        overall_risk_score=overall_score,
                        risk_level=level,
                        velocity_score=vel,
                        geographical_anomaly=geo,
                        amount_deviation=amt,
                        generated_at=datetime.fromisoformat(generated)
                    )
                return None
        except Exception as e:
            print(f"Error finding risk result by ID {transaction_id}: {e}")
            return None

    def get_high_risk_results(self, limit: int = 100) -> List[TransactionRiskResult]:
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE overall_risk_score >= 80.0 ORDER BY generated_at DESC LIMIT ?"
        results = []
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (limit,))
                rows = cursor.fetchall()
                for row in rows:
                    (
                        tx_id, overall_score, level, 
                        vel, geo, amt, generated
                    ) = row
                    
                    
                    results.append(TransactionRiskResult(
                        transaction_id=tx_id,
                        overall_risk_score=overall_score,
                        risk_level=level,
                        velocity_score=vel,
                        geographical_anomaly=geo,
                        amount_deviation=amt,
                        generated_at=datetime.fromisoformat(generated)
                    ))
                return results
        except Exception as e:
            print(f"Error fetching high risk results: {e}")
            return []

    def get_pandas_df(self, limit=100) -> pd.DataFrame:
        sql = f"SELECT {self.column_names} FROM {self.table_name} LIMIT ?"
        try:
            with self._connect() as conn:
                df = pd.read_sql_query(sql, conn, params=(limit,))
                return df
        except Exception as e:
            print(f"Error fetching risk results as DataFrame: {e}")
            return pd.DataFrame() 

# --- Example Usage ---

if __name__ == '__main__':
    
    DB_FILE = test_database
    
    # 1. Initialize the Repository
    repo = TransactionRiskRepository(DB_FILE)
    repo.create_table()
    
   
    test_result = TransactionRiskResult(
        transaction_id="TXN_12345",
        overall_risk_score=83.5,
        risk_level='High',
        velocity_score=95,
        geographical_anomaly=70,
        amount_deviation=85,
    )
    
    
    test_result_low = TransactionRiskResult(
        transaction_id="TXN_67890",
        overall_risk_score=13.5,
        risk_level='Low',
        velocity_score=10,
        geographical_anomaly=5,
        amount_deviation=15,
    )

    print("--- Testing Repository Access ---")
    
    # 3. Test insertion
    if repo.insert_result(test_result):
        print(f"Inserted/Updated high risk result for {test_result.transaction_id}.")
    
    if repo.insert_result(test_result_low):
        print(f"Inserted/Updated low risk result for {test_result_low.transaction_id}.")
        
    # 4. Test finding by ID
    found_result = repo.get_result_by_id(test_result.transaction_id)
    if found_result:
        print(f"Found Result by ID {found_result.transaction_id}. Risk: {found_result.overall_risk_score:.1f}, Level: {found_result.risk_level}")
        print(f"Breakdown: Velocity={found_result.velocity_score}, Geo={found_result.geographical_anomaly}")
    
    # 5. Test getting high risk transactions
    high_risk_list = repo.get_high_risk_results(limit=5)
    print(f"\nFound {len(high_risk_list)} high risk transactions.")
    if high_risk_list:
        print(f"Sample High Risk ID: {high_risk_list[0].transaction_id}, Score: {high_risk_list[0].overall_risk_score}")
        
    # 6. Test getting DataFrame
    df = repo.get_pandas_df(limit=5)
    print("\n--- DataFrame Sample ---")
    print(df.head())