import sqlite3
import pandas as pd
from typing import Optional, List
from app.model.risk_and_sanctions_models import CustomerRiskProfile
from dataclasses import dataclass
from app.config import customer_risk_profiles_table_name, test_database
from app.model.risk_and_sanctions_models import CustomerRiskProfile

class CustomerRiskRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.table_name = customer_risk_profiles_table_name
        
        self.columns = [field.name for field in CustomerRiskProfile.__dataclass_fields__.values()]
        self.column_names = ", ".join(self.columns)
        
    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error at {self.db_path}: {e}")
            raise

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            CUSTOMERID INTEGER PRIMARY KEY,
            ACCOUNTNO TEXT,
            DEMOGRAPHICS_RISK REAL,
            CUSTOMER_TYPE_RISK REAL,
            TRANSACTION_HISTORY_RISK REAL,
            RISKSCORE REAL,
            RISKLEVEL TEXT,
            REVIEWFREQUENCY_DAYS INTEGER,
            LASTREVIEWDATE TEXT,
            NEXTREVIEWDATE TEXT,
            REASONCODES_JSON TEXT,
            STATUS TEXT,
            CREATED_AT TEXT,
            UPDATED_AT TEXT
        )
        """
        try:
            with self._connect() as conn:
                conn.execute(sql)
                conn.commit()
        except Exception as e:
            print(f"Error creating table {self.table_name}: {e}")
            raise

    def insert_or_update_profile(self, profile):
        placeholders = ', '.join(['?' for _ in self.columns])
        
        update_set = ", ".join([f"{col}=excluded.{col}" for col in self.columns if col not in ['CUSTOMERID', 'CREATED_AT']])
        
        sql = f"""
        INSERT INTO {self.table_name} ({self.column_names})
        VALUES ({placeholders})
        ON CONFLICT(CUSTOMERID) DO UPDATE SET {update_set}
        """
        
        values = tuple(getattr(profile, col) for col in self.columns)
        
        try:
            with self._connect() as conn:
                conn.execute(sql, values)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting/updating profile for ID {profile.CUSTOMERID}: {e}")
            return False

    def find_by_customer_id(self, customer_id):
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE CUSTOMERID = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (customer_id,))
                row = cursor.fetchone()
                if row:
                    return CustomerRiskProfile.from_db_row(row)
                return None
        except Exception as e:
            print(f"Error finding profile by ID {customer_id}: {e}")
            return None

    def get_profiles_by_risk_level(self, risk_level):
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE RISKLEVEL = ? ORDER BY RISKSCORE DESC"
        profiles = []
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (risk_level,))
                rows = cursor.fetchall()
                for row in rows:
                    profiles.append(CustomerRiskProfile.from_db_row(row))
                return profiles
        except Exception as e:
            print(f"Error fetching profiles by risk level {risk_level}: {e}")
            return []

if __name__ == '__main__':
    
    DB_FILE = test_database
    repo = CustomerRiskRepository(DB_FILE)
    repo.create_table()
    
    profile_data = {
        'CUSTOMERID': 1001,
        'ACCOUNTNO': 'ACC001',
        'DEMOGRAPHICS_RISK': 20.0,
        'CUSTOMER_TYPE_RISK': 15.0,
        'TRANSACTION_HISTORY_RISK': 50.0,
        'RISKSCORE': 65.0,
        'RISKLEVEL': 'High',
        'REVIEWFREQUENCY_DAYS': 90,
        'LASTREVIEWDATE': '2025-11-01',
        'NEXTREVIEWDATE': '2026-01-30',
        'REASONCODES_JSON': '["high_cash_vol"]',
        'STATUS': 'Active',
        'CREATED_AT': '2025-10-01',
        'UPDATED_AT': '2025-11-01'
    }

    profile = CustomerRiskProfile(**profile_data)
    
    print("--- Testing Customer Risk Repository ---")
    
    if repo.insert_or_update_profile(profile):
        print(f"Inserted profile for Customer ID {profile.CUSTOMERID}.")
    
    found_profile = repo.find_by_customer_id(1001)
    if found_profile:
        print(f"Found profile. Risk Score: {found_profile.RISKSCORE}, Level: {found_profile.RISKLEVEL}")
    
    high_risk_profiles = repo.get_profiles_by_risk_level('High')
    print(f"Found {len(high_risk_profiles)} 'High' risk profiles.")
    if high_risk_profiles:
        print(f"Sample High Risk Account: {high_risk_profiles[0].ACCOUNTNO}")