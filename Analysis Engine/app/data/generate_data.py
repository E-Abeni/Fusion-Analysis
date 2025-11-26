import sqlite3
import time
from faker import Faker
from random import uniform, choice
from decimal import Decimal
from app.config import mock_data_size, database_name, transactions_table_name
import os

# --- Configuration ---
DATABASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DATABASE_PATH, database_name)
TABLE_NAME = transactions_table_name
NUM_RECORDS = mock_data_size

# Initialize Faker with a specific locale for somewhat consistent data
fake = Faker(['en_US', 'en_CA', 'en_GB'])

# 56 Fields provided by the user
FIELDS_DEFINITION = {
    'TRANSACTIONID': 'INTEGER PRIMARY KEY',
    'REPORTNO': 'TEXT',
    'REPORTDATE': 'TEXT',
    'BRANCHID': 'INTEGER',
    'BRANCHNAME': 'TEXT',
    'TRANSACTIONDATE': 'TEXT',
    'TRANSACTIONTIME': 'TEXT',
    'TRANSACTIONTYPE': 'TEXT',
    'CONDUCTINGMANNER': 'TEXT',
    'CURRENCYTYPE': 'TEXT',
    'AMOUNTINBIRR': 'REAL',
    'AMOUNTINCURRENCY': 'REAL',
    'FULL_NAME': 'TEXT',
    'OTHERNAME': 'TEXT',
    'SEX': 'TEXT',
    'BIRTHDATE': 'TEXT',
    'IDCARDNO': 'TEXT',
    'PASSPORTNO': 'TEXT',
    'PASSPORTISSUEDBY': 'TEXT',
    'RESIDENCECOUNTRY': 'TEXT',
    'ORIGINCOUNTRY': 'TEXT',
    'OCCUPATION': 'TEXT',
    'COUNTRY': 'TEXT',
    'REGION': 'TEXT',
    'CITY': 'TEXT',
    'SUBCITY': 'TEXT',
    'WOREDA': 'TEXT',
    'HOUSENO': 'TEXT',
    'POSTALCODE': 'TEXT',
    'BUSINESSMOBILENO': 'TEXT',
    'BUSSINESSTELNO': 'TEXT',
    'BUSINESSFAXNO': 'TEXT',
    'RESIDENCETELNO': 'TEXT',
    'EMAILADDRESS': 'TEXT',
    'ACCOUNTNO': 'TEXT',
    'ACCHOLDERBRANCH': 'TEXT',
    'ACCOWNERNAME': 'TEXT',
    'ACCOUNTTYPE': 'TEXT',
    'OPENEDDATE': 'TEXT',
    'BALANCEHELD': 'REAL',
    'BALANCEHELDDATE': 'TEXT',
    'CLOSEDDATE': 'TEXT',
    'BENFULLNAME': 'TEXT',
    'BENACCOUNTNO': 'TEXT',
    'BENBRANCHID': 'INTEGER',
    'BENBRANCHNAME': 'TEXT',
    'BENOWNERENTITY': 'TEXT',
    'BENCOUNTRY': 'TEXT',
    'BENREGION': 'TEXT',
    'BENCITY': 'TEXT',
    'BENZONE': 'TEXT',
    'BENWOREDA': 'TEXT',
    'BENHOUSENO': 'TEXT',
    'BENTELNO': 'TEXT',
    'BENISENTITY': 'INTEGER',
}

