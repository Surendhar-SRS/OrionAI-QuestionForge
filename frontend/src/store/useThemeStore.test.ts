import { describe, it, expect, beforeEach } from 'vitest';
import { useThemeStore } from './useThemeStore';

describe('useThemeStore', () => {
  // Reset the store to its initial state before each test
  beforeEach(() => {
    // Just reset the theme, don't replace the whole state (which would delete functions)
    useThemeStore.setState({ theme: 'dark' });
  });

  it('should have a default theme of "dark"', () => {
    const { theme } = useThemeStore.getState();
    expect(theme).toBe('dark');
  });

  it('should toggle the theme from "dark" to "light"', () => {
    const { toggleTheme } = useThemeStore.getState();
    toggleTheme();

    expect(useThemeStore.getState().theme).toBe('light');
  });

  it('should toggle the theme from "light" to "dark"', () => {
    useThemeStore.setState({ theme: 'light' });

    const { toggleTheme } = useThemeStore.getState();
    toggleTheme();

    expect(useThemeStore.getState().theme).toBe('dark');
  });

  it('should set the theme directly using setTheme', () => {
    const { setTheme } = useThemeStore.getState();

    setTheme('light');
    expect(useThemeStore.getState().theme).toBe('light');

    setTheme('dark');
    expect(useThemeStore.getState().theme).toBe('dark');
  });
});
