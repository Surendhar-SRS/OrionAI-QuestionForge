import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api, generateQuestion } from './api';

describe('generateQuestion', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should call the /generate/ endpoint with correctly formatted parameters', async () => {
    // Arrange
    const mockResponse = {
      data: {
        id: 101,
        text: 'What is the sum of 2 and 2?',
        type: 'MCQ',
        marks: 5,
        bloom_level: 'Recall',
        difficulty: 'Easy',
        answer_key: '4',
        rubric: 'Assign 5 marks for correct answer.',
        accepted: false
      }
    };

    // Spy on api.post and return the mock response
    const postSpy = vi.spyOn(api, 'post').mockResolvedValue(mockResponse as any);

    const courseId = 42;
    const topic = 'Basic Arithmetic';
    const bloom = 'Recall';
    const difficulty = 'Easy';

    // Act
    const result = await generateQuestion(courseId, topic, bloom, difficulty);

    // Assert
    expect(postSpy).toHaveBeenCalledTimes(1);
    expect(postSpy).toHaveBeenCalledWith('/generate/', {
      course_id: courseId,
      topic: topic,
      bloom_level: bloom,
      difficulty: difficulty
    });

    expect(result).toEqual(mockResponse.data);
  });

  it('should handle special characters and whitespace in string parameters', async () => {
    // Arrange
    const mockResponse = { data: { id: 102 } };
    const postSpy = vi.spyOn(api, 'post').mockResolvedValue(mockResponse as any);

    const courseId = 99;
    const topic = '  Advanced   Topic! @#$%^&*()_+ ';
    const bloom = 'Synthesis & Evaluation';
    const difficulty = 'Very Hard / Expert';

    // Act
    await generateQuestion(courseId, topic, bloom, difficulty);

    // Assert
    expect(postSpy).toHaveBeenCalledWith('/generate/', {
      course_id: courseId,
      topic: topic, // ensuring strings are passed through without unexpected modification
      bloom_level: bloom,
      difficulty: difficulty
    });
  });

  it('should propagate API errors effectively', async () => {
    // Arrange
    const mockError = new Error('Network Error');
    const postSpy = vi.spyOn(api, 'post').mockRejectedValue(mockError);

    const courseId = 5;
    const topic = 'History';
    const bloom = 'Understanding';
    const difficulty = 'Medium';

    // Act & Assert
    await expect(generateQuestion(courseId, topic, bloom, difficulty)).rejects.toThrow('Network Error');

    expect(postSpy).toHaveBeenCalledWith('/generate/', {
      course_id: courseId,
      topic: topic,
      bloom_level: bloom,
      difficulty: difficulty
    });
  });
});
