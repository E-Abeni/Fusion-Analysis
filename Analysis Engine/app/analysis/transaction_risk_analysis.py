import pprint
import pandas as pd
import json
from app.service.data_processing_service import preprocessing
import numpy as np
import math

class TransactionRiskAnalysis:
    def __init__(self, df: pd.DataFrame, transaction = None):
        self.df = df
        self.transaction = transaction
        if self.df is not None:
            #self.df = self.preprocessing(self.df)
            self.transaction = preprocessing(self.transaction.to_frame(name="0").T).iloc[0]
            self.customer_df = self.df[self.df["ACCOUNTNO"] == self.transaction['ACCOUNTNO']].copy()
        else:
            self.customer_df = pd.DataFrame()

        """
        print("Data filterd length: ", len(self.customer_df)) 
        pprint.pprint(self.generate_transaction_risk_report())
        pprint.pprint(self.df['BENACCOUNTNO'].head())
        pprint.pprint(self.transaction['ACCOUNTNO'])
        pprint.pprint(self.df["BENACCOUNTNO"].dtypes)
        """

    def convert_nan(self, n):
        return float(np.nan_to_num(n))

    def old_preprocessing(self, df):
        if df is None or df.empty:
            return

        if 'TRANSACTIONDATE' in df.columns and 'TRANSACTIONTIME' in df.columns:
            combined_series = df['TRANSACTIONDATE'].astype(str) + ' ' + df['TRANSACTIONTIME'].astype(str)
            df['TIMESTAMP'] = pd.to_datetime(combined_series, errors='coerce')
     
        for col in ['TRANSACTIONDATE', 'TRANSACTIONTIME', 'BIRTHDATE', 'OPENEDDATE', 'CLOSEDDATE']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df.sort_values(by='TIMESTAMP', inplace=True)
        df.reset_index(drop=True, inplace=True)

    
        if 'AMOUNTINBIRR' in df.columns:
            df['BRENTFORDIGIT'] = df['AMOUNTINBIRR'].astype(str).str[0].astype(int, errors='ignore')

        return (df)
        

    def _filter_time_window(self, df_source: pd.DataFrame, hours: int) -> pd.DataFrame:
        if 'TIMESTAMP' not in self.transaction or 'TIMESTAMP' not in df_source.columns or df_source.empty:
             return pd.DataFrame()
             
        current_time = self.transaction['TIMESTAMP']
        start_time = current_time - pd.Timedelta(hours=hours)
        
        return df_source[
            (df_source['TIMESTAMP'] > start_time) & 
            (df_source['TIMESTAMP'] <= current_time)
        ].copy()



    def time_window_1hr(self):
        data = self._filter_time_window(self.customer_df, 1)
        return self.convert_nan(data['AMOUNTINBIRR'].sum() if 'AMOUNTINBIRR' in data.columns else 0)

    def time_window_24hr(self):
        data = self._filter_time_window(self.customer_df, 24)
        return self.convert_nan(data['AMOUNTINBIRR'].sum() if 'AMOUNTINBIRR' in data.columns else 0)

    def time_window_aggregation_7days(self):
        data = self._filter_time_window(self.customer_df, 7*24)
        return self.convert_nan(data['AMOUNTINBIRR'].sum() if 'AMOUNTINBIRR' in data.columns else 0)

    

    def variance_analysis_24hr(self):
        data = self._filter_time_window(self.customer_df, 24)
        return self.convert_nan(data['AMOUNTINBIRR'].var() if not data.empty and 'AMOUNTINBIRR' in data.columns else 0)

    def variance_analysis_7days(self):
        data = self._filter_time_window(self.customer_df, 7*24)
        return self.convert_nan(data['AMOUNTINBIRR'].var() if not data.empty and 'AMOUNTINBIRR' in data.columns else 0)



    def z_score_for_individual(self):
        if self.customer_df.empty or 'AMOUNTINBIRR' not in self.transaction or 'AMOUNTINBIRR' not in self.customer_df.columns:
             return 0
             
        mean = self.customer_df['AMOUNTINBIRR'].mean()
        std = self.customer_df['AMOUNTINBIRR'].std()
        
        if std == 0:
            return 0
            
        z_score = (self.transaction['AMOUNTINBIRR'] - mean) / std
        return self.convert_nan(z_score)
        
    def z_score_for_branch(self):
        if 'BRANCHNAME' not in self.transaction or 'AMOUNTINBIRR' not in self.transaction or 'BRANCHNAME' not in self.df.columns or 'AMOUNTINBIRR' not in self.df.columns:
            return 0
            
        data = self.df[self.df["BRANCHNAME"] == self.transaction['BRANCHNAME']]
        if data.empty:
            return 0
            
        mean = data['AMOUNTINBIRR'].mean()
        std = data['AMOUNTINBIRR'].std()
        
        if std == 0:
            return 0
            
        z_score = (self.transaction['AMOUNTINBIRR'] - mean) / std
        return self.convert_nan(z_score)

    def z_score_for_population(self):
        if self.df.empty or 'AMOUNTINBIRR' not in self.transaction or 'AMOUNTINBIRR' not in self.df.columns:
             return 0
             
        mean = self.df['AMOUNTINBIRR'].mean()
        std = self.df['AMOUNTINBIRR'].std()
        
        if std == 0:
            return 0
            
        z_score = (self.transaction['AMOUNTINBIRR'] - mean) / std
        return self.convert_nan(z_score)



    def percentile_for_branch(self):
        if 'BRANCHNAME' not in self.transaction or 'AMOUNTINBIRR' not in self.transaction or 'BRANCHNAME' not in self.df.columns or 'AMOUNTINBIRR' not in self.df.columns:
            return 0
            
        df = self.df[self.df["BRANCHNAME"] == self.transaction['BRANCHNAME']]
        if df.empty:
             return 0
             
        percentile = (df['AMOUNTINBIRR'] < self.transaction['AMOUNTINBIRR']).mean() * 100
        return self.convert_nan(percentile)
        
    def percentile_for_transaction_type(self):
        if 'TRANSACTIONTYPE' not in self.transaction or 'AMOUNTINBIRR' not in self.transaction or 'TRANSACTIONTYPE' not in self.df.columns or 'AMOUNTINBIRR' not in self.df.columns:
             return 0
             
        df = self.df[self.df["TRANSACTIONTYPE"] == self.transaction['TRANSACTIONTYPE']]
        if df.empty:
             return 0
             
        percentile = (df['AMOUNTINBIRR'] < self.transaction['AMOUNTINBIRR']).mean() * 100
        return self.convert_nan(percentile)



    def frequency_analysis_1hr(self):
        data = self._filter_time_window(self.customer_df, 1)
        return len(data)

    def frequency_analysis_24hr(self):
        data = self._filter_time_window(self.customer_df, 24)
        return len(data)

    def frequency_analysis_7day(self):
        data = self._filter_time_window(self.customer_df, 7*24)
        return len(data)



    def turn_over_ratio_24hr(self):
        if 'TIMESTAMP' not in self.transaction or 'ACCOUNTNO' not in self.transaction or 'AMOUNTINBIRR' not in self.df.columns or 'BENACCOUNTNO' not in self.df.columns:
             return 0
             
        time_window_df = self._filter_time_window(self.df, 24)
        if time_window_df.empty:
            return 0
            
        debit = time_window_df[time_window_df['BENACCOUNTNO'] == self.transaction['ACCOUNTNO']]['AMOUNTINBIRR'].sum() 
        
        credit = self._filter_time_window(self.customer_df, 24)['AMOUNTINBIRR'].sum()
        
        if credit == 0:
            return float('inf') if debit > 0 else 0
            
        return self.convert_nan(debit / credit)

    def turn_over_ratio_7day(self):
        if 'TIMESTAMP' not in self.transaction or 'ACCOUNTNO' not in self.transaction or 'AMOUNTINBIRR' not in self.df.columns or 'BENACCOUNTNO' not in self.df.columns:
             return 0
             
        time_window_df = self._filter_time_window(self.df, 7*24)
        if time_window_df.empty:
            return 0
            
        
        debit = time_window_df[time_window_df['BENACCOUNTNO'] == self.transaction['ACCOUNTNO']]['AMOUNTINBIRR'].sum()
        
        credit = self._filter_time_window(self.customer_df, 7*24)['AMOUNTINBIRR'].sum()
        
        if credit == 0:
            return float('inf') if debit > 0 else 0
            
        return self.convert_nan(debit / credit)

    
    
    def leading_digit_distribution(self):
        if self.customer_df.empty or 'BRENTFORDIGIT' not in self.customer_df.columns:
            return json.dumps({})

        distribution = self.customer_df['BRENTFORDIGIT'].value_counts(normalize=True).sort_index()
        return json.dumps(distribution.to_dict())

    def round_number_hoarding(self):
        if self.customer_df.empty or 'AMOUNTINBIRR' not in self.customer_df.columns:
            return 0
            
        count = self.customer_df[self.customer_df['AMOUNTINBIRR'] % 100 == 0].shape[0]
        total = self.customer_df.shape[0]
        
        if total == 0:
            return 0
            
        return self.convert_nan(count / total)

    def transaction_geography_risk(self):
        if self.customer_df.empty or 'BENREGION' not in self.customer_df.columns or 'BENREGION' not in self.transaction:
            return 0
            
        locations = self.customer_df['BENREGION'].dropna().unique()
        if len(locations) == 0:
            return 0
            
        current_location_count = self.customer_df[self.customer_df['BENREGION'] == self.transaction['BENREGION']].shape[0]
        total_customer_transactions = self.customer_df.shape[0]
        
        
        if total_customer_transactions == 0:
             return 0
        
        proportion_in_region = current_location_count / total_customer_transactions
        
        return proportion_in_region 
        
    
    def calculate_comprehensive_risk(self, data):
        W_ANOMALY   = 0.25
        W_PATTERN   = 0.15
        W_VELOCITY  = 0.40
        W_RANKING   = 0.10
        W_CONTEXT   = 0.10

        reason_codes = []

        z_ind = abs(data.get('ZScoreIndividual', 0))
        z_bra = abs(data.get('ZScoreBranch', 0))
        z_pop = abs(data.get('ZScorePopulation', 0))
        
        avg_z = (z_ind + z_bra + z_pop)
        score_anomaly = min((avg_z / 2.0) * 100, 100)

       
        score_round = data.get('RoundNumberHoarding', 0) * 100
        
        
        digits = json.loads(data.get('LeadingDigitDistribution', ""))
        max_digit_prob = max(digits.values()) if digits else 0
        if max_digit_prob <= 0.3:
            score_benford = 0
        else:
            score_benford = min(((max_digit_prob - 0.3) / 0.5) * 100, 100)

        score_pattern = (score_round + score_benford) / 2


        freq_1h = data.get('Frequency1hr', 0)
        freq_24h = data.get('Frequency24hr', 0)
        freq_7d = data.get('Frequency7day', 0)
        
        s_freq_1 = min((freq_1h / 3.0) * 100, 100)
        s_freq_24 = min((freq_24h / 5.0) * 100, 100)
        s_freq_7d = min((freq_7d / 7.0) * 100, 100)

        
        amt_1hr = data.get('TimeWindow1hr', 0)
        amt_24hr = data.get('TimeWindow24hr', 1)

        
        burst_ratio = 0
        if amt_24hr > 0:
            if (amt_1hr / amt_24hr) > 0.5 and amt_1hr > 1000:
                burst_ratio = 100
                
        score_velocity = (s_freq_1 + s_freq_24 + s_freq_7d + burst_ratio) / 2

       
        p_branch = data.get('PercentileBranch', 0)
        p_type = data.get('PercentileTransactionType', 0)
        
        score_ranking = (p_branch + p_type) / 2

       
        score_geo = data.get('TransactionGeographyRisk', 0) * 100
        
        to_24 = data.get('TurnOverRatio24hr', 0)
        score_turnover = min(to_24 * 100, 100)
        
        score_context = (score_geo + score_turnover) / 1.2

        
        total_score = (
            (score_anomaly * W_ANOMALY) +
            (score_pattern * W_PATTERN) +
            (score_velocity * W_VELOCITY) +
            (score_ranking * W_RANKING) +
            (score_context * W_CONTEXT)
        )
        
        total_score = round(total_score, 2)

       
        if total_score >= 80:
            risk_level = "CRITICAL"
        elif total_score >= 60:
            risk_level = "HIGH"
        elif total_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        
        if score_benford > 70:
            reason_codes.append(f"R_BENFORD: Unnatural digit distribution detected (Max prob: {max_digit_prob})")
        if score_geo > 70:
            reason_codes.append(f"R_GEO: High risk geography ({data.get('TransactionGeographyRisk')})")
        if p_type > 90:
            reason_codes.append(f"R_SIZE: Top percentile for transaction type ({p_type}%)")
        if score_velocity > 70:
            reason_codes.append("R_BURST: High volume transaction in 1 and 24 hour")
        if z_ind < -2 or z_ind > 2:
            reason_codes.append(f"R_OUTLIER: Significant Z-Score deviation ({data.get('ZScoreIndividual')})")
        if score_round > 50:
            reason_codes.append("R_STRUCT: Round number hoarding detected")

        
        if risk_level in ["HIGH", "CRITICAL"] and not reason_codes:
            reason_codes.append("R_GENERIC: Cumulative risk factors exceeded threshold")

        return total_score, risk_level, reason_codes

    
    def generate_transaction_risk_report(self):
        report = {
            "TimeWindow1hr": self.time_window_1hr(),
            "TimeWindow24hr": self.time_window_24hr(),
            "TimeWindow7day": self.time_window_aggregation_7days(),
            "Variance24hr": self.variance_analysis_24hr(),
            "Variance7day": self.variance_analysis_7days(),
            "ZScoreIndividual": self.z_score_for_individual(),
            "ZScoreBranch": self.z_score_for_branch(),
            "ZScorePopulation": self.z_score_for_population(),
            "PercentileBranch": self.percentile_for_branch(),
            "PercentileTransactionType": self.percentile_for_transaction_type(),
            "Frequency1hr": self.frequency_analysis_1hr(),
            "Frequency24hr": self.frequency_analysis_24hr(),
            "Frequency7day": self.frequency_analysis_7day(),
            "TurnOverRatio24hr": self.turn_over_ratio_24hr(),
            "TurnOverRatio7day": self.turn_over_ratio_7day(),
            "LeadingDigitDistribution": self.leading_digit_distribution(),
            "RoundNumberHoarding": self.round_number_hoarding(),
            "TransactionGeographyRisk": self.transaction_geography_risk(),
        }

        overall_risk_score, risk_level, reason_codes = self.calculate_comprehensive_risk(report)

        report["overall_risk_score"] = overall_risk_score
        report["risk_level"] = risk_level
        report["reason_codes"] = ",".join(reason_codes)

        return report


    
if __name__ == "__main__":
    pass