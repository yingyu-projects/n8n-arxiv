import api from './api';

export interface Config {
  key: string;
  value: string;
}

export const configService = {
  get: async (key: string): Promise<Config> => {
    const response = await api.get<Config>('/config', {
      params: { key },
    });
    return response.data;
  },

  update: async (key: string, value: string): Promise<Config> => {
    const response = await api.post<Config>('/config', {
      key,
      value,
    });
    return response.data;
  },
};

