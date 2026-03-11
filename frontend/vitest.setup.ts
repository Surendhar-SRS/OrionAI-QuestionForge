import { vi } from 'vitest';

const storeStorage: Record<string, string> = {};

const localStorageMock = {
  getItem: vi.fn((key: string) => storeStorage[key] || null),
  setItem: vi.fn((key: string, value: string) => {
    storeStorage[key] = value;
  }),
  removeItem: vi.fn((key: string) => {
    delete storeStorage[key];
  }),
  clear: vi.fn(() => {
    for (const key in storeStorage) {
      delete storeStorage[key];
    }
  }),
  length: 0,
  key: vi.fn((index: number) => Object.keys(storeStorage)[index] || null),
};

Object.defineProperty(global, 'localStorage', {
  value: localStorageMock,
  writable: true
});

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
});
import '@testing-library/jest-dom';
