import { useState, useEffect, useRef } from 'react';
import { paperService } from '@/api/paperService';
import { workflowService } from '@/api/workflowService';
import { useWorkflows } from './useWorkflows';

export interface WorkflowStatus {
  status: string;
  total_papers: number;
  processed: number;
  skipped: number;
  errors: string[];
  papers: Array<{ id: string; title: string; pdf_link: string }>;
  elapsed_time: number | null;
}

export function useWorkflowTrigger() {
  const { workflows } = useWorkflows(true); // Only enabled workflows
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<WorkflowStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);


  const startPolling = () => {
    // Clear existing interval
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
    }
    
    // Poll every 1 second
    pollingIntervalRef.current = setInterval(async () => {
      try {
        const currentStatus = await paperService.getWorkflowStatus();
        setStatus(currentStatus);
        
        // Stop polling if workflow is completed, stopped, or error
        if (['completed', 'stopped', 'error', 'idle'].includes(currentStatus.status)) {
          stopPolling();
          setLoading(false);
        }
      } catch (err: any) {
        console.error('Failed to fetch workflow status:', err);
      }
    }, 1000);
  };

  const stopPolling = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  };

  const triggerWorkflow = async () => {
    setLoading(true);
    setError(null);
    setStatus(null);

    try {
      if (!selectedWorkflowId) {
        throw new Error('Please select a workflow');
      }

      await workflowService.triggerWorkflow(selectedWorkflowId);
      
      // Start polling for status updates
      startPolling();
      
      // Fetch initial status
      const initialStatus = await paperService.getWorkflowStatus();
      setStatus(initialStatus);
    } catch (err: any) {
      setError(err.message || 'Failed to trigger workflow');
      setLoading(false);
    }
  };

  const stopWorkflow = async () => {
    try {
      await paperService.stopWorkflow();
      // Status will update via polling
    } catch (err: any) {
      setError(err.message || 'Failed to stop workflow');
    }
  };

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, []);

  const isRunning = status?.status === 'running' || status?.status === 'stopping';

  return {
    workflows,
    selectedWorkflowId,
    setSelectedWorkflowId,
    loading,
    status,
    error,
    isRunning,
    triggerWorkflow,
    stopWorkflow,
  };
}

