import { useState, useEffect } from 'react';
import { paperService } from '@/api/paperService';
import type { Paper } from '@/types/paper';

export function usePaperDetail(id: string) {
  const [paper, setPaper] = useState<Paper | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPaper = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await paperService.getPaper(id);
      setPaper(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load paper');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      loadPaper();
    }
  }, [id]);

  return {
    paper,
    loading,
    error,
    loadPaper,
  };
}

