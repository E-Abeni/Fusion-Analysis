from app.repository.transaction_risk_repository import TransactionRiskRepository
from app.repository.transaction_repository import TransactionRepository
from app.analysis.transaction_monitoring import TransactionMonitoringRisk
from app.model.transaction_risk_model import TransactionRiskResult
from app.config import test_database

def start_transaction_monitoring_service():
    # Initialize repositories
    transaction_repo = TransactionRepository(test_database)
    counter = 0
    
    # Fetch transactions
    transactions = transaction_repo.get_all_transactions()

    # Monitor each transaction
    for transaction in transactions:
        try:
            monitoring = TransactionMonitoringRisk(transaction_repo.get_pandas_df(), transaction)
            risk_report = monitoring.generate_transaction_risk_report()
            
            # Save risk report
            save_transaction_risk_report(transaction, risk_report)
            counter += 1
            print(f"Processed transaction {transaction.TRANSACTIONID} - Total processed: {counter}")
        except Exception as e:
            print(f"Error processing transaction {transaction.TRANSACTIONID}: {e}")
            
    print("completed.........................")
    return {
        "status": "completed",
        "total_transactions_processed": len(transactions),
        "successful_reports_saved": counter,
        "message": "Transaction monitoring service has finished processing."
    }


def save_transaction_risk_report(transaction, risk_report):
    transaction_risk_repo = TransactionRiskRepository(test_database)
    
    risk_result = TransactionRiskResult(
        transaction_id=transaction.TRANSACTIONID,
        overall_risk_score=risk_report['overall_risk'],
        risk_level=risk_report['risk_level'],
        velocity_score=risk_report['details']['velocity_score'],
        geographical_anomaly=risk_report['details']['geographical_anomaly'],
        amount_deviation=risk_report['details']['amount_deviation']
    )

    transaction_risk_repo.insert_result(risk_result)

    return {
        "status": "success",
        "message": f"Risk report for transaction {transaction.TRANSACTIONID} saved.",
        "risk_report": risk_report
    }