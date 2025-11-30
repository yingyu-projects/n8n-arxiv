import { useState, useEffect, useRef } from 'react';
import { paperService } from '@/api/paperService';

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
  const [categories, setCategories] = useState<string[]>(['cs.AI', 'cs.CL', 'cs.LG', 'cs.HC', 'cs.CV']);
  const [numPapers, setNumPapers] = useState(50);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<WorkflowStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const addCategory = () => {
    setCategories([...categories, '']);
  };

  const removeCategory = (index: number) => {
    setCategories(categories.filter((_, i) => i !== index));
  };

  const updateCategory = (index: number, value: string) => {
    const newCategories = [...categories];
    newCategories[index] = value;
    setCategories(newCategories);
  };

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
      const validCategories = categories.filter(cat => cat.trim() !== '');
      if (validCategories.length === 0) {
        throw new Error('At least one category is required');
      }

      await paperService.triggerWorkflow(validCategories, numPapers);
      
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
    categories,
    setCategories,
    updateCategory,
    numPapers,
    setNumPapers,
    loading,
    status,
    error,
    isRunning,
    addCategory,
    removeCategory,
    triggerWorkflow,
    stopWorkflow,
  };
}

