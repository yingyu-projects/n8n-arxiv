'use client';

import { useWorkflowTrigger } from '@/hooks/useWorkflowTrigger';
import styles from './WorkflowTrigger.module.scss';

export default function WorkflowTrigger() {
  const {
    workflows,
    selectedWorkflowId,
    setSelectedWorkflowId,
    loading,
    status,
    error,
    isRunning,
    triggerWorkflow,
    stopWorkflow,
  } = useWorkflowTrigger();

  const selectedWorkflow = workflows.find(w => w.id === selectedWorkflowId);

  return (
    <div className={styles.workflowTrigger}>
      <h2>Trigger Parsing Workflow</h2>

      <div className={styles.formSection}>
        <label>Select Workflow</label>
        <select
          value={selectedWorkflowId}
          onChange={(e) => setSelectedWorkflowId(e.target.value)}
          disabled={isRunning}
          className={styles.select}
        >
          <option value="">-- Select a workflow --</option>
          {workflows.map((workflow) => (
            <option key={workflow.id} value={workflow.id}>
              {workflow.name} ({workflow.categories.join(', ')}) - {workflow.num_papers} papers
            </option>
          ))}
        </select>
        {selectedWorkflow && (
          <div className={styles.workflowInfo}>
            <p><strong>Description:</strong> {selectedWorkflow.description || 'No description'}</p>
            <p><strong>Categories:</strong> {selectedWorkflow.categories.join(', ')}</p>
            <p><strong>Papers per category:</strong> {selectedWorkflow.num_papers}</p>
          </div>
        )}
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

