from fastapi import FastAPI
from app.repository.transaction_repository import TransactionRepository
from app.analysis.transaction_monitoring import TransactionMonitoringRisk
from app.analysis.customer_risk_analysis import CustomerRiskAnalysis
from app.analysis.sanction_and_watchlist_analysis import SanctionWatchlistRisk
from app.model.transaction_model import Transaction as TransactionData
from app.service.Transaction_monitoring_service import start_transaction_monitoring_service, save_transaction_risk_report
from app.service.customer_risk_analysis_service import start_customer_risk_analysis_service, save_customer_risk_report
from app.service.sanction_watchlist_analysis_service import start_sanction_watchlist_risk_analysis_service, save_sanction_watchlist_report
from app.config import test_database
from fastapi import HTTPException
import time

app = FastAPI(
    title="AML Transaction Fusion Analysis Service",
    description="Endpoint for receiving raw transaction data for monitoring."
)


@app.post("/transactions/ingest")
def ingest_transaction_and_calculate_risk_score(transaction: TransactionData):
   
    try:
        # Example of processing: print a subset of the data using the new uppercase attributes
        print(f"--- Received Transaction Ingestion Request ---")
        print(f"ID: {transaction.TRANSACTIONID}")
        print(f"Account: {transaction.ACCOUNTNO}")
        print(f"Amount: {transaction.AMOUNTINBIRR} {transaction.CURRENCYTYPE}")
        print(f"Full Name: {transaction.FULL_NAME}")
        
        # NOTE: This is where you would call your monitoring model or repository.
        # Example integration point:
        # risk_score = run_monitoring_model(transaction.dict())

        all_transactions = TransactionRepository(test_database).get_pandas_df()
        print(f"Total transactions in repository: {all_transactions.shape}")

        transaction_risk = TransactionMonitoringRisk(all_transactions, transaction)
        transaction_risk_report = transaction_risk.generate_transaction_risk_report()
        save_transaction_risk_report(transaction, transaction_risk_report)

        customer_risk = CustomerRiskAnalysis(all_transactions, transaction)
        customer_risk_report = customer_risk.generate_customer_risk_report()
        save_customer_risk_report(transaction, customer_risk_report)


        sanction_watchlist_risk = SanctionWatchlistRisk(all_transactions, transaction)
        sanction_watchlist_report = sanction_watchlist_risk.generate_sanction_and_watchlist_risk_report()
        save_sanction_watchlist_report(transaction, sanction_watchlist_report)

        return {
            "status": "success",
            "message": "Transaction data received and risk is assessed",
            "transaction_id": transaction.TRANSACTIONID,
            "timestamp": time.time(),
            "transaction_risk_report": transaction_risk_report,
            "customer_risk_report": customer_risk_report,
            "sanction_watchlist_report": sanction_watchlist_report            
        }
        
    except Exception as e:
        # Handle unexpected server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during ingestion: {e}")
    

@app.get("/transactions/update_all")
def update_all_transactions_risk():
  
    try:
        result = start_transaction_monitoring_service()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during bulk update: {e}")
    
@app.get("/customers/risk_analysis_all")
def analyze_all_customers_risk():
   
    try:
        result = start_customer_risk_analysis_service()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during customer risk analysis: {e}")
    

@app.get("/sanctionsandwatchlist/risk_analysis_all")
def analyze_all_sanctions_and_watchlist_risk():
   
    try:
        result = start_sanction_watchlist_risk_analysis_service()
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error during sanctions and watchlist risk analysis: {e}")

