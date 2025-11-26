from app.repository.transaction_repository import TransactionRepository
from app.analysis.customer_risk_analysis import CustomerRiskAnalysis
from app.repository.customer_risk_repository import CustomerRiskRepository
from app.model.risk_and_sanctions_models import CustomerRiskProfile
from app.config import test_database


def start_customer_risk_analysis_service():
    # Initialize repository
    transaction_repo = TransactionRepository(test_database)
    
    # Fetch transactions
    transactions = transaction_repo.get_all_transactions()
    counter = 0
    
    # Analyze each customer's risk
    for transaction in transactions:
        try:
            customer_risk = CustomerRiskAnalysis(transaction_repo.get_pandas_df(), transaction)
            risk_report = customer_risk.generate_customer_risk_report()
            save_customer_risk_report(transaction, risk_report)
            counter += 1

            print(f"Analyzed customer risk for transaction {transaction.TRANSACTIONID}")
        except Exception as e:
            print(f"Error analyzing customer risk for transaction {transaction.TRANSACTIONID}: {e}")
            
    print("Customer risk analysis completed.")
    return {
        "status": "completed",
        "total_customers_analyzed": len(transactions),
        "customer_risk_reports_saved": counter,
        "message": "Customer risk analysis service has finished processing."
    }


def save_customer_risk_report(transaction, risk_report):
    customer_risk_repo = CustomerRiskRepository(test_database)

    data = CustomerRiskProfile(
        CUSTOMERID=transaction.ACCOUNTNO,
        ACCOUNTNO=risk_report.get("account_no", transaction.ACCOUNTNO),
        DEMOGRAPHICS_RISK=risk_report['details']['demographics_risk'],
        CUSTOMER_TYPE_RISK=risk_report['details']['customer_type_risk'],
        TRANSACTION_HISTORY_RISK=risk_report['details']['transaction_history_risk'],
        RISKSCORE=risk_report['overall_risk'],
        RISKLEVEL="High" if risk_report['overall_risk'] > 70 else "Medium" if risk_report['overall_risk'] > 40 else "Low",
        REVIEWFREQUENCY_DAYS=90,
        LASTREVIEWDATE="2025-11-01",
        NEXTREVIEWDATE="2026-01-30",
        REASONCODES_JSON='[]',
        STATUS="Active",
        CREATED_AT="2025-10-01",
        UPDATED_AT="2025-11-01"
    )

    customer_risk_repo.insert_or_update_profile(data)

    #print(f"Customer risk report for transaction {transaction_id} saved.")
    return {
        "status": "success",
        "message": f"Customer risk report for transaction {transaction.TRANSACTIONID} saved.",
        "risk_report": risk_report
    }