from app.model.transaction_risk_profile import TransactionRiskProfile

def report_to_transaction_risk_profile(report_dict: dict, transaction_id: str, 
                                        t_from: str, t_to: str, tf_name: str, 
                                        tt_name: str, amount: int, ttype: str, timestamp:str) -> TransactionRiskProfile:
  
    def to_float(value):
        if hasattr(value, 'value'): 
            return value.value
        return float(value)

    mapping = {
        'time_window_1hr': ('TimeWindow1hr', to_float),
        'time_window_24hr': ('TimeWindow24hr', to_float),
        'time_window_7days': ('TimeWindow7day', to_float),
        'variance_24hr': ('Variance24hr', to_float),
        'variance_7days': ('Variance7day', to_float),
        'z_score_individual': ('ZScoreIndividual', to_float),
        'z_score_branch': ('ZScoreBranch', to_float),
        'z_score_population': ('ZScorePopulation', to_float),
        'percentile_branch': ('PercentileBranch', to_float),
        'percentile_transaction_type': ('PercentileTransactionType', to_float),
        'frequency_1hr': ('Frequency1hr', int),
        'frequency_24hr': ('Frequency24hr', int),
        'frequency_7days': ('Frequency7day', int),
        'turnover_ratio_24hr': ('TurnOverRatio24hr', to_float),
        'turnover_ratio_7days': ('TurnOverRatio7day', to_float),
        'leading_digit_distribution': ('LeadingDigitDistribution', str),
        'round_number_hoarding': ('RoundNumberHoarding', to_float),
        'transaction_geography_risk': ('TransactionGeographyRisk', to_float),
    }


    profile_args = {
        'transaction_id': transaction_id,
        'id': None,
        "from_account" : t_from,
        "from_name" : tf_name,
        "to_account" : t_to,
        "to_name" : tt_name,
        "amount" : amount,
        "transaction_type" : ttype,
        "transaction_time" : timestamp
        
    }


    for attr, (key, conversion_func) in mapping.items():
        try:
            profile_args[attr] = conversion_func(report_dict[key])
        except KeyError:
            print(f"Warning: Key '{key}' not found in report dictionary. Skipping '{attr}'.")
            
    profile_args['overall_risk_score'] = report_dict.get('overall_risk_score', None)
    profile_args['risk_level'] = report_dict.get('risk_level', None)
    profile_args['reason_codes'] = report_dict.get('reason_codes', None)
    
   
    return TransactionRiskProfile(**profile_args)
