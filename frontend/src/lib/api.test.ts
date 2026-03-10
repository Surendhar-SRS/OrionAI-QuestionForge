import { describe, it, expect, vi, beforeEach } from 'vitest';
import { register, api } from './api';

describe('api.ts', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('register', () => {
    it('should call api.post with correct parameters and return response data', async () => {
      // Arrange
      const mockData = { id: 1, email: 'test@example.com', full_name: 'Test User' };
      const mockResponse = { data: mockData };

      // Use vi.spyOn to intercept api.post
      vi.spyOn(api, 'post').mockResolvedValueOnce(mockResponse as any);

      // Act
      const result = await register('test@example.com', 'password123', 'Test User');

      // Assert
      expect(api.post).toHaveBeenCalledTimes(1);
      expect(api.post).toHaveBeenCalledWith('/auth/register', {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      });
      expect(result).toEqual(mockData);
    });

    it('should throw an error if api.post fails', async () => {
      // Arrange
      const mockError = new Error('Network Error');
      vi.spyOn(api, 'post').mockRejectedValueOnce(mockError);

      // Act & Assert
      await expect(register('test@example.com', 'password123', 'Test User')).rejects.toThrow('Network Error');
    });
  });
});
