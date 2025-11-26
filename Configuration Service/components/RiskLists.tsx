import React, { useState, useEffect } from 'react';
import { RiskListEntry } from '../types';
import { Plus, Trash2, Search, Globe, ShieldAlert, Eye, X, Save } from 'lucide-react';

interface RiskListsProps {
  mode: 'sanction' | 'watchlist' | 'high_risk_country';
  lists: RiskListEntry[]; // Expects the full list from state
  onUpdate: (lists: RiskListEntry[]) => void;
}

export const RiskLists: React.FC<RiskListsProps> = ({ mode, lists, onUpdate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [newItem, setNewItem] = useState({ name: '', score: 75, code: '' });

  // Reset state when switching between list modes (e.g. Sanctions -> Watchlists)
  useEffect(() => {
    setSearchTerm('');
    setShowAddModal(false);
    setNewItem({ name: '', score: 75, code: '' });
  }, [mode]);

  // Filter the full list to only show items relevant to this mode AND matching search
  const filteredLists = lists.filter(l => {
    if (l.type !== mode) return false;
    const term = searchTerm.toLowerCase();
    return l.name.toLowerCase().includes(term) || (l.code && l.code.toLowerCase().includes(term));
  });

  const handleDelete = (id: string) => {
    // We update the FULL list by filtering out the ID, preserving other types
    onUpdate(lists.filter(l => l.id !== id));
  };

  const handleSave = () => {
    if (!newItem.name.trim()) return;

    const newEntry: RiskListEntry = {
      id: Date.now().toString(),
      name: newItem.name,
      type: mode,
      riskScore: newItem.score,
      updatedAt: new Date().toISOString().split('T')[0],
      code: mode === 'high_risk_country' ? (newItem.code || 'XX').toUpperCase() : undefined
    };

    onUpdate([...lists, newEntry]);
    setShowAddModal(false);
    setNewItem({ name: '', score: 75, code: '' });
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-red-600 bg-red-50 border-red-100';
    if (score >= 70) return 'text-orange-600 bg-orange-50 border-orange-100';
    return 'text-yellow-600 bg-yellow-50 border-yellow-100';
  };

  const getPageDetails = () => {
    switch(mode) {
      case 'sanction': return { title: 'Sanction Lists', desc: 'Manage local sanction list.', icon: ShieldAlert, entity: 'Sanction List' };
      case 'watchlist': return { title: 'Watchlists', desc: 'Monitor PEPs and adverse media watchlists.', icon: Eye, entity: 'Watchlist Entry' };
      case 'high_risk_country': return { title: 'High Risk Countries', desc: 'Configure jurisdictional risk scores and FATF gray/black lists.', icon: Globe, entity: 'Country' };
    }
  };

  const details = getPageDetails();
  const Icon = details.icon;

  return (
    <div className="space-y-6 relative">
      
      {/* Add Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full overflow-hidden border border-slate-200">
            <div className="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h3 className="font-bold text-slate-800">Add New {details.entity}</h3>
              <button 
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
                <input 
                  type="text"
                  autoFocus
                  placeholder={`e.g. ${mode === 'high_risk_country' ? 'Eritrea' : 'Abebe Bekele'}`}
                  value={newItem.name}
                  onChange={(e) => setNewItem({...newItem, name: e.target.value})}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-900"
                />
              </div>

              {mode === 'high_risk_country' && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Country Code (2-Char)</label>
                  <input 
                    type="text"
                    maxLength={2}
                    placeholder="e.g. ER"
                    value={newItem.code}
                    onChange={(e) => setNewItem({...newItem, code: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none uppercase font-mono text-slate-900"
                  />
                </div>
              )}

              <div>
                 <div className="flex justify-between mb-1">
                    <label className="block text-sm font-medium text-slate-700">Risk Score</label>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${getScoreColor(newItem.score)}`}>{newItem.score}</span>
                 </div>
                 <input 
                    type="range"
                    min="0"
                    max="100"
                    value={newItem.score}
                    onChange={(e) => setNewItem({...newItem, score: parseInt(e.target.value)})}
                    className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                  />
                 <div className="flex justify-between text-xs text-slate-400 mt-1">
                   <span>Low Risk (0)</span>
                   <span>Critical (100)</span>
                 </div>
              </div>
            </div>

            <div className="p-5 border-t border-slate-100 bg-slate-50 flex justify-end space-x-3">
              <button 
                onClick={() => setShowAddModal(false)} 
                className="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg text-sm font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleSave}
                disabled={!newItem.name}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors disabled:opacity-50 flex items-center shadow-sm"
              >
                <Save size={16} className="mr-2" />
                Save Entry
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 flex items-center">
            <Icon className="mr-3 text-blue-600" size={28} />
            {details.title}
          </h2>
          <p className="text-slate-500 mt-1">{details.desc}</p>
        </div>
        <button 
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
        >
          <Plus size={18} />
          <span>Add {details.entity}</span>
        </button>
      </div>

      {/* Main Content Area */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        
        {/* Search Bar */}
        <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text" 
              placeholder={`Search ${details.title.toLowerCase()}...`} 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-900"
            />
          </div>
        </div>

        {/* Table */}
        {filteredLists.length === 0 ? (
           <div className="p-12 text-center text-slate-400">
             <p>No matching entries found.</p>
             <button onClick={() => { setSearchTerm(''); setShowAddModal(true); }} className="text-blue-600 hover:underline mt-2 text-sm">Add a new entry</button>
           </div>
        ) : (
          <table className="w-full text-left">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                <th className="px-6 py-3 font-semibold">Name</th>
                <th className="px-6 py-3 font-semibold">Risk Score</th>
                <th className="px-6 py-3 font-semibold">Last Updated</th>
                <th className="px-6 py-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredLists.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      {item.type === 'high_risk_country' && <Globe size={18} className="text-slate-400" />}
                      <div>
                        <p className="font-medium text-slate-900">{item.name}</p>
                        {item.code && <p className="text-xs text-slate-400 font-mono">{item.code}</p>}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getScoreColor(item.riskScore)}`}>
                      {item.riskScore}/100
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-sm">
                    {item.updatedAt}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => handleDelete(item.id)} 
                      className="text-slate-400 hover:text-red-600 transition-colors p-2 hover:bg-slate-100 rounded-full"
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};