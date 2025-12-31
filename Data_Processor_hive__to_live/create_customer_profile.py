
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Program Starting at " + str(datetime.now()))

"""##What to do:

1. ** accountno,
2. ** amount_avg,
3. ** amount_std,
4. ** count_of_transactions,

5. ** frequency_1hr_all,
6. ** frequency_24hr_all,
7. ** volume_1hr_all,
8. ** volume_24hr_all,
9. ** frequency_1hr_max,
10. ** frequency_24hr_max,
11. ** volume_1hr_max,
12. ** volume_24hr_max,

13. ** prefered_branches,
14. ** used_transaction_types,
15. ** frequent_destinations,
16. ** transaction_timedelta_all,
17. ** transaction_timedelta_min,
18. ** transaction_timedelta_max,
19. ** transaction_timedelta_average,
20. ** last_transaction_time,
21. ** top_beneficiaries,
22. ** score_unseen_transactions,


23. ** account_age_days,
24. ** account_age_years,
25. ** account_age_bucket,

26. profile_account_age,
27. profile_occupation



Other tables
- Table Occupation_profile:  Occupation, mean, std, count
- Table Account_age_profile: Account_age_bucket, mean, std, count

##Data Fetching and Processing

### Data Fetching
"""

logging.info("[Profile Service] Creating and connecting with database ...")
url = "postgresql://postgres:admin@172.20.137.129:5432/postgres"
engine = create_engine(url)

logging.info("[Profile Service] Database connected successfully!")

selected_columns = ['transactionid', 'transactiondate', 'transactiontime', 'accountno', 'benaccountno', 'amountinbirr',
                    'branchid', 'transactiontype', 'benworeda', 'occupation', 'openeddate']

logging.info("[Profile Service] Importing Data to Memory ...")
df = pd.read_sql_query(f"SELECT {','.join(selected_columns)} FROM test_transactions", engine)

logging.info("[Profile Service] Data imported Successfully")
logging.info("[Profile Service] Shape: " + str(df.shape))

logging.info("[Profile Service] Processing the data ...")


"""###Data Processing"""
"""
df = df[selected_columns]\
.assign(transactiondatetime = pd.to_datetime(df['transactiondate'].astype(str) + " " + df['transactiontime'].astype(str)).dt.tz_localize(None))\
.assign(transactiondate = pd.to_datetime(df['transactiondate']).dt.tz_localize(None))\
.assign(transactiontime = pd.to_datetime(df['transactiontime']).dt.time)\
.assign(amountinbirr = df['amountinbirr'].astype(float))\
.assign(branchid = df['branchid'].astype(str))\
.assign(accountno = df['accountno'].astype(str).str.strip())\
.assign(benaccountno = df['benaccountno'].astype(str).str.strip())\
.assign(transactiontype = df['transactiontype'].astype(str).str.strip())\
.assign(occupation = df['occupation'].astype(str).str.strip())\
.assign(openeddate = pd.to_datetime(df['openeddate']).dt.tz_localize(None))
"""
OLD_DATE = pd.Timestamp('1900-01-01')
DEFAULT_AMOUNT = 0.0

df = df[selected_columns]\
    .assign(
        transactiondatetime = pd.to_datetime(df['transactiondate'].astype(str) + " " + df['transactiontime'].astype(str), errors='coerce').dt.tz_localize(None),
        transactiondate = pd.to_datetime(df['transactiondate'], errors='coerce').dt.tz_localize(None),
        transactiontime = pd.to_datetime(df['transactiontime'], errors='coerce').fillna(pd.Timestamp("1900-01-01 00:00:00")).dt.time,
        amountinbirr = pd.to_numeric(df['amountinbirr'], errors='coerce'),
        branchid = df['branchid'].astype(str).str.strip(),
        accountno = df['accountno'].astype(str).str.strip(),
        benaccountno = df['benaccountno'].astype(str).str.strip(),
        transactiontype = df['transactiontype'].astype(str).str.strip(),
        occupation = df['occupation'].astype(str).str.strip(),
        openeddate = pd.to_datetime(df['openeddate'], errors='coerce').dt.tz_localize(None)
    )\
    .fillna({
        'transactiondatetime': OLD_DATE,
        'transactiondate': OLD_DATE,
        'openeddate': OLD_DATE,
        'amountinbirr': DEFAULT_AMOUNT
    })

logging.info("[Profile Service] Data Processing Completed!")


"""## Initialization of Empty list for Aggregation"""

all_profiles = []


logging.info("[Profile Service] Customer Profiling Started ...")
logging.info("0%")

"""#Profile Calculations


##Average and Standard Deviation (1, 2, 3, 4)
"""

all_profiles.append(
df[selected_columns]\
.groupby(['accountno'])\
.agg(mean=('amountinbirr', 'mean'), std=('amountinbirr', 'std'), count=('transactionid', 'count'))\
.apply(lambda x: round(x, 2))\
.sort_values(by="count", ascending=False)
)

logging.info(f"{(4/25)*100}%")

