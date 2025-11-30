import { useState, useEffect } from 'react';
import { paperService } from '@/api/paperService';
import type { PaperList as PaperListType } from '@/types/paper';

export function usePaperList() {
  const [papers, setPapers] = useState<PaperListType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(50);
  const [totalPages, setTotalPages] = useState(1);

  const loadPapers = async () => {
    setLoading(true);
    setError(null);
    try {
      const offset = (currentPage - 1) * pageSize;
      const data = await paperService.getPapers(
        selectedCategory || undefined,
        pageSize,
        offset
      );
      setPapers(data);
      // Simple pagination - if we get less than pageSize, we're on the last page
      setTotalPages(data.length < pageSize ? currentPage : currentPage + 1);
    } catch (err: any) {
      setError(err.message || 'Failed to load papers');
    } finally {
      setLoading(false);
    }
  };

  const onCategoryChange = () => {
    setCurrentPage(1);
    loadPapers();
  };

  const onPageChange = (page: number) => {
    setCurrentPage(page);
  };

  useEffect(() => {
    loadPapers();
  }, [currentPage, selectedCategory]);

  return {
    papers,
    loading,
    error,
    selectedCategory,
    setSelectedCategory,
    currentPage,
    pageSize,
    totalPages,
    loadPapers,
    onCategoryChange,
    onPageChange,
  };
}

