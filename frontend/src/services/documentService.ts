import api from './api';

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const listDocuments = async () => {
  const response = await api.get('/documents/list');
  return response.data;
};

export const queryDocuments = async (question: string) => {
  const response = await api.post('/documents/query', { question });
  return response.data;
};
