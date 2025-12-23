import pandas as pd
import requests
import logging


logging.basicConfig(
    level=logging.INFO, # Set the minimum level to log
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


URL = "http://analysis_engine:8000/risk/all"

df = pd.read_csv("transactions_offset_0_size_500000.csv")

df.columns = [i.split(".")[1].upper() for i in df.columns]


df = df.fillna("")
df['ACCOUNTNO'] = df['ACCOUNTNO'].astype(str)
df['BRANCHID'] = df['BRANCHID'].astype(str)


for i in range(len(df)):
    data = df.iloc[i].to_dict()

    #print(data)

    try:
        response = requests.post(url=URL, json=data)
        response.raise_for_status() 
    
        #print("Success:", response.json())

    except requests.exceptions.HTTPError as err:
        logger.error(f"[Live Producer] HTTP Error Occurred: {err}")
        
        
    except requests.exceptions.RequestException as e:
        logger.error(f"[Live Producer] Other Request Error: {e}")

    if response.status_code == 200:
        logger.info(f"[Live Producer] Processed Transaction with ID={data["TRANSACTIONID"]} for the account={data["ACCOUNTNO"]} - [{i}]")
    else:
        logger.error(f"[Live Producer] Faild to process transaction! ID={data["TRANSACTIONID"]} Account={data["ACCOUNTNO"]}")
        logger.error(response)