def main():
    from app.model.transaction_model import Transaction

    tm = TransactionRepository(test_database)
    df = tm.get_pandas_df()
    d = 1
    tmm = TransactionMonitoringRisk(df, 
        Transaction(
            TRANSACTIONID = df.iloc[d]['TRANSACTIONID'],
            REPORTNO= str(df.iloc[d]['REPORTNO']),
            REPORTDATE= str(df.iloc[d]['REPORTDATE']),
            BRANCHID= int(df.iloc[d]['BRANCHID']),
            BRANCHNAME= str(df.iloc[d]['BRANCHNAME']),
            TRANSACTIONDATE= str(df.iloc[d]['TRANSACTIONDATE']),
            TRANSACTIONTIME= str(df.iloc[d]['TRANSACTIONTIME']),
            TRANSACTIONTYPE= str(df.iloc[d]['TRANSACTIONTYPE']),
            CONDUCTINGMANNER= str(df.iloc[d]['CONDUCTINGMANNER']),
            CURRENCYTYPE= str(df.iloc[d]['CURRENCYTYPE']),
            AMOUNTINBIRR= float(df.iloc[d]['AMOUNTINBIRR']),
            AMOUNTINCURRENCY= float(df.iloc[d]['AMOUNTINCURRENCY']),
            FULL_NAME= str(df.iloc[d]['FULL_NAME']),
            OTHERNAME= str(df.iloc[d]['OTHERNAME']),
            SEX= str(df.iloc[d]['SEX']),
            BIRTHDATE= str(df.iloc[d]['BIRTHDATE']),
            IDCARDNO= str(df.iloc[d]['IDCARDNO']),
            PASSPORTNO= str(df.iloc[d]['PASSPORTNO']),  
            PASSPORTISSUEDBY= str(df.iloc[d]['PASSPORTISSUEDBY']),
            RESIDENCECOUNTRY= str(df.iloc[d]['RESIDENCECOUNTRY']),
            ORIGINCOUNTRY= str(df.iloc[d]['ORIGINCOUNTRY']),
            OCCUPATION= str(df.iloc[d]['OCCUPATION']),
            COUNTRY= str(df.iloc[d]['COUNTRY']),
            REGION= str(df.iloc[d]['REGION']),
            CITY= str(df.iloc[d]['CITY']),
            SUBCITY= str(df.iloc[d]['SUBCITY']),
            WOREDA= str(df.iloc[d]['WOREDA']),
            HOUSENO= str(df.iloc[d]['HOUSENO']),
            POSTALCODE=(str(df.iloc[d]['POSTALCODE'])),
            BUSINESSMOBILENO= str(df.iloc[d]['BUSINESSMOBILENO']),
            BUSSINESSTELNO= str(df.iloc[d]['BUSSINESSTELNO']),
            BUSINESSFAXNO= str(df.iloc[d]['BUSINESSFAXNO']),
            RESIDENCETELNO= str(df.iloc[d]['RESIDENCETELNO']),
            EMAILADDRESS= str(df.iloc[d]['EMAILADDRESS']),
            ACCOUNTNO= str(df.iloc[d]['ACCOUNTNO']),
            ACCHOLDERBRANCH= str(df.iloc[d]['ACCHOLDERBRANCH']),
            ACCOWNERNAME= str(df.iloc[d]['ACCOWNERNAME']),
            ACCOUNTTYPE= str(df.iloc[d]['ACCOUNTTYPE']),
            OPENEDDATE= str(df.iloc[d]['OPENEDDATE']),
            BALANCEHELD= float(df.iloc[d]['BALANCEHELD']),
            BALANCEHELDDATE= str(df.iloc[d]['BALANCEHELDDATE']),
            CLOSEDDATE= str(df.iloc[d]['CLOSEDDATE']),
            BENFULLNAME= str(df.iloc[d]['BENFULLNAME']),
            BENACCOUNTNO= str(df.iloc[d]['BENACCOUNTNO']),
            BENBRANCHID= int(df.iloc[d]['BENBRANCHID']),
            BENBRANCHNAME= str(df.iloc[d]['BENBRANCHNAME']),
            BENOWNERENTITY= str(df.iloc[d]['BENOWNERENTITY']),
            BENCOUNTRY= str(df.iloc[d]['BENCOUNTRY']),
            BENREGION= str(df.iloc[d]['BENREGION']),
            BENCITY= str(df.iloc[d]['BENCITY']),
            BENZONE= str(df.iloc[d]['BENZONE']),
            BENWOREDA= str(df.iloc[d]['BENWOREDA']),
            BENHOUSENO= str(df.iloc[d]['BENHOUSENO']),
            BENTELNO= str(df.iloc[d]['BENTELNO']),
            BENISENTITY= int(df.iloc[d]['BENISENTITY'])

        )
    )
    
if __name__ == "__main__":
    main()
