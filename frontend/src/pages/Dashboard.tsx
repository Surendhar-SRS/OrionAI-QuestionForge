import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { 
    generateQuestion, 
    ingestDocument, 
    auditQuestion,
    refineQuestion,
    type Question,
    getCourses
} from '../lib/api';
import { 
    Loader2, 
    Sparkles, 
    CheckCircle, 
    AlertCircle,
    ArrowUpRight,
    Search,
    Filter,
    Upload,
    Zap,
    ChevronDown,
    MoreHorizontal,
    Download,
    BookOpen,
    X,
    LayoutGrid
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';

const Dashboard = () => {
    const activeCourseIdString = localStorage.getItem('activeCourseId');
    const activeCourseId = activeCourseIdString ? parseInt(activeCourseIdString) : null;
    
    const [selectedAudit, setSelectedAudit] = useState<any>(null);
    const [topic, setTopic] = useState('');
    const [bloom, setBloom] = useState('Understand');
    const [difficulty, setDifficulty] = useState('Medium');
    const [questions, setQuestions] = useState<Question[]>([]);
    const [isIngesting, setIsIngesting] = useState(false);

    const { data: courses } = useQuery({ 
        queryKey: ['courses'], 
        queryFn: getCourses,
        enabled: !!activeCourseId 
    });
    
    const currentCourse = courses?.find(c => c.id === activeCourseId);

    const generateMutation = useMutation({
        mutationFn: () => {
            if (!activeCourseId) throw new Error("No active course");
            return generateQuestion(activeCourseId, topic, bloom, difficulty);
        },
        onSuccess: (newQuestion) => {
            setQuestions([newQuestion, ...questions]);
        }
    });

    const auditMutation = useMutation({
        mutationFn: ({ id, t }: { id: number, t: string }) => auditQuestion(id, t),
        onSuccess: (result, variables) => {
            setSelectedAudit({ ...result, questionId: variables.id });
        }
    });

    const refineMutation = useMutation({
        mutationFn: () => {
            if (!selectedAudit) throw new Error("No audit selected");
            return refineQuestion(selectedAudit.questionId, selectedAudit.feedback, topic);
        },
        onSuccess: (updatedQuestion) => {
            setQuestions(questions.map(q => q.id === updatedQuestion.id ? updatedQuestion : q));
            setSelectedAudit(null);
        }
    });

    const handleAuditClick = (qId: number, t: string) => {
        auditMutation.mutate({ id: qId, t });
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0] && activeCourseId) {
            setIsIngesting(true);
            try {
                await ingestDocument(activeCourseId, e.target.files[0]);
            } finally {
                setIsIngesting(false);
            }
        }
    };

    if (!activeCourseId) {
        return (
            <div className="flex flex-col items-center justify-center h-[80vh] text-center space-y-4">
                <div className="p-4 bg-[var(--secondary)] rounded-full text-[var(--primary)]">
                    <AlertCircle className="w-10 h-10" />
                </div>
                <h2 className="text-xl font-semibold text-[var(--foreground)]">No Active Course Selected</h2>
                <p className="text-[var(--muted-foreground)] max-w-sm text-sm">Please select a course from the Portfolio page to start generating questions.</p>
                <button 
                    onClick={() => window.location.href = '/course-setup'}
                    className="mt-2 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors shadow-sm"
                >
                    Go to Portfolio
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-6 max-w-7xl mx-auto relative pb-10">
            {/* Audit Modal */}
            <AnimatePresence>
                {selectedAudit && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
                        <motion.div 
                            initial={{ scale: 0.95, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.95, opacity: 0 }}
                            className="bg-[var(--card)] w-full max-w-lg rounded-xl border border-[var(--border)] shadow-xl overflow-hidden"
                        >
                            <div className="p-5 border-b border-[var(--border)] flex justify-between items-center bg-[var(--secondary)]/30">
                                <h3 className="text-base font-semibold text-[var(--foreground)] flex items-center gap-2">
                                    <Sparkles className="w-4 h-4 text-blue-600" />
                                    AI Audit Report
                                </h3>
                                <button 
                                    onClick={() => setSelectedAudit(null)}
                                    className="p-1.5 rounded-md hover:bg-[var(--secondary)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                            
                            <div className="p-6 space-y-6">
                                <div className="flex items-center gap-4">
                                    <div className="flex flex-col items-center bg-[var(--secondary)] p-3 rounded-xl border border-[var(--border)] min-w-[80px]">
                                        <span className="text-[10px] font-bold text-[var(--muted-foreground)] uppercase">Score</span>
                                        <span className={clsx(
                                            "text-3xl font-black",
                                            selectedAudit.score >= 8 ? "text-green-500" : selectedAudit.score >= 5 ? "text-amber-500" : "text-red-500"
                                        )}>{selectedAudit.score}</span>
                                    </div>
                                    <div className="flex-1">
                                        <h4 className="font-bold text-[var(--foreground)] text-sm mb-1">Critique Summary</h4>
                                        <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                                            {selectedAudit.feedback}
                                        </p>
                                    </div>
                                </div>

                                {selectedAudit.actions && (
                                    <div className="bg-[var(--primary)]/5 rounded-xl p-4 border border-[var(--primary)]/10">
                                        <span className="text-[10px] font-bold text-[var(--primary)] uppercase tracking-wider mb-2 block">Suggested Actions</span>
                                        <ul className="list-disc list-inside text-xs text-[var(--foreground)] space-y-1 opacity-80">
                                            {Array.isArray(selectedAudit.actions) 
                                                ? selectedAudit.actions.map((action: string, i: number) => <li key={i}>{action}</li>) 
                                                : <li>{selectedAudit.actions}</li>}
                                        </ul>
                                    </div>
                                )}
                            </div>

                            <div className="p-4 bg-[var(--secondary)]/50 border-t border-[var(--border)] flex justify-end gap-3">
                                <button 
                                    onClick={() => setSelectedAudit(null)}
                                    className="px-4 py-2 rounded-xl text-sm font-bold text-[var(--muted-foreground)] hover:bg-[var(--secondary)] transition-colors"
                                >
                                    Dismiss
                                </button>
                                <button 
                                    onClick={() => refineMutation.mutate()}
                                    disabled={refineMutation.isPending}
                                    className="px-4 py-2 rounded-xl text-sm font-bold bg-[var(--primary)] text-white hover:opacity-90 transition-opacity flex items-center gap-2"
                                >
                                    {refineMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                                    Auto-Refine Question
                                </button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Context Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[var(--card)] p-4 rounded-xl border border-[var(--border)] shadow-sm">
                <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-[var(--primary)]/10 text-[var(--primary)] rounded-lg flex items-center justify-center">
                        <BookOpen className="w-5 h-5" />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-[var(--foreground)]">{currentCourse?.name}</h2>
                        <div className="flex items-center space-x-2 text-xs text-[var(--muted-foreground)]">
                            <span className="font-mono bg-[var(--secondary)] px-1.5 py-0.5 rounded">{currentCourse?.code}</span>
                            <span>•</span>
                            <span>{new Date().toLocaleDateString()}</span>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <div className="relative group">
                        <input 
                            type="file" 
                            id="doc-upload"
                            className="hidden" 
                            onChange={handleFileUpload}
                            accept=".pdf,.txt,.docx"
                            disabled={isIngesting}
                        />
                        <label 
                            htmlFor="doc-upload"
                            className={clsx(
                                "flex items-center space-x-2 px-3 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg text-sm font-medium hover:bg-[var(--secondary)] transition-colors cursor-pointer",
                                isIngesting && "opacity-50 pointer-events-none"
                            )}
                        >
                            {isIngesting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
                            <span>Ingest Material</span>
                        </label>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                {/* Generator Panel */}
                <motion.div 
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2, type: "spring", stiffness: 100, damping: 15 }}
                    className="lg:col-span-4 space-y-6 sticky top-8"
                >   
                    {/* Course Card */}
                    {currentCourse && (
                         <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-6 text-white shadow-lg relative overflow-hidden group">
                            <div className="relative z-10">
                                <div className="flex items-start justify-between">
                                    <div className="p-3 bg-white/10 backdrop-blur-sm rounded-lg mb-4 group-hover:bg-white/20 transition-colors">
                                        <BookOpen className="w-6 h-6 text-white" />
                                    </div>
                                    <span className="text-xs font-medium bg-white/20 backdrop-blur-sm px-2.5 py-1 rounded-full text-white/90">
                                        Active Course
                                    </span>
                                </div>
                                <h2 className="text-2xl font-bold mb-1 tracking-tight">{currentCourse.name}</h2>
                                <p className="text-blue-100 text-sm mb-6 max-w-[90%]">{currentCourse.code}</p>
                                
                                <div className="flex items-center justify-between pt-4 border-t border-white/10">
                                    <div className="flex -space-x-2">
                                        <div className="w-8 h-8 rounded-full bg-blue-400 border-2 border-blue-600 flex items-center justify-center text-xs font-bold">JD</div>
                                        <div className="w-8 h-8 rounded-full bg-indigo-400 border-2 border-blue-600 flex items-center justify-center text-xs font-bold">AS</div>
                                        <div className="w-8 h-8 rounded-full bg-white/10 border-2 border-blue-600 flex items-center justify-center text-xs backdrop-blur-sm">+3</div>
                                    </div>
                                    <button className="text-sm font-medium hover:text-white/80 transition-colors flex items-center">
                                        Settings <ArrowUpRight className="w-4 h-4 ml-1" />
                                    </button>
                                </div>
                            </div>
                            
                            {/* Decorative Background */}
                            <div className="absolute top-0 right-0 p-8 opacity-10 transform translate-x-10 -translate-y-10">
                                <BookOpen className="w-48 h-48" />
                            </div>
                        </div>
                    )}

                    {/* Generator Controls */}
                    <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl shadow-sm p-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                                <Zap className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-[var(--foreground)]">Generate Questions</h3>
                                <p className="text-xs text-[var(--muted-foreground)]">AI-powered generation from your docs</p>
                            </div>
                        </div>

                        <div className="space-y-5">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-[var(--foreground)]">Topic / Concept</label>
                                <div className="relative">
                                    <input 
                                        type="text" 
                                        className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 pl-3 pr-10 text-sm text-[var(--foreground)] focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all shadow-sm"
                                        placeholder="e.g. Cognitive Dissonance"
                                        value={topic}
                                        onChange={(e) => setTopic(e.target.value)}
                                    />
                                    <Search className="w-4 h-4 text-[var(--muted-foreground)] absolute right-3 top-3" />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-[var(--foreground)]">Taxonomy</label>
                                    <div className="relative">
                                        <select 
                                            className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 px-3 text-sm text-[var(--foreground)] focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 appearance-none shadow-sm transition-all cursor-pointer"
                                            value={bloom}
                                            onChange={(e) => setBloom(e.target.value)}
                                        >
                                            <option>Remember</option>
                                            <option>Understand</option>
                                            <option>Apply</option>
                                            <option>Analyze</option>
                                            <option>Evaluate</option>
                                            <option>Create</option>
                                        </select>
                                        <ChevronDown className="w-4 h-4 text-[var(--muted-foreground)] absolute right-3 top-3 pointer-events-none" />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-[var(--foreground)]">Difficulty</label>
                                    <div className="relative">
                                        <select 
                                            className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 px-3 text-sm text-[var(--foreground)] focus:ring-2 focus:ring-blue-600/20 focus:focus:border-blue-600 appearance-none shadow-sm transition-all cursor-pointer"
                                            value={difficulty}
                                            onChange={(e) => setDifficulty(e.target.value)}
                                        >
                                            <option>Easy</option>
                                            <option>Medium</option>
                                            <option>Hard</option>
                                        </select>
                                        <ChevronDown className="w-4 h-4 text-[var(--muted-foreground)] absolute right-3 top-3 pointer-events-none" />
                                    </div>
                                </div>
                            </div>

                            <motion.button 
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => generateMutation.mutate()}
                                disabled={generateMutation.isPending || !topic}
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg flex items-center justify-center space-x-2 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            > 
                                {generateMutation.isPending ? (
                                    <>
                                        <Loader2 className="w-4 h-4 animate-spin" />
                                        <span>Generating...</span>
                                    </>
                                ) : (
                                    <>
                                        <Sparkles className="w-4 h-4" />
                                        <span>Generate Question</span>
                                    </>
                                )}
                            </motion.button>
                        </div>

                        {/* File Upload Mini */}
                        <div className="mt-6 pt-6 border-t border-[var(--border)]">
                            <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-dashed border-[var(--border)] rounded-lg cursor-pointer bg-[var(--background)]/50 hover:bg-[var(--secondary)]/50 hover:border-blue-400 transition-all group">
                                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                    {isIngesting ? (
                                        <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
                                    ) : (
                                        <>
                                            <Upload className="w-6 h-6 text-[var(--muted-foreground)] group-hover:text-blue-600 mb-2 transition-colors" />
                                            <p className="text-xs text-[var(--muted-foreground)] group-hover:text-[var(--foreground)] transition-colors">
                                                <span className="font-semibold">Click to upload</span> docs
                                            </p>
                                        </>
                                    )}
                                </div>
                                <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf,.txt,.md" disabled={isIngesting} />
                            </label>
                        </div>
                    </div>
                </motion.div>

                {/* Questions Grid */}
                <div className="lg:col-span-8 space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                             <div className="flex items-center space-x-2 bg-[var(--card)] border border-[var(--border)] rounded-lg p-1">
                                <button className="p-1.5 bg-[var(--secondary)] text-[var(--foreground)] rounded-md shadow-sm transition-all">
                                    <LayoutGrid className="w-4 h-4" />
                                </button>
                                <button className="p-1.5 text-[var(--muted-foreground)] hover:text-[var(--foreground)] rounded-md transition-all hover:bg-[var(--secondary)]/50">
                                    <MoreHorizontal className="w-4 h-4" />
                                </button>
                            </div>
                            <span className="text-sm text-[var(--muted-foreground)] font-medium bg-[var(--card)] border border-[var(--border)] px-3 py-1.5 rounded-lg">
                                {questions.length} Questions Generated
                            </span>
                        </div>
                        <div className="flex items-center space-x-2">
                            <button className="flex items-center space-x-2 text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] bg-[var(--card)] border border-[var(--border)] px-3 py-1.5 rounded-lg transition-all hover:bg-[var(--secondary)]">
                                <Filter className="w-4 h-4" />
                                <span>Filter</span>
                            </button>
                            <button className="flex items-center space-x-2 text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] bg-[var(--card)] border border-[var(--border)] px-3 py-1.5 rounded-lg transition-all hover:bg-[var(--secondary)]">
                                <Download className="w-4 h-4" />
                                <span>Export</span>
                            </button>
                        </div>
                    </div>

                    <motion.div layout className="grid grid-cols-1 gap-4">
                        <AnimatePresence mode="popLayout">
                            {questions.length === 0 ? (
                                <motion.div 
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-12 text-center"
                                >
                                    <div className="w-16 h-16 bg-[var(--secondary)] rounded-full flex items-center justify-center mx-auto mb-4">
                                        <Sparkles className="w-8 h-8 text-[var(--muted-foreground)]" />
                                    </div>
                                    <h3 className="text-lg font-medium text-[var(--foreground)]">No questions generated yet</h3>
                                    <p className="text-[var(--muted-foreground)] mt-2 max-w-sm mx-auto">
                                        Use the generator panel on the right to create your first set of questions.
                                    </p>
                                </motion.div>
                            ) : (
                                questions.map((q) => (
                                    <motion.div 
                                        layout
                                        initial={{ opacity: 0, scale: 0.95 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.95 }}
                                        transition={{ type: "spring", stiffness: 350, damping: 25 }}
                                        key={q.id} 
                                        className="group bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 shadow-sm hover:shadow-md transition-all relative overflow-hidden"
                                    >
                                        <div className="flex justify-between items-start gap-4">
                                            <div className="space-y-2 flex-1">
                                                <div className="flex items-center gap-2">
                                                    <span className={clsx(
                                                        "text-xs px-2.5 py-1 rounded-full font-medium border",
                                                        q.difficulty === 'Hard' ? "bg-red-50 text-red-700 border-red-100 dark:bg-red-900/20 dark:text-red-400 dark:border-red-900/30" :
                                                        q.difficulty === 'Medium' ? "bg-yellow-50 text-yellow-700 border-yellow-100 dark:bg-yellow-900/20 dark:text-yellow-400 dark:border-yellow-900/30" :
                                                        "bg-green-50 text-green-700 border-green-100 dark:bg-green-900/20 dark:text-green-400 dark:border-green-900/30"
                                                    )}>
                                                        {q.difficulty}
                                                    </span>
                                                    <span className="text-xs px-2.5 py-1 bg-[var(--secondary)] text-[var(--foreground)] rounded-full font-medium border border-[var(--border)]">
                                                        {q.bloom_level}
                                                    </span>
                                                    {/* <span className="text-xs text-[var(--muted-foreground)]">
                                                        {new Date(q.created_at).toLocaleDateString()}
                                                    </span> - Removed created_at until available */}
                                                </div>
                                                <h4 className="font-medium text-[var(--foreground)] pr-12">{q.text}</h4>
                                                
                                                {/* Details Section */}
                                                <div className="mt-2 text-sm text-[var(--muted-foreground)] space-y-1">
                                                    <p><span className="font-medium text-[var(--foreground)]">Answer:</span> {q.answer_key}</p>
                                                </div>
                                            </div>
                                            <div className="flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                                                <motion.button 
                                                    whileHover={{ scale: 1.05 }}
                                                    whileTap={{ scale: 0.95 }}
                                                    onClick={() => handleAuditClick(q.id, topic)}
                                                    className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors border border-transparent hover:border-blue-100 dark:hover:border-blue-800"
                                                    title="Audit Question"
                                                >
                                                    <CheckCircle className="w-5 h-5" />
                                                </motion.button>
                                                <motion.button 
                                                    whileHover={{ scale: 1.05 }}
                                                    whileTap={{ scale: 0.95 }}
                                                    className="p-2 text-[var(--muted-foreground)] hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors border border-transparent hover:border-red-100 dark:hover:border-red-800"
                                                >
                                                    <AlertCircle className="w-5 h-5" />
                                                </motion.button>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </AnimatePresence>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
