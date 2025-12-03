from app.model.transaction import Transaction
from app.repository.transaction_repository import TransactionRepository
from app.analysis.sanction_and_watchlist_analysis import SanctionWatchlistRisk
from app.repository.sanction_watchlist_risk_repository import SanctionWatchlistRiskRepository
from app.model.customer_risk_profile import SanctionWatchlistRiskProfile
from app.config import test_database

def start_sanction_watchlist_risk_analysis_service():
    """
    Service to analyze sanctions and watchlist risk for all customers in the database.
    """

    transaction_repo = TransactionRepository(test_database)
    counter = 0

    all_transactions = transaction_repo.get_all_transactions()

    for transaction in all_transactions:
        sanction_watchlist_risk = SanctionWatchlistRisk(transaction_repo.get_pandas_df(), transaction)
        sanction_watchlist_report = sanction_watchlist_risk.generate_sanction_and_watchlist_risk_report()
        
        save_sanction_watchlist_report(transaction, sanction_watchlist_report)

        counter += 1
        print(f"Processed transaction {transaction.TRANSACTIONID} - Total processed: {counter}")

    return {
        "status": "success",
        "message": "Sanctions and watchlist risk analysis completed for all transactions",
        "total_transactions_processed": len(all_transactions),
        "successful_reports_saved": counter
    }


def save_sanction_watchlist_report(transaction, sanction_watchlist_report):

    sanction_watchlist_risk_repo = SanctionWatchlistRiskRepository(test_database)

    risk_result = SanctionWatchlistRiskProfile(
        SANCTIONWATCHLISTHITID=None,
        CUSTOMERID=transaction.ACCOUNTNO,
        ACCOUNTNO=transaction.ACCOUNTNO,
        SANCTIONS_RISK=sanction_watchlist_report['details']['sanctions_risk'],
        WATCHLIST_RISK=sanction_watchlist_report['details']['watchlists_risk'],
        PEP_RISK=sanction_watchlist_report['details']['pep_risk'],
        ADVERSE_MEDIA_RISK=sanction_watchlist_report['details']['adverse_media_risk'],
        REGULATORY_WARNINGS_RISK=sanction_watchlist_report['details']['regulatory_warnings_risk'],
        OVERALL_RISK_SCORE=sanction_watchlist_report['overall_risk'],
        RISKLEVEL='High' if sanction_watchlist_report['overall_risk'] > 70 else 'Medium' if sanction_watchlist_report['overall_risk'] > 40 else 'Low',
        LASTSCREENEDDATE=None,
        NEXTSCREENINGDATE=None,
        REVIEWFREQUENCY_DAYS=None,
        STATUS=None,
        CREATED_AT=None,
        UPDATED_AT=None,

    )

    sanction_watchlist_risk_repo.insert_hit(risk_result)

    return {
        "status": "success",
        "message": f"Sanction and watchlist report for transaction {transaction.TRANSACTIONID} saved.",
        "sanction_watchlist_report": sanction_watchlist_report
    }