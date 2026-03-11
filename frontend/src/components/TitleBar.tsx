import React, { useState, useEffect } from 'react';
import { Minus, X, Copy, Maximize2 } from 'lucide-react';

declare global {
    interface Window {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        require: (module: string) => any;
        electronAPI?: {
            windowMinimize: () => void;
            windowMaximize: () => void;
            windowFullscreen: () => void;
            windowClose: () => void;
        };
    }
}

const TitleBar = () => {
    const [isMaximized, setIsMaximized] = useState(false);
    const [isElectron, setIsElectron] = useState(false);

    useEffect(() => {
        // Check if running in Electron using safer detection
        const userAgent = navigator.userAgent.toLowerCase();
        if (userAgent.indexOf(' electron/') > -1 || window.electronAPI) {
            // eslint-disable-next-line react-hooks/set-state-in-effect
            setIsElectron(true);
        }
    }, []);

    const handleMinimize = () => {
        if (isElectron && window.electronAPI) {
            window.electronAPI.windowMinimize();
        }
    };

    const handleMaximize = () => {
        if (isElectron && window.electronAPI) {
            window.electronAPI.windowMaximize();
            setIsMaximized(!isMaximized);
        }
    };

    const handleFullscreen = () => {
        if (isElectron && window.electronAPI) {
            window.electronAPI.windowFullscreen();
        }
    };

    const handleClose = () => {
        if (isElectron && window.electronAPI) {
            window.electronAPI.windowClose();
        }
    };

    if (!isElectron) {
        // In browser dev mode, show a simplified header or nothing
         return (
            <div className="h-8 bg-[var(--background)] border-b border-[var(--border)] flex items-center justify-between px-4 select-none">
                <div className="text-xs font-medium text-[var(--muted-foreground)]">QuestGen Pro (Browser Mode)</div>
            </div>
        );
    }

    return (
        <div className="h-9 bg-[var(--background)] flex items-center justify-between select-none border-b border-[var(--border)]" style={{ WebkitAppRegion: 'drag' } as React.CSSProperties}>
            {/* Left Side - Logo/Title */}
            <div className="flex items-center px-4 space-x-2">
                <div className="w-4 h-4 rounded bg-blue-600 flex items-center justify-center">
                    <span className="text-[10px] font-bold text-white">Q</span>
                </div>
                <span className="text-xs font-medium text-[var(--foreground)] opacity-80">QuestGen Pro</span>
            </div>

            {/* Right Side - Window Controls */}
            <div className="flex h-full" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
                 <button 
                    onClick={handleFullscreen}
                    className="focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none focus-visible:ring-[var(--primary)]"
                    title="Fullscreen"
                >
                    <Maximize2 className="w-3.5 h-3.5" />
                </button>
                <button 
                    onClick={handleMinimize}
                    className="focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none focus-visible:ring-[var(--primary)]"
                    title="Minimize"
                >
                    <Minus className="w-4 h-4" />
                </button>
                <button 
                    onClick={handleMaximize}
                    className="focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none focus-visible:ring-[var(--primary)]"
                    title="Maximize"
                >
                    <Copy className="w-3.5 h-3.5 transform rotate-90" />
                </button>
                <button 
                    onClick={handleClose}
                    className="focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none focus-visible:ring-[var(--primary)]"
                    title="Close"
                >
                    <X className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
};

export default TitleBar;
