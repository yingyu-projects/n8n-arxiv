import { useState } from 'react';
import { paperService } from '@/api/paperService';

export function useWorkflowTrigger() {
  const [categories, setCategories] = useState<string[]>(['cs.AI', 'cs.CL', 'cs.LG', 'cs.HC', 'cs.CV']);
  const [numPapers, setNumPapers] = useState(50);
  const [summarizePrompt, setSummarizePrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

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

  const triggerWorkflow = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const validCategories = categories.filter(cat => cat.trim() !== '');
      if (validCategories.length === 0) {
        throw new Error('At least one category is required');
      }

      const data = await paperService.triggerWorkflow(
        validCategories,
        numPapers,
        summarizePrompt
      );
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to trigger workflow');
    } finally {
      setLoading(false);
    }
  };

  return {
    categories,
    setCategories,
    updateCategory,
    numPapers,
    setNumPapers,
    summarizePrompt,
    setSummarizePrompt,
    loading,
    result,
    error,
    addCategory,
    removeCategory,
    triggerWorkflow,
  };
}

