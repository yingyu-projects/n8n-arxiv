'use client';

import { usePaperDetail } from '@/hooks/usePaperDetail';
import styles from './PaperDetail.module.scss';

interface PaperDetailProps {
  id: string;
}

export default function PaperDetail({ id }: PaperDetailProps) {
  const { paper, loading, error } = usePaperDetail(id);

  const formatContent = (content: any): string => {
    if (typeof content === 'string') {
      return content.replace(/\n/g, '<br>');
    }
    if (typeof content === 'object') {
      return JSON.stringify(content, null, 2).replace(/\n/g, '<br>');
    }
    return '';
  };

  if (loading) {
    return <div className={styles.loading}>Loading paper...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!paper) {
    return null;
  }

  return (
    <div className={styles.paperDetail}>
      <div className={styles.content}>
        <div className={styles.header}>
          <h1 className={styles.title}>{paper.title}</h1>
          <div className={styles.meta}>
            <span className={styles.category}>{paper.category}</span>
            {paper.arxiv_id && (
              <span className={styles.arxivId}>{paper.arxiv_id}</span>
            )}
            <a
              href={paper.pdf_link}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.pdfLink}
            >
              View PDF
            </a>
          </div>
        </div>

        {paper.summary ? (
          <div className={styles.summary}>
            <h2>Summary</h2>
            <div className={styles.summaryContent}>
              {paper.summary.topic && (
                <div className={styles.topic}>
                  <h3>Topic</h3>
                  <p>{paper.summary.topic}</p>
                </div>
              )}
              {paper.summary.content && (
                <div
                  className={styles.contentText}
                  dangerouslySetInnerHTML={{
                    __html: formatContent(paper.summary.content),
                  }}
                />
              )}
            </div>
          </div>
        ) : (
          <div className={styles.noSummary}>
            <p>This paper has not been parsed yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}