"""##Transaction Frequency and Volume (5, 6, 7, 8, 9, 10, 11, 12)
- The highest frequency (hourly)
- The highes frequency (daily)

###5. Frequency 1hr
"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1h').count()\
.reset_index()\
.rename(columns={'amountinbirr': 'Frequency_1hr'})\
.assign(frequency_1hr_all=lambda x: '"' + x['transactiondatetime'].astype(str) + '": ' + x['Frequency_1hr'].astype(int).astype(str))\
.groupby('accountno')['frequency_1hr_all']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

"""###6. Frequency 24hr"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1D').count()\
.reset_index()\
.rename(columns={'amountinbirr': 'Frequency_24hr'})\
.assign(frequency_24hr_all=lambda x: '"' + x['transactiondatetime'].astype(str) + '": ' + x['Frequency_24hr'].astype(int).astype(str))\
.groupby('accountno')['frequency_24hr_all']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

logging.info(f"{(6/25)*100}%")

"""###7. Volume 1hr"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1h').sum()\
.reset_index()\
.rename(columns={'amountinbirr': 'volume_1hr'})\
.assign(volume_1hr_all=lambda x: '"' + x['transactiondatetime'].astype(str) + '": ' + x['volume_1hr'].astype(int).astype(str))\
.groupby('accountno')['volume_1hr_all']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

"""###8. Volume 24hr"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1D').sum()\
.reset_index()\
.assign(transactiondatetime = lambda x: x['transactiondatetime'].astype(str))\
.rename(columns={'amountinbirr': 'volume_24hr'})\
.assign(volume_24hr_all=lambda x: '"' + x['transactiondatetime'].astype(str) + '": ' + x['volume_24hr'].astype(int).astype(str))\
.groupby('accountno')['volume_24hr_all']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

logging.info(f"{(8/25)*100}%")

"""###Max Frequency and Volume 1hr (9, 11)"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1h').count()\
.groupby('accountno')\
.max()\
.rename("Max_Freq_1hr")
)

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1h').sum()\
.groupby('accountno')\
.max()\
.apply(lambda x: int(x))\
.rename("Max_Sum_1hr")
)

logging.info(f"{(10/25)*100}%")

"""###Max Frequency and Volume 24hr (10, 12)"""

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1D').count()\
.groupby('accountno')\
.max()\
.rename("Max_Freq_24hr")
)

all_profiles.append(
df.set_index(['transactiondatetime'])\
.sort_index()\
.groupby('accountno')\
['amountinbirr'].rolling('1D').sum()\
.groupby('accountno')\
.max()\
.apply(lambda x: int(x))\
.rename("Max_Sum_24hr")
)

logging.info(f"{(12/25)*100}%")

"""##Prefered Branch For the account (13)"""

all_profiles.append(
df\
.groupby(['accountno', 'branchid'])\
.size()\
.reset_index()\
.rename(columns={0: "count"})\
.assign(prefered_branches=lambda x: '"' + x['branchid'].astype(str) + '": ' + x['count'].astype(int).astype(str))\
.groupby('accountno')['prefered_branches']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

"""##Typical Transaction Type for the account (14)"""

all_profiles.append(
df\
.groupby(['accountno', 'transactiontype'])\
.size()\
.reset_index()\
.rename(columns={0: "count"})\
.assign(used_transaction_types=lambda x: '"' + x['transactiontype'].astype(str) + '": ' + x['count'].astype(int).astype(str))\
.groupby('accountno')['used_transaction_types']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)


"""##Most frequent Destinations of transaction for an account (15)

"""

all_profiles.append(
df\
.groupby(['accountno', 'benworeda'])\
.size()\
.reset_index()\
.rename(columns={0: "count"})\
.assign(frequent_destinations=lambda x: '"' + x['benworeda'].astype(str) + '": ' + x['count'].astype(int).astype(str))\
.groupby('accountno')['frequent_destinations']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

logging.info(f"{(15/25)*100}%")

"""## Timedelat Between Transaction for the account (16, 17. 18, 19, 20)
- All and
- Max, Min, Average
- Last Transaction Time

### 16. All
"""

all_profiles.append(
df.sort_values(by=['accountno', 'transactiondatetime'])\
.assign(time_lapse = lambda x: x.groupby('accountno')['transactiondatetime'].diff())\
.reset_index(drop=True)\
.assign(transactiondatetime = lambda x: x['transactiondatetime'].astype(str))\
.assign(time_lapse = lambda x: x['time_lapse'].astype(str))\
[['accountno', 'transactiondatetime', 'time_lapse']]\
.assign(transaction_timedelta_all=lambda x: '"' + x['transactiondatetime'].astype(str) + '": ' + x['time_lapse'].astype(str).astype(str))\
.groupby('accountno')['transaction_timedelta_all']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

"""### (17, 18, 19). Min, Max, Average"""

all_profiles.append(
df.sort_values(by=['accountno', 'transactiondatetime'])\
.assign(time_lapse = lambda x: x.groupby('accountno')['transactiondatetime'].diff().dt.total_seconds() / 60)\
.reset_index(drop=True)\
.groupby("accountno")\
.agg(min_time_lapse_minutes=('time_lapse', 'min'), max_time_lapse_minutes=('time_lapse', 'max'), avg_time_lapse_minutes=('time_lapse', 'mean'))\
.fillna(-1)\
.apply(lambda x: round(x, 2))
)

"""###20. Last Transaction Time"""

all_profiles.append(
df.sort_values(by=['accountno', 'transactiondatetime'])\
.groupby('accountno')\
.last()['transactiondatetime']\
.rename("last_transaction_time")
)

logging.info(f"{(20/25)*100}%")

"""##Top Beneficiaries for the account (21)
- Later to join with beneficiaries risk
"""

all_profiles.append(
df\
.groupby(['accountno', 'benaccountno'])\
.size()\
.reset_index()\
.rename(columns={0: "count"})\
.sort_values(by=['accountno', 'count'], ascending=[True, False])\
.assign(top_beneficiaries=lambda x: '"' + x['benaccountno'].astype(str) + '": ' + x['count'].astype(int).astype(str))\
.groupby('accountno')['top_beneficiaries']\
.agg(lambda x: '{' + ', '.join(x) + '}')
)

"""##Indicator of new Beneficiaries (22)
- Ratio of beneficiaries with single transaction over all transactions
"""

from os import rename
def get_single_ratio(group):
    total_volume = group[0].count()
    single_volume = group.loc[group[0] == 1, 0].count()
    return (single_volume / total_volume) * group[0].sum()

all_profiles.append(
df\
.groupby(['accountno', 'benaccountno'])\
.size()\
.reset_index()\
.sort_values(by=['accountno', 0], ascending=[True, False])\
.groupby(['accountno'])\
.apply(get_single_ratio)\
.rename("unknown_beneficiary_risk_score")
)

logging.info(f"{(22/25)*100}%")

"""## account_age_days, account_age_years, account_age_bucket (23, 24, 25)"""

today = pd.Timestamp.now()

bins = list(range(0,21, 2)) + [np.inf]
labels = [f"{x} < x < {bins[i+1]}" for i,x in enumerate(bins[:-2])] + [f"> {bins[-2]}"]

all_profiles.append(
df\
.groupby(['accountno'])\
.agg(openeddate=('openeddate', 'min'), avg_amount=('amountinbirr', 'mean'))\
.assign(account_age = lambda x: today - x['openeddate'])\
.assign(account_age_days = lambda x: x['account_age'].dt.days)\
.assign(account_age_years = lambda x: x['account_age_days'] / 365)\
.assign(account_age_bucket = lambda x: pd.cut(x['account_age_years'], bins=bins, labels=labels))\
[['account_age_days', 'account_age_years', 'account_age_bucket']]
)

logging.info(f"{(25/25)*100}%")
logging.info("[Profile Service] Completed Customer Profiling.")

"""#Average and Standard Deviation for Occupation"""

occupation_summary = df\
.groupby('occupation')\
.agg(mean=('amountinbirr', 'mean'), std=('amountinbirr', 'std'), count=('transactionid', 'count'))\
.apply(lambda x: round(x, 2))\
.sort_values(by="count", ascending=False)

logging.info("[Profile Service] Occupation Profile Created! ")

"""#Average and Standard Deviation for Account Age"""

today = pd.Timestamp.now()

bins = list(range(0,21, 2)) + [np.inf]
labels = [f"{x} < x < {bins[i+1]}" for i,x in enumerate(bins[:-2])] + [f"> {bins[-2]}"]

account_age_summary = df\
.groupby(['accountno'])\
.agg(openeddate=('openeddate', 'min'), avg_amount=('amountinbirr', 'mean'))\
.assign(account_age = lambda x: today - x['openeddate'])\
.assign(account_age_days = lambda x: x['account_age'].dt.days)\
.assign(account_age_years = lambda x: x['account_age_days'] / 365)\
.assign(account_age_bucket = lambda x: pd.cut(x['account_age_years'], bins=bins, labels=labels))\
.groupby("account_age_bucket")\
.agg(mean_age=('account_age_years', 'mean'), mean_amount=('avg_amount', 'sum'), std=('avg_amount', 'mean'), count=('account_age_years', 'count'))\
.apply(lambda x: round(x, 2))

logging.info("[Profile Service] Account Age Profile Created! ")

"""#Dataframes to store Behavior Profile, Occupation Profile and Account Age Profile"""

all_profiles_df = pd.concat(all_profiles, axis=1)

print("Customer Profile: ", all_profiles_df.shape)
print("Occupation Profile: ", occupation_summary.shape)
print("Account Age Profile: ", account_age_summary.shape)

"""
all_profiles_df.to_csv("customer_profile.csv")
occupation_summary.to_csv("occupation_profile.csv")
account_age_summary.to_csv("account_age_profile.csv")
"""

all_profiles_df.to_sql("customer_profile", engine, if_exists='replace')
occupation_summary.to_sql("occupation_profile", engine, if_exists='replace')
account_age_summary.to_sql("account_age_profile", engine, if_exists='replace')

logging.info("Finish time: " + datetime.now())