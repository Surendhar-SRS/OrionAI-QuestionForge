import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createCourse, getCourses } from '../lib/api';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Loader2, 
    Plus, 
    Search,
    LayoutGrid,
    List as ListIcon,
    GraduationCap,
    ChevronRight,
} from 'lucide-react';
import { clsx } from 'clsx';

const CourseSetup = () => {
    const [name, setName] = useState('');
    const [code, setCode] = useState('');
    const [description, setDescription] = useState(''); // Added description state
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
    
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    const { data: courses, isLoading: isCoursesLoading } = useQuery({
        queryKey: ['courses'],
        queryFn: getCourses
    });

    const createCourseMutation = useMutation({
        mutationFn: (data: { name: string, course_code: string }) => createCourse({ name: data.name, code: data.course_code, blueprint_json: {} }),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['courses'] });
            setName('');
            setCode('');
            setDescription('');
            setIsCreateModalOpen(false);
        }
    });

    const handleCreateCourse = () => {
        createCourseMutation.mutate({ name, course_code: code });
    };

    const handleSelectCourse = (id: number) => {
        localStorage.setItem('activeCourseId', id.toString());
        navigate('/dashboard');
    };

    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-semibold text-[var(--foreground)] tracking-tight">Academic Portfolio</h1>
                    <p className="text-[var(--muted-foreground)] text-sm mt-1">Manage and configure your course question banks.</p>
                </div>
                <button 
                    onClick={() => setIsCreateModalOpen(true)}
                    className="flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium shadow-sm transition-all"
                >
                    <Plus className="w-4 h-4" />
                    <span>New Course</span>
                </button>
            </div>

            {/* Toolbar */}
            <div className="flex items-center justify-between pb-4 border-b border-[var(--border)]">
                <div className="flex items-center space-x-2 flex-1 max-w-sm bg-[var(--card)] border border-[var(--border)] rounded-lg px-3 py-2">
                    <Search className="w-4 h-4 text-[var(--muted-foreground)]" />
                    <input 
                        type="text" 
                        placeholder="Search courses..." 
                        className="bg-transparent border-none focus:ring-0 text-sm w-full text-[var(--foreground)] outline-none placeholder:text-[var(--muted-foreground)]"
                    />
                </div>
                <div className="flex items-center space-x-1 bg-[var(--card)] border border-[var(--border)] rounded-lg p-1">
                    <button 
                        onClick={() => setViewMode('grid')}
                        aria-label="Grid view"
                        title="Grid view"
                        aria-pressed={viewMode === 'grid'}
                        className={clsx("p-1.5 rounded-md transition-colors focus-visible:ring-2 focus-visible:ring-blue-500", viewMode === 'grid' ? "bg-[var(--secondary)] text-[var(--foreground)]" : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]")}
                    >
                        <LayoutGrid className="w-4 h-4" />
                    </button>
                    <button 
                        onClick={() => setViewMode('list')}
                        aria-label="List view"
                        title="List view"
                        aria-pressed={viewMode === 'list'}
                        className={clsx("p-1.5 rounded-md transition-colors focus-visible:ring-2 focus-visible:ring-blue-500", viewMode === 'list' ? "bg-[var(--secondary)] text-[var(--foreground)]" : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]")}
                    >
                        <ListIcon className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Courses View */}
            {isCoursesLoading ? (
                <div className="flex flex-col items-center justify-center py-20 space-y-4">
                    <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
                    <p className="text-[var(--muted-foreground)] text-sm font-medium">Loading courses...</p>
                </div>
            ) : (
                <motion.div 
                    layout
                    className={clsx(
                        "grid gap-4",
                        viewMode === 'grid' ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3" : "grid-cols-1"
                    )}
                >
                    <AnimatePresence>
                        {courses?.map((course: Record<string, unknown>) => (
                            <motion.div
                                layout
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                whileHover={{ y: -4, boxShadow: "0 10px 30px -10px rgba(0,0,0,0.1)" }}
                                transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                key={course.id}
                                onClick={() => handleSelectCourse(course.id)}
                                className="group bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 hover:shadow-md hover:border-blue-500/30 transition-all cursor-pointer relative overflow-hidden"
                            >
                                <div className="flex items-start justify-between mb-4">
                                    <div className="p-2.5 bg-blue-50 dark:bg-blue-900/20 rounded-lg group-hover:scale-110 transition-transform duration-300">
                                        <GraduationCap className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                                    </div>
                                    <span className="text-xs font-medium px-2.5 py-1 bg-[var(--secondary)] text-[var(--foreground)] rounded-full">
                                        Active
                                        {/* {new Date(course.created_at).toLocaleDateString()} - Removed created_at until available in API */}
                                    </span>
                                </div>
                                <h3 className="font-semibold text-lg text-[var(--foreground)] mb-2 group-hover:text-blue-600 transition-colors">{course.name}</h3>
                                <p className="text-sm text-[var(--muted-foreground)] mb-4 line-clamp-2">{course.code}</p>
                                <div className="flex items-center text-sm font-medium text-blue-600 group-hover:translate-x-1 transition-transform">
                                    View Details <ChevronRight className="w-4 h-4 ml-1" />
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </motion.div>
            )}

            {/* Create Modal */}
            <AnimatePresence>
                {isCreateModalOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsCreateModalOpen(false)}
                            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                        />
                        <motion.div 
                            initial={{ opacity: 0, scale: 0.95, y: 10 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95, y: 10 }}
                            transition={{ type: "spring", duration: 0.5, bounce: 0.3 }}
                            className="bg-[var(--card)] rounded-xl shadow-xl w-full max-w-md relative z-10 overflow-hidden"
                        >
                            <div className="p-6 border-b border-[var(--border)]">
                                <h2 className="text-lg font-semibold text-[var(--foreground)]">Create New Course</h2>
                                <p className="text-sm text-[var(--muted-foreground)]">Add a new course to your question bank.</p>
                            </div>
                            <div className="p-6 space-y-4">
                                <div className="space-y-1.5">
                                    <label className="text-sm font-medium text-[var(--foreground)]">Course Title</label>
                                    <input 
                                        type="text"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        className="w-full bg-[var(--background)] border border-[var(--border)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all"
                                        placeholder="e.g. Introduction to Psychology"
                                    />
                                </div>
                                <div className="space-y-1.5">
                                    <label className="text-sm font-medium text-[var(--foreground)]">Course Code</label>
                                    <input 
                                        type="text"
                                        value={code}
                                        onChange={(e) => setCode(e.target.value)}
                                        className="w-full bg-[var(--background)] border border-[var(--border)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all"
                                        placeholder="e.g. PSY101"
                                    />
                                </div>
                                <div className="space-y-1.5">
                                    <label className="text-sm font-medium text-[var(--foreground)]">Description</label>
                                    <textarea 
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        className="w-full bg-[var(--background)] border border-[var(--border)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all min-h-[100px] resize-none"
                                        placeholder="Brief description of the course content..."
                                    />
                                </div>
                            </div>
                            <div className="p-6 border-t border-[var(--border)] flex justify-end gap-3 bg-[var(--muted)]/30">
                                <button 
                                    onClick={() => setIsCreateModalOpen(false)}
                                    className="px-4 py-2 text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors"
                                >
                                    Cancel
                                </button>
                                <motion.button 
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    onClick={handleCreateCourse}
                                    disabled={createCourseMutation.isPending || !name || !code}
                                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center shadow-sm"
                                >
                                    {createCourseMutation.isPending ? (
                                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                                    ) : null}
                                    Create Course
                                </motion.button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default CourseSetup;
