import { useState, useEffect } from 'react';
import { workflowService } from '@/api/workflowService';
import type { WorkflowConfig, UpdateWorkflowConfigRequest } from '@/types/workflow';

export function useWorkflowConfig(workflowId: string | null) {
  const [config, setConfig] = useState<WorkflowConfig | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadConfig = async () => {
    if (!workflowId) return;
    
    setLoading(true);
    setError(null);
    try {
      const data = await workflowService.getWorkflowConfig(workflowId);
      setConfig(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load workflow config');
    } finally {
      setLoading(false);
    }
  };

  const saveConfig = async (updates: UpdateWorkflowConfigRequest) => {
    if (!workflowId) return;
    
    setSaving(true);
    setError(null);
    try {
      const data = await workflowService.updateWorkflowConfig(workflowId, updates);
      setConfig(data);
    } catch (err: any) {
      setError(err.message || 'Failed to save workflow config');
      throw err;
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, [workflowId]);

  return {
    config,
    loading,
    saving,
    error,
    reload: loadConfig,
    saveConfig,
  };
}

