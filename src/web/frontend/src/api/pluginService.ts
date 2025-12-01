import api from './api';
import type { Plugin, PluginConfigSchema, PluginType } from '@/types/plugin';

export const pluginService = {
  async getPlugins(
    pluginType?: PluginType,
    enabledOnly: boolean = false
  ): Promise<Plugin[]> {
    const response = await api.get('/plugins', {
      params: {
        plugin_type: pluginType,
        enabled_only: enabledOnly,
      },
    });
    return response.data;
  },

  async getPlugin(id: string): Promise<Plugin> {
    const response = await api.get(`/plugins/${id}`);
    return response.data;
  },

  async getPluginConfigSchema(id: string): Promise<PluginConfigSchema> {
    const response = await api.get(`/plugins/${id}/config-schema`);
    return response.data;
  },

  async updatePlugin(id: string, data: { enabled?: boolean }): Promise<Plugin> {
    const response = await api.put(`/plugins/${id}`, data);
    return response.data;
  },

  async discoverPlugins(): Promise<{ message: string; count: number }> {
    const response = await api.post('/plugins/discover');
    return response.data;
  },
};

