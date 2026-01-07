import React, { useEffect } from 'react';
import Sidebar from './Sidebar';
import TitleBar from './TitleBar';
import { useThemeStore } from '../store/useThemeStore';

const Layout = ({ children }: { children: React.ReactNode }) => {
    const { theme } = useThemeStore();

    useEffect(() => {
        const root = window.document.documentElement;
        if (theme === 'dark') {
            root.classList.add('dark');
        } else {
            root.classList.remove('dark');
        }
    }, [theme]);

    return (
        <div className="flex flex-col h-screen bg-[var(--background)] text-[var(--foreground)] overflow-hidden font-sans transition-colors duration-300">
            <TitleBar />
            <div className="flex flex-1 overflow-hidden">
                <Sidebar />
                <main className="flex-1 overflow-y-auto relative p-6">
                    <div className="max-w-7xl mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;
