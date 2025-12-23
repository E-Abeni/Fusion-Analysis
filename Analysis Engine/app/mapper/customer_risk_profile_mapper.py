import json
from typing import Any, Optional
from datetime import datetime, timezone
import numpy as np 
from app.model.customer_risk_profile import CustomerRiskProfile 


def report_to_customer_risk_profile(report_dict: dict, account_age: int, occupation: str, region: str,
                                    customer_id: Optional[int] = None, 
                                    account_no: Optional[str] = None, full_name: Optional[str] = None
                                    ) -> CustomerRiskProfile:
   
    
    def safe_to_float(value: Any) -> Optional[float]:
        if value is None:
            return float(0)
        if isinstance(value, (np.floating, np.integer)):
            if np.isnan(value):
                return float(0)
            return float(value)
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def safe_to_str(value: Any) -> str:
        if value is None or (isinstance(value, np.floating) and np.isnan(value)):
            return ""
        return str(value)

   
    peer_profile_occupation = safe_to_str(report_dict.get('peer_profile_occupation', {}))
    peer_profile_region = safe_to_str(report_dict.get('peer_profile_region', {}))
    peer_profile_account_age = safe_to_str(report_dict.get('peer_profile_account_age', {}))

    
    time_series_gap_data = report_dict.get('time_series_gap', {})
    time_series_gap_str = safe_to_str(time_series_gap_data)

    kyc_uniqueness_data = report_dict.get('kyc_uniqueness_check', {})
    kyc_uniqueness_str = safe_to_str(kyc_uniqueness_data)

    kyc_completeness_ratio = safe_to_float(report_dict.get('kyc_completeness_ratio'))
    
    demographics_risk_data = report_dict.get('demographics_risk', {})
    demographics_risk_str = safe_to_str(demographics_risk_data)

    sanction_hits_str = safe_to_str(report_dict.get('sanctions_screening', {}))
    watchlist_hits_str = safe_to_str(report_dict.get('watchlist_screening', {}))
    pep_hits_str = safe_to_str(report_dict.get('pep_screening', {}))
    

    now_utc = datetime.now(timezone.utc).isoformat()
    default_review_days = 90

    profile_args = {
        'Customer_ID': customer_id,
        'Account_No': account_no if account_no is not None else "N/A",
        'Full_Name': full_name if full_name is not None else "N/A",
        
        'PEER_PROFILE_OCCUPATION': peer_profile_occupation,
        'PEER_PROFILE_REGION': peer_profile_region,
        'PEER_PROFILE_ACCOUNT_AGE': peer_profile_account_age,
        'TIME_SERIES_GAP': time_series_gap_str,
        'KYC_INTEGRITY_UNIQUENESS': kyc_uniqueness_str,
        'KYC_INTEGRITY_COMPLETENESS_RATIO': kyc_completeness_ratio if kyc_completeness_ratio is not None else 0.0,
        'DEMOGRAPHICS_RISK': demographics_risk_str,
        'SANCTION_HITS': sanction_hits_str,
        'WATCHLIST_HITS': watchlist_hits_str,
        'PEP_HITS': pep_hits_str,

        'account_age': account_age,
        'occupation': occupation,
        'region': region,
        

        'RISK_SCORE': safe_to_float(report_dict.get('overall_risk_score', None)),
        'RISK_LEVEL': safe_to_str(report_dict.get('risk_level', None)),
        'REASON_CODES_JSON': json.dumps(report_dict.get('reason_codes', [])),

        'REVIEW_FREQUENCY_DAYS': default_review_days,
        'LAST_REVIEW_DATE': now_utc, 
        'NEXT_REVIEW_DATE': now_utc, 
        'STATUS': "ACTIVE", 
        'CREATED_AT': now_utc,
        'UPDATED_AT': now_utc,
       
    }
    
 
    for key, value in profile_args.items():
        if key in ['PEER_PROFILE_OCCUPATION', 'PEER_PROFILE_REGION', 'PEER_PROFILE_ACCOUNT_AGE', 
                   'TIME_SERIES_GAP', 'KYC_INTEGRITY_UNIQUENESS', 'DEMOGRAPHICS_RISK', 
                   'SANCTION_HITS', 'WATCHLIST_HITS', 'PEP_HITS', 'RISK_LEVEL', 'REASON_CODES_JSON', 
                   'LAST_REVIEW_DATE', 'NEXT_REVIEW_DATE', 'STATUS', 'CREATED_AT', 'UPDATED_AT']:
            if value is None:
                profile_args[key] = ""
       
       
        elif key in ['KYC_INTEGRITY_COMPLETENESS_RATIO', 'RISK_SCORE'] and value is None:
             profile_args[key] = None 

  
    profile_args.pop('id', None)
    
    return CustomerRiskProfile(**profile_args)