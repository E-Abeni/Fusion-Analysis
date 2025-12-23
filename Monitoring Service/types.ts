export enum RiskLevel {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

export enum TransactionType {
  WIRE = 'WIRE',
  DEPOSIT = 'DEPOSIT',
  WITHDRAWAL = 'WITHDRAWAL',
  MOBILE_BANKING = 'MOBILE_BANKING',
  TRADE = 'TRADE'
}

export interface Customer {
  Account_No: string;
  Customer_ID: string | null;
  Profile_ID: number;
  Full_Name: string;

  CREATED_AT: string;
  LAST_REVIEW_DATE: string;
  NEXT_REVIEW_DATE: string;
  UPDATED_AT: string;
  STATUS: string;

  RISK_SCORE: number;
  RISK_LEVEL: string;
  REVIEW_FREQUENCY_DAYS: number;

  KYC_INTEGRITY_COMPLETENESS_RATIO: number;
  
  DEMOGRAPHICS_RISK: any;
  KYC_INTEGRITY_UNIQUENESS: any;
  PEP_HITS: any;
  SANCTION_HITS: any;
  WATCHLIST_HITS: any;
  
  PEER_PROFILE_ACCOUNT_AGE: any;
  PEER_PROFILE_OCCUPATION: any ;
  PEER_PROFILE_REGION: any;

  REASON_CODES_JSON: any;
  TIME_SERIES_GAP: string;

  account_age: number;
  occupation: string;
  region: string;
}

export interface Transaction {
  from_account: string;
  from_name: string;
  to_account: string;
  to_name: string;
  amount: number;
  transaction_type: string;
  transaction_time: string;

  frequency_1hr: number;
  frequency_7days: number;
  frequency_24hr: number;
  
  generated_at: string; 
  time_window_1hr: number;
  time_window_7days: number;
  time_window_24hr: number;
  
  id: number;
  transaction_id: string;

  overall_risk_score: number | null;
  risk_level: string | null;
  reason_codes: string | null;
  
  percentile_branch: number;
  percentile_transaction_type: number;
  z_score_branch: number;
  z_score_individual: number;
  z_score_population: number;

  turnover_ratio_7days: number;
  turnover_ratio_24hr: number;
  variance_7days: number;
  variance_24hr: number;
  
  leading_digit_distribution: string;
  round_number_hoarding: number;
  transaction_geography_risk: number; 

}

export interface STR {
  id: string;
  transactionId: string;
  customerId: string;
  generatedAt: Date;
  reason: string;
  status: 'PENDING' | 'FILED' | 'DISMISSED';
  aiAnalysis?: string;
}

export interface EngineStats {
  transactionsProcessed: number;
  messagesInQueue: number;
  processingSpeed: number; // tx/sec
  flaggedCount: number;
  cpuUsage: number; // %
  ramUsage: number; // %
}