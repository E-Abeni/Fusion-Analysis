import sqlite3
import pandas as pd
from typing import Optional, List
from app.model.risk_and_sanctions_models import SanctionWatchlistRiskProfile
from app.config import sanction_watchlist_hits_table_name, test_database

class SanctionWatchlistRiskRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.table_name = sanction_watchlist_hits_table_name
        
        self.columns = [field.name for field in SanctionWatchlistRiskProfile.__dataclass_fields__.values()]
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
            SANCTIONWATCHLISTHITID INTEGER PRIMARY KEY AUTOINCREMENT,
            CUSTOMERID INTEGER,
            ACCOUNTNO TEXT,
            SANCTIONS_RISK REAL ,
            WATCHLIST_RISK REAL ,
            PEP_RISK REAL,
            ADVERSE_MEDIA_RISK REAL,
            REGULATORY_WARNINGS_RISK REAL,
            OVERALL_RISK_SCORE REAL,
            RISKLEVEL TEXT ,
            LASTSCREENEDDATE TEXT ,
            NEXTSCREENINGDATE TEXT,
            REVIEWFREQUENCY_DAYS INTEGER,
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

    def get_all_hits(self) -> List[SanctionWatchlistRiskProfile]:
        sql = f"SELECT {self.column_names} FROM {self.table_name}"
        hits = []
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    hits.append(SanctionWatchlistRiskProfile.from_db_row(row))
                return hits
        except Exception as e:
            print(f"Error fetching all sanction hits: {e}")
            return []

    def insert_hit(self, hit):
        placeholders = ', '.join(['?' for _ in self.columns])
        sql = f"""
        INSERT INTO {self.table_name} ({self.column_names})
        VALUES ({placeholders})
        """
        values = list(getattr(hit, col) for col in self.columns)
        if not values[0]:
            values[0] = None
        
        try:
            with self._connect() as conn:
                cursor = conn.execute(sql, tuple(values))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting sanction hit for Customer {hit.CUSTOMERID}: {e}")
            return None

    def find_by_hit_id(self, hit_id):
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE SANCTIONWATCHLISTHITID = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (hit_id,))
                row = cursor.fetchone()
                if row:
                    return SanctionWatchlistRiskProfile.from_db_row(row)
                return None
        except Exception as e:
            print(f"Error finding sanction hit by ID {hit_id}: {e}")
            return None

    def get_pending_reviews(self):
        sql = f"SELECT {self.column_names} FROM {self.table_name} WHERE DISPOSITION = 'Pending' ORDER BY SCREENDATE ASC"
        hits = []
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    hits.append(SanctionWatchlistRiskProfile.from_db_row(row))
                return hits
        except Exception as e:
            print(f"Error fetching pending sanction hits: {e}")
            return []
            
    def update_disposition(self, hit_id, disposition, reviewer_id):
        sql = f"UPDATE {self.table_name} SET DISPOSITION = ?, REVIEWERID = ? WHERE SANCTIONHITID = ?"
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (disposition, reviewer_id, hit_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating sanction hit {hit_id}: {e}")
            return False

if __name__ == '__main__':

    DB_FILE = test_database
    repo = SanctionWatchlistRiskRepository(DB_FILE)
    repo.create_table()
    
    hit_data = {
        'SANCTIONWATCHLISTHITID': None,
        'CUSTOMERID': 2005,
        'ACCOUNTNO': 'ACC12345678',
        'SANCTIONS_RISK': 0.45,
        'WATCHLIST_RISK': 0.55,
        'PEP_RISK': 0.30,
        'ADVERSE_MEDIA_RISK': 0.60,
        'REGULATORY_WARNINGS_RISK': 0.50,
        'OVERALL_RISK_SCORE': 0.50,
        'RISKLEVEL': 'Medium',
        'LASTSCREENEDDATE': '2025-11-20 09:00:00',
        'NEXTSCREENINGDATE': '2026-05-20 09:00:00',
        'REVIEWFREQUENCY_DAYS': 180, # Semi-annual review
        'STATUS': 'On Hold',
        'CREATED_AT': '2025-08-10 16:20:00',
        'UPDATED_AT': '2025-11-20 09:00:00'
    }

    hit = SanctionWatchlistRiskProfile(**hit_data)
    
    print("--- Testing Sanction Watchlist Risk Repository ---")
    
    new_id = repo.insert_hit(hit)
    if new_id:
        print(f"Inserted Sanction Watchlist Risk with ID: {new_id}.")
        
        all_hits = repo.get_all_hits()
        print(f"Found {len(all_hits)} sanction and watchlist hits.")
        if all_hits:
            print(f"Oldest hit is {all_hits[0].SANCTIONWATCHLISTHITID}.")
            
                
            verified_hit = repo.find_by_hit_id(new_id)
            if verified_hit:
                print(f"Verification: STATUS is now '{verified_hit.STATUS}'.")