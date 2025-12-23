from fastapi import FastAPI
from app.service.transaction_risk_analysis_service import calculate_transaction_risk_single_transaction
from app.service.customer_risk_analysis_service import calculate_customer_risk_single_transaction
from app.service.configuration_service import get_all_configurations, update_configuration
from app.dto.transaction_data import TransactionDataDTO as TransactionData
from app.dto.configuration_data import SettingsRootDTO
from app.service.data_processing_service import get_processed_data
from fastapi import HTTPException
import time
import pandas as pd

app = FastAPI(
    title="AML Transaction Fusion Analysis Service",
    description="Endpoint for receiving raw transaction data for monitoring."
)

transactions = get_processed_data()


@app.post("/risk/transaction")
def ingest_transaction_and_generate_transaction_risk_report(transaction: TransactionData):
   
    try:
        # Example of processing: print a subset of the data using the new uppercase attributes
        print(f"--- Received Transaction Ingestion Request ---")
        print(f"ID: {transaction.TRANSACTIONID}")
        print(f"Account: {transaction.ACCOUNTNO}")
        print(f"Amount: {transaction.AMOUNTINBIRR} {transaction.CURRENCYTYPE}")
        print(f"Full Name: {transaction.ACCOWNERNAME}")
        
        transaction_risk_report = calculate_transaction_risk_single_transaction(transaction.generate_transaction_series(transaction), transactions)
        
       
        return {
            "status": "success",
            "message": "Transaction data received and Transaction related risk is assessed",
            "transaction_id": transaction.TRANSACTIONID,
            "timestamp": time.time(),
            "transaction_risk_report": transaction_risk_report           
        }
        
        
    except Exception as e:
        # Handle unexpected server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during ingestion: {e}")


@app.post("/risk/customer")
def ingest_transaction_and_generate_customer_risk_report(transaction: TransactionData):
   
    try:
        # Example of processing: print a subset of the data using the new uppercase attributes
        print(f"--- Received Transaction Ingestion Request ---")
        print(f"ID: {transaction.TRANSACTIONID}")
        print(f"Account: {transaction.ACCOUNTNO}")
        print(f"Amount: {transaction.AMOUNTINBIRR} {transaction.CURRENCYTYPE}")
        print(f"Full Name: {transaction.ACCOWNERNAME}")
        
        customer_risk_report = calculate_customer_risk_single_transaction(transaction.generate_transaction_series(transaction), transactions)
        

        return {
            "status": "success",
            "message": "Transaction data received and Customer related risk is assessed",
            "transaction_id": transaction.TRANSACTIONID,
            "timestamp": time.time(),
            "customer_risk_report": customer_risk_report,         
        }
        
    except Exception as e:
        # Handle unexpected server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during ingestion: {e}")


@app.post("/risk/all")
def ingest_transaction_and_generate_transaction_and_customer_risk_report(transaction: TransactionData):
   
    try:
        # Example of processing: print a subset of the data using the new uppercase attributes
        print(f"--- Received Transaction Ingestion Request ---")
        print(f"ID: {transaction.TRANSACTIONID}")
        print(f"Account: {transaction.ACCOUNTNO}")
        print(f"Amount: {transaction.AMOUNTINBIRR} {transaction.CURRENCYTYPE}")
        print(f"Full Name: {transaction.ACCOWNERNAME}")
        
        transaction_series = transaction.generate_transaction_series(transaction)
        transaction_risk_report = calculate_transaction_risk_single_transaction(transaction_series, transactions)
        customer_risk_report = calculate_customer_risk_single_transaction(transaction_series, transactions)
        

        return {
            "status": "success",
            "message": "Transaction data received and Transaction and Customer related risk is assessed",
            "transaction_id": transaction.TRANSACTIONID,
            "timestamp": time.time(),
            "transaction_risk_report": transaction_risk_report,
            "customer_risk_report": customer_risk_report,           
        }
        
    except Exception as e:
        # Handle unexpected server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during ingestion: {e}")


@app.get("/configuration")
def get_all_configuration_for_the_analysis_engine():
    return get_all_configurations()


@app.put("/configuration/update")
async def update_settings_endpoint(settings_update: SettingsRootDTO):
    
    provided_updates = settings_update.model_dump(exclude_none=True)
    
    result = update_configuration(provided_updates)
    
    return {"message": "Settings received for update", "changes": result}
    
if __name__ == "__main__":
    pass
