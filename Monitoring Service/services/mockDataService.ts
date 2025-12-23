import { Transaction, Customer, RiskLevel, TransactionType, STR } from '../types';

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
};

export const generateTransaction = (customer: Customer)/*: Transaction */=> {
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