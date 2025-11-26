import React, { useState, useEffect } from 'react';
import { Database, RefreshCw, Check, AlertTriangle, Server, UploadCloud, CheckCircle2, XCircle } from 'lucide-react';
import { ConnectionConfig, EngineNode } from '../types';
import { FieldMapper } from './FieldMapper';
import { MOCK_DB_FIELDS } from '../constants';

interface DatabaseConfigProps {
  config: ConnectionConfig;
  nodes: EngineNode[];
  onUpdate: (config: ConnectionConfig) => void;
}

export const DatabaseConfig: React.FC<DatabaseConfigProps> = ({ config, nodes, onUpdate }) => {
  const [isTesting, setIsTesting] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [opResults, setOpResults] = useState<Record<string, 'success' | 'error' | 'pending'>>({});
  
  // Default to all online nodes initially
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
    
    // Simulate parallel testing/deployment to nodes
    const results: Record<string, 'success' | 'error'> = {};
    
    await Promise.all(selectedNodeIds.map(async (id) => {
      setOpResults(prev => ({ ...prev, [id]: 'pending' }));
      await new Promise(r => setTimeout(r, 800 + Math.random() * 1000));
      // fail 10% of the time for realism
      results[id] = Math.random() > 0.1 ? 'success' : 'error';
      setOpResults(prev => ({ ...prev, [id]: results[id] }));
    }));

    setIsTesting(false);

    // If at least one succeeded, mark app state as connected for UI purposes
    const anySuccess = Object.values(results).includes('success');
    if (anySuccess) {
      onUpdate({ ...config, status: 'connected', lastTest: new Date() });
    } else {
      onUpdate({ ...config, status: 'error' });
    }
  };

  const handleUploadMapping = async () => {
    if (selectedNodeIds.length === 0) return;
    setIsUploading(true);
    setOpResults({});

    await Promise.all(selectedNodeIds.map(async (id) => {
       setOpResults(prev => ({ ...prev, [id]: 'pending' }));
       await new Promise(r => setTimeout(r, 600 + Math.random() * 800));
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
          <h2 className="text-2xl font-bold text-slate-900">Central Database</h2>
          <p className="text-slate-500 mt-1">Configure the primary SQL connection for transaction history retrieval.</p>
        </div>
        <div className={`px-4 py-2 rounded-full flex items-center space-x-2 text-sm font-medium border ${
          config.status === 'connected' ? 'bg-green-50 border-green-200 text-green-700' :
          config.status === 'error' ? 'bg-red-50 border-red-200 text-red-700' :
          'bg-slate-50 border-slate-200 text-slate-600'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            config.status === 'connected' ? 'bg-green-500' :
            config.status === 'error' ? 'bg-red-500' :
            'bg-slate-400'
          }`} />
          <span>{config.status === 'connected' ? 'Connected' : config.status === 'error' ? 'Error' : 'Disconnected'}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Connection Form */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl border border-slate-200 shadow-sm h-fit">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Database className="w-5 h-5 mr-2 text-blue-600" /> Connection Details
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Host</label>
              <input 
                type="text" 
                value={config.host} 
                onChange={(e) => handleChange('host', e.target.value)}
                className="w-full bg-white text-slate-900 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Port</label>
              <input 
                type="text" 
                value={config.port} 
                onChange={(e) => handleChange('port', e.target.value)}
                className="w-full bg-white text-slate-900 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Database Name</label>
              <input 
                type="text" 
                value={config.databaseName} 
                onChange={(e) => handleChange('databaseName', e.target.value)}
                className="w-full bg-white text-slate-900 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>
            
            <div className="pt-4 border-t border-slate-100 mt-2">
              <div className="flex justify-between items-center mb-2">
                 <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">Target Nodes</label>
                 <button onClick={selectAll} className="text-xs text-blue-600 hover:text-blue-800 font-medium">Select All</button>
              </div>
              <div className="max-h-32 overflow-y-auto space-y-1 mb-4 border border-slate-100 rounded-lg p-2 bg-slate-50">
                {nodes.map(n => (
                  <div key={n.id} 
                    onClick={() => toggleNode(n.id)}
                    className={`flex items-center space-x-2 text-sm p-1.5 rounded cursor-pointer select-none transition-colors ${selectedNodeIds.includes(n.id) ? 'bg-blue-100 text-blue-800' : 'hover:bg-slate-200 text-slate-600'}`}
                  >
                    <div className={`w-3 h-3 rounded border flex items-center justify-center ${selectedNodeIds.includes(n.id) ? 'bg-blue-600 border-blue-600' : 'border-slate-400'}`}>
                      {selectedNodeIds.includes(n.id) && <Check size={10} className="text-white" />}
                    </div>
                    <span className="truncate flex-1">{n.name}</span>
                    {opResults[n.id] === 'success' && <CheckCircle2 size={14} className="text-green-500" />}
                    {opResults[n.id] === 'error' && <XCircle size={14} className="text-red-500" />}
                    {opResults[n.id] === 'pending' && <RefreshCw size={14} className="text-blue-500 animate-spin" />}
                  </div>
                ))}
              </div>

              <button 
                onClick={handleTestAndDeploy}
                disabled={isTesting || selectedNodeIds.length === 0}
                className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isTesting ? <RefreshCw className="animate-spin w-4 h-4 mr-2" /> : <RefreshCw className="w-4 h-4 mr-2" />}
                {isTesting ? 'Deploying...' : `Test & Load to ${selectedNodeIds.length} Nodes`}
              </button>
            </div>
          </div>
        </div>

        {/* Mapper */}
        <div className="lg:col-span-2 space-y-6">
          {config.status === 'connected' ? (
            <>
              <FieldMapper 
                availableFields={MOCK_DB_FIELDS}
                currentMappings={config.mappings}
                onMappingChange={(m) => handleChange('mappings', m)}
              />
              
              <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                <div>
                   <h3 className="text-sm font-bold text-slate-800">Upload Schema Mapping</h3>
                   <p className="text-xs text-slate-500 mt-1">Push the current field definitions to selected analysis engines.</p>
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
              <p>Connect to database to enable field mapping</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};