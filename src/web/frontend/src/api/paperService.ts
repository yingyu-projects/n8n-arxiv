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
    numPapers = 50,
    summarizePrompt = ''
  ): Promise<{
    processed: number;
    skipped: number;
    errors: string[];
    papers: Array<{ id: string; title: string; pdf_link: string }>;
  }> {
    const response = await api.post('/workflow/trigger', {
      categories,
      num_papers: numPapers,
      summarize_prompt: summarizePrompt,
    });
    return response.data;
  },
};

