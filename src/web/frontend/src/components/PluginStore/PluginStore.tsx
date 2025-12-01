'use client';

import { useState } from 'react';
import { usePlugins } from '@/hooks/usePlugins';
import { pluginService } from '@/api/pluginService';
import type { PluginType } from '@/types/plugin';
import styles from './PluginStore.module.scss';

interface PluginStoreProps {
  workflowId?: string;
  onAddPlugin?: (pluginId: string) => void;
}

export default function PluginStore({ workflowId, onAddPlugin }: PluginStoreProps) {
  const [selectedType, setSelectedType] = useState<PluginType | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState('');
  const { plugins, loading, error, reload } = usePlugins(selectedType);

  const filteredPlugins = plugins.filter(plugin =>
    plugin.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleDiscover = async () => {
    try {
      await pluginService.discoverPlugins();
      reload();
      alert('Plugins discovered successfully!');
    } catch (err: any) {
      alert(err.message || 'Failed to discover plugins');
    }
  };

  return (
    <div className={styles.pluginStore}>
      <div className={styles.header}>
        <h2>Plugin Store</h2>
        <button onClick={handleDiscover} className={styles.discoverButton}>
          Discover Plugins
        </button>
      </div>

      <div className={styles.filters}>
        <input
          type="text"
          placeholder="Search plugins..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className={styles.searchInput}
        />
        <select
          value={selectedType || ''}
          onChange={(e) => setSelectedType(e.target.value as PluginType || undefined)}
          className={styles.typeFilter}
        >
          <option value="">All Types</option>
          <option value="output">Output</option>
          <option value="input">Input</option>
          <option value="processing">Processing</option>
        </select>
      </div>

      {loading && <div className={styles.loading}>Loading plugins...</div>}
      {error && <div className={styles.error}>{error}</div>}

      {!loading && !error && filteredPlugins.length === 0 && (
        <div className={styles.empty}>No plugins found.</div>
      )}

      {!loading && !error && filteredPlugins.length > 0 && (
        <div className={styles.plugins}>
          {filteredPlugins.map((plugin) => (
            <div key={plugin.id} className={styles.pluginCard}>
              <div className={styles.pluginHeader}>
                <h3>{plugin.name}</h3>
                <span className={styles.pluginType}>{plugin.type}</span>
              </div>
              <div className={styles.pluginMeta}>
                <span>Version: {plugin.version}</span>
                {plugin.metadata.description && (
                  <p>{plugin.metadata.description}</p>
                )}
              </div>
              {workflowId && onAddPlugin && (
                <button
                  onClick={() => onAddPlugin(plugin.id)}
                  className={styles.addButton}
                >
                  Add to Workflow
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

