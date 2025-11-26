import React, { useState } from 'react';
import { AnalysisRule, AnalysisCategory } from '../types';
import { Zap, AlertOctagon } from 'lucide-react';

interface AnalysisConfigProps {
  rules: AnalysisRule[];
  onUpdate: (rules: AnalysisRule[]) => void;
}

export const AnalysisConfig: React.FC<AnalysisConfigProps> = ({ rules, onUpdate }) => {
  const [filter, setFilter] = useState<AnalysisCategory | 'ALL'>('ALL');

  const handleToggle = (id: string) => {
    onUpdate(rules.map(r => r.id === id ? { ...r, enabled: !r.enabled } : r));
  };

  const handleParamChange = (id: string, key: string, value: string | number) => {
    onUpdate(rules.map(r => {
      if (r.id === id) {
        return { ...r, parameters: { ...r.parameters, [key]: value } };
      }
      return r;
    }));
  };

  const filteredRules = filter === 'ALL' ? rules : rules.filter(r => r.category === filter);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Analysis Engine Configuration</h2>
          <p className="text-slate-500 mt-1">Fine-tune detection algorithms, thresholds, and risk models.</p>
        </div>
        <div className="flex bg-white p-1 rounded-lg border border-slate-200 shadow-sm">
          {(['ALL', AnalysisCategory.CUSTOMER, AnalysisCategory.TRANSACTION] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-all ${
                filter === cat 
                  ? 'bg-slate-900 text-white shadow' 
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              {cat === 'ALL' ? 'All Rules' : cat === 'CUSTOMER' ? 'Customer Risk' : 'Transaction Risk'}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {filteredRules.map((rule) => (
          <div key={rule.id} className={`bg-white rounded-xl border transition-all ${rule.enabled ? 'border-slate-200 shadow-sm' : 'border-slate-100 opacity-75'}`}>
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${rule.enabled ? 'bg-blue-100 text-blue-600' : 'bg-slate-100 text-slate-400'}`}>
                    {rule.category === AnalysisCategory.CUSTOMER ? <Zap size={20} /> : <AlertOctagon size={20} />}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800">{rule.name}</h3>
                    <p className="text-sm text-slate-500">{rule.description}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" checked={rule.enabled} onChange={() => handleToggle(rule.id)} />
                    <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>

              {rule.enabled && (
                <div className="mt-4 pt-4 border-t border-slate-100 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(rule.parameters).map(([key, val]) => (
                    <div key={key}>
                      <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </label>
                      <div className="relative">
                        <input
                          type={typeof val === 'number' ? 'number' : 'text'}
                          value={val.toString()}
                          onChange={(e) => handleParamChange(rule.id, key, typeof val === 'number' ? parseFloat(e.target.value) : e.target.value)}
                          className="block w-full px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 font-medium focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none shadow-sm transition-all"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};