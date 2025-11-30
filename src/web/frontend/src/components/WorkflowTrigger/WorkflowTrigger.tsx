'use client';

import { useWorkflowTrigger } from '@/hooks/useWorkflowTrigger';
import styles from './WorkflowTrigger.module.scss';

export default function WorkflowTrigger() {
  const {
    categories,
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
  } = useWorkflowTrigger();

  return (
    <div className={styles.workflowTrigger}>
      <h2>Trigger Parsing Workflow</h2>

      <div className={styles.formSection}>
        <label>Categories</label>
        {categories.map((category, index) => (
          <div key={index} className={styles.categoryInputGroup}>
            <input
              value={category}
              onChange={(e) => updateCategory(index, e.target.value)}
              type="text"
              placeholder="e.g., cs.AI"
              className={styles.categoryInput}
            />
            <button
              onClick={() => removeCategory(index)}
              type="button"
              className={styles.removeBtn}
              disabled={categories.length === 1}
            >
              Remove
            </button>
          </div>
        ))}
        <button onClick={addCategory} type="button" className={styles.addBtn}>
          Add Category
        </button>
      </div>

      <div className={styles.formSection}>
        <label>Number of Papers</label>
        <input
          value={numPapers}
          onChange={(e) => setNumPapers(Number(e.target.value))}
          type="number"
          min="1"
          max="100"
          disabled={isRunning}
        />
      </div>

      <button
        onClick={isRunning ? stopWorkflow : triggerWorkflow}
        disabled={loading && !isRunning}
        className={`${styles.triggerBtn} ${isRunning ? styles.stopBtn : ''}`}
      >
        {isRunning ? 'Stop Workflow' : 'Trigger Workflow'}
      </button>

      {error && <div className={styles.error}>{error}</div>}

      {status && (
        <div className={styles.statusSection}>
          <h3>Workflow Status</h3>
          
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{
                width: status.total_papers > 0
                  ? `${(status.processed / status.total_papers) * 100}%`
                  : '0%',
              }}
            />
          </div>
          <div className={styles.progressText}>
            {status.processed} / {status.total_papers} papers processed
          </div>

          <div className={styles.stats}>
            <div className={styles.stat}>
              <span className={styles.label}>Status:</span>
              <span className={`${styles.value} ${styles[status.status]}`}>
                {status.status}
              </span>
            </div>
            <div className={styles.stat}>
              <span className={styles.label}>Total Papers:</span>
              <span className={styles.value}>{status.total_papers}</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.label}>Processed:</span>
              <span className={styles.value}>{status.processed}</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.label}>Skipped:</span>
              <span className={styles.value}>{status.skipped}</span>
            </div>
            {status.errors.length > 0 && (
              <div className={styles.stat}>
                <span className={styles.label}>Errors:</span>
                <span className={`${styles.value} ${styles.errorCount}`}>
                  {status.errors.length}
                </span>
              </div>
            )}
            {status.elapsed_time !== null && (
              <div className={styles.stat}>
                <span className={styles.label}>Elapsed Time:</span>
                <span className={styles.value}>
                  {Math.floor(status.elapsed_time)}s
                </span>
              </div>
            )}
          </div>

          {status.errors.length > 0 && (
            <div className={styles.errors}>
              <h4>Errors:</h4>
              <ul>
                {status.errors.map((err: string, index: number) => (
                  <li key={index}>{err}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

