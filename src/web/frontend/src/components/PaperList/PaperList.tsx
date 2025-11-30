'use client';

import { useRouter } from 'next/navigation';
import { usePaperList } from '@/hooks/usePaperList';
import styles from './PaperList.module.scss';

export default function PaperList() {
  const router = useRouter();
  const {
    papers,
    loading,
    error,
    selectedCategory,
    setSelectedCategory,
    currentPage,
    pageSize,
    onPageChange,
  } = usePaperList();

  const goToDetail = (id: string) => {
    router.push(`/papers/${id}`);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedCategory(e.target.value);
  };

  return (
    <div className={styles.paperList}>
      <div className={styles.filters}>
        <input
          value={selectedCategory}
          onChange={handleCategoryChange}
          type="text"
          placeholder="Filter by category (e.g., cs.AI)"
          className={styles.categoryFilter}
        />
      </div>

      {loading && <div className={styles.loading}>Loading papers...</div>}
      {error && <div className={styles.error}>{error}</div>}
      {!loading && !error && papers.length === 0 && (
        <div className={styles.empty}>No papers found</div>
      )}
      {!loading && !error && papers.length > 0 && (
        <div className={styles.papers}>
          {papers.map((paper) => (
            <div
              key={paper.id}
              className={styles.paperItem}
              onClick={() => goToDetail(paper.id)}
            >
              <h3 className={styles.paperTitle}>{paper.title}</h3>
              <div className={styles.paperMeta}>
                <span className={styles.category}>{paper.category}</span>
                {paper.parsed_at && (
                  <span className={styles.parsedBadge}>Parsed</span>
                )}
                <span className={styles.date}>{formatDate(paper.created_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && papers.length > 0 && (
        <div className={styles.pagination}>
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>Page {currentPage}</span>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={papers.length < pageSize}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

