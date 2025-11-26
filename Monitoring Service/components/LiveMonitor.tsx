import React, { useState } from 'react';
import { Transaction, RiskLevel, TransactionType } from '../types';
import { RiskBadge } from './ui/RiskBadge';
import { Filter, Search, FileWarning, LineChart, Network } from 'lucide-react';

interface LiveMonitorProps {
  transactions: Transaction[];
  onGenerateSTR: (tx: Transaction) => void;
  onViewTimeline: (customerId: string) => void;
}

export const LiveMonitor: React.FC<LiveMonitorProps> = ({ transactions, onGenerateSTR, onViewTimeline }) => {
  const [filterText, setFilterText] = useState('');
  const [riskFilter, setRiskFilter] = useState<RiskLevel | 'ALL'>('ALL');

  const filtered = transactions.filter(tx => {
    const matchesText = tx.id.toLowerCase().includes(filterText.toLowerCase()) || 
                        tx.customerId.toLowerCase().includes(filterText.toLowerCase());
    const matchesRisk = riskFilter === 'ALL' || tx.riskLevel === riskFilter;
    return matchesText && matchesRisk;
  });

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg flex flex-col h-full shadow-sm">
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4">
        <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900 dark:text-slate-100">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-ping"></div>
          Live Transaction Feed
        </h2>
        
        <div className="flex gap-2 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-2 top-2.5 w-4 h-4 text-slate-500" />
            <input 
              type="text" 
              placeholder="Search TX ID or Customer..." 
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded pl-8 pr-2 py-1.5 text-sm focus:outline-none focus:border-blue-500 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500"
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
            />
          </div>
          <div className="relative">
             <Filter className="absolute left-2 top-2.5 w-4 h-4 text-slate-500" />
            <select 
              className="bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded pl-8 pr-4 py-1.5 text-sm focus:outline-none focus:border-blue-500 appearance-none text-slate-900 dark:text-slate-100"
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value as any)}
            >
              <option value="ALL">All Risks</option>
              <option value={RiskLevel.CRITICAL}>Critical</option>
              <option value={RiskLevel.HIGH}>High</option>
              <option value={RiskLevel.MEDIUM}>Medium</option>
              <option value={RiskLevel.LOW}>Low</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-auto flex-1">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-950 text-slate-500 dark:text-slate-400 sticky top-0 z-10 shadow-sm">
            <tr>
              <th className="p-3 font-medium">Timestamp</th>
              <th className="p-3 font-medium">Tx ID</th>
              <th className="p-3 font-medium">Account</th>
              <th className="p-3 font-medium">Type</th>
              <th className="p-3 font-medium text-right">Amount</th>
              <th className="p-3 font-medium">Flags</th>
              <th className="p-3 font-medium">Risk Score</th>
              <th className="p-3 font-medium text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {filtered.map((tx) => (
              <tr key={tx.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group">
                <td className="p-3 text-slate-600 dark:text-slate-500 whitespace-nowrap">
                  {tx.timestamp.toLocaleTimeString()}
                </td>
                <td className="p-3 font-mono text-xs text-blue-600 dark:text-blue-400">{tx.id}</td>
                <td className="p-3 text-slate-800 dark:text-slate-200">{tx.customerId}</td>
                <td className="p-3">
                  <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold
                    ${tx.type === TransactionType.WIRE ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400' : 
                      tx.type === TransactionType.MOBILE_BANKING ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400' :
                      'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-300'}`}>
                    {tx.type}
                  </span>
                </td>
                <td className="p-3 text-right font-mono text-slate-900 dark:text-slate-200">
                  {tx.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })} {tx.currency}
                </td>
                <td className="p-3">
                   <div className="flex flex-wrap gap-1">
                     {tx.flags.slice(0, 2).map((f, i) => (
                       <span key={i} className="text-[10px] border border-slate-300 dark:border-slate-700 px-1 rounded text-slate-500 dark:text-slate-400">{f}</span>
                     ))}
                     {tx.flags.length > 2 && <span className="text-[10px] text-slate-500">+{tx.flags.length - 2}</span>}
                   </div>
                </td>
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs w-6 text-right text-slate-600 dark:text-slate-400">{tx.riskScore}</span>
                    <RiskBadge level={tx.riskLevel} />
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex justify-center gap-2 opacity-80 group-hover:opacity-100 transition-opacity">
                    <button 
                      onClick={() => onGenerateSTR(tx)}
                      title="Generate STR"
                      className="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                    >
                      <FileWarning className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => onViewTimeline(tx.customerId)}
                      title="Timeline Analysis"
                      className="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
                    >
                      <LineChart className="w-4 h-4" />
                    </button>
                    <button 
                      title="Link Analysis (Graph)"
                      className="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 hover:text-green-500 dark:hover:text-green-400 transition-colors"
                    >
                      <Network className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={8} className="p-8 text-center text-slate-500">
                  No transactions matching filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};