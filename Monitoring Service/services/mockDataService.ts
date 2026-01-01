import { Transaction, Customer, RiskLevel, TransactionType, STR } from '../types';


export const mockAccounts = [
    {
        accountno: "'1013410023715015",
        mean: 846913.9,
        std: 216496.43,
        count: "2",
        max_freq_1hr: 2,
        max_sum_1hr: "1693827",
        max_freq_24hr: 2,
        max_sum_24hr: "1693827",
        frequent_destinations: null,
        min_time_lapse_minutes: 0,
        max_time_lapse_minutes: 0,
        avg_time_lapse_minutes: 0,
        last_transaction_time: "2023-12-31T21:32:44.000Z",
        unknown_beneficiary_risk_score: 2,
        account_age_days: "46020",
        account_age_years: 126.08,
        account_age_bucket: "> 20"
    },
    {
        accountno: "'2024510098716022",
        mean: 4500.5,
        std: 1200.22,
        count: "15",
        max_freq_1hr: 4,
        max_sum_1hr: "18000",
        max_freq_24hr: 8,
        max_sum_24hr: "36000",
        frequent_destinations: ["Amazon", "Target"],
        min_time_lapse_minutes: 5,
        max_time_lapse_minutes: 120,
        avg_time_lapse_minutes: 45,
        last_transaction_time: "2024-05-15T14:20:00.000Z",
        unknown_beneficiary_risk_score: 4,
        account_age_days: "365",
        account_age_years: 1.0,
        account_age_bucket: "1-2"
    },
    {
        accountno: "'3035610011223344",
        mean: 125000.0,
        std: 50000.0,
        count: "50",
        max_freq_1hr: 10,
        max_sum_1hr: "1250000",
        max_freq_24hr: 25,
        max_sum_24hr: "3125000",
        frequent_destinations: ["Crypto Exchange"],
        min_time_lapse_minutes: 1,
        max_time_lapse_minutes: 10,
        avg_time_lapse_minutes: 3,
        last_transaction_time: "2024-05-20T09:15:00.000Z",
        unknown_beneficiary_risk_score: 9,
        account_age_days: "30",
        account_age_years: 0.08,
        account_age_bucket: "< 1"
    },
    {
        accountno: "'4046710055667788",
        mean: 250.75,
        std: 50.12,
        count: "120",
        max_freq_1hr: 1,
        max_sum_1hr: "300",
        max_freq_24hr: 3,
        max_sum_24hr: "800",
        frequent_destinations: ["Starbucks", "Gas Station"],
        min_time_lapse_minutes: 60,
        max_time_lapse_minutes: 1440,
        avg_time_lapse_minutes: 480,
        last_transaction_time: "2024-05-18T18:45:00.000Z",
        unknown_beneficiary_risk_score: 1,
        account_age_days: "1825",
        account_age_years: 5.0,
        account_age_bucket: "5-10"
    },
    {
        accountno: "'5057810099001122",
        mean: 12500.0,
        std: 2500.0,
        count: "5",
        max_freq_1hr: 5,
        max_sum_1hr: "62500",
        max_freq_24hr: 5,
        max_sum_24hr: "62500",
        frequent_destinations: null,
        min_time_lapse_minutes: 1,
        max_time_lapse_minutes: 2,
        avg_time_lapse_minutes: 1.5,
        last_transaction_time: "2024-05-19T23:59:00.000Z",
        unknown_beneficiary_risk_score: 7,
        account_age_days: "15",
        account_age_years: 0.04,
        account_age_bucket: "< 1"
    }
];




const NAMES = [
  "Abenezer Tamirat",                 
  "Midroc Investment Group", 
  "Abebe Kebede",             
  "Almaz Ayana",              
  "Blue Nile Technologies",   
  "Abebe Kebede",        
  "Ethiopian Airlines",       
  "Awash Bank S.C.",         
  "Tomoca Coffee PLC",        
  "Ethio-Telecom"             
];

const REGIONS = [
  "Addis Ababa", 
  "Oromia", 
  "Amhara", 
  "Sidama", 
  "Somali"
];

