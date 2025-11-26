import { AnalysisCategory, AnalysisMethod, AnalysisRule, ConnectionConfig, DataSourceType, RiskListEntry, EngineNode } from './types';

export const MOCK_DB_FIELDS = ['transaction_id', 'account_id', 'amount', 'currency', 'timestamp', 'branch_id', 'branch_name', 'region', 'ben_account'];
export const MOCK_KAFKA_FIELDS = ['msg_id', 'event_time', 'transaction_id', 'account_id', 'amount', 'currency', 'timestamp', 'branch_id', 'branch_name', 'region', 'ben_account'];

export const REQUIRED_ENGINE_FIELDS = [
  { name: 'transaction_id', type: 'string' },
  { name: 'account_number', type: 'string' },
  { name: 'amount', type: 'number' },
  { name: 'timestamp', type: 'date' },
  { name: 'branch_id', type: 'string' }
];

export const INITIAL_DB_CONFIG: ConnectionConfig = {
  type: DataSourceType.DATABASE,
  host: 'db-01.internal',
  port: '5432',
  databaseName: 'core_banking',
  status: 'disconnected',
  mappings: []
};

export const INITIAL_KAFKA_CONFIG: ConnectionConfig = {
  type: DataSourceType.KAFKA,
  host: 'kafka-broker',
  port: '9092',
  topicName: 'live-transactions',
  status: 'disconnected',
  mappings: []
};

export const INITIAL_RISK_LISTS: RiskListEntry[] = [
  { id: '1', name: 'Eritrea', type: 'high_risk_country', riskScore: 100, code: 'ER', updatedAt: '2024-01-01' },
  { id: '2', name: 'Djibouti', type: 'high_risk_country', riskScore: 95, code: 'DJ', updatedAt: '2024-01-01' },
  { id: '3', name: 'Abebe Bekele', type: 'sanction', riskScore: 100, updatedAt: '2024-05-12' },
  { id: '4', name: 'Abenezer Tamirat', type: 'watchlist', riskScore: 75, updatedAt: '2024-02-20' },
  { id: '5', name: 'Alemayhu Tesfaye', type: 'watchlist', riskScore: 90, updatedAt: '2024-02-22' },
];

export const INITIAL_RULES: AnalysisRule[] = [
  // Customer Risk
  {
    id: 'c1',
    method: AnalysisMethod.PEER_GROUP,
    category: AnalysisCategory.CUSTOMER,
    name: 'Peer Group Deviation',
    description: 'Detects outliers within occupation/region peer groups.',
    enabled: true,
    severity: 'medium',
    parameters: { deviationThreshold: 2.5, minPeerSize: 50 }
  },
  {
    id: 'c2',
    method: AnalysisMethod.TIME_SERIES_GAP,
    category: AnalysisCategory.CUSTOMER,
    name: 'Zombie Account Activation',
    description: 'Flags sudden activity after long dormancy.',
    enabled: true,
    severity: 'high',
    parameters: { dormancyDays: 180, activationAmount: 5000 }
  },
  // Transaction Risk
  {
    id: 't1',
    method: AnalysisMethod.Z_SCORE,
    category: AnalysisCategory.TRANSACTION,
    name: 'Statistical Outlier (Z-Score)',
    description: 'Standard deviation analysis for individual transaction amounts.',
    enabled: true,
    severity: 'medium',
    parameters: { zScoreThreshold: 3.0, lookbackPeriodDays: 90 }
  },
  {
    id: 't2',
    method: AnalysisMethod.BENFORD_LAW,
    category: AnalysisCategory.TRANSACTION,
    name: 'Benford\'s Law Analysis',
    description: 'Analyzes first-digit distribution to detect artificial numbers.',
    enabled: false,
    severity: 'low',
    parameters: { confidenceLevel: 95, minTransactionCount: 100 }
  },
  {
    id: 't3',
    method: AnalysisMethod.ROUND_NUMBER,
    category: AnalysisCategory.TRANSACTION,
    name: 'Round Number Hoarding',
    description: 'Detects excessive frequency of round amounts (e.g., 10,000).',
    enabled: true,
    severity: 'medium',
    parameters: { thresholdPercentage: 15 }
  }
];

export const INITIAL_NODES: EngineNode[] = [
  {
    id: 'node-01',
    name: 'Engine One (Addis Ababa)',
    location: 'Ethiopia',
    apiUrl: 'https://engine.one.internal:8080',
    status: 'online',
    health: { cpuUsage: 45, ramUsage: 62, uptime: '14d 02h', throughput: 850, latency: 42 }
  },
  {
    id: 'node-02',
    name: 'Engine Two (Bahir Dar)',
    location: 'Ethiopia',
    apiUrl: 'https://engine.two.internal:8080',
    status: 'online',
    health: { cpuUsage: 32, ramUsage: 55, uptime: '3d 12h', throughput: 620, latency: 38 }
  },
  {
    id: 'node-03',
    name: 'Engine Three (Bishoftu)',
    location: 'Ethiopia',
    apiUrl: 'https://engine.three.internal:8080',
    status: 'degraded',
    health: { cpuUsage: 88, ramUsage: 91, uptime: '21d 05h', throughput: 410, latency: 156 }
  }
];