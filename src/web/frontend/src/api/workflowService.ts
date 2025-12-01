import api from './api';
import type {
  Workflow,
  WorkflowConfig,
  CreateWorkflowRequest,
  UpdateWorkflowRequest,
  UpdateWorkflowConfigRequest,
} from '@/types/workflow';

export const workflowService = {
  async getWorkflows(enabledOnly: boolean = false, projectId?: string): Promise<Workflow[]> {
    const params: any = { enabled_only: enabledOnly };
    if (projectId) {
      params.project_id = projectId;
    }
    const response = await api.get('/workflows', { params });
    return response.data;
  },

  async getWorkflow(id: string): Promise<Workflow> {
    const response = await api.get(`/workflows/${id}`);
    return response.data;
  },

  async createWorkflow(data: CreateWorkflowRequest): Promise<Workflow> {
    const response = await api.post('/workflows', data);
    return response.data;
  },

  async updateWorkflow(id: string, data: UpdateWorkflowRequest): Promise<Workflow> {
    const response = await api.put(`/workflows/${id}`, data);
    return response.data;
  },

  async deleteWorkflow(id: string): Promise<void> {
    await api.delete(`/workflows/${id}`);
  },

  async getWorkflowConfig(id: string): Promise<WorkflowConfig> {
    const response = await api.get(`/workflows/${id}/config`);
    return response.data;
  },

  async updateWorkflowConfig(id: string, data: UpdateWorkflowConfigRequest): Promise<WorkflowConfig> {
    const response = await api.put(`/workflows/${id}/config`, data);
    return response.data;
  },

  async addPluginToWorkflow(
    workflowId: string,
    pluginId: string,
    config?: Record<string, any>,
    enabled: boolean = true
  ): Promise<void> {
    await api.post(`/workflows/${workflowId}/plugins`, {
      plugin_id: pluginId,
      config: config || {},
      enabled,
    });
  },

  async removePluginFromWorkflow(workflowId: string, pluginId: string): Promise<void> {
    await api.delete(`/workflows/${workflowId}/plugins/${pluginId}`);
  },

  async triggerWorkflow(id: string): Promise<{ message: string; status: string }> {
    const response = await api.post(`/workflows/${id}/trigger`);
    return response.data;
  },
};

