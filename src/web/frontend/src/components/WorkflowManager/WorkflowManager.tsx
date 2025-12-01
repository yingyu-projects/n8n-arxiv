'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useWorkflows } from '@/hooks/useWorkflows';
import { useProjectContext } from '@/hooks/useProjectContext';
import { workflowService } from '@/api/workflowService';
import styles from './WorkflowManager.module.scss';

export default function WorkflowManager() {
  const router = useRouter();
  const { projectId } = useProjectContext();
  const { workflows, loading, error, reload } = useWorkflows(false, projectId || undefined);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    categories: [''],
    num_papers: 50,
  });

  const handleCreate = async () => {
    if (!projectId) {
      alert('Project ID is required');
      return;
    }
    setCreating(true);
    try {
      const categories = formData.categories.filter(c => c.trim() !== '');
      await workflowService.createWorkflow({
        name: formData.name,
        description: formData.description || undefined,
        categories,
        num_papers: formData.num_papers,
        project_id: projectId,
      });
      setShowCreateForm(false);
      setFormData({ name: '', description: '', categories: [''], num_papers: 50 });
      reload();
    } catch (err: any) {
      alert(err.message || 'Failed to create workflow');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this workflow?')) return;
    try {
      await workflowService.deleteWorkflow(id);
      reload();
    } catch (err: any) {
      alert(err.message || 'Failed to delete workflow');
    }
  };

  const handleToggleEnabled = async (id: string, enabled: boolean) => {
    try {
      await workflowService.updateWorkflow(id, { enabled: !enabled });
      reload();
    } catch (err: any) {
      alert(err.message || 'Failed to update workflow');
    }
  };

  return (
    <div className={styles.workflowManager}>
      <div className={styles.header}>
        <h2>Workflows</h2>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className={styles.createButton}
        >
          {showCreateForm ? 'Cancel' : 'Create Workflow'}
        </button>
      </div>

      {!projectId && (
        <div className={styles.error}>Project ID is required. Please navigate to a project first.</div>
      )}

      {showCreateForm && (
        <div className={styles.createForm}>
          <h3>Create New Workflow</h3>
          <input
            type="text"
            placeholder="Workflow name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className={styles.input}
          />
          <textarea
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className={styles.textarea}
          />
          <div className={styles.categories}>
            <label>Categories:</label>
            {formData.categories.map((cat, idx) => (
              <input
                key={idx}
                type="text"
                placeholder="e.g., cs.AI"
                value={cat}
                onChange={(e) => {
                  const newCategories = [...formData.categories];
                  newCategories[idx] = e.target.value;
                  setFormData({ ...formData, categories: newCategories });
                }}
                className={styles.input}
              />
            ))}
            <button
              onClick={() => setFormData({ ...formData, categories: [...formData.categories, ''] })}
              className={styles.addButton}
            >
              Add Category
            </button>
          </div>
          <input
            type="number"
            placeholder="Number of papers"
            value={formData.num_papers}
            onChange={(e) => setFormData({ ...formData, num_papers: parseInt(e.target.value) || 50 })}
            className={styles.input}
            min="1"
            max="100"
          />
          <button onClick={handleCreate} disabled={creating || !projectId} className={styles.submitButton}>
            {creating ? 'Creating...' : 'Create'}
          </button>
        </div>
      )}

      {loading && <div className={styles.loading}>Loading workflows...</div>}
      {error && <div className={styles.error}>{error}</div>}

      {!loading && !error && workflows.length === 0 && (
        <div className={styles.empty}>No workflows found. Create one to get started.</div>
      )}

      {!loading && !error && workflows.length > 0 && (
        <div className={styles.workflows}>
          {workflows.map((workflow) => (
            <div key={workflow.id} className={styles.workflowItem}>
              <div className={styles.workflowInfo}>
                <h3>{workflow.name}</h3>
                {workflow.description && <p>{workflow.description}</p>}
                <div className={styles.meta}>
                  <span>Categories: {workflow.categories.join(', ')}</span>
                  <span>Papers: {workflow.num_papers}</span>
                  <span className={workflow.enabled ? styles.enabled : styles.disabled}>
                    {workflow.enabled ? 'Enabled' : 'Disabled'}
                  </span>
                </div>
              </div>
              <div className={styles.actions}>
                <button
                  onClick={() => router.push(`/workflows/${workflow.id}/config`)}
                  className={styles.configButton}
                >
                  Configure
                </button>
                <button
                  onClick={() => handleToggleEnabled(workflow.id, workflow.enabled)}
                  className={styles.toggleButton}
                >
                  {workflow.enabled ? 'Disable' : 'Enable'}
                </button>
                <button
                  onClick={() => handleDelete(workflow.id)}
                  className={styles.deleteButton}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

