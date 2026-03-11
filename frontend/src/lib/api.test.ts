import { describe, it, expect, vi, beforeEach } from 'vitest';
import { register, getCourses, api, refineQuestion } from './api';

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
      vi.spyOn(api, 'post').mockResolvedValueOnce(mockResponse as unknown);

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

  describe('getCourses', () => {
    it('should call api.get with correct parameters and return response data', async () => {
      // Arrange
      const mockData = [
        { id: 1, name: 'Course 1', code: 'CS101' },
        { id: 2, name: 'Course 2', code: 'CS102' }
      ];
      const mockResponse = { data: mockData };

      // Use vi.spyOn to intercept api.get
      vi.spyOn(api, 'get').mockResolvedValueOnce(mockResponse as unknown);

      // Act
      const result = await getCourses();

      // Assert
      expect(api.get).toHaveBeenCalledTimes(1);
      expect(api.get).toHaveBeenCalledWith('/courses/');
      expect(result).toEqual(mockData);
    });

    it('should throw an error if api.get fails', async () => {
      // Arrange
      const mockError = new Error('Network Error');
      vi.spyOn(api, 'get').mockRejectedValueOnce(mockError);

      // Act & Assert
      await expect(getCourses()).rejects.toThrow('Network Error');
    });
  });

  describe('refineQuestion', () => {
    it('should call api.post with correct parameters and return response data', async () => {
      // Arrange
      const mockData = { id: 1, text: 'refined text' };
      const mockResponse = { data: mockData };

      // Use vi.spyOn to intercept api.post
      vi.spyOn(api, 'post').mockResolvedValueOnce(mockResponse as unknown);

      // Act
      const result = await refineQuestion(1, 'needs more depth', 'Biology');

      // Assert
      expect(api.post).toHaveBeenCalledTimes(1);
      expect(api.post).toHaveBeenCalledWith('/refine/', {
        question_id: 1,
        critique: 'needs more depth',
        topic: 'Biology'
      });
      expect(result).toEqual(mockData);
    });

    it('should throw an error if api.post fails', async () => {
      // Arrange
      const mockError = new Error('Network Error');
      vi.spyOn(api, 'post').mockRejectedValueOnce(mockError);

      // Act & Assert
      await expect(refineQuestion(1, 'needs more depth', 'Biology')).rejects.toThrow('Network Error');
    });
  });
});
