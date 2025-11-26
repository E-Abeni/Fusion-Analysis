import React, { useState } from 'react';
import { EngineNode } from '../types';
import { Server, FileJson, Check, RefreshCw, Copy, Terminal, Code2, Cpu } from 'lucide-react';

interface GeneralSettingsProps {
  nodes: EngineNode[];
}

export const GeneralSettings: React.FC<GeneralSettingsProps> = ({ nodes }) => {
  const [selectedNodes, setSelectedNodes] = useState<string[]>([]);
  const [configs, setConfigs] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<string | null>(null);

  const handleToggle = (id: string) => {
    setSelectedNodes(prev => prev.includes(id) ? prev.filter(n => n !== id) : [...prev, id]);
  };

  const handleSelectAll = () => {
    if (selectedNodes.length === nodes.length) {
      setSelectedNodes([]);
    } else {
      setSelectedNodes(nodes.map(n => n.id));
    }
  };

  const handleFetch = async () => {
    if (selectedNodes.length === 0) return;
    setLoading(true);
    setConfigs({});
    setActiveTab(null);
    
    // Simulate API calls to multiple nodes
    const newConfigs: Record<string, string> = {};
    
    await Promise.all(selectedNodes.map(async (id) => {
      await new Promise(r => setTimeout(r, 600 + Math.random() * 800));
      const node = nodes.find(n => n.id === id);
      
      // Mock Configuration Payload simulation
      const mockConfig = {
        system: {
          nodeId: node?.id,
          hostname: `worker-${node?.location.toLowerCase().replace(/\s/g, '-')}-01`,
          version: "2.4.1-stable",
          buildHash: "a1b2c3d4",
          uptimeSeconds: Math.floor(Math.random() * 1000000),
          env: "production"
        },
        connections: {
          database: {
            active: true,
            type: "POSTGRES",
            poolSize: 40,
            activeConnections: Math.floor(Math.random() * 30),
            idleTimeout: 30000
          },
          kafka: {
             active: true,
             bootstrapServers: "broker-01.internal:9092",
             topics: ["tx-ingress-live", "tx-dlq"],
             consumerGroup: "sconsumer-01",
             lag: Math.floor(Math.random() * 20)
          }
        },
        schema: {
           validationMode: "STRICT",
           fieldCount: 14,
           mappedFields: ["amount", "currency", "transaction_id", "timestamp", "branch_id", "branch_name"],
           lastValidation: new Date().toISOString()
        },
        engine: {
           ruleSetVersion: "v1",
           activeRules: Math.floor(Math.random() * 50) + 100,
           riskThresholds: {
             high: 90,
             medium: 65,
             low: 30
           },
           hotSwappable: true
        }
      };
      
      newConfigs[id] = JSON.stringify(mockConfig, null, 2);
    }));

    setConfigs(newConfigs);
    // Automatically select the first one that returned
    if (selectedNodes.length > 0) {
      setActiveTab(selectedNodes[0]);
    }
    setLoading(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">General Settings</h2>
          <p className="text-slate-500 mt-1">Inspect runtime configurations directly from active engine nodes.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
        
        {/* Left Column: Selection & Controls */}
        <div className="lg:col-span-1 flex flex-col space-y-4">
          
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex-shrink-0">
             <h3 className="font-semibold text-slate-800 mb-4 flex items-center">
               <Server size={18} className="mr-2 text-blue-600" /> Target Nodes
             </h3>
             
             <div className="flex justify-between items-center mb-3 text-xs">
                <span className="text-slate-500 font-medium">{selectedNodes.length} Selected</span>
                <button onClick={handleSelectAll} className="text-blue-600 hover:text-blue-800 font-medium">
                  {selectedNodes.length === nodes.length ? 'Deselect All' : 'Select All'}
                </button>
             </div>

             <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
               {nodes.map(node => (
                 <div 
                   key={node.id}
                   onClick={() => handleToggle(node.id)}
                   className={`p-3 rounded-lg border cursor-pointer transition-all flex items-center justify-between ${
                     selectedNodes.includes(node.id) 
                       ? 'bg-blue-50 border-blue-200 shadow-sm' 
                       : 'bg-white border-slate-200 hover:bg-slate-50'
                   }`}
                 >
                   <div className="flex items-center space-x-3 overflow-hidden">
                     <div className={`w-2 h-2 rounded-full flex-shrink-0 ${node.status === 'online' ? 'bg-green-500' : 'bg-slate-300'}`} />
                     <div>
                       <p className={`text-sm font-medium truncate ${selectedNodes.includes(node.id) ? 'text-blue-900' : 'text-slate-700'}`}>{node.name}</p>
                       <p className="text-xs text-slate-400 truncate">{node.apiUrl}</p>
                     </div>
                   </div>
                   {selectedNodes.includes(node.id) && <Check size={16} className="text-blue-600" />}
                 </div>
               ))}
             </div>

             <div className="mt-6">
               <button
                 onClick={handleFetch}
                 disabled={loading || selectedNodes.length === 0}
                 className="w-full flex justify-center items-center py-2.5 px-4 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm shadow-sm"
               >
                 {loading ? <RefreshCw className="animate-spin w-4 h-4 mr-2" /> : <Terminal className="w-4 h-4 mr-2" />}
                 {loading ? 'Fetching Configs...' : 'Retrieve Configuration'}
               </button>
             </div>
          </div>

          {/* Quick Help */}
          <div className="bg-blue-50 p-5 rounded-xl border border-blue-100 text-blue-900 flex-1">
            <h4 className="font-semibold text-sm mb-2 flex items-center"><Code2 size={16} className="mr-2"/> Configuration Dump</h4>
            <p className="text-xs leading-relaxed text-blue-800/80">
              The retrieved JSON represents the actual in-memory configuration of the running service, including:
            </p>
            <ul className="mt-2 space-y-1 text-xs list-disc list-inside text-blue-800/80">
              <li>Active Database Pool State</li>
              <li>Kafka Consumer Lag & Topics</li>
              <li>Loaded Schema Validation Rules</li>
              <li>Rule Engine Version Hash</li>
            </ul>
          </div>

        </div>

        {/* Right Column: Code Display */}
        <div className="lg:col-span-2 bg-slate-900 rounded-xl shadow-xl overflow-hidden flex flex-col border border-slate-800">
          
          {/* Tab Bar */}
          <div className="flex items-center bg-slate-950 border-b border-slate-800 px-2 pt-2 overflow-x-auto no-scrollbar">
            {Object.keys(configs).length > 0 ? (
              Object.keys(configs).map(nodeId => {
                const node = nodes.find(n => n.id === nodeId);
                return (
                  <button
                    key={nodeId}
                    onClick={() => setActiveTab(nodeId)}
                    className={`flex items-center space-x-2 px-4 py-3 text-xs font-medium rounded-t-lg border-t border-x mr-1 transition-colors min-w-[120px] max-w-[200px] ${
                      activeTab === nodeId
                        ? 'bg-slate-900 border-slate-700 text-blue-400 border-b-slate-900' // 'active' look
                        : 'bg-slate-950 border-transparent text-slate-500 hover:bg-slate-900 hover:text-slate-300'
                    }`}
                  >
                    <Cpu size={12} />
                    <span className="truncate">{node?.name || nodeId}</span>
                  </button>
                )
              })
            ) : (
              <div className="px-4 py-3 text-xs text-slate-600 font-mono">NO_DATA</div>
            )}
          </div>

          {/* Code Area */}
          <div className="flex-1 overflow-auto p-4 relative font-mono text-sm group">
            {activeTab && configs[activeTab] ? (
              <>
                <button 
                  onClick={() => copyToClipboard(configs[activeTab])}
                  className="absolute top-4 right-4 p-2 bg-slate-800 text-slate-400 rounded hover:bg-slate-700 hover:text-white transition-colors opacity-0 group-hover:opacity-100"
                  title="Copy JSON"
                >
                  <Copy size={14} />
                </button>
                <pre className="text-green-400">
                  <code>{configs[activeTab]}</code>
                </pre>
              </>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-slate-600">
                <FileJson size={48} className="mb-4 opacity-20" />
                <p className="text-sm">Select nodes and click "Retrieve Configuration"</p>
                <p className="text-xs mt-2 opacity-50">Response data will appear here</p>
              </div>
            )}
          </div>
          
          {/* Status Footer */}
          <div className="bg-slate-950 px-4 py-2 border-t border-slate-800 flex justify-between items-center text-[10px] text-slate-500 font-mono">
            <span>STATUS: {loading ? 'RECEIVING STREAM...' : Object.keys(configs).length > 0 ? 'OK' : 'IDLE'}</span>
            <span>FORMAT: APPLICATION/JSON</span>
          </div>

        </div>

      </div>
    </div>
  );
};
