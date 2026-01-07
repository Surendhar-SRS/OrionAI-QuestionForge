import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, Sparkles, ShieldCheck } from 'lucide-react';
import { login, register } from '../lib/api';
import { useAuthStore } from '../store/useAuthStore';

const AuthPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    
    const navigate = useNavigate();
    const setAuth = useAuthStore((state) => state.setAuth);

    const loginMutation = useMutation({
        mutationFn: () => login(email, password),
        onSuccess: (data) => {
            setAuth({ id: 0, email, full_name: 'User' }, data.access_token);
            navigate('/');
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Authentication failed. Please check your credentials.');
        }
    });

    const registerMutation = useMutation({
        mutationFn: () => register(email, password, fullName),
        onSuccess: () => {
            setIsLogin(true);
            setError('');
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        if (isLogin) {
            loginMutation.mutate();
        } else {
            registerMutation.mutate();
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[var(--background)] p-6">
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, ease: "easeOut" }}
                className="w-full max-w-sm relative z-10"
            >
                <div className="bg-[var(--card)] border border-[var(--border)] rounded-xl p-8 shadow-sm transition-all duration-300 hover:shadow-md">
                    <motion.div 
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.1, type: "spring", stiffness: 200, damping: 15 }}
                        className="flex flex-col items-center mb-8 text-center"
                    >
                        <div className="w-12 h-12 bg-blue-600 text-white rounded-lg flex items-center justify-center mb-4 shadow-blue-200 dark:shadow-blue-900/20 shadow-lg">
                            <Sparkles className="w-6 h-6" />
                        </div>
                        <h1 className="text-2xl font-semibold text-[var(--foreground)] tracking-tight">
                            {isLogin ? 'Welcome Back' : 'Create Account'}
                        </h1>
                        <p className="text-[var(--muted-foreground)] mt-2 text-sm">
                            {isLogin ? 'Sign in to your account.' : 'Get started for free.'}
                        </p>
                    </motion.div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <AnimatePresence mode="wait">
                            {!isLogin && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    exit={{ opacity: 0, height: 0 }}
                                    transition={{ duration: 0.2 }}
                                    className="overflow-hidden"
                                >
                                    <div className="space-y-1.5 pb-4">
                                        <label className="text-sm font-medium text-[var(--foreground)]">Full Name</label>
                                        <div className="relative">
                                            <input 
                                                type="text" 
                                                value={fullName}
                                                onChange={(e) => setFullName(e.target.value)}
                                                required={!isLogin}
                                                className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 px-3 text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all placeholder:text-[var(--muted-foreground)]"
                                                placeholder="John Doe"
                                            />
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <div className="space-y-1.5">
                            <label className="text-sm font-medium text-[var(--foreground)]">Email</label>
                            <div className="relative">
                                <input 
                                    type="email" 
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 px-3 text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all placeholder:text-[var(--muted-foreground)]"
                                    placeholder="name@example.com"
                                />
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <div className="flex items-center justify-between">
                                <label className="text-sm font-medium text-[var(--foreground)]">Password</label>
                                {isLogin && (
                                    <button type="button" className="text-xs text-blue-600 hover:text-blue-700 font-medium hover:underline transition-all">Forgot password?</button>
                                )}
                            </div>
                            <div className="relative">
                                <input 
                                    type="password" 
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="w-full bg-[var(--background)] border border-[var(--input)] rounded-lg py-2.5 px-3 text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all placeholder:text-[var(--muted-foreground)]"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        {error && (
                            <motion.div 
                                initial={{ opacity: 0, y: -5 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="text-red-600 text-xs bg-red-50 p-3 rounded-lg flex items-start gap-2 border border-red-100"
                            >
                                <ShieldCheck className="w-4 h-4 shrink-0 mt-0.5" />
                                <span>{error}</span>
                            </motion.div>
                        )}

                        <motion.button 
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            type="submit"
                            disabled={loginMutation.isPending || registerMutation.isPending}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-all flex items-center justify-center text-sm shadow-sm hover:shadow-md"
                        >
                            {(loginMutation.isPending || registerMutation.isPending) ? (
                                <Loader2 className="animate-spin w-4 h-4" />
                            ) : (
                                <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
                            )}
                        </motion.button>
                    </form>

                    <div className="mt-8 text-center">
                        <p className="text-xs text-[var(--muted-foreground)]">
                            {isLogin ? "New here?" : "Already have an account?"}
                            <button 
                                onClick={() => setIsLogin(!isLogin)}
                                className="ml-1 text-blue-600 hover:text-blue-700 font-medium transition-all hover:underline"
                            >
                                {isLogin ? 'Create an account' : 'Sign in'}
                            </button>
                        </p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default AuthPage;
