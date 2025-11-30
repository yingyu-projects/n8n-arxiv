'use client';

import { useWorkflowTrigger } from '@/hooks/useWorkflowTrigger';
import styles from './WorkflowTrigger.module.scss';

export default function WorkflowTrigger() {
  const {
    categories,
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
        />
      </div>

      <div className={styles.formSection}>
        <label>Summarize Prompt (optional)</label>
        <textarea
          value={summarizePrompt}
          onChange={(e) => setSummarizePrompt(e.target.value)}
          rows={5}
          placeholder="Leave empty to use default prompt"
        />
      </div>

      <button
        onClick={triggerWorkflow}
        disabled={loading}
        className={styles.triggerBtn}
      >
        {loading ? 'Processing...' : 'Trigger Workflow'}
      </button>

      {error && <div className={styles.error}>{error}</div>}

      {result && (
        <div className={styles.result}>
          <h3>Workflow Result</h3>
          <div className={styles.stats}>
            <div className={styles.stat}>
              <span className={styles.label}>Processed:</span>
              <span className={styles.value}>{result.processed}</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.label}>Skipped:</span>
              <span className={styles.value}>{result.skipped}</span>
            </div>
            {result.errors.length > 0 && (
              <div className={styles.stat}>
                <span className={styles.label}>Errors:</span>
                <span className={`${styles.value} ${styles.errorCount}`}>
                  {result.errors.length}
                </span>
              </div>
            )}
          </div>
          {result.errors.length > 0 && (
            <div className={styles.errors}>
              <h4>Errors:</h4>
              <ul>
                {result.errors.map((err: string, index: number) => (
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

