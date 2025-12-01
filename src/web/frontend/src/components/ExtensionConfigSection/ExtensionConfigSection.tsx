'use client';

import { useState, useEffect } from 'react';
import type { Plugin } from '@/types/plugin';
import PluginConfigForm from '@/components/PluginConfigForm/PluginConfigForm';
import styles from './ExtensionConfigSection.module.scss';

interface ExtensionConfigSectionProps {
  plugin: Plugin;
  initialConfig?: Record<string, any>;
  onSave: (config: Record<string, any>) => Promise<void>;
  saving?: boolean;
  error?: string | null;
}

export default function ExtensionConfigSection({
  plugin,
  initialConfig = {},
  onSave,
  saving = false,
  error: externalError = null,
}: ExtensionConfigSectionProps) {
  const [expanded, setExpanded] = useState(false);
  const [config, setConfig] = useState<Record<string, any>>(initialConfig);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    setConfig(initialConfig);
  }, [initialConfig]);

  const validateConfig = (): boolean => {
    const schema = plugin.config_schema;
    const properties = schema.properties || {};
    const required = schema.required || [];
    const newErrors: Record<string, string> = {};

    required.forEach((key: string) => {
      const value = config[key];
      if (value === undefined || value === null || value === '') {
        const prop = properties[key];
        const title = prop?.title || key;
        newErrors[key] = `${title} is required`;
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    setSaveError(null);
    if (!validateConfig()) {
      return;
    }

    try {
      await onSave(config);
    } catch (err: any) {
      setSaveError(err.message || 'Failed to save configuration');
    }
  };

  const description = plugin.metadata?.description || plugin.metadata?.summary || 'No description available';

  return (
    <div className={styles.section}>
      <div className={styles.header} onClick={() => setExpanded(!expanded)}>
        <div className={styles.headerContent}>
          <h3 className={styles.title}>{plugin.name}</h3>
          <span className={styles.version}>v{plugin.version}</span>
        </div>
        <button
          type="button"
          className={styles.expandButton}
          aria-expanded={expanded}
        >
          {expanded ? '−' : '+'}
        </button>
      </div>

      {expanded && (
        <div className={styles.content}>
          <p className={styles.description}>{description}</p>

          <PluginConfigForm
            schema={plugin.config_schema}
            initialValues={config}
            onChange={setConfig}
            errors={errors}
          />

          {(saveError || externalError) && (
            <div className={styles.error}>
              {saveError || externalError}
            </div>
          )}

          <div className={styles.actions}>
            <button
              type="button"
              onClick={handleSave}
              disabled={saving}
              className={styles.saveButton}
            >
              {saving ? 'Saving...' : 'Save Configuration'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

