import { useQuery } from '@tanstack/react-query';
import { getStats, getAuditLogs } from '../lib/api';
import { 
    BarChart, 
    Bar, 
    XAxis, 
    YAxis, 
    CartesianGrid, 
    Tooltip, 
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell
} from 'recharts';
import { 
    Loader2, 
    BarChart3, 
    PieChart as PieIcon, 
    MessageSquare, 
    TrendingUp,
    AlertCircle,
    Download,
    CheckCircle
} from 'lucide-react';
import { motion } from 'framer-motion';

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6366f1'];

const AuditReport = () => {
    const activeCourseIdString = localStorage.getItem('activeCourseId');
    const activeCourseId = activeCourseIdString ? parseInt(activeCourseIdString) : null;

    const { data: stats, isLoading: isStatsLoading } = useQuery({
        queryKey: ['stats', activeCourseId],
        queryFn: () => getStats(activeCourseId!),
        enabled: !!activeCourseId
    });

    const { data: logs, isLoading: isLogsLoading } = useQuery({
        queryKey: ['audit-logs', activeCourseId],
        queryFn: () => getAuditLogs(activeCourseId!),
        enabled: !!activeCourseId
    });

    if (!activeCourseId) {
        return (
            <div className="flex flex-col items-center justify-center h-[80vh] text-center space-y-4">
                <div className="p-6 bg-[var(--secondary)] rounded-full text-[var(--primary)]">
                    <AlertCircle className="w-12 h-12" />
                </div>
                <h2 className="text-2xl font-bold text-[var(--foreground)]">No Active Course Selected</h2>
                <p className="text-[var(--muted-foreground)] max-w-sm">Please select a course to view quality analytics and audit reports.</p>
            </div>
        );
    }

    if (isStatsLoading || isLogsLoading) {
        return (
            <div className="flex flex-col items-center justify-center h-[80vh] space-y-4">
                <Loader2 className="w-12 h-12 animate-spin text-[var(--primary)]" />
                <p className="text-[var(--muted-foreground)] font-medium">Aggregating quality reports...</p>
            </div>
        );
    }

    const bloomData = Object.entries(stats?.bloom_distribution || {}).map(([name, value]) => ({ name, value }));
    const difficultyData = Object.entries(stats?.difficulty_distribution || {}).map(([name, value]) => ({ name, value }));

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-[var(--foreground)] tracking-tight">Quality Analytics</h1>
                    <p className="text-[var(--muted-foreground)] mt-1">Intelligence-driven metrics for your assessment bank.</p>
                </div>
                <button className="flex items-center justify-center space-x-2 bg-[var(--secondary)] text-[var(--foreground)] border border-[var(--border)] px-5 py-2.5 rounded-xl font-bold hover:bg-[var(--border)] transition-all">
                    <Download className="w-4 h-4" />
                    <span>Report PDF</span>
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Bloom's Distribution Chart */}
                <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-[var(--card)] border border-[var(--border)] rounded-3xl p-8 shadow-sm"
                >
                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-[var(--primary)]/10 text-[var(--primary)] rounded-xl flex items-center justify-center">
                                <BarChart3 className="w-5 h-5" />
                            </div>
                            <h2 className="text-xl font-bold text-[var(--foreground)]">Cognitive Depth</h2>
                        </div>
                        <span className="text-[var(--muted-foreground)] text-[10px] font-bold uppercase tracking-widest bg-[var(--secondary)] px-2.5 py-1 rounded-md border border-[var(--border)]">Bloom's Distribution</span>
                    </div>

                    <div className="h-[320px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={bloomData} margin={{ top: 10, right: 10, left: -20, bottom: 10 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                                <XAxis 
                                    dataKey="name" 
                                    stroke="var(--muted-foreground)" 
                                    fontSize={10} 
                                    tickLine={false} 
                                    axisLine={false}
                                    fontWeight="bold"
                                />
                                <YAxis 
                                    stroke="var(--muted-foreground)" 
                                    fontSize={10} 
                                    tickLine={false} 
                                    axisLine={false}
                                    fontWeight="bold"
                                />
                                <Tooltip 
                                    contentStyle={{ 
                                        backgroundColor: 'var(--card)', 
                                        border: '1px solid var(--border)', 
                                        borderRadius: '12px',
                                        color: 'var(--foreground)',
                                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                                    }}
                                    itemStyle={{ color: 'var(--primary)', fontWeight: 'bold' }}
                                />
                                <Bar dataKey="value" fill="var(--primary)" radius={[6, 6, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Difficulty Distribution Pie */}
                <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-[var(--card)] border border-[var(--border)] rounded-3xl p-8 shadow-sm"
                >
                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-[var(--primary)]/10 text-[var(--primary)] rounded-xl flex items-center justify-center">
                                <PieIcon className="w-5 h-5" />
                            </div>
                            <h2 className="text-xl font-bold text-[var(--foreground)]">Pedagogical Balance</h2>
                        </div>
                        <span className="text-[var(--muted-foreground)] text-[10px] font-bold uppercase tracking-widest bg-[var(--secondary)] px-2.5 py-1 rounded-md border border-[var(--border)]">Complexity</span>
                    </div>

                    <div className="h-[320px] w-full flex items-center justify-center">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={difficultyData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={70}
                                    outerRadius={110}
                                    paddingAngle={8}
                                    dataKey="value"
                                    stroke="var(--card)"
                                    strokeWidth={4}
                                >
                                    {difficultyData.map((_, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip 
                                    contentStyle={{ 
                                        backgroundColor: 'var(--card)', 
                                        border: '1px solid var(--border)', 
                                        borderRadius: '12px',
                                        color: 'var(--foreground)'
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            </div>

            {/* AI Critique Logs */}
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-[var(--card)] border border-[var(--border)] rounded-3xl p-8 shadow-sm"
            >
                <div className="flex items-center justify-between mb-10 border-b border-[var(--border)] pb-6">
                    <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-[var(--primary)]/10 text-[var(--primary)] rounded-2xl flex items-center justify-center shadow-inner">
                            <MessageSquare className="w-6 h-6" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-[var(--foreground)]">Critique Intelligence</h2>
                            <p className="text-[var(--muted-foreground)] text-sm">Synthetic audit history and refinement iterations.</p>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-4">
                    {logs?.length === 0 ? (
                        <div className="text-center py-20 bg-[var(--secondary)] rounded-3xl border-2 border-dashed border-[var(--border)]">
                            <TrendingUp className="w-16 h-16 text-[var(--muted-foreground)] mx-auto mb-4 opacity-20" />
                            <h3 className="text-lg font-bold text-[var(--foreground)]">No Audit Data Found</h3>
                            <p className="text-[var(--muted-foreground)] max-w-xs mx-auto mt-2 text-sm">Initiate an AI audit on individual questions to populate this stream.</p>
                        </div>
                    ) : (
                        logs?.map((log: any) => (
                            <div key={log.id} className="border border-[var(--border)] rounded-2xl p-6 hover:bg-[var(--secondary)]/50 transition-all flex flex-col md:flex-row gap-6">
                                <div className="md:w-32 flex flex-col justify-center items-center p-4 bg-[var(--secondary)] rounded-xl border border-[var(--border)]">
                                    <span className="text-[10px] font-bold text-[var(--muted-foreground)] uppercase tracking-tighter mb-1">Score</span>
                                    <span className="text-2xl font-extrabold text-[var(--primary)] leading-none">{log.metrics_snapshot?.score || '--'}</span>
                                    <span className="text-[8px] font-black text-[var(--muted-foreground)] uppercase mt-2 opacity-40">AI-Rank</span>
                                </div>
                                <div className="flex-1 space-y-4">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-2">
                                            <span className="text-[10px] font-black bg-[var(--primary)] text-white px-2 py-0.5 rounded uppercase tracking-wider">Iter-{log.iteration_id}</span>
                                            <span className="text-[10px] font-bold text-[var(--muted-foreground)] uppercase tracking-widest">Question Ref: #{log.question_id}</span>
                                        </div>
                                    </div>
                                    <div className="bg-[var(--card)] p-5 rounded-xl border border-[var(--border)] shadow-inner">
                                        <p className="text-[var(--foreground)] text-sm font-medium leading-relaxed opacity-90">{log.ai_critique}</p>
                                    </div>
                                    <div className="flex items-center gap-4 text-[10px] font-bold text-[var(--muted-foreground)] uppercase tracking-wide">
                                        <span className="flex items-center gap-1.5"><TrendingUp className="w-3.5 h-3.5" /> Refined logic</span>
                                        <span className="flex items-center gap-1.5"><CheckCircle className="w-3.5 h-3.5" /> Validated</span>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default AuditReport;
