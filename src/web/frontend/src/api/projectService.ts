import api from './api';
import type { Project } from '@/types/project';

export interface CreateProjectRequest {
  name: string;
  description?: string | null;
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string | null;
}

export const projectService = {
  async getProjects(): Promise<Project[]> {
    const response = await api.get('/projects');
    return response.data;
  },

  async getProject(id: string): Promise<Project> {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },

  async createProject(data: CreateProjectRequest): Promise<Project> {
    const response = await api.post('/projects', data);
    return response.data;
  },

  async updateProject(id: string, data: UpdateProjectRequest): Promise<Project> {
    const response = await api.put(`/projects/${id}`, data);
    return response.data;
  },

  async deleteProject(id: string): Promise<void> {
    await api.delete(`/projects/${id}`);
  },
};

