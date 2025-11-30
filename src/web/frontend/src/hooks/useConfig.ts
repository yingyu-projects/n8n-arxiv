import { useState, useEffect } from 'react';
import api from '@/api/api';
import type { Category } from '@/types/category';

export function useConfig() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategories, setNewCategories] = useState<string[]>(['cs.AI', 'cs.CL', 'cs.LG', 'cs.HC', 'cs.CV']);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Category[]>('/categories');
      setCategories(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load categories');
    } finally {
      setLoading(false);
    }
  };

  const saveCategories = async () => {
    setSaving(true);
    setError(null);
    try {
      await api.post('/categories', {
        categories: newCategories.filter(cat => cat.trim() !== ''),
      });
      await loadCategories();
    } catch (err: any) {
      setError(err.message || 'Failed to save categories');
    } finally {
      setSaving(false);
    }
  };

  const addCategory = () => {
    setNewCategories([...newCategories, '']);
  };

  const removeCategory = (index: number) => {
    setNewCategories(newCategories.filter((_, i) => i !== index));
  };

  const updateCategory = (index: number, value: string) => {
    const newCategoriesArray = [...newCategories];
    newCategoriesArray[index] = value;
    setNewCategories(newCategoriesArray);
  };

  useEffect(() => {
    loadCategories();
  }, []);

  return {
    categories,
    newCategories,
    setNewCategories,
    updateCategory,
    loading,
    saving,
    error,
    loadCategories,
    saveCategories,
    addCategory,
    removeCategory,
  };
}

