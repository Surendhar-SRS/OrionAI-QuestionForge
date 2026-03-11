/* @vitest-environment jsdom */
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { useAuthStore } from '../useAuthStore';

// We need to properly clear Zustand state and localStorage between tests
describe('useAuthStore', () => {
  const initialUserState = useAuthStore.getState();

  beforeEach(() => {
    // Clear localStorage
    localStorage.clear();
    // Reset state
    useAuthStore.setState(initialUserState, true);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should have correct initial state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });

  it('should set authentication state correctly and persist to storage', () => {
    const mockUser = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const mockToken = 'mock-jwt-token';

    useAuthStore.getState().setAuth(mockUser, mockToken);

    const state = useAuthStore.getState();
    expect(state.user).toEqual(mockUser);
    expect(state.token).toBe(mockToken);
    expect(state.isAuthenticated).toBe(true);

    // Verify localStorage has been updated correctly
    const storedState = JSON.parse(localStorage.getItem('auth-storage') || '{}');
    expect(storedState.state.user).toEqual(mockUser);
    expect(storedState.state.token).toBe(mockToken);
    expect(storedState.state.isAuthenticated).toBe(true);
  });

  it('should logout correctly and remove from storage', () => {
    // First setup an authenticated state
    const mockUser = { id: 1, email: 'test@example.com', full_name: 'Test User' };
    const mockToken = 'mock-jwt-token';
    useAuthStore.getState().setAuth(mockUser, mockToken);

    // Verify it's authenticated
    expect(useAuthStore.getState().isAuthenticated).toBe(true);
    expect(JSON.parse(localStorage.getItem('auth-storage') || '{}').state.isAuthenticated).toBe(true);

    // Perform logout
    useAuthStore.getState().logout();

    // Verify state is cleared
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);

    // Verify localStorage has been updated correctly
    const storedState = JSON.parse(localStorage.getItem('auth-storage') || '{}');
    expect(storedState.state.user).toBeNull();
    expect(storedState.state.token).toBeNull();
    expect(storedState.state.isAuthenticated).toBe(false);
  });
});
