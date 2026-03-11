import axios from 'axios';

import { useAuthStore } from '../store/useAuthStore';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add interceptor for JWT
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface Course {
  id: number;
  name: string;
  code: string;
  semester?: string;
  blueprint_json: any;
}

export interface Question {
  id: number;
  text: string;
  type: string;
  marks: number;
  bloom_level: string;
  difficulty: string;
  answer_key: string;
  rubric: string;
  accepted: boolean;
}

export const createCourse = async (course: Omit<Course, 'id'>) => {
  const response = await api.post<Course>('/courses/', course);
  return response.data;
};

export const getCourses = async () => {
  const response = await api.get<Course[]>('/courses/');
  return response.data;
};

export const ingestDocument = async (courseId: number, file: File) => {
  const formData = new FormData();
  formData.append('course_id', courseId.toString());
  formData.append('file', file);
  const response = await api.post('/ingest/', formData);
  return response.data;
};

export const generateQuestion = async (courseId: number, topic: string, bloom: string, difficulty: string) => {
  const response = await api.post<Question>('/generate/', {
    course_id: courseId,
    topic,
    bloom_level: bloom,
    difficulty: difficulty
  });
  return response.data;
};

export const auditQuestion = async (questionId: number, topic: string) => {
  const response = await api.post('/audit/', {
    question_id: questionId,
    topic
  });
  return response.data;
};

export const refineQuestion = async (questionId: number, critique: string, topic: string) => {
  const response = await api.post('/refine/', {
    question_id: questionId,
    critique,
    topic
  });
  return response.data;
};

export const login = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', email); // FastAPI OAuth2 uses 'username'
  formData.append('password', password);
  
  const response = await api.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const register = async (email: string, password: string, fullName: string) => {
  const response = await api.post('/auth/register', {
    email,
    password,
    full_name: fullName,
  });
  return response.data;
};

export const getAuditLogs = async (courseId: number) => {
  const response = await api.get(`/audit-logs/${courseId}`);
  return response.data;
};

export const getStats = async (courseId: number) => {
  const response = await api.get(`/stats/${courseId}`);
  return response.data;
};
