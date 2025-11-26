import React, { useState } from 'react';
import { Layout } from './components/Layout';
import { DatabaseConfig } from './components/DatabaseConfig';
import { BrokerConfig } from './components/BrokerConfig';
import { RiskLists } from './components/RiskLists';
import { AnalysisConfig } from './components/AnalysisConfig';
import { EngineNodes } from './components/EngineNodes';
import { GeneralSettings } from './components/GeneralSettings';
import { AppState } from './types';
import { INITIAL_DB_CONFIG, INITIAL_KAFKA_CONFIG, INITIAL_RISK_LISTS, INITIAL_RULES, INITIAL_NODES } from './constants';
import { 
  AreaChart, Area, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ComposedChart 
} from 'recharts';
import { 
  Activity, Clock, Cpu, Database, Globe, Radio, 
  Server, ShieldAlert, Zap, CheckCircle, XCircle,
  ArrowUpRight, ArrowDownRight, Terminal, Layers, FileText
} from 'lucide-react';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [state, setState] = useState<AppState>({
    dbConfig: INITIAL_DB_CONFIG,
    kafkaConfig: INITIAL_KAFKA_CONFIG,
    riskLists: INITIAL_RISK_LISTS,
    analysisRules: INITIAL_RULES,
    nodes: INITIAL_NODES
  });

  // Derived Metrics
  const totalThroughput = state.nodes.reduce((acc, node) => acc + node.health.throughput, 0);
  const avgLatency = Math.round(state.nodes.reduce((acc, node) => acc + node.health.latency, 0) / (state.nodes.length || 1));
  const activeNodes = state.nodes.filter(n => n.status === 'online').length;

  // Mock Dashboard Data
  const performanceData = [
    { time: '00:00', tps: 2400, latency: 45 },
    { time: '04:00', tps: 1398, latency: 38 },
    { time: '08:00', tps: 9800, latency: 65 },
    { time: '12:00', tps: 3908, latency: 50 },
    { time: '16:00', tps: 4800, latency: 48 },
    { time: '20:00', tps: 3800, latency: 42 },
    { time: '23:59', tps: 2100, latency: 40 },
  ];

  // Inventory Counts
  const sanctionCount = state.riskLists.filter(l => l.type === 'sanction').length;
  const watchlistCount = state.riskLists.filter(l => l.type === 'watchlist').length;
  const countryCount = state.riskLists.filter(l => l.type === 'high_risk_country').length;
  const activeRulesCount = state.analysisRules.filter(r => r.enabled).length;

  const MetricCard = ({ label, value, subtext, icon: Icon, color, trend }: any) => (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start justify-between">
      <div className="flex items-start space-x-4">
        <div className={`p-3 rounded-lg bg-${color}-50 text-${color}-600`}>
          <Icon size={24} />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
          {subtext && <p className="text-xs text-slate-400 mt-1">{subtext}</p>}
        </div>
      </div>
      {trend && (
        <div className={`flex items-center text-xs font-medium ${trend === 'up' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'} px-2 py-1 rounded-full`}>
          {trend === 'up' ? <ArrowUpRight size={14} className="mr-1" /> : <ArrowDownRight size={14} className="mr-1" />}
          {trend === 'up' ? '+12%' : '-4%'}
        </div>
      )}
    </div>
  );

  const InfoCard = ({ title, icon: Icon, status, items, color }: any) => (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-full">
      <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg bg-${color}-100 text-${color}-600`}>
            <Icon size={18} />
          </div>
          <h3 className="font-semibold text-slate-800">{title}</h3>
        </div>
        {status && (
          <div className={`px-2 py-0.5 rounded text-xs font-bold uppercase flex items-center ${
            status === 'connected' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {status === 'connected' ? <CheckCircle size={12} className="mr-1"/> : <XCircle size={12} className="mr-1"/>}
            {status}
          </div>
        )}
      </div>
      <div className="p-5 flex-1 flex flex-col justify-center">
        <div className="space-y-3">
          {items.map((item: any, idx: number) => (
            <div key={idx} className="flex justify-between items-center">
              <span className="text-sm text-slate-500">{item.label}</span>
              <span className="text-sm font-medium text-slate-900 font-mono text-right">{item.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'database':
        return <DatabaseConfig config={state.dbConfig} nodes={state.nodes} onUpdate={(c) => setState(prev => ({ ...prev, dbConfig: c }))} />;
      case 'kafka':
        return <BrokerConfig config={state.kafkaConfig} nodes={state.nodes} onUpdate={(c) => setState(prev => ({ ...prev, kafkaConfig: c }))} />;
      case 'analysis':
        return <AnalysisConfig rules={state.analysisRules} onUpdate={(r) => setState(prev => ({ ...prev, analysisRules: r }))} />;
      case 'sanctions':
        return <RiskLists mode="sanction" lists={state.riskLists} onUpdate={(l) => setState(prev => ({ ...prev, riskLists: l }))} />;
      case 'watchlists':
        return <RiskLists mode="watchlist" lists={state.riskLists} onUpdate={(l) => setState(prev => ({ ...prev, riskLists: l }))} />;
      case 'countries':
        return <RiskLists mode="high_risk_country" lists={state.riskLists} onUpdate={(l) => setState(prev => ({ ...prev, riskLists: l }))} />;
      case 'nodes':
        return <EngineNodes nodes={state.nodes} onUpdate={(n) => setState(prev => ({ ...prev, nodes: n }))} />;
      case 'settings':
        return <GeneralSettings nodes={state.nodes} />;
      case 'dashboard':
      default:
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-end">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">System Dashboard</h2>
                <p className="text-slate-500 mt-1">Operational overview of {state.nodes.length} active analysis engines.</p>
              </div>
              <div className="flex items-center space-x-2 text-sm text-green-700 bg-green-50 px-3 py-1.5 rounded-full border border-green-200 shadow-sm">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                  </span>
                  <span className="font-semibold">System Operational</span>
              </div>
            </div>

            {/* KPI Metrics - 3 Columns */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <MetricCard 
                label="Total Throughput" 
                value={`${totalThroughput.toLocaleString()}`} 
                subtext="Transactions per second" 
                icon={Zap} 
                color="blue"
                trend="up" 
              />
              <MetricCard 
                label="Avg Latency" 
                value={`${avgLatency}ms`} 
                subtext="Global weighted average" 
                icon={Clock} 
                color="purple" 
                trend="down"
              />
              <MetricCard 
                label="Compute Grid" 
                value={`${activeNodes}/${state.nodes.length}`} 
                subtext="Nodes Online" 
                icon={Server} 
                color="slate" 
              />
            </div>

            {/* Traffic Chart */}
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h3 className="text-lg font-semibold text-slate-800">Traffic & Performance</h3>
                  <p className="text-xs text-slate-500">Transaction volume vs Processing latency (24h)</p>
                </div>
                <div className="flex items-center space-x-4 text-xs">
                    <div className="flex items-center"><div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>Volume (TPS)</div>
                    <div className="flex items-center"><div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>Latency (ms)</div>
                </div>
              </div>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} dy={10} />
                    <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                    <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                    <Tooltip 
                      contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} 
                      labelStyle={{color: '#64748b', marginBottom: '5px'}}
                    />
                    <Area yAxisId="left" type="monotone" dataKey="tps" fill="url(#colorTps)" stroke="#3b82f6" fillOpacity={0.1} strokeWidth={2} />
                    <Line yAxisId="right" type="monotone" dataKey="latency" stroke="#8b5cf6" strokeWidth={2} dot={{r: 4, strokeWidth: 0, fill: '#8b5cf6'}} activeDot={{r: 6}} />
                    <defs>
                      <linearGradient id="colorTps" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Operational Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <InfoCard 
                title="Database Cluster" 
                icon={Database} 
                color="blue"
                status={state.dbConfig.status}
                items={[
                  { label: 'Host', value: state.dbConfig.host },
                  { label: 'Port', value: state.dbConfig.port },
                  { label: 'Database', value: state.dbConfig.databaseName },
                  { label: 'Connection Pool', value: 'Active' },
                ]}
              />
              <InfoCard 
                title="Message Broker" 
                icon={Radio} 
                color="purple"
                status={state.kafkaConfig.status}
                items={[
                  { label: 'Bootstrap Servers', value: state.kafkaConfig.host.split(',')[0] + '...' },
                  { label: 'Ingest Topic', value: state.kafkaConfig.topicName },
                  { label: 'Partitions', value: '16' },
                  { label: 'Replication Factor', value: '3' },
                ]}
              />
               <InfoCard 
                title="Risk Data Inventory" 
                icon={ShieldAlert} 
                color="orange"
                // status="connected"
                items={[
                  { label: 'Sanction Lists', value: sanctionCount },
                  { label: 'Watchlist Entries', value: watchlistCount },
                  { label: 'High Risk Countries', value: countryCount },
                  { label: 'Active Rules', value: activeRulesCount },
                ]}
              />
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Node Status Grid */}
              <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                 <div className="flex justify-between items-center mb-4">
                    <h3 className="font-semibold text-slate-800">Node Health Grid</h3>
                    <span className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-full">{state.nodes.length} Nodes</span>
                 </div>
                 <div className="space-y-3">
                   {state.nodes.map(node => (
                     <div key={node.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <div className="flex items-center space-x-3">
                           <div className={`w-2 h-2 rounded-full ${node.status === 'online' ? 'bg-green-500' : node.status === 'degraded' ? 'bg-orange-500' : 'bg-red-500'}`} />
                           <div>
                              <p className="text-sm font-medium text-slate-700">{node.name}</p>
                              <p className="text-xs text-slate-400">{node.location}</p>
                           </div>
                        </div>
                        <div className="text-right flex items-center space-x-6">
                           <div>
                              <p className="text-xs text-slate-500">CPU</p>
                              <p className="text-xs font-mono font-bold text-slate-700">{node.health.cpuUsage}%</p>
                           </div>
                           <div>
                              <p className="text-xs text-slate-500">RAM</p>
                              <p className="text-xs font-mono font-bold text-slate-700">{node.health.ramUsage}%</p>
                           </div>
                           <div>
                              <p className="text-xs text-slate-500">LATENCY</p>
                              <p className="text-xs font-mono font-bold text-slate-700">{node.health.latency}ms</p>
                           </div>
                        </div>
                     </div>
                   ))}
                 </div>
                 <button onClick={() => setActiveTab('nodes')} className="w-full py-2 text-xs text-blue-600 font-medium hover:bg-blue-50 rounded-lg transition-colors mt-3">
                   View Detailed Node Telemetry &rarr;
                 </button>
              </div>

              {/* Infrastructure Details */}
              <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-semibold text-slate-800 mb-4">Infrastructure Status</h3>
                <div className="space-y-6">
                   <div>
                      <div className="flex items-center justify-between mb-2">
                         <div className="flex items-center text-sm text-slate-600"><Database size={14} className="mr-2" /> Database Pool</div>
                         <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded">Healthy</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1">
                        <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '65%' }}></div>
                      </div>
                      <div className="flex justify-between text-xs text-slate-400">
                        <span>65 Active Connections</span>
                        <span>Capacity: 100</span>
                      </div>
                   </div>

                   <div>
                      <div className="flex items-center justify-between mb-2">
                         <div className="flex items-center text-sm text-slate-600"><Radio size={14} className="mr-2" /> Kafka Consumer Lag</div>
                         <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded">Optimal</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1">
                        <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: '12%' }}></div>
                      </div>
                      <div className="flex justify-between text-xs text-slate-400">
                        <span>12ms Lag</span>
                        <span>Threshold: 200ms</span>
                      </div>
                   </div>

                   <div>
                      <div className="flex items-center justify-between mb-2">
                         <div className="flex items-center text-sm text-slate-600"><Cpu size={14} className="mr-2" /> Grid CPU Load</div>
                         <span className="text-xs font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded">Heavy</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-1.5 mb-1">
                        <div className="bg-slate-600 h-1.5 rounded-full" style={{ width: '78%' }}></div>
                      </div>
                      <div className="flex justify-between text-xs text-slate-400">
                        <span>78% Avg Utilization</span>
                        <span>Peak: 92%</span>
                      </div>
                   </div>
                </div>
              </div>

            </div>
          </div>
        );
    }
  };

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {renderContent()}
    </Layout>
  );
};

export default App;