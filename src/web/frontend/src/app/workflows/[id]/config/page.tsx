'use client';

import { useParams, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { useWorkflowConfig } from '@/hooks/useWorkflowConfig';
import { usePlugins } from '@/hooks/usePlugins';
import { workflowService } from '@/api/workflowService';
import PluginStore from '@/components/PluginStore/PluginStore';
import styles from './WorkflowConfig.module.scss';

export default function WorkflowConfigPage() {
  const params = useParams();
  const router = useRouter();
  const workflowId = params.id as string;
  const { config, loading, saving, error, saveConfig } = useWorkflowConfig(workflowId);
  const { plugins } = usePlugins();
  const [showPluginStore, setShowPluginStore] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    categories: [] as string[],
    num_papers: 50,
    enabled: true,
  });

  useEffect(() => {
    if (config) {
      setFormData({
        name: config.workflow.name,
        description: config.workflow.description || '',
        categories: config.workflow.categories,
        num_papers: config.workflow.num_papers,
        enabled: config.workflow.enabled,
      });
    }
  }, [config]);

  const handleSave = async () => {
    try {
      await saveConfig({
        name: formData.name,
        description: formData.description || undefined,
        categories: formData.categories,
        num_papers: formData.num_papers,
        enabled: formData.enabled,
      });
      alert('Workflow configuration saved!');
    } catch (err) {
      // Error already handled in hook
    }
  };

  const handleAddPlugin = async (pluginId: string) => {
    try {
      await workflowService.addPluginToWorkflow(workflowId, pluginId, {}, true);
      setShowPluginStore(false);
      // Reload config
      window.location.reload();
    } catch (err: any) {
      alert(err.message || 'Failed to add plugin');
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading workflow configuration...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!config) {
    return <div className={styles.error}>Workflow not found</div>;
  }

  return (
    <div className={styles.workflowConfig}>
      <div className={styles.header}>
        <h2>Configure Workflow: {config.workflow.name}</h2>
        <button onClick={() => router.push('/workflows')} className={styles.backButton}>
          Back to Workflows
        </button>
      </div>

      <div className={styles.sections}>
        <div className={styles.section}>
          <h3>Basic Settings</h3>
          <div className={styles.formGroup}>
            <label>Name:</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className={styles.input}
            />
          </div>
          <div className={styles.formGroup}>
            <label>Description:</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className={styles.textarea}
            />
          </div>
          <div className={styles.formGroup}>
            <label>Categories:</label>
            {formData.categories.map((cat, idx) => (
              <input
                key={idx}
                type="text"
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
          <div className={styles.formGroup}>
            <label>Number of Papers:</label>
            <input
              type="number"
              value={formData.num_papers}
              onChange={(e) => setFormData({ ...formData, num_papers: parseInt(e.target.value) || 50 })}
              className={styles.input}
              min="1"
              max="100"
            />
          </div>
          <div className={styles.formGroup}>
            <label>
              <input
                type="checkbox"
                checked={formData.enabled}
                onChange={(e) => setFormData({ ...formData, enabled: e.target.checked })}
              />
              Enabled
            </label>
          </div>
          <button onClick={handleSave} disabled={saving} className={styles.saveButton}>
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>

        <div className={styles.section}>
          <div className={styles.pluginHeader}>
            <h3>Plugins</h3>
            <button
              onClick={() => setShowPluginStore(!showPluginStore)}
              className={styles.browseButton}
            >
              {showPluginStore ? 'Hide Plugin Store' : 'Browse Plugin Store'}
            </button>
          </div>

          {showPluginStore && (
            <div className={styles.pluginStoreContainer}>
              <PluginStore workflowId={workflowId} onAddPlugin={handleAddPlugin} />
            </div>
          )}

          <div className={styles.pluginsList}>
            {config.plugin_configs.length === 0 ? (
              <p>No plugins configured. Browse the plugin store to add plugins.</p>
            ) : (
              config.plugin_configs.map((pc) => {
                const plugin = plugins.find(p => p.id === pc.plugin_id);
                return (
                  <div key={pc.id} className={styles.pluginItem}>
                    <div className={styles.pluginInfo}>
                      <h4>{plugin?.name || 'Unknown Plugin'}</h4>
                      <span className={pc.enabled ? styles.enabled : styles.disabled}>
                        {pc.enabled ? 'Enabled' : 'Disabled'}
                      </span>
                    </div>
                    <button
                      onClick={async () => {
                        try {
                          await workflowService.removePluginFromWorkflow(workflowId, pc.plugin_id);
                          window.location.reload();
                        } catch (err: any) {
                          alert(err.message || 'Failed to remove plugin');
                        }
                      }}
                      className={styles.removeButton}
                    >
                      Remove
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