const COUNTRIES = ["ETH", "ER", "DJ", "SO", "KE", "SD"];
const OCCUPATIONS = ["Consultant", "Trader", "Real Estate", "Tech", "Unemployed", "Politician", "Retail", "Government Worker"];
const FLAGS = [
  "Benford Law Violation", 
  "Round Number Hoarding", 
  "Rapid Velocity", 
  "Geo Risk Mismatch", 
  "Zombie Account Activation",
  "Structing (Smurfing)",
  "Sanction Match",
  "Layering"
];

/*
export const generateCustomer = (): Customer => {
  const score = Math.floor(Math.random() * 100);
  let level = RiskLevel.LOW;
  if (score > 50) level = RiskLevel.MEDIUM;
  if (score > 80) level = RiskLevel.HIGH;
  if (score > 95) level = RiskLevel.CRITICAL;

  const tags = [];
  // Logic for Zombie Accounts
  const isZombie = Math.random() > 0.9;
  if (isZombie) tags.push("Zombie Account");
  if (Math.random() > 0.95) tags.push("PEP");

  // Mock specific data
  const accountAgeDays = Math.floor(Math.random() * 2000) + 30;
  // If zombie, last active was long ago (e.g., > 180 days)
  const lastActiveDaysAgo = isZombie ? Math.floor(Math.random() * 200) + 180 : Math.floor(Math.random() * 7);
  const lastActiveDate = new Date();
  lastActiveDate.setDate(lastActiveDate.getDate() - lastActiveDaysAgo);

  const avgTxValue = Math.random() * 10000;
  // If high risk, maybe they deviate significantly from peer group
  const peerDeviation = level === RiskLevel.HIGH || level === RiskLevel.CRITICAL ? (Math.random() * 2 + 1.5) : (Math.random() * 0.4 + 0.8);

  return {
    id: `ACC-${Math.floor(Math.random() * 100000)}`,
    name: NAMES[Math.floor(Math.random() * NAMES.length)],
    occupation: OCCUPATIONS[Math.floor(Math.random() * OCCUPATIONS.length)],
    region: REGIONS[Math.floor(Math.random() * REGIONS.length)],
    riskScore: score,
    riskLevel: level,
    kycIntegrity: parseFloat((Math.random() * 0.3 + 0.7).toFixed(2)), // 0.7 - 1.0
    isSanctioned: Math.random() > 0.98,
    tags,
    accountAgeDays,
    lastActiveDate,
    avgTransactionValue: avgTxValue * peerDeviation,
    peerGroupAvgTransactionValue: avgTxValue
  };
};*/

/*
export const generateTransaction = (customer: Customer)/*: Transaction *//*=> {
  const isHighRisk = customer.riskLevel === RiskLevel.HIGH || customer.riskLevel === RiskLevel.CRITICAL;
  const baseAmount = Math.random() * 50000;
  // Simulate structuring or round numbers if high risk
  const amount = isHighRisk && Math.random() > 0.5 ? Math.round(baseAmount / 1000) * 1000 : parseFloat(baseAmount.toFixed(2));
  
  const score = isHighRisk ? Math.floor(Math.random() * 50 + 50) : Math.floor(Math.random() * 60);
  
  let level = RiskLevel.LOW;
  if (score > 50) level = RiskLevel.MEDIUM;
  if (score > 70) level = RiskLevel.HIGH;
  if (score > 80) level = RiskLevel.CRITICAL;

  const txFlags = [];
  if (score > 70) {
    txFlags.push(FLAGS[Math.floor(Math.random() * FLAGS.length)]);
    if (Math.random() > 0.5) txFlags.push(FLAGS[Math.floor(Math.random() * FLAGS.length)]);
  }

  return {
    id: `TX-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    customerId: customer.id,
    amount,
    currency: "BIRR",
    timestamp: new Date(),
    type: Object.values(TransactionType)[Math.floor(Math.random() * 5)],
    destinationCountry: COUNTRIES[Math.floor(Math.random() * COUNTRIES.length)],
    riskScore: score,
    riskLevel: level,
    flags: [...new Set(txFlags)]
  };
};
*/

export const generateSTR = (tx: Transaction, customer: Customer)/*: STR*/ => {
  /*
  return {
    id: `STR-${Date.now()}`,
    //transactionId: tx.id,
    customerId: customer.id,
    generatedAt: new Date(),
    reason: `Automated Trigger: ${tx.flags.join(', ')}`,
    status: 'PENDING'
  };
  */
};