from app.analysis.transaction_risk_analysis import TransactionRiskAnalysis
#from app.service.data_processing_service import get_processed_data
from app.repository.transaction_repository import get_transaction_by_column
from app.repository.transaction_risk_profile_repository import insert_transaction_risk_profile
from app.mapper.transaction_risk_profile_mapper import report_to_transaction_risk_profile

#transactions = get_processed_data()

def calculate_transaction_risk_single_transaction(transaction, transactions):
    risk = TransactionRiskAnalysis(transactions, transaction)
    
    report = risk.generate_transaction_risk_report()
    
    transaction_id = transaction['TRANSACTIONID'],
    t_from=str(transaction['ACCOUNTNO'])
    t_to = str(transaction['BENACCOUNTNO'])
    tf_name = str(transaction['ACCOWNERNAME'])
    tt_name = str(transaction['BENFULLNAME'])
    amount = float(transaction['AMOUNTINBIRR'])
    ttype = str(transaction['TRANSACTIONTYPE'])
    timestamp = transaction['TRANSACTIONDATE'] + " " + transaction['TRANSACTIONTIME']    
    
    
    profile = report_to_transaction_risk_profile(report, transaction_id = transaction_id,
                                                                        t_from = t_from,
                                                                        t_to = t_to,
                                                                        tf_name = tf_name,
                                                                        tt_name = tt_name,
                                                                        amount = amount,
                                                                        ttype = ttype,
                                                                        timestamp = timestamp
                                                                        )
    insert_transaction_risk_profile(profile)

    return(report)




if __name__ == "__main__":
    print("[Transaction Monitoring Service] Started ...")
    tran = get_transaction_by_column("accountno", "1000604494307", all=False, pandas_df=True)
    #tran.index = [reversed_schema.get(name, name) for name in tran.index]
    risk_report = calculate_transaction_risk_single_transaction(tran)

    print(risk_report)

