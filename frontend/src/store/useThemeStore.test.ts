import { describe, it, expect, beforeEach } from 'vitest';
import { useThemeStore } from './useThemeStore';

describe('useThemeStore', () => {
  beforeEach(() => {
    // Reset the store before each test to ensure a clean state
    useThemeStore.setState({ theme: 'dark' });
    global.localStorage.clear();
  });

  it('should initialize with the dark theme as default', () => {
    const { theme } = useThemeStore.getState();
    expect(theme).toBe('dark');
  });

  it('should toggle theme from dark to light', () => {
    const { toggleTheme } = useThemeStore.getState();
    toggleTheme();

    expect(useThemeStore.getState().theme).toBe('light');
  });

  it('should toggle theme from light to dark', () => {
    useThemeStore.setState({ theme: 'light' });
    const { toggleTheme } = useThemeStore.getState();
    toggleTheme();

    expect(useThemeStore.getState().theme).toBe('dark');
  });

  it('should explicitly set the theme to light', () => {
    const { setTheme } = useThemeStore.getState();
    setTheme('light');

    expect(useThemeStore.getState().theme).toBe('light');
  });

  it('should explicitly set the theme to dark', () => {
    useThemeStore.setState({ theme: 'light' });
    const { setTheme } = useThemeStore.getState();
    setTheme('dark');

    expect(useThemeStore.getState().theme).toBe('dark');
  });
});
