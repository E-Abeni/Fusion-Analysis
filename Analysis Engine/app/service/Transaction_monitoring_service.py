from app.analysis.transaction_monitoring import TransactionRelatedRisk
from app.model.transaction_risk_profile import TransactionRiskProfile
from app.configuration.schema_configuration import get_schema_configuration_settings
from app.repository.transaction_repository import get_all_transactions, get_transaction_by_column
from app.model.transaction import Transaction

schema = get_schema_configuration_settings()
reversed_schema = {v: k for k, v in schema.items()}


transactions = get_all_transactions(pandas_df=True)
transactions.columns = [reversed_schema.get(name, name) for name in transactions.columns]

def calculate_risk_single_transaction(transaction):
    monitoring = TransactionRelatedRisk(transactions, transaction)
    risk_report = monitoring.generate_transaction_risk_report()
    
    return risk_report


if __name__ == "__main__":
    #print(transactions.head())
    transaction = get_transaction_by_column("BRANCHNAME", "ansho branch", all=False, pandas_df=True)

    risk_report = calculate_risk_single_transaction(transaction)
    print(risk_report)

