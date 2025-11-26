import React, { useState, useEffect } from 'react';
import { Radio, RefreshCw, AlertTriangle, Check, CheckCircle2, XCircle, UploadCloud } from 'lucide-react';
import { ConnectionConfig, EngineNode } from '../types';
import { FieldMapper } from './FieldMapper';
import { MOCK_KAFKA_FIELDS } from '../constants';

interface BrokerConfigProps {
  config: ConnectionConfig;
  nodes: EngineNode[];
  onUpdate: (config: ConnectionConfig) => void;
}

export const BrokerConfig: React.FC<BrokerConfigProps> = ({ config, nodes, onUpdate }) => {
  const [isTesting, setIsTesting] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [opResults, setOpResults] = useState<Record<string, 'success' | 'error' | 'pending'>>({});
  
  const [selectedNodeIds, setSelectedNodeIds] = useState<string[]>([]);

  useEffect(() => {
    // Initialize selection to all online nodes if not set
    if (selectedNodeIds.length === 0 && nodes.length > 0) {
      setSelectedNodeIds(nodes.filter(n => n.status !== 'offline').map(n => n.id));
    }
  }, [nodes]);

  const toggleNode = (id: string) => {
    setSelectedNodeIds(prev => 
      prev.includes(id) ? prev.filter(n => n !== id) : [...prev, id]
    );
  };

  const selectAll = () => setSelectedNodeIds(nodes.map(n => n.id));
  
  const handleTestAndDeploy = async () => {
    if (selectedNodeIds.length === 0) return;
    setIsTesting(true);
    setOpResults({});

    const results: Record<string, 'success' | 'error'> = {};
    
    await Promise.all(selectedNodeIds.map(async (id) => {
      setOpResults(prev => ({ ...prev, [id]: 'pending' }));
      await new Promise(r => setTimeout(r, 800 + Math.random() * 1000));
      results[id] = 'success'; // Assume kafka connects fine usually
      setOpResults(prev => ({ ...prev, [id]: results[id] }));
    }));

    setIsTesting(false);
    onUpdate({ ...config, status: 'connected', lastTest: new Date() });
  };

  const handleUploadMapping = async () => {
    if (selectedNodeIds.length === 0) return;
    setIsUploading(true);
    setOpResults({});

    await Promise.all(selectedNodeIds.map(async (id) => {
       setOpResults(prev => ({ ...prev, [id]: 'pending' }));
       await new Promise(r => setTimeout(r, 500 + Math.random() * 500));
       setOpResults(prev => ({ ...prev, [id]: 'success' }));
    }));

    setIsUploading(false);
  };

  const handleChange = (field: keyof ConnectionConfig, value: any) => {
    onUpdate({ ...config, [field]: value, status: 'disconnected' });
  };

  return (
    <div className="space-y-6">
       <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Message Broker (Kafka)</h2>
          <p className="text-slate-500 mt-1">Configure real-time ingestion streams for live transaction monitoring.</p>
        </div>
        <div className={`px-4 py-2 rounded-full flex items-center space-x-2 text-sm font-medium border ${
          config.status === 'connected' ? 'bg-green-50 border-green-200 text-green-700' :
          'bg-slate-50 border-slate-200 text-slate-600'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            config.status === 'connected' ? 'bg-green-500' : 'bg-slate-400'
          }`} />
          <span>{config.status === 'connected' ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-fit">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Radio className="w-5 h-5 mr-2 text-purple-600" /> Broker Details
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Bootstrap Servers</label>
              <input 
                type="text" 
                value={config.host} 
                onChange={(e) => handleChange('host', e.target.value)}
                placeholder="broker1:9092,broker2:9092"
                className="w-full bg-white text-slate-900 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-purple-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Topic Name</label>
              <input 
                type="text" 
                value={config.topicName} 
                onChange={(e) => handleChange('topicName', e.target.value)}
                className="w-full bg-white text-slate-900 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-purple-500 outline-none"
              />
            </div>
            
            <div className="pt-4 border-t border-slate-100 mt-2">
               <div className="flex justify-between items-center mb-2">
                 <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Target Nodes</label>
                 <button onClick={selectAll} className="text-xs text-purple-600 hover:text-purple-800 font-medium">Select All</button>
              </div>
              <div className="max-h-32 overflow-y-auto space-y-1 mb-4 border border-slate-100 rounded-lg p-2 bg-slate-50">
                {nodes.map(n => (
                  <div key={n.id} 
                    onClick={() => toggleNode(n.id)}
                    className={`flex items-center space-x-2 text-sm p-1.5 rounded cursor-pointer select-none transition-colors ${selectedNodeIds.includes(n.id) ? 'bg-purple-100 text-purple-800' : 'hover:bg-slate-200 text-slate-600'}`}
                  >
                    <div className={`w-3 h-3 rounded border flex items-center justify-center ${selectedNodeIds.includes(n.id) ? 'bg-purple-600 border-purple-600' : 'border-slate-400'}`}>
                      {selectedNodeIds.includes(n.id) && <Check size={10} className="text-white" />}
                    </div>
                    <span className="truncate flex-1">{n.name}</span>
                    {opResults[n.id] === 'success' && <CheckCircle2 size={14} className="text-green-500" />}
                    {opResults[n.id] === 'error' && <XCircle size={14} className="text-red-500" />}
                    {opResults[n.id] === 'pending' && <RefreshCw size={14} className="text-purple-500 animate-spin" />}
                  </div>
                ))}
              </div>

              <button 
                onClick={handleTestAndDeploy}
                disabled={isTesting || selectedNodeIds.length === 0}
                className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none disabled:opacity-50"
              >
                {isTesting ? <RefreshCw className="animate-spin w-4 h-4 mr-2" /> : <RefreshCw className="w-4 h-4 mr-2" />}
                {isTesting ? 'Deploying Config...' : `Test & Deploy to ${selectedNodeIds.length} Nodes`}
              </button>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {config.status === 'connected' ? (
            <>
              <FieldMapper 
                availableFields={MOCK_KAFKA_FIELDS}
                currentMappings={config.mappings}
                onMappingChange={(m) => handleChange('mappings', m)}
              />
              <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                <div>
                   <h3 className="text-sm font-bold text-slate-800">Upload Topic Schema</h3>
                   <p className="text-xs text-slate-500 mt-1">Push the current JSON payload map to selected ingestion nodes.</p>
                </div>
                <button 
                  onClick={handleUploadMapping}
                  disabled={isUploading || selectedNodeIds.length === 0}
                  className="flex items-center px-4 py-2 bg-slate-800 text-white rounded-lg hover:bg-slate-900 transition-colors disabled:opacity-50 text-sm font-medium"
                >
                  {isUploading ? <RefreshCw className="animate-spin w-4 h-4 mr-2" /> : <UploadCloud className="w-4 h-4 mr-2" />}
                  Upload to {selectedNodeIds.length} Services
                </button>
              </div>
            </>
          ) : (
             <div className="h-full min-h-[300px] bg-slate-50 rounded-xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-400">
              <AlertTriangle className="w-12 h-12 mb-3 opacity-50" />
              <p>Connect to broker to enable payload mapping</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};