/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

// We need to properly mock localStorage and let vitest use the jsdom environment
// so that zustand/persist middleware picks it up correctly.

// Using a custom storage directly via zustand might be better, but we want
// to use the actual default storage in the app (localStorage).
// The error "[zustand persist middleware] Unable to update item..." usually means
// localStorage is undefined when the persist middleware initializes, or the
// vitest environment is not 'jsdom'.

import { useAuthStore } from './useAuthStore';

// In vitest with jsdom environment, localStorage is already available.
// Let's set the environment via docblock just in case vitest isn't
// defaulting to it here.

describe('useAuthStore', () => {
  // Reset state and localStorage before each test
  beforeEach(() => {
    localStorage.clear();
    // Reset Zustand store state manually
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe('Initial State', () => {
    it('should have initial state with null user and token, and isAuthenticated false', () => {
      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
      expect(state.token).toBeNull();
      expect(state.isAuthenticated).toBe(false);
    });
  });

  describe('Actions', () => {
    const mockUser = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const mockToken = 'valid-jwt-token';

    it('should set authentication state when setAuth is called with valid data', () => {
      useAuthStore.getState().setAuth(mockUser, mockToken);

      const state = useAuthStore.getState();
      expect(state.user).toEqual(mockUser);
      expect(state.token).toBe(mockToken);
      expect(state.isAuthenticated).toBe(true);
    });

    it('should handle setAuth called with null/empty values', () => {
      const emptyUser = null as unknown as typeof mockUser;
      const emptyToken = '' as unknown as string;

      useAuthStore.getState().setAuth(emptyUser, emptyToken);

      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
      expect(state.token).toBe('');
      expect(state.isAuthenticated).toBe(true);
    });

    it('should clear authentication state when logout is called', () => {
      useAuthStore.setState({
        user: { id: 1, email: 'test@example.com', full_name: 'Test User' },
        token: 'valid-jwt-token',
        isAuthenticated: true,
      });

      useAuthStore.getState().logout();

      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
      expect(state.token).toBeNull();
      expect(state.isAuthenticated).toBe(false);
    });
  });

  describe('Persistence', () => {
    const mockUser = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const mockToken = 'valid-jwt-token';

    it('should persist auth state to localStorage on setAuth', () => {
      useAuthStore.getState().setAuth(mockUser, mockToken);

      const storedDataStr = localStorage.getItem('auth-storage');
      expect(storedDataStr).not.toBeNull();

      const storedData = JSON.parse(storedDataStr as string);
      expect(storedData.state.user).toEqual(mockUser);
      expect(storedData.state.token).toBe(mockToken);
      expect(storedData.state.isAuthenticated).toBe(true);
    });

    it('should remove auth state from localStorage on logout', () => {
      useAuthStore.getState().setAuth(mockUser, mockToken);
      useAuthStore.getState().logout();

      const storedDataStr = localStorage.getItem('auth-storage');
      expect(storedDataStr).not.toBeNull();

      const storedData = JSON.parse(storedDataStr as string);
      expect(storedData.state.user).toBeNull();
      expect(storedData.state.token).toBeNull();
      expect(storedData.state.isAuthenticated).toBe(false);
    });
  });
});
