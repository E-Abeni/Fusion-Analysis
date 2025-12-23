import random
import pandas as pd
import numpy as np
from app.repository.swc_repository import get_all_countries, get_all_sanction_list_entries, get_all_watch_list_entries
from app.service.data_processing_service import preprocessing

class CustomerRiskAnalysis:
    
    def __init__(self, df: pd.DataFrame, transaction: pd.Series):
        
        self.df = df
        self.transaction = transaction
        
        
        self.sanctionlist = get_all_sanction_list_entries(pandas_df=True)
        self.watchlist = get_all_watch_list_entries(pandas_df=True)
        self.countries = get_all_countries(pandas_df=True)
        self.pep_list = [] 

        if self.df is not None:
            #self.df = self.preprocessing(self.df)
            
            if isinstance(self.transaction, pd.Series):
                 self.transaction = preprocessing(self.transaction.to_frame(name="0").T).iloc[0]
            else:
                 pass 
                 
            self.customer_df = self.df[self.df["ACCOUNTNO"] == self.transaction['ACCOUNTNO']].copy()
        else:
            self.customer_df = pd.DataFrame()

    def convert_nan(self, n):
        return float(np.nan_to_num(n))


    def old_preprocessing(self, df):
        if df is None or df.empty:
            return pd.DataFrame() 

        if 'TRANSACTIONDATE' in df.columns and 'TRANSACTIONTIME' in df.columns:
            combined_series = df['TRANSACTIONDATE'].astype(str) + ' ' + df['TRANSACTIONTIME'].astype(str)
            df['TIMESTAMP'] = pd.to_datetime(combined_series, errors='coerce', utc=True)
        
        for col in ['TRANSACTIONDATE', 'TRANSACTIONTIME', 'BIRTHDATE', 'OPENEDDATE', 'CLOSEDDATE']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)

        if 'TIMESTAMP' in df.columns:
            df.sort_values(by='TIMESTAMP', inplace=True)
            df.reset_index(drop=True, inplace=True)

        if 'AMOUNTINBIRR' in df.columns:
            df['BRENTFORDIGIT'] = df['AMOUNTINBIRR'].astype(str).str[0].astype(int, errors='ignore')

        now = pd.Timestamp.now(tz="UTC")
        if 'BIRTHDATE' in df.columns:
            df['AGE'] = (now - df['BIRTHDATE']).dt.days // 365
        if 'OPENEDDATE' in df.columns:
            df['ACCOUNT_AGE_DAYS'] = (now - df['OPENEDDATE']).dt.days

        return df


    def peer_group_behavior_profile_occupation(self):
        data = self.df[self.df["OCCUPATION"] == self.transaction["OCCUPATION"]]
        
        peer_average = data['AMOUNTINBIRR'].mean()
        peer_std = data['AMOUNTINBIRR'].std()
        amount = self.transaction.get('AMOUNTINBIRR', 0)
        amount_std = amount / peer_std if peer_std and peer_std !=0 else None
        
        return {"peer_average": self.convert_nan(peer_average), 
                "peer_std": self.convert_nan(peer_std),
                "amount": self.convert_nan(amount),
                "amount_std": self.convert_nan(amount_std)
                }

    def peer_group_behavior_profile_region(self):
        data = self.df[self.df["REGION"] == self.transaction["REGION"]]
        
        std_dev = data['AMOUNTINBIRR'].std()
        amount = self.transaction.get('AMOUNTINBIRR', 0)
        
        amount_std_dev_ratio = amount / std_dev if std_dev and std_dev !=0 else None
        
        return {"peer_average": self.convert_nan(data['AMOUNTINBIRR'].mean()), 
                "peer_std": self.convert_nan(std_dev),
                "amount": self.convert_nan(amount),
                "amount_std": self.convert_nan(amount_std_dev_ratio)
                }

    def peer_group_behavior_profile_account_age(self):
        data = self.df[self.df["ACCOUNT_AGE_DAYS"] == self.transaction["ACCOUNT_AGE_DAYS"]]

        peer_average = data['AMOUNTINBIRR'].mean()
        peer_std = data['AMOUNTINBIRR'].std()
        amount = self.transaction.get('AMOUNTINBIRR', 0)
        amount_std = amount / peer_std if peer_std and peer_std !=0 else None

        return {"peer_average": self.convert_nan(peer_average), 
                "peer_std": self.convert_nan(peer_std),
                "amount": self.convert_nan(amount),
                "amount_std": self.convert_nan(amount_std)
                }

    def time_series_gap_analysis(self):
        if self.customer_df.empty:
            return pd.DataFrame(columns=['TIMESTAMP', 'TIME_DIFF'])
            
        data = self.customer_df.sort_values(by='TIMESTAMP')
        data['TIME_DIFF'] = data['TIMESTAMP'].diff().dt.total_seconds().fillna(0) // 60
        data['TIMESTAMP'] = data['TIMESTAMP'].astype(str)
        
        if not data.empty:
            return data[['TIMESTAMP', 'TIME_DIFF']].to_dict('list')
        return {}



    def kyc_integrity_uniqueness_check_old(self):
        data_passport = self.df[self.df["PASSPORTNO"] == self.transaction["PASSPORTNO"]]
        data_idcard = self.df[self.df["IDCARDNO"] == self.transaction["IDCARDNO"]]
        data_fullname = self.df[(self.df["FULL_NAME"] == self.transaction["FULL_NAME"])]

        return {
            "passport_matches": len(data_passport),
            "idcard_matches": len(data_idcard),
            "fullname_matches": len(data_fullname)
        }
    
    def kyc_integrity_uniqueness_check(self):
        def is_valid(val):
            return pd.notna(val) and str(val).strip() != ""

        passport = self.transaction.get("PASSPORTNO")
        idcard = self.transaction.get("IDCARDNO")
        fullname = self.transaction.get("FULL_NAME")

        passport_matches = len(self.df[self.df["PASSPORTNO"] == passport]) if is_valid(passport) else 0
        idcard_matches = len(self.df[self.df["IDCARDNO"] == idcard]) if is_valid(idcard) else 0
        fullname_matches = len(self.df[self.df["FULL_NAME"] == fullname]) if is_valid(fullname) else 0

        return {
            "passport_matches": passport_matches,
            "idcard_matches": idcard_matches,
            "fullname_matches": fullname_matches
        }

    
    def kyc_integrity_completeness_ratio(self):
        if self.customer_df.empty:
            return 0.0
            
        latest_kyc = self.customer_df.iloc[-1]
        
        total_fields = len(latest_kyc)
        filled_fields = latest_kyc.notnull().sum()
        
        completeness_ratio = filled_fields / total_fields if total_fields > 0 else 0.0
        return completeness_ratio



    def risk_score_demographics(self):
        
        high_risk_country_hit = self.transaction.get("BENREGION") in (self.countries["name"].astype(str)).values
        return {
            "high_risk_country_hit": high_risk_country_hit,
            "demographics_risk_score": 100 if high_risk_country_hit else 0
            }

    def risk_score_sanctions(self):
        
        sanction_full_names = (self.sanctionlist["FirstName"].astype(str) + " " + self.sanctionlist["LastName"].astype(str)).str.upper().values
        
        account_name_upper = self.transaction.get("FULL_NAME", "").upper()
        ben_name_upper = self.transaction.get("BENFULLNAME", "").upper()
        
        sanction_hit_account = account_name_upper in sanction_full_names
        sanction_hit_ben = ben_name_upper in sanction_full_names
        
        return {
            "account_sanction_hit": sanction_hit_account,
            "beneficiary_sanction_hit": sanction_hit_ben,
            "sanction_risk_score": 100 if sanction_hit_account or sanction_hit_ben else 0
        }

    def risk_score_watchlists(self):
        watchlist_full_names = (self.watchlist["FirstName"].astype(str) + " " + self.watchlist["LastName"].astype(str)).str.upper().values
        
        account_name_upper = self.transaction.get("FULL_NAME", "").upper()
        ben_name_upper = self.transaction.get("BENFULLNAME", "").upper()
        
        watchlist_hit_account = account_name_upper in watchlist_full_names
        watchlist_hit_ben = ben_name_upper in watchlist_full_names
        
        return {
            "account_watchlist_hit": watchlist_hit_account,
            "beneficiary_watchlist_hit": watchlist_hit_ben,
            "watchlist_risk_score": 100 if watchlist_hit_account or watchlist_hit_ben else 0
        }

    def risk_score_pep(self):
        pep_list_upper = [name.upper() for name in self.pep_list]
        
        account_name_upper = self.transaction.get("FULL_NAME", "").upper()
        ben_name_upper = self.transaction.get("BENFULLNAME", "").upper()

        pep_hit_account = account_name_upper in pep_list_upper
        pep_hit_ben = ben_name_upper in pep_list_upper
        
        return {
            "account_pep_hit": pep_hit_account,
            "beneficiary_pep_hit": pep_hit_ben,
            "pep_risk_score": 100 if pep_hit_account or pep_hit_ben else 0
        }



    def calculate_customer_profile_risk(self, data):        
        W_PEER      = 0.74
        W_SANCTION  = 0.05
        W_KYC       = 0.05
        W_TEMPORAL  = 0.25

        reason_codes = []

             
        def calculate_peer_z_score_risk(peer_data):
            amount = peer_data.get('amount', 0)
            avg = peer_data.get('peer_average', 0)
            std = peer_data.get('peer_std', 0)
            
            if std == 0:
                if amount != avg:
                    z_score = 5.0 
                else:
                    z_score = 0.0
            else:
                z_score = abs(amount - avg) / std
            
            return min((z_score / 1.5) * 100, 100)

        s_occ = calculate_peer_z_score_risk(data.get('peer_profile_occupation', {}))
        s_reg = calculate_peer_z_score_risk(data.get('peer_profile_region', {}))
        s_age = calculate_peer_z_score_risk(data.get('peer_profile_account_age', {}))
        
        score_peer = (s_occ + s_reg + s_age) / 2.0

        
                
        s_sanct = data.get('sanctions_screening', {}).get('sanction_risk_score', 0) * 100
        s_watch = data.get('watchlist_screening', {}).get('watchlist_risk_score', 0) * 100
        s_pep   = data.get('pep_screening', {}).get('pep_risk_score', 0) * 100
        s_demo  = data.get('demographics_risk', {}).get('demographics_risk_score', 0) * 100
        
        score_sanction = (s_sanct + s_watch + s_pep + s_demo) / 2

      
        
        completeness_ratio = data.get('kyc_completeness_ratio', 1.0)
        score_comp = (1 - completeness_ratio) * 100

        
        kyc_unique = data.get('kyc_uniqueness_check', {})
        

        max_match = max(
            kyc_unique.get('passport_matches', 0),
            kyc_unique.get('fullname_matches', 0),
        )
       

        score_match = min((max_match / 100000.0) * 100, 100)
        
        score_kyc = (score_comp * 0.4 + score_match * 0.6) # Weighing match risk higher

        
        time_diffs = data.get('time_series_gap', {}).get('TIME_DIFF', [])
        
        
        time_diffs = [td for td in time_diffs if td > 0] 
        
        if len(time_diffs) > 1:
           
            std_time_diff = np.std(time_diffs)
            
            score_temporal = min((std_time_diff / 3600.0) * 100, 100)
        else:
            score_temporal = 0

        
        total_score = (
            (score_peer * W_PEER) +
            (score_sanction * W_SANCTION) +
            (score_kyc * W_KYC) +
            (score_temporal * W_TEMPORAL)
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

        if score_match > 70:
            reason_codes.append("RC_ID_MATCH: High number of matching IDs/Names detected (Identity risk)")
        if s_occ > 70 or s_reg > 70 or s_age > 70:
            reason_codes.append("RC_PEER_ANOMALY: Account activity highly unusual compared to peer groups (Occupation/Region/Age)")
        if s_sanct > 0 or s_watch > 0 or s_pep > 0:
            reason_codes.append("RC_SANCTION: Account hit Sanction, Watchlist, or PEP lists")
        if score_comp > 30:
            reason_codes.append(f"RC_KYC_COMP: Low KYC completeness ratio ({completeness_ratio})")
        if score_temporal > 50:
            reason_codes.append("RC_TEMP_IRREG: Highly irregular transaction timing detected")


        return total_score, risk_level, reason_codes    
    


    def generate_customer_risk_report(self):
        
       
        report = {}
        report.update({"sanctions_screening": self.risk_score_sanctions()})
        report.update({"watchlist_screening": self.risk_score_watchlists()})
        report.update({"pep_screening": self.risk_score_pep()})
        report.update({"demographics_risk": self.risk_score_demographics()})

        report.update({"kyc_uniqueness_check": self.kyc_integrity_uniqueness_check()})
        report.update({"kyc_completeness_ratio": self.kyc_integrity_completeness_ratio()})

        report.update({"peer_profile_occupation": self.peer_group_behavior_profile_occupation()})
        report.update({"peer_profile_region": self.peer_group_behavior_profile_region()})
        report.update({"peer_profile_account_age": self.peer_group_behavior_profile_account_age()})
        report.update({"time_series_gap": self.time_series_gap_analysis()})

        overall_risk_score, risk_level, reason_codes = self.calculate_customer_profile_risk(report)

        report["overall_risk_score"] = overall_risk_score
        report["risk_level"] = risk_level
        report["reason_codes"] = ",".join(reason_codes)
         
        return report

if __name__ == "__main__":
    risk_calculator = CustomerRiskAnalysis(df=None, transaction=None, customer=None)
    risk_report = risk_calculator.generate_customer_risk_report()
    print(risk_report)

    