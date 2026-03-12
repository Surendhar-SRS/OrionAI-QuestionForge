import { describe, it, expect, vi, beforeEach } from 'vitest';
import { login, api } from './api';

describe('api.auth.ts - login', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should call api.post with correct parameters and return response data', async () => {
    // Arrange
    const mockData = { access_token: 'fake-token', token_type: 'bearer' };
    const mockResponse = { data: mockData };

    // Use vi.spyOn to intercept api.post
    vi.spyOn(api, 'post').mockResolvedValueOnce(mockResponse as unknown);

    // Act
    const result = await login('test@example.com', 'password123');

    // Assert
    expect(api.post).toHaveBeenCalledTimes(1);

    const expectedFormData = new URLSearchParams();
    expectedFormData.append('username', 'test@example.com');
    expectedFormData.append('password', 'password123');

    expect(api.post).toHaveBeenCalledWith('/auth/login', expectedFormData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    expect(result).toEqual(mockData);
  });

  it('should throw a network error if api.post fails with a network error', async () => {
    // Arrange
    const mockError = new Error('Network Error');
    vi.spyOn(api, 'post').mockRejectedValueOnce(mockError);

    // Act & Assert
    await expect(login('test@example.com', 'password123')).rejects.toThrow('Network Error');
  });

  it('should handle 401 Unauthorized error response structure', async () => {
    // Arrange
    const mockError = {
      response: {
        status: 401,
        data: { detail: 'Incorrect username or password' },
      },
    };
    vi.spyOn(api, 'post').mockRejectedValueOnce(mockError);

    // Act & Assert
    await expect(login('test@example.com', 'wrongpassword')).rejects.toEqual(mockError);
  });

  it('should correctly pass empty strings in the payload if provided', async () => {
    // Arrange
    const mockData = { access_token: 'fake-token', token_type: 'bearer' };
    vi.spyOn(api, 'post').mockResolvedValueOnce({ data: mockData } as unknown);

    // Act
    await login('', '');

    // Assert
    expect(api.post).toHaveBeenCalledTimes(1);

    const expectedFormData = new URLSearchParams();
    expectedFormData.append('username', '');
    expectedFormData.append('password', '');

    expect(api.post).toHaveBeenCalledWith('/auth/login', expectedFormData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  });

  it('should handle missing data in response structure', async () => {
    // Arrange
    const mockResponse = {}; // No data property
    vi.spyOn(api, 'post').mockResolvedValueOnce(mockResponse as unknown);

    // Act
    const result = await login('test@example.com', 'password123');

    // Assert
    expect(result).toBeUndefined();
  });
});
