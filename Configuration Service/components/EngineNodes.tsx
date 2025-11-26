import React, { useState } from 'react';
import { EngineNode } from '../types';
import { Plus, Server, Activity, MapPin, Globe, Cpu, MoreVertical, Terminal, Trash2 } from 'lucide-react';

interface EngineNodesProps {
  nodes: EngineNode[];
  onUpdate: (nodes: EngineNode[]) => void;
}

export const EngineNodes: React.FC<EngineNodesProps> = ({ nodes, onUpdate }) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [newNode, setNewNode] = useState({ name: '', location: '', apiUrl: '' });

  const handleAdd = () => {
    if (!newNode.name || !newNode.apiUrl) return;
    
    const node: EngineNode = {
      id: Date.now().toString(),
      name: newNode.name,
      location: newNode.location || 'Unknown Location',
      apiUrl: newNode.apiUrl,
      status: 'online',
      health: {
        cpuUsage: Math.floor(Math.random() * 30) + 10,
        ramUsage: Math.floor(Math.random() * 40) + 20,
        uptime: '0h 1m',
        throughput: 0,
        latency: 20
      }
    };

    onUpdate([...nodes, node]);
    setNewNode({ name: '', location: '', apiUrl: '' });
    setShowAddForm(false);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to remove this engine node?')) {
      onUpdate(nodes.filter(n => n.id !== id));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Compute Nodes</h2>
          <p className="text-slate-500 mt-1">Manage and monitor distributed analysis engine instances.</p>
        </div>
        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
        >
          <Plus size={18} />
          <span>Add New Node</span>
        </button>
      </div>

      {showAddForm && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm animate-in fade-in slide-in-from-top-4">
          <h3 className="text-lg font-semibold mb-4">Register New Engine Node</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Instance Name</label>
              <input 
                type="text" 
                placeholder="e.g. Delta Node 01"
                value={newNode.name}
                onChange={e => setNewNode({...newNode, name: e.target.value})}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">API Endpoint URL</label>
              <input 
                type="text" 
                placeholder="https://ip:port"
                value={newNode.apiUrl}
                onChange={e => setNewNode({...newNode, apiUrl: e.target.value})}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Location (Manual)</label>
              <input 
                type="text" 
                placeholder="City, Country"
                value={newNode.location}
                onChange={e => setNewNode({...newNode, location: e.target.value})}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex justify-end space-x-3">
             <button onClick={() => setShowAddForm(false)} className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
             <button onClick={handleAdd} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Register Node</button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {nodes.map(node => (
          <div key={node.id} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-5 border-b border-slate-100 flex justify-between items-start bg-slate-50/50">
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-lg ${
                  node.status === 'online' ? 'bg-green-100 text-green-600' :
                  node.status === 'degraded' ? 'bg-orange-100 text-orange-600' :
                  'bg-red-100 text-red-600'
                }`}>
                  <Server size={20} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">{node.name}</h3>
                  <div className="flex items-center text-xs text-slate-500 mt-0.5">
                    <MapPin size={12} className="mr-1" />
                    {node.location}
                    <span className="mx-2">•</span>
                    <span className="font-mono">{node.apiUrl}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                 <div className={`px-2 py-1 rounded text-xs font-bold uppercase ${
                    node.status === 'online' ? 'bg-green-100 text-green-700' :
                    node.status === 'degraded' ? 'bg-orange-100 text-orange-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {node.status}
                  </div>
                  <button onClick={() => handleDelete(node.id)} className="p-1 text-slate-400 hover:text-red-500 transition-colors">
                    <Trash2 size={16} />
                  </button>
              </div>
            </div>

            <div className="p-5 grid grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-500 font-medium">CPU Load</span>
                    <span className="text-slate-900 font-bold">{node.health.cpuUsage}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${node.health.cpuUsage > 80 ? 'bg-red-500' : 'bg-blue-500'}`} 
                      style={{ width: `${node.health.cpuUsage}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-500 font-medium">Memory Usage</span>
                    <span className="text-slate-900 font-bold">{node.health.ramUsage}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${node.health.ramUsage > 80 ? 'bg-red-500' : 'bg-purple-500'}`} 
                      style={{ width: `${node.health.ramUsage}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                   <span className="text-sm text-slate-500 flex items-center"><Activity size={14} className="mr-2" /> Throughput</span>
                   <span className="text-sm font-mono font-bold text-slate-900">{node.health.throughput} TPS</span>
                </div>
                <div className="flex justify-between items-center">
                   <span className="text-sm text-slate-500 flex items-center"><Terminal size={14} className="mr-2" /> Latency</span>
                   <span className="text-sm font-mono font-bold text-slate-900">{node.health.latency}ms</span>
                </div>
                <div className="flex justify-between items-center">
                   <span className="text-sm text-slate-500 flex items-center"><Activity size={14} className="mr-2" /> Uptime</span>
                   <span className="text-sm font-mono font-bold text-slate-900">{node.health.uptime}</span>
                </div>
              </div>
            </div>

            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
               <button className="text-xs font-medium text-blue-600 hover:text-blue-800">View Node Logs</button>
               <button className="text-xs font-medium text-slate-500 hover:text-slate-700">Health Check Endpoint &rarr;</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};