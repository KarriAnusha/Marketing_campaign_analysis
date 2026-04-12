import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";
import {
  Users,
  TrendingUp,
  Target,
  DollarSign,
  Filter,
  Download,
  LayoutDashboard,
  PieChart as PieChartIcon,
  BarChart3,
  Table as TableIcon,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/src/lib/utils";

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];

interface Stats {
  totalCustomers: number;
  avgSpend: number;
  responseRate: number;
  avgIncome: number;
}

interface SegmentData {
  Segment: string;
  count: number;
  avgSpend: number;
  responseRate: number;
}

export default function App() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [segments, setSegments] = useState<SegmentData[]>([]);
  const [spending, setSpending] = useState<any>(null);
  const [campaigns, setCampaigns] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "segments" | "campaigns">("overview");

  useEffect(() => {
    fetch("/api/stats").then(res => res.json()).then(setStats);
    fetch("/api/segments").then(res => res.json()).then(setSegments);
    fetch("/api/spending-by-category").then(res => res.json()).then(setSpending);
    fetch("/api/response-by-campaign").then(res => res.json()).then(setCampaigns);
  }, []);

  const spendingData = spending ? Object.entries(spending).map(([name, value]) => ({ name, value })) : [];
  const campaignData = campaigns ? Object.entries(campaigns).map(([name, value]) => ({ name, value })) : [];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6 border-b border-slate-100">
          <div className="flex items-center gap-2 text-blue-600 mb-1">
            <TrendingUp size={24} />
            <span className="font-bold text-xl tracking-tight">Marketlytics</span>
          </div>
          <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Campaign Analysis</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setActiveTab("overview")}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
              activeTab === "overview" ? "bg-blue-50 text-blue-600 shadow-sm" : "text-slate-600 hover:bg-slate-50"
            )}
          >
            <LayoutDashboard size={18} />
            Overview
          </button>
          <button 
            onClick={() => setActiveTab("segments")}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
              activeTab === "segments" ? "bg-blue-50 text-blue-600 shadow-sm" : "text-slate-600 hover:bg-slate-50"
            )}
          >
            <PieChartIcon size={18} />
            Segmentation
          </button>
          <button 
            onClick={() => setActiveTab("campaigns")}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
              activeTab === "campaigns" ? "bg-blue-50 text-blue-600 shadow-sm" : "text-slate-600 hover:bg-slate-50"
            )}
          >
            <Target size={18} />
            Campaigns
          </button>
        </nav>

        <div className="p-4 border-t border-slate-100">
          <div className="bg-slate-900 rounded-2xl p-4 text-white">
            <p className="text-xs text-slate-400 mb-1">Current Campaign</p>
            <p className="text-sm font-semibold mb-3">Spring Sale 2024</p>
            <div className="w-full bg-slate-700 h-1.5 rounded-full overflow-hidden">
              <div className="bg-blue-500 h-full w-3/4" />
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between sticky top-0 z-10">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {activeTab === "overview" && "Executive Overview"}
              {activeTab === "segments" && "Customer Segmentation"}
              {activeTab === "campaigns" && "Campaign Performance"}
            </h1>
            <p className="text-sm text-slate-500">Real-time marketing insights & analytics</p>
          </div>
          
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors">
              <Filter size={16} />
              Filters
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 rounded-lg text-sm font-medium text-white hover:bg-blue-700 transition-colors shadow-sm shadow-blue-200">
              <Download size={16} />
              Export Report
            </button>
          </div>
        </header>

        <div className="p-8 space-y-8">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard 
              title="Total Customers" 
              value={stats?.totalCustomers.toLocaleString() ?? "..."} 
              icon={<Users className="text-blue-600" />} 
              trend="+12% from last month"
            />
            <StatCard 
              title="Avg. Total Spend" 
              value={stats ? `₹${Math.round(stats.avgSpend).toLocaleString()}` : "..."} 
              icon={<DollarSign className="text-emerald-600" />} 
              trend="+5.4% vs target"
            />
            <StatCard 
              title="Response Rate" 
              value={stats ? `${stats.responseRate.toFixed(1)}%` : "..."} 
              icon={<Target className="text-amber-600" />} 
              trend="-2.1% vs last campaign"
            />
            <StatCard 
              title="Avg. HH Income" 
              value={stats ? `₹${Math.round(stats.avgIncome).toLocaleString()}` : "..."} 
              icon={<TrendingUp className="text-purple-600" />} 
              trend="Stable"
            />
          </div>

          {activeTab === "overview" && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <ChartCard title="Spending by Category">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={spendingData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
                    <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
                    <Tooltip 
                      contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                    />
                    <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard title="Campaign Acceptance">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={campaignData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {campaignData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend verticalAlign="bottom" height={36}/>
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>
          )}

          {activeTab === "segments" && (
            <div className="space-y-8">
              <ChartCard title="Customer Segments Distribution">
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={segments} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                    <XAxis type="number" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
                    <YAxis dataKey="Segment" type="category" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} width={150} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>

              <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                  <h3 className="font-bold text-slate-900">Segment Performance Matrix</h3>
                  <button className="text-blue-600 text-sm font-medium hover:underline">View All Details</button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-semibold">
                        <th className="px-6 py-4">Segment</th>
                        <th className="px-6 py-4">Customer Count</th>
                        <th className="px-6 py-4">Avg. Spend</th>
                        <th className="px-6 py-4">Response Rate</th>
                        <th className="px-6 py-4">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {segments.map((seg, i) => (
                        <tr key={i} className="hover:bg-slate-50 transition-colors">
                          <td className="px-6 py-4 font-medium text-slate-900">{seg.Segment}</td>
                          <td className="px-6 py-4 text-slate-600">{seg.count}</td>
                          <td className="px-6 py-4 text-slate-600">₹{Math.round(seg.avgSpend).toLocaleString()}</td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                <div className="bg-blue-500 h-full" style={{width: `${seg.responseRate}%`}} />
                              </div>
                              <span className="text-xs font-medium text-slate-600">{seg.responseRate.toFixed(1)}%</span>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <span className={cn(
                              "px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-tight",
                              seg.responseRate > 15 ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"
                            )}>
                              {seg.responseRate > 15 ? "High Value" : "Target"}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === "campaigns" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <ChartCard title="Historical Campaign Response Trend">
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={campaignData}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                      <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
                      <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
                      <Tooltip />
                      <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} dot={{r: 6, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff'}} activeDot={{r: 8}} />
                    </LineChart>
                  </ResponsiveContainer>
                </ChartCard>
              </div>
              
              <div className="space-y-6">
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                  <h3 className="font-bold text-slate-900 mb-4">Actionable Insights</h3>
                  <ul className="space-y-4">
                    <InsightItem 
                      text="High Income segment shows 2.5x higher response rate than average." 
                      type="positive" 
                    />
                    <InsightItem 
                      text="Wine and Meat products account for 70% of total revenue." 
                      type="neutral" 
                    />
                    <InsightItem 
                      text="Web visits are high but conversion rate in 'Family' segment is lagging." 
                      type="negative" 
                    />
                    <InsightItem 
                      text="Campaign 2 had the lowest engagement; consider revising strategy." 
                      type="negative" 
                    />
                  </ul>
                </div>

                <div className="bg-blue-600 p-6 rounded-2xl text-white shadow-lg shadow-blue-200">
                  <h3 className="font-bold mb-2">Next Campaign Recommendation</h3>
                  <p className="text-sm text-blue-100 mb-4">Focus on 'Young Customers' with mobile-first deals on 'Gold' and 'Sweets' categories.</p>
                  <button className="w-full py-2 bg-white text-blue-600 rounded-lg text-sm font-bold hover:bg-blue-50 transition-colors">
                    Generate Strategy
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function StatCard({ title, value, icon, trend }: { title: string; value: string; icon: React.ReactNode; trend: string }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="p-2 bg-slate-50 rounded-lg">{icon}</div>
        <span className={cn(
          "text-[10px] font-bold px-2 py-1 rounded-full",
          trend.includes('+') ? "bg-emerald-100 text-emerald-700" : trend.includes('-') ? "bg-rose-100 text-rose-700" : "bg-slate-100 text-slate-600"
        )}>
          {trend}
        </span>
      </div>
      <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
      <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
    </div>
  );
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="font-bold text-slate-900 mb-6">{title}</h3>
      {children}
    </div>
  );
}

function InsightItem({ text, type }: { text: string; type: "positive" | "negative" | "neutral" }) {
  return (
    <li className="flex gap-3">
      <div className={cn(
        "mt-1.5 w-1.5 h-1.5 rounded-full shrink-0",
        type === "positive" ? "bg-emerald-500" : type === "negative" ? "bg-rose-500" : "bg-blue-500"
      )} />
      <p className="text-sm text-slate-600 leading-relaxed">{text}</p>
    </li>
  );
}
