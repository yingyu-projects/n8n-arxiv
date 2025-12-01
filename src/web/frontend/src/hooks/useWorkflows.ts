import { useState, useEffect } from 'react';
import { workflowService } from '@/api/workflowService';
import type { Workflow } from '@/types/workflow';

export function useWorkflows(enabledOnly: boolean = false, projectId?: string) {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadWorkflows = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await workflowService.getWorkflows(enabledOnly, projectId);
      setWorkflows(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflows');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, [enabledOnly, projectId]);

  return {
    workflows,
    loading,
    error,
    reload: loadWorkflows,
  };
}

