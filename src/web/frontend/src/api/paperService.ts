import api from './api';
import type { Paper, PaperList } from '@/types/paper';

export const paperService = {
  async getPapers(category?: string, limit = 50, offset = 0): Promise<PaperList[]> {
    const params: Record<string, any> = { limit, offset };
    if (category) {
      params.category = category;
    }
    const response = await api.get<PaperList[]>('/papers', { params });
    return response.data;
  },

  async getPaper(id: string): Promise<Paper> {
    const response = await api.get<Paper>(`/papers/${id}`);
    return response.data;
  },

  async triggerWorkflow(
    categories: string[],
    numPapers = 50
  ): Promise<{ message: string; status: string }> {
    const response = await api.post('/workflow/trigger', {
      categories,
      num_papers: numPapers,
    });
    return response.data;
  },

  async getWorkflowStatus(): Promise<{
    status: string;
    total_papers: number;
    processed: number;
    skipped: number;
    errors: string[];
    papers: Array<{ id: string; title: string; pdf_link: string }>;
    elapsed_time: number | null;
  }> {
    const response = await api.get('/workflow/status');
    return response.data;
  },

  async stopWorkflow(): Promise<{ message: string }> {
    const response = await api.post('/workflow/stop');
    return response.data;
  },
};

