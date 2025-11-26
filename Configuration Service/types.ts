export enum DataSourceType {
  DATABASE = 'DATABASE',
  KAFKA = 'KAFKA'
}

export interface FieldMapping {
  sourceField: string;
  engineField: string;
  dataType: 'string' | 'number' | 'date' | 'boolean';
  isRequired: boolean;
}

export interface ConnectionConfig {
  type: DataSourceType;
  host: string;
  port: string;
  username?: string;
  password?: string; // In real app, handle securely
  databaseName?: string; // For DB
  topicName?: string; // For Kafka
  status: 'disconnected' | 'connected' | 'error';
  lastTest?: Date;
  mappings: FieldMapping[];
}

export interface RiskListEntry {
  id: string;
  name: string;
  type: 'sanction' | 'watchlist' | 'high_risk_country';
  riskScore: number; // 0-100
  code?: string; 
  updatedAt: string;
}

export enum AnalysisCategory {
  CUSTOMER = 'CUSTOMER',
  TRANSACTION = 'TRANSACTION'
}

export enum AnalysisMethod {
  PEER_GROUP = 'PEER_GROUP',
  TIME_SERIES_GAP = 'TIME_SERIES_GAP',
  KYC_INTEGRITY = 'KYC_INTEGRITY',
  CUSTOMER_RISK_SCORE = 'CUSTOMER_RISK_SCORE',
  SANCTION_MATCH = 'SANCTION_MATCH',
  TIME_WINDOW_AGGREGATION = 'TIME_WINDOW_AGGREGATION',
  VARIANCE_ANALYSIS = 'VARIANCE_ANALYSIS',
  Z_SCORE = 'Z_SCORE',
  FREQUENCY_ANALYSIS = 'FREQUENCY_ANALYSIS',
  TURNOVER_RATIO = 'TURNOVER_RATIO',
  BENFORD_LAW = 'BENFORD_LAW',
  ROUND_NUMBER = 'ROUND_NUMBER',
  GEO_RISK = 'GEO_RISK'
}

export interface AnalysisRule {
  id: string;
  method: AnalysisMethod;
  category: AnalysisCategory;
  name: string;
  description: string;
  enabled: boolean;
  parameters: Record<string, number | string | boolean>; // Flexible params
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface EngineNode {
  id: string;
  name: string;
  location: string;
  apiUrl: string;
  status: 'online' | 'offline' | 'degraded';
  health: {
    cpuUsage: number; // Percentage 0-100
    ramUsage: number; // Percentage 0-100
    uptime: string;
    throughput: number; // TPS
    latency: number; // ms
  };
}

export interface AppState {
  dbConfig: ConnectionConfig;
  kafkaConfig: ConnectionConfig;
  riskLists: RiskListEntry[];
  analysisRules: AnalysisRule[];
  nodes: EngineNode[];
}