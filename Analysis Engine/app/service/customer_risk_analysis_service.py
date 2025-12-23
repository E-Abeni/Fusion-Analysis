from app.analysis.customer_risk_analysis import CustomerRiskAnalysis
#from app.service.data_processing_service import get_processed_data
from app.repository.transaction_repository import get_transaction_by_column
from app.repository.customer_risk_profile_repository import insert_customer_risk_profile
from app.mapper.customer_risk_profile_mapper import report_to_customer_risk_profile
from app.service.data_processing_service import preprocessing
import pprint

#transactions = get_processed_data()

def calculate_customer_risk_single_transaction(transaction, transactions):
    risk = CustomerRiskAnalysis(transactions, transaction)
    transaction = preprocessing(transaction.to_frame(name="0").T).iloc[0]
    
    report = risk.generate_customer_risk_report()

    insert_customer_risk_profile(report_to_customer_risk_profile(report,
                                                                 account_age= int(transaction['ACCOUNT_AGE_DAYS']), 
                                                                 occupation= str(transaction['OCCUPATION']), 
                                                                 region= str(transaction['HOUSENO']),
                                                                 account_no = str(transaction['ACCOUNTNO']), 
                                                                 full_name=transaction['ACCOWNERNAME'] ))

    return(report)



if __name__ == "__main__":
    print("[Customer Monitoring Service] Started ...")
    tran = get_transaction_by_column("accountno", "1000604494307", all=False, pandas_df=True)
    #tran.index = [reversed_schema.get(name, name) for name in tran.index]
    risk_report = calculate_customer_risk_single_transaction(tran)

    pprint.pprint(risk_report)