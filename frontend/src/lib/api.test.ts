import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('axios', () => {
  const mockPost = vi.fn();
  const mockGet = vi.fn();
  return {
    default: {
      create: vi.fn(() => ({
        post: mockPost,
        get: mockGet,
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() },
        },
      })),
    },
    mockPost, // Export these so we can use them in tests
    mockGet,
  };
});

// Now import our api which will use the mocked axios
import { createCourse, Course, api } from './api';

describe('api functions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('createCourse', () => {
    it('should successfully post course data and return the created course', async () => {
      const mockCourseInput: Omit<Course, 'id'> = {
        name: 'Introduction to Testing',
        code: 'TEST101',
        semester: 'Fall 2024',
        blueprint_json: { test: true },
      };

      const mockCourseOutput: Course = {
        id: 1,
        ...mockCourseInput,
      };

      // Set up the mock to return our expected output
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (api.post as any).mockResolvedValueOnce({ data: mockCourseOutput });

      // Call the function
      const result = await createCourse(mockCourseInput);

      // Verify the api.post was called with the correct URL and body
      expect(api.post).toHaveBeenCalledTimes(1);
      expect(api.post).toHaveBeenCalledWith('/courses/', mockCourseInput);

      // Verify the result matches our expected output
      expect(result).toEqual(mockCourseOutput);
    });

    it('should throw an error if the request fails', async () => {
      const mockCourseInput: Omit<Course, 'id'> = {
        name: 'Introduction to Testing',
        code: 'TEST101',
        semester: 'Fall 2024',
        blueprint_json: { test: true },
      };

      const errorMessage = 'Network Error';

      // Set up the mock to throw an error
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (api.post as any).mockRejectedValueOnce(new Error(errorMessage));

      // Verify that calling the function throws the error
      await expect(createCourse(mockCourseInput)).rejects.toThrow(errorMessage);
    });
  });
});