# --- Database Setup Functions ---

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.execute('PRAGMA journal_mode = WAL;') # Improves write performance
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """Create the transactions table based on the FIELDS_DEFINITION."""
    # Build the column definitions string
    columns_sql = ", ".join(f"{name} {dtype}" for name, dtype in FIELDS_DEFINITION.items())
    
    # Construct the final CREATE TABLE statement
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {columns_sql}
    );
    """
    try:
        conn.execute(create_table_sql)
        conn.commit()
        print(f"Successfully created table '{TABLE_NAME}'.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

# --- Data Generation Function ---

def generate_fake_transaction_data(transaction_id):
    """Generates a single dictionary of fake data for all 56 fields."""
    
    # Generate common values first
    is_closed = choice([True, False])
    amount_birr = float(Decimal(uniform(100.00, 999999.99)).quantize(Decimal('0.01')))
    is_entity = choice([0, 1])

    # Map faker methods to the fields
    data = {
        # Identifiers & Reporting
        'TRANSACTIONID': transaction_id,
        'REPORTNO': fake.unique.bothify(text='REP#####'),
        'REPORTDATE': fake.date_this_decade().isoformat(),
        'BRANCHID': fake.random_int(min=100, max=999),
        'BRANCHNAME': fake.city() + ' Branch',
        'TRANSACTIONDATE': fake.date_this_month().isoformat(),
        'TRANSACTIONTIME': fake.time(pattern='%H:%M:%S'),
        'TRANSACTIONTYPE': choice(['Deposit', 'Withdrawal', 'Transfer', 'Forex', 'Payment']),
        'CONDUCTINGMANNER': choice(['In Person', 'Online', 'Mobile App', 'ATM']),
        'CURRENCYTYPE': fake.currency_code(),
        'AMOUNTINBIRR': amount_birr,
        'AMOUNTINCURRENCY': float(Decimal(amount_birr / uniform(20.0, 50.0)).quantize(Decimal('0.01'))),

        # Payer/Customer Details
        'FULL_NAME': fake.name(),
        'OTHERNAME': fake.first_name(),
        'SEX': choice(['M', 'F', 'Other']),
        'BIRTHDATE': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        'IDCARDNO': fake.bothify(text='ET#########'),
        'PASSPORTNO': fake.bothify(text='P######'),
        'PASSPORTISSUEDBY': fake.country(),
        'RESIDENCECOUNTRY': fake.country(),
        'ORIGINCOUNTRY': fake.country(),
        'OCCUPATION': fake.job(),
        
        # Payer/Customer Address
        'COUNTRY': 'Ethiopia',
        'REGION': fake.state(),
        'CITY': fake.city(),
        'SUBCITY': fake.city(),
        'WOREDA': fake.word().capitalize(),
        'HOUSENO': fake.building_number(),
        'POSTALCODE': fake.postcode(),

        # Payer/Customer Contact
        'BUSINESSMOBILENO': fake.phone_number(),
        'BUSSINESSTELNO': fake.phone_number(),
        'BUSINESSFAXNO': fake.phone_number(),
        'RESIDENCETELNO': fake.phone_number(),
        'EMAILADDRESS': fake.unique.email(),

        # Account Details
        'ACCOUNTNO': fake.bothify(text='A########-####'),
        'ACCHOLDERBRANCH': fake.city() + ' Branch',
        'ACCOWNERNAME': fake.name(),
        'ACCOUNTTYPE': choice(['Savings', 'Checking', 'Corporate', 'Forex']),
        'OPENEDDATE': fake.date_this_decade().isoformat(),
        'BALANCEHELD': float(Decimal(uniform(1000.00, 9999999.99)).quantize(Decimal('0.01'))),
        'BALANCEHELDDATE': fake.date_this_month().isoformat(),
        'CLOSEDDATE': fake.date_this_year().isoformat() if is_closed else None,

        # Beneficiary Details
        'BENFULLNAME': fake.name(),
        'BENACCOUNTNO': fake.bothify(text='A########-####'),
        'BENBRANCHID': fake.random_int(min=100, max=999),
        'BENBRANCHNAME': fake.city() + ' Branch',
        'BENOWNERENTITY': fake.company() if is_entity else None,
        
        # Beneficiary Address & Contact
        'BENCOUNTRY': fake.country(),
        'BENREGION': fake.state(),
        'BENCITY': fake.city(),
        'BENZONE': fake.word().capitalize(),
        'BENWOREDA': fake.word().capitalize(),
        'BENHOUSENO': fake.building_number(),
        'BENTELNO': fake.phone_number(),
        'BENISENTITY': is_entity,
    }
    return data

def insert_data(conn):
    """Generates and inserts a large number of records into the table."""
    
    # 1. Prepare the insert query
    columns = list(FIELDS_DEFINITION.keys())
    placeholders = ', '.join(['?'] * len(columns))
    insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({placeholders})"

    # 2. Generate all the data in memory (list of tuples)
    print(f"Generating {NUM_RECORDS} synthetic records...")
    start_gen = time.time()
    data_to_insert = []
    
    # Note: TRANSACTIONID starts from 1
    for i in range(1, NUM_RECORDS + 1):
        record_dict = generate_fake_transaction_data(i)
        # Convert the dictionary values into a tuple respecting the column order
        record_tuple = tuple(record_dict[col] for col in columns)
        data_to_insert.append(record_tuple)
        
    end_gen = time.time()
    print(f"Data generated in {end_gen - start_gen:.2f} seconds.")

    # 3. Insert the data using executemany for efficiency
    print(f"Inserting {NUM_RECORDS} records into the database...")
    start_insert = time.time()
    try:
        conn.executemany(insert_sql, data_to_insert)
        conn.commit()
        end_insert = time.time()
        print(f"Insertion complete. Total time: {end_insert - start_insert:.2f} seconds.")
        print(f"Database '{DATABASE_NAME}' is ready with {conn.execute(f'SELECT COUNT(*) FROM {TABLE_NAME}').fetchone()[0]} records.")
    except sqlite3.Error as e:
        print(f"Error during bulk insert: {e}")
        conn.rollback()


# --- Main Execution Block ---

if __name__ == '__main__':
    conn = create_connection(DATABASE_NAME)
    if conn:
        try:
            create_table(conn)
            insert_data(conn)
        finally:
            conn.close()
            print("Database connection closed.")