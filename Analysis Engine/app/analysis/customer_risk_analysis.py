import random
import pandas as pd
from app.model.transaction_model import Transaction


class CustomerRiskAnalysis:
    def __init__(self, df, transaction):
        self.df = df
        self.transaction = transaction
        self.preprocessing()
        self.customer_df = self.df[self.df["ACCOUNTNO"] == self.transaction.ACCOUNTNO]
        print("===================================================================")
        print(self.df.head())
        print(self.df.dtypes)
        print("===================================================================")
        print(Transaction.generate_transactions_dataframe([self.transaction]))
        print("===================================================================")
        print("Time Window Analysis: ")
        print("One hour: ", self.time_window_1hr())
        print("24 hours: ", self.time_window_24hr())
        print("7 days aggregation: ", self.time_window_aggregation_7days())
        print("Variance Analysis: ")

    def preprocessing(self):
        self.df['TIMESTAMP'] = pd.to_datetime(self.df['TRANSACTIONDATE'] + ' ' + self.df['TRANSACTIONTIME'])
        self.df['TIMESTAMP'] = pd.to_datetime(self.df['TIMESTAMP'])
        self.df.sort_values(by='TIMESTAMP', inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.df['BIRTHDATE'] = pd.to_datetime(self.df['BIRTHDATE'], errors='coerce')
        self.df['OPENEDDATE'] = pd.to_datetime(self.df['OPENEDDATE'], errors='coerce')
        self.df['AGE'] = (pd.Timestamp.now() - self.df['BIRTHDATE']).dt.days // 365
        self.df['ACCOUNT_AGE_DAYS'] = (pd.Timestamp.now() - self.df['OPENEDDATE']).dt.days
        self.df['CLOSEDDATE'] = pd.to_datetime(self.df['CLOSEDDATE'], errors='coerce')
        self.df['BRENTFORDIGIT'] = self.df['AMOUNTINBIRR'].astype(str).str[0].astype(int)

    def peer_group_behavior_profile_occupation(self):
        data = self.df[self.df["OCCUPATION"] == self.transaction.OCCUPATION]
        return {"peer_average": data['AMOUNTINBIRR'].mean(), 
                "peer_std": data['AMOUNTINBIRR'].std(),
                "amount": self.transaction.AMOUNTINBIRR
                }

    def peer_group_behaviro_profile_region(self):
        data = self.df[self.df["REGION"] == self.transaction.REGION]
        return {"peer_average": data['AMOUNTINBIRR'].mean(), 
                "peer_std": data['AMOUNTINBIRR'].std(),
                "amount": self.transaction.AMOUNTINBIRR
                }

    def peer_group_behavior_profile_account_age(self):
        data = self.df[self.df["ACCOUNT_AGE_DAYS"] == self.transaction.ACCOUNT_AGE_DAYS]
        return {"peer_average": data['AMOUNTINBIRR'].mean(), 
                "peer_std": data['AMOUNTINBIRR'].std(),
                "amount": self.transaction.AMOUNTINBIRR
                }

    def time_series_gap_analysis(self):
        data = self.customer_df.sort_values(by='TIMESTAMP')
        data['TIME_DIFF'] = data['TIMESTAMP'].diff().dt.total_seconds().fillna(0)
        return data[['TIMESTAMP', 'TIME_DIFF']]

    def customer_behavior_geographic_risk_analysis(self):
        data = self.df[self.df["REGION"] == self.transaction.REGION]
        return {"peer_average": data['AMOUNTINBIRR'].mean(), 
                "peer_std": data['AMOUNTINBIRR'].std(),
                "amount": self.transaction.AMOUNTINBIRR,
                "amount_std": self.transaction.AMOUNTINBIRR / data['AMOUNTINBIRR'].std() if data['AMOUNTINBIRR'].std() !=0 else None
                }
        

    def kyc_integrity_uniqueness_check(self):
        data_passport = self.df[self.df["PASSPORTNO"] == self.transaction.PASSPORTNO]
        data_idcard = self.df[self.df["IDCARDNO"] == self.transaction.IDCARDNO]
        data_fullname = self.df[(self.df["FULLNAME"] == self.transaction.FULLNAME)]

        return {
            "passport_matches": len(data_passport),
            "idcard_matches": len(data_idcard),
            "fullname_matches": len(data_fullname)
        }

    def kyc_integrity_completness_ratio(self):
        data = self.customer_df
        total_fields = 55
        filled_fields = data.notnull().sum(axis=1).mean()
        completeness_ratio = filled_fields / total_fields
        return completeness_ratio

    def risk_score_demographics(self, sanction_list):
        data = self.customer_df[self.customer_df["BENREGION"].isin(sanction_list) ].value_counts()
        return data


    def risk_score_customer_type(self):
        return random.randint(1, 100)

    def risk_score_transaction_history(self):
        return random.randint(1, 100)

    def overall_customer_risk(self):
        scores = [
            self.risk_score_demographics(),
            self.risk_score_customer_type(),
            self.risk_score_transaction_history()
        ]
        return sum(scores) / len(scores)

    def detailed_customer_risk(self):
        return {
            "demographics_risk": self.risk_score_demographics(),
            "customer_type_risk": self.risk_score_customer_type(),
            "transaction_history_risk": self.risk_score_transaction_history()
        }

    def generate_customer_risk_report(self):
        overall_risk = self.overall_customer_risk()
        details = self.detailed_customer_risk()
        return {
            "overall_risk": overall_risk,
            "details": details
        }


if __name__ == "__main__":
    risk_calculator = CustomerRiskAnalysis(df=None, transaction=None, customer=None)
    risk_report = risk_calculator.generate_customer_risk_report()
    print(risk_report)

    