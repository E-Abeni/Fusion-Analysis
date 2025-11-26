import React, { ReactNode, useState } from 'react';
import { ShieldAlert, Database, Radio, Settings, LayoutDashboard, Activity, Globe, Eye, Server, ExternalLink, LineChart, Menu, X } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const NavItem = ({ id, label, icon: Icon, active, onClick }: any) => (
  <button
    onClick={() => onClick(id)}
    className={`w-full flex items-center space-x-3 px-4 py-3 text-sm font-medium transition-colors rounded-lg mb-1
      ${active 
        ? 'bg-blue-600 text-white shadow-md' 
        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
      }`}
  >
    <Icon size={18} />
    <span>{label}</span>
  </button>
);

export const Layout: React.FC<LayoutProps> = ({ children, activeTab, onTabChange }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleTabChange = (tab: string) => {
    onTabChange(tab);
    setIsSidebarOpen(false);
  };

  return (
    <div className="flex h-screen bg-slate-100 overflow-hidden">
      
      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-16 bg-slate-900 z-30 flex items-center justify-between px-4 border-b border-slate-800 shadow-md">
        <div className="flex items-center space-x-3">
          <div className="bg-blue-600 p-1.5 rounded-lg">
            <ShieldAlert size={20} className="text-white" />
          </div>
          <span className="text-white font-bold text-lg">Fusion Analysis</span>
        </div>
        <button 
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="text-slate-300 hover:text-white p-2 focus:outline-none"
        >
          {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/50 z-30 md:hidden backdrop-blur-sm"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 text-white flex flex-col transition-transform duration-300 ease-in-out shadow-2xl
        md:static md:translate-x-0 md:shadow-xl flex-shrink-0
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <ShieldAlert size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">Fusion Analysis <span className="text-blue-400"></span></h1>
              <p className="text-xs text-slate-500">Configuration Portal</p>
            </div>
          </div>
          {/* Close button inside sidebar for mobile */}
          <button 
            onClick={() => setIsSidebarOpen(false)}
            className="md:hidden text-slate-400 hover:text-white"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 px-4 py-6 overflow-y-auto">
          <div className="mb-2">
            <h3 className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Overview</h3>
            <NavItem id="dashboard" label="Dashboard" icon={LayoutDashboard} active={activeTab === 'dashboard'} onClick={handleTabChange} />
             <NavItem id="nodes" label="Compute Nodes" icon={Server} active={activeTab === 'nodes'} onClick={handleTabChange} />
          </div>

          <div className="mb-2">
            <h3 className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Data Sources</h3>
            <NavItem id="database" label="Central Database" icon={Database} active={activeTab === 'database'} onClick={handleTabChange} />
            <NavItem id="kafka" label="Message Broker" icon={Radio} active={activeTab === 'kafka'} onClick={handleTabChange} />
          </div>

          <div className="mb-2">
            <h3 className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Risk Engine</h3>
            <NavItem id="analysis" label="Analysis Rules" icon={Activity} active={activeTab === 'analysis'} onClick={handleTabChange} />
            <NavItem id="sanctions" label="Sanction Lists" icon={ShieldAlert} active={activeTab === 'sanctions'} onClick={handleTabChange} />
            <NavItem id="watchlists" label="Watchlists" icon={Eye} active={activeTab === 'watchlists'} onClick={handleTabChange} />
            <NavItem id="countries" label="High Risk Countries" icon={Globe} active={activeTab === 'countries'} onClick={handleTabChange} />
          </div>

          <div>
             <h3 className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">System</h3>
            <NavItem id="settings" label="General Settings" icon={Settings} active={activeTab === 'settings'} onClick={handleTabChange} />
          </div>
        </nav>

        {/* Footer: External Monitoring Link */}
        <div className="p-4 bg-slate-950 border-t border-slate-800">
          <a 
            href="http://localhost:3000" 
            className="flex items-center p-3 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800 transition-all group"
            title="Open Monitoring Portal"
          >
            <div className="bg-green-500/10 p-2 rounded-md mr-3 group-hover:bg-green-500/20 transition-colors">
              <LineChart size={20} className="text-green-500" />
            </div>
            <div className="flex-1 overflow-hidden">
              <h4 className="text-sm font-semibold text-slate-200 truncate">Live Monitor</h4>
              <p className="text-[10px] text-slate-500 truncate group-hover:text-slate-400">Monitoring Portal</p>
            </div>
            <ExternalLink size={14} className="text-slate-600 group-hover:text-slate-400 ml-2" />
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative pt-16 md:pt-0">
        <div className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};