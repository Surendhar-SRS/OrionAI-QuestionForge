/* @vitest-environment jsdom */
import { describe, it, expect, beforeEach } from 'vitest';
import { useThemeStore } from './useThemeStore';

describe('useThemeStore', () => {
  beforeEach(() => {
    // Clear localStorage to prevent test pollution
    localStorage.clear();

    // Manually reset the store's in-memory state
    useThemeStore.setState({
      theme: 'dark' // The default state
    });
  });

  it('should have an initial theme of "dark"', () => {
    const state = useThemeStore.getState();
    expect(state.theme).toBe('dark');
  });

  it('should toggle theme from dark to light', () => {
    useThemeStore.getState().toggleTheme();
    expect(useThemeStore.getState().theme).toBe('light');
  });

  it('should toggle theme from light to dark', () => {
    // Set to light first
    useThemeStore.getState().setTheme('light');
    expect(useThemeStore.getState().theme).toBe('light');

    // Toggle back to dark
    useThemeStore.getState().toggleTheme();
    expect(useThemeStore.getState().theme).toBe('dark');
  });

  it('should set theme to a specific value', () => {
    useThemeStore.getState().setTheme('light');
    expect(useThemeStore.getState().theme).toBe('light');

    useThemeStore.getState().setTheme('dark');
    expect(useThemeStore.getState().theme).toBe('dark');
  });
});
