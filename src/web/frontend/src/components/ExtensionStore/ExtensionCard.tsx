'use client';

import { useState } from 'react';
import type { Plugin } from '@/types/plugin';
import styles from './ExtensionCard.module.scss';

interface ExtensionCardProps {
  plugin: Plugin;
  onToggle: (id: string, enabled: boolean) => Promise<void>;
}

export default function ExtensionCard({ plugin, onToggle }: ExtensionCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [toggling, setToggling] = useState(false);

  const handleToggle = async () => {
    setToggling(true);
    try {
      await onToggle(plugin.id, !plugin.enabled);
    } catch (err) {
      console.error('Failed to toggle plugin:', err);
    } finally {
      setToggling(false);
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'output':
        return styles.typeOutput;
      case 'input':
        return styles.typeInput;
      case 'processing':
        return styles.typeProcessing;
      default:
        return '';
    }
  };

  const description = plugin.metadata?.description || plugin.metadata?.summary || 'No description available';

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h3 className={styles.name}>{plugin.name}</h3>
          <span className={`${styles.typeBadge} ${getTypeColor(plugin.type)}`}>
            {plugin.type}
          </span>
        </div>
        <span className={styles.version}>v{plugin.version}</span>
      </div>

      <p className={styles.description}>{description}</p>

      <div className={styles.footer}>
        <div className={styles.status}>
          <span className={plugin.enabled ? styles.enabled : styles.disabled}>
            {plugin.enabled ? 'Enabled' : 'Disabled'}
          </span>
        </div>
        <div className={styles.actions}>
          <button
            onClick={handleToggle}
            disabled={toggling}
            className={`${styles.toggleButton} ${plugin.enabled ? styles.disableButton : styles.enableButton}`}
          >
            {toggling ? '...' : plugin.enabled ? 'Disable' : 'Enable'}
          </button>
          <button
            onClick={() => setExpanded(!expanded)}
            className={styles.detailsButton}
          >
            {expanded ? 'Hide Details' : 'View Details'}
          </button>
        </div>
      </div>

      {expanded && (
        <div className={styles.details}>
          <div className={styles.detailsSection}>
            <h4>Configuration Schema</h4>
            <pre className={styles.schema}>
              {JSON.stringify(plugin.config_schema, null, 2)}
            </pre>
          </div>
          {Object.keys(plugin.metadata || {}).length > 0 && (
            <div className={styles.detailsSection}>
              <h4>Metadata</h4>
              <pre className={styles.metadata}>
                {JSON.stringify(plugin.metadata, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}


