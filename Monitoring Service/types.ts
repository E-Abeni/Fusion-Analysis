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
  id: string;
  name: string;
  occupation: string;
  region: string;
  riskScore: number; // 0-100
  riskLevel: RiskLevel;
  kycIntegrity: number; // 0-1
  isSanctioned: boolean;
  tags: string[]; // e.g., "Zombie Account", "PEP"
  // New fields for extended analysis
  accountAgeDays: number;
  lastActiveDate: Date;
  avgTransactionValue: number;
  peerGroupAvgTransactionValue: number;
}

export interface Transaction {
  id: string;
  customerId: string;
  amount: number;
  currency: string;
  timestamp: Date;
  type: TransactionType;
  destinationCountry: string;
  riskScore: number;
  riskLevel: RiskLevel;
  flags: string[]; // e.g., "Benford Violation", "Round Number", "Velocity"
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