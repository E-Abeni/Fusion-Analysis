import React, { useEffect, useState, useCallback } from 'react';
import { Dashboard } from './components/Dashboard';
import { LiveMonitor } from './components/LiveMonitor';
import { STRManager } from './components/STRManager';
import { CustomerRiskMonitor } from './components/CustomerRiskMonitor';
import { EngineStats, Transaction, Customer, STR, RiskLevel } from './types';
import { generateTransaction, generateCustomer, generateSTR } from './services/mockDataService';
import { LayoutDashboard, Activity, AlertTriangle, ShieldCheck, Menu, Users, Settings, Moon, Sun, ExternalLink } from 'lucide-react';

enum View {
  DASHBOARD = 'DASHBOARD',
  MONITOR = 'MONITOR',
  CUSTOMERS = 'CUSTOMERS',
  ALERTS = 'ALERTS'
}

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<View>(View.DASHBOARD);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  
  // State
  const [stats, setStats] = useState<EngineStats>({
    transactionsProcessed: 1245890,
    messagesInQueue: 42,
    processingSpeed: 850,
    flaggedCount: 142,
    cpuUsage: 42,
    ramUsage: 65
  });
  
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [strs, setStrs] = useState<STR[]>([]);
  const [volumeHistory, setVolumeHistory] = useState<{ time: string; count: number; riskScoreAvg: number }[]>([]);

  // Navigation state for deep linking
  const [targetCustomerId, setTargetCustomerId] = useState<string | null>(null);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  useState(() => {
    toggleTheme();
  } , [])

  const handleGenerateSTR = (tx: Transaction) => {
    // Check if duplicate
    const exists = strs.find(s => s.transactionId === tx.id);
    if (exists) {
      alert(`STR already exists for Transaction ${tx.id}`);
      return;
    }
    const customer = customers.find(c => c.id === tx.customerId);
    if (!customer) return;

    const newSTR = generateSTR(tx, customer);
    newSTR.reason = "Manual Trigger by Analyst";
    setStrs(prev => [newSTR, ...prev]);
    alert(`STR Generated successfully: ${newSTR.id}`);
  };

  const handleViewCustomerTimeline = (customerId: string) => {
    setTargetCustomerId(customerId);
    setCurrentView(View.CUSTOMERS);
  };

  // Simulate Real-time Data Feed
  useEffect(() => {
    // Initial Population
    const initialCustomers = Array.from({ length: 25 }, generateCustomer);
    setCustomers(initialCustomers);

    const interval = setInterval(() => {
      // 1. Pick a random customer
      const customerIndex = Math.floor(Math.random() * initialCustomers.length);
      const customer = initialCustomers[customerIndex];
      
      // 2. Generate Transaction
      const newTx = generateTransaction(customer);
      
      // 3. Update Transactions State (Keep last 100 for performance in UI)
      setTransactions(prev => [newTx, ...prev].slice(0, 100));
      
      // 4. Update Stats
      setStats(prev => ({
        ...prev,
        transactionsProcessed: prev.transactionsProcessed + 1,
        messagesInQueue: Math.floor(Math.random() * 50),
        processingSpeed: 800 + Math.floor(Math.random() * 100),
        flaggedCount: prev.flaggedCount + (newTx.riskLevel === RiskLevel.HIGH ? 1 : 0),
        cpuUsage: Math.floor(Math.random() * 40) + 20, // 20-60%
        ramUsage: Math.floor(Math.random() * 20) + 50  // 50-70%
      }));

      // 5. Check for STR Generation
      if (newTx.riskLevel === RiskLevel.CRITICAL || (newTx.riskLevel === RiskLevel.HIGH && Math.random() > 0.5)) {
        const newSTR = generateSTR(newTx, customer);
        setStrs(prev => [newSTR, ...prev]);
      }

      // 6. Update Volume History (simulated 5-sec aggregation)
      setVolumeHistory(prev => {
        const now = new Date();
        const timeStr = `${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
        const newPoint = {
          time: timeStr,
          count: Math.floor(Math.random() * 50) + 100, // Simulated volume
          riskScoreAvg: Math.floor(Math.random() * 30) + 20 // Simulated risk baseline
        };
        return [...prev, newPoint].slice(-20); // Keep last 20 points
      });

      // 7. Simulate Live Customer Risk Updates (Drift)
      setCustomers(prev => {
        return prev.map((c, idx) => {
          if (idx === customerIndex || Math.random() > 0.9) {
             // Drastic change for demo purposes if triggered
             const newScore = Math.min(100, Math.max(0, c.riskScore + (Math.random() > 0.5 ? 2 : -2)));
             let level = RiskLevel.LOW;
             if (newScore > 50) level = RiskLevel.MEDIUM;
             if (newScore > 80) level = RiskLevel.HIGH;
             if (newScore > 95) level = RiskLevel.CRITICAL;
             
             return { ...c, riskScore: Math.floor(newScore), riskLevel: level };
          }
          return c;
        });
      });

    }, 2000); // New data every 2 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-slate-300 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-300">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 flex flex-col hidden md:flex">
        <div className="p-6 flex items-center gap-3 border-b border-slate-200 dark:border-slate-800">
          <ShieldCheck className="w-8 h-8 text-blue-500" />
          <span className="text-xl font-bold tracking-tight">CTMS Fusion Analysis</span>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setCurrentView(View.DASHBOARD)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${currentView === View.DASHBOARD ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:text-slate-800 dark:hover:text-slate-200'}`}
          >
            <LayoutDashboard className="w-5 h-5" />
            Dashboard
          </button>
          
          <button 
            onClick={() => setCurrentView(View.MONITOR)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${currentView === View.MONITOR ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:text-slate-800 dark:hover:text-slate-200'}`}
          >
            <Activity className="w-5 h-5" />
            Live Monitor
          </button>

          <button 
            onClick={() => setCurrentView(View.CUSTOMERS)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${currentView === View.CUSTOMERS ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:text-slate-800 dark:hover:text-slate-200'}`}
          >
            <Users className="w-5 h-5" />
            Customer Risk
          </button>
          
          <button 
            onClick={() => setCurrentView(View.ALERTS)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${currentView === View.ALERTS ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:text-slate-800 dark:hover:text-slate-200'}`}
          >
            <AlertTriangle className="w-5 h-5" />
            <span className="flex-1 text-left">STR Alerts</span>
            {strs.filter(s => s.status === 'PENDING').length > 0 && (
              <span className="bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                {strs.filter(s => s.status === 'PENDING').length}
              </span>
            )}
          </button>
        </nav>

        <div className="p-4 border-t border-slate-200 dark:border-slate-800">
           {/* Theme Toggle */}
           <div className="flex justify-between items-center mb-4 px-2">
             <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Theme</span>
             <button 
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-slate-300 dark:bg-slate-900 text-slate-800 dark:text-slate-400 hover:text-blue-500 transition-colors"
             >
               {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
             </button>
           </div>
          <div className="text-xs text-slate-500 mb-1">System Status</div>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-sm font-medium text-green-600 dark:text-green-400">Engine Online</span>
          </div>
          
          <a 
            href="http://localhost:3001"
            target=""
            rel="noopener noreferrer"
             className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded border border-slate-200 dark:border-slate-700 text-sm transition-all text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <Settings className="w-3 h-3" />
            Configuration Portal
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Mobile Header */}
        <header className="md:hidden h-16 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-4 bg-white dark:bg-slate-950">
          <div className="flex items-center gap-2">
             <ShieldCheck className="w-6 h-6 text-blue-500" />
             <span className="font-bold text-slate-900 dark:text-slate-100">CTMS Fusion</span>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={toggleTheme} className="p-2 text-slate-500">
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <button className="text-slate-500"><Menu /></button>
          </div>
        </header>

        {/* View Area */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">
            <header className="mb-6 flex justify-between items-end">
              <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                  {currentView === View.DASHBOARD && 'Operational Overview'}
                  {currentView === View.MONITOR && 'Real-time Transaction Analysis'}
                  {currentView === View.CUSTOMERS && 'Customer Risk Profiling'}
                  {currentView === View.ALERTS && 'Suspicious Activity Reports'}
                </h1>
                <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
                  {currentView === View.DASHBOARD && 'Central Database & Message Broker Metrics'}
                  {currentView === View.MONITOR && 'Live stream of processed transactions and risk scoring'}
                  {currentView === View.CUSTOMERS && 'Behavioral analysis, peer grouping, and KYC integrity checks'}
                  {currentView === View.ALERTS && 'Review and file generated STRs'}
                </p>
              </div>
            </header>

            {currentView === View.DASHBOARD && (
              <Dashboard 
                stats={stats} 
                volumeHistory={volumeHistory} 
                transactions={transactions} 
              />
            )}
            
            {currentView === View.MONITOR && (
              <div className="h-[calc(100vh-200px)]">
                <LiveMonitor 
                  transactions={transactions} 
                  onGenerateSTR={handleGenerateSTR}
                  onViewTimeline={handleViewCustomerTimeline}
                />
              </div>
            )}

            {currentView === View.CUSTOMERS && (
              <CustomerRiskMonitor 
                customers={customers} 
                targetCustomerId={targetCustomerId}
              />
            )}
            
            {currentView === View.ALERTS && (
              <STRManager 
                strs={strs} 
                transactions={transactions} 
                customers={customers} 
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;