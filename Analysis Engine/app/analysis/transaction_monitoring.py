import random
from app.model.transaction_model import Transaction
import pandas as pd

class TransactionMonitoringRisk:
    def __init__(self, df, transaction: Transaction):
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


    def time_window_1hr(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=1)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return data['AMOUNTINBIRR'].sum()

    def time_window_24hr(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return data['AMOUNTINBIRR'].sum()

    def time_window_aggregation_7days(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=7*24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return data['AMOUNTINBIRR'].sum()

    def variance_analysis_24hr(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return data['AMOUNTINBIRR'].var()

    def variance_analysis_7days(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=7*24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return data['AMOUNTINBIRR'].var()

    def z_score_for_individual(self):
        z_score = (self.transaction.AMOUNTINBIRR - self.customer_df['AMOUNTINBIRR'].mean()) / self.customer_df['AMOUNTINBIRR'].std()
        return z_score
        
    def z_score_for_branch(self):
        data = self.df[self.df["BRANCHCODE"] == self.transaction.BRANCHCODE]
        z_score = (self.transaction.AMOUNTINBIRR - data['AMOUNTINBIRR'].mean()) / data['AMOUNTINBIRR'].std()
        return z_score

    def z_score_for_population(self):
        z_score = (self.transaction.AMOUNTINBIRR - self.df['AMOUNTINBIRR'].mean()) / self.df['AMOUNTINBIRR'].std()
        return z_score

    def percentile_for_branch(self):
        df = self.df[self.df["BRANCHCODE"] == self.transaction.BRANCHCODE]
        percentile = (df['AMOUNTINBIRR'] < self.transaction.AMOUNTINBIRR).mean() * 100
        return percentile
        

    def percentile_for_transaction_type(self):
        df = self.df[self.df["TRANSACTIONTYPE"] == self.transaction.TRANSACTIONTYPE]
        percentile = (df['AMOUNTINBIRR'] < self.transaction.AMOUNTINBIRR).mean() * 100
        return percentile

    def frequency_analysis_1hr(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=1)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return len(data)

    def frequency_analysis_24hr(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return len(data)

    def frequency_analysis_7day(self):
        data = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=7*24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]
        return len(data)

    def turn_over_ratio_24hr(self):
        debit = self.df[(self.df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=24)) & (self.df['TIMESTAMP'] <= self.transaction.get_timestamp()) & (self.df['BENACCOUNT'] == self.transaction.ACCOUNTNO)]['AMOUNTINBIRR'].sum()
        credit = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]['AMOUNTINBIRR'].sum()
        if credit == 0:
            return float('inf')
        return debit / credit

    def turn_over_ratio_7day(self):
        debit = self.df[(self.df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=7*24)) & (self.df['TIMESTAMP'] <= self.transaction.get_timestamp()) & (self.df['BENACCOUNT'] == self.transaction.ACCOUNTNO)]['AMOUNTINBIRR'].sum()
        credit = self.customer_df[(self.customer_df['TIMESTAMP'] >= self.transaction.get_timestamp() - pd.Timedelta(hours=7*24)) & (self.customer_df['TIMESTAMP'] <= self.transaction.get_timestamp())]['AMOUNTINBIRR'].sum()
        if credit == 0:
            return float('inf')
        return debit / credit

    def leading_digit_distribution(self):
        distribution = self.customer_df['BRENTFORDIGIT'].value_counts(normalize=True).sort_index()
        return distribution.to_dict()

    def round_number_hoarding(self):
        count = self.customer_df[self.customer_df['AMOUNTINBIRR'] % 1000 == 0].shape[0]
        total = self.customer_df.shape[0]
        if total == 0:
            return 0
        return count / total

    def transaction_geography_risk(self):
        locations = self.customer_df['BENREGION']
        current_location_count = self.customer_df[self.customer_df['BENREGION'] == self.transaction.BENREGION].count()
        if len(locations.unique()) == 0:
            return 0
        return (current_location_count / len(locations.unique()))
        

    def risk_score_transaction_amount(self):
        pass

    
    def risk_score_transaction_frequency(self):
        pass


    def overall_transaction_risk(self):
        scores = [
            self.risk_score_transaction_amount(),
            self.risk_score_transaction_frequency()
        ]
        return sum(scores) / len(scores)


    def detailed_transaction_risk(self):
        return {
            "amount_risk": self.risk_score_transaction_amount(),
            "frequency_risk": self.risk_score_transaction_frequency(),
            "velocity_score": random.randint(1, 100),
            "geographical_anomaly": random.randint(1, 100),
            "amount_deviation": random.randint(1, 100)
        }
    def generate_transaction_risk_report(self):
        overall_risk = self.overall_transaction_risk()
        details = self.detailed_transaction_risk()
        return {
            "overall_risk": overall_risk,
            "risk_level": "High" if overall_risk > 70 else "Medium" if overall_risk > 40 else "Low",
            "details": details
        }


if __name__ == "__main__":
    risk_calculator = TransactionMonitoringRisk(df=None, transaction=None)
    risk_report = risk_calculator.generate_transaction_risk_report()
    print(risk_report)

