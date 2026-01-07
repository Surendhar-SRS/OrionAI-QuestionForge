import { useNavigate, useLocation } from 'react-router-dom';
import { 
    LayoutDashboard, 
    BookOpen, 
    Settings, 
    LogOut, 
    Sparkles, 
    BarChart3,
    Sun,
    Moon
} from 'lucide-react';
import { clsx } from 'clsx';
import { useAuthStore } from '../store/useAuthStore';
import { useThemeStore } from '../store/useThemeStore';
import { motion } from 'framer-motion';

const Sidebar = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { logout, user } = useAuthStore();
    const { theme, toggleTheme } = useThemeStore();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navItems = [
        { icon: BookOpen, label: 'Course Setup', path: '/' },
        { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
        { icon: BarChart3, label: 'Audit Analytics', path: '/audit-report' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    return (
        <aside className="w-[240px] bg-[var(--secondary)]/30 border-r border-[var(--border)] flex flex-col transition-colors duration-300">
            {/* Header / Logo */}
            <div className="h-14 flex items-center px-4 space-x-3 border-b border-[var(--border)]/50">
                <div className="w-6 h-6 bg-[var(--primary)] rounded md:rounded-lg flex items-center justify-center shadow-sm">
                    <Sparkles className="text-white w-3.5 h-3.5" />
                </div>
                <span className="font-semibold text-sm text-[var(--foreground)] tracking-tight">QuestGen Pro</span>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
                {navItems.map((item) => (
                    <button
                        key={item.path}
                        onClick={() => navigate(item.path)}
                        className={clsx(
                            "w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group relative",
                            location.pathname === item.path
                                ? "bg-[var(--background)] text-[var(--foreground)] shadow-sm border border-[var(--border)]"
                                : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/50 hover:text-[var(--foreground)]"
                        )}
                    >
                        <item.icon className={clsx(
                            "w-4 h-4",
                            location.pathname === item.path ? "text-[var(--primary)]" : "text-[var(--muted-foreground)] group-hover:text-[var(--foreground)]"
                        )} />
                        <span>{item.label}</span>
                        
                        {location.pathname === item.path && (
                            <motion.div
                                layoutId="activeNav"
                                className="absolute left-0 w-1 h-3/5 bg-[var(--primary)] rounded-r-full"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 0.2 }}
                            />
                        )}
                    </button>
                ))}
            </nav>

            {/* Bottom Actions */}
            <div className="p-3 border-t border-[var(--border)] space-y-2">
                
                {/* Theme Toggle */}
                <div className="flex items-center justify-between px-3 py-2 rounded-lg bg-[var(--background)]/50 border border-[var(--border)]/50">
                    <span className="text-xs font-medium text-[var(--muted-foreground)]">Theme</span>
                    <button
                        onClick={toggleTheme}
                        className="relative w-10 h-5 rounded-full bg-[var(--secondary)] border border-[var(--border)] transition-colors focus:outline-none"
                    >
                        <div className={clsx(
                            "absolute top-0.5 left-0.5 w-4 h-4 rounded-full transition-transform duration-200 flex items-center justify-center",
                            theme === 'dark' ? "translate-x-5 bg-slate-700" : "bg-white shadow-sm"
                        )}>
                            {theme === 'dark' ? (
                                <Moon className="w-2.5 h-2.5 text-slate-200" />
                            ) : (
                                <Sun className="w-2.5 h-2.5 text-amber-500" />
                            )}
                        </div>
                    </button>
                </div>

                {/* User Profile */}
                <div className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-[var(--background)] transition-colors cursor-pointer group">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-inner">
                        <span className="text-xs font-bold">{user?.full_name?.charAt(0) || 'U'}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-[var(--foreground)] truncate">{user?.full_name || 'User'}</p>
                        <p className="text-xs text-[var(--muted-foreground)] truncate">{user?.email || 'email@example.com'}</p>
                    </div>
                    <button 
                        onClick={handleLogout}
                        className="text-[var(--muted-foreground)] hover:text-red-500 transition-colors bg-transparent p-1.5 rounded-md hover:bg-red-50 dark:hover:bg-red-900/10"
                        title="Logout"
                    >
                        <LogOut className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
