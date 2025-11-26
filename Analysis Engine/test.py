# This is a script to change my data in my test database from a real anomolus data

import sqlite3
import pandas as pd

db = sqlite3.Connection("app/data/postgres.db")
cursor = db.cursor()

"""
df = pd.read_csv("C:\\Users\\Guest User\\Desktop\\trash\\anomalous_transactions.csv")

col_rel = {
    'TransactionDate':'TRANSACTIONDATE',
    'TransactionTime':'TRANSACTIONTIME',
    'TransactionType':'TRANSACTIONTYPE',
    'CurrencyType':'CURRENCYTYPE',
    'BranchName':'BRANCHNAME',
    'Account':'ACCOUNTNO',
    'OpenedDate':'OPENEDDATE',
    'BenAccountNo':'BENACCOUNTNO',
    'BenBranchName':'BENBRANCHNAME'
    }

col_rel_num = {
    'Amount':'AMOUNTINBIRR',
    'BalanceHeld':'BALANCEHELD'

}
reversed_col_rel = {}
reversed_col_rel_num = {}

for x, y in col_rel.items():
    reversed_col_rel[y] = x

for x, y in col_rel_num.items():
    reversed_col_rel_num[y] = x



def change_field(transaction_id, data):
    query1 = ",".join([str(x) + "=\'" + str(data[reversed_col_rel.get(x)]) + "\'" for x in reversed_col_rel.keys()])
    query2 = ",".join([str(x) + "=" + str(data[reversed_col_rel_num.get(x)]) for x in reversed_col_rel_num.keys()])
    #query3 = "TRANSACTIONID = " + str(20000 + transaction_id)

    sql = "UPDATE transactions SET " + query1 + "," + query2 + " WHERE TRANSACTIONID = " + str(transaction_id) 
    result = cursor.execute(sql)
    
    return("Success!" if result.fetchall() == [] else "Failed!")


size_data = cursor.execute("select count(*) from transactions;").fetchone()[0]

for i in range(size_data + 1):
    try:
        row = df.iloc[i]
        print(f"Data-{i+1} [{change_field(i, row)}]")
    except Exception as e:
        print(e)
        break

print("Finished Processing Data!")
"""

data = cursor.execute("select * from transactions;").fetchall()
df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
df.to_csv("C:\\Users\\Guest User\\Desktop\\trash\\anomalous_transactions_modified.csv", index=False)

db.commit()
db.close()