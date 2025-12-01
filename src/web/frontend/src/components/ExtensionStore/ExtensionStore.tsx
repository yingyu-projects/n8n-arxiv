'use client';

import { useState, useMemo } from 'react';
import { usePlugins } from '@/hooks/usePlugins';
import type { PluginType } from '@/types/plugin';
import ExtensionCard from './ExtensionCard';
import styles from './ExtensionStore.module.scss';

export default function ExtensionStore() {
  const [selectedType, setSelectedType] = useState<PluginType | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState('');
  const { plugins, loading, error, reload, updatePlugin, discoverPlugins } = usePlugins();

  const [discovering, setDiscovering] = useState(false);

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      await discoverPlugins();
    } catch (err) {
      console.error('Failed to discover plugins:', err);
    } finally {
      setDiscovering(false);
    }
  };

  const filteredPlugins = useMemo(() => {
    let filtered = plugins;

    if (selectedType) {
      filtered = filtered.filter(p => p.type === selectedType);
    }

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(query) ||
        (p.metadata?.description && p.metadata.description.toLowerCase().includes(query)) ||
        (p.metadata?.summary && p.metadata.summary.toLowerCase().includes(query))
      );
    }

    return filtered;
  }, [plugins, selectedType, searchQuery]);

  const handleToggle = async (id: string, enabled: boolean) => {
    await updatePlugin(id, enabled);
  };

  return (
    <div className={styles.extensionStore}>
      <div className={styles.header}>
        <h2>Extension Store</h2>
        <button
          onClick={handleDiscover}
          disabled={discovering}
          className={styles.refreshButton}
        >
          {discovering ? 'Discovering...' : 'Discover Plugins'}
        </button>
      </div>

      <div className={styles.filters}>
        <div className={styles.searchSection}>
          <input
            type="text"
            placeholder="Search extensions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
        </div>

        <div className={styles.typeFilters}>
          <button
            onClick={() => setSelectedType(undefined)}
            className={`${styles.filterButton} ${selectedType === undefined ? styles.active : ''}`}
          >
            All
          </button>
          <button
            onClick={() => setSelectedType('output')}
            className={`${styles.filterButton} ${selectedType === 'output' ? styles.active : ''}`}
          >
            Output
          </button>
          <button
            onClick={() => setSelectedType('input')}
            className={`${styles.filterButton} ${selectedType === 'input' ? styles.active : ''}`}
          >
            Input
          </button>
          <button
            onClick={() => setSelectedType('processing')}
            className={`${styles.filterButton} ${selectedType === 'processing' ? styles.active : ''}`}
          >
            Processing
          </button>
        </div>
      </div>

      {loading && <div className={styles.loading}>Loading extensions...</div>}
      {error && <div className={styles.error}>{error}</div>}

      {!loading && !error && filteredPlugins.length === 0 && (
        <div className={styles.empty}>
          {plugins.length === 0
            ? 'No extensions found. Click "Discover Plugins" to scan for available extensions.'
            : 'No extensions match your filters.'}
        </div>
      )}

      {!loading && !error && filteredPlugins.length > 0 && (
        <>
          <div className={styles.count}>
            Showing {filteredPlugins.length} of {plugins.length} extension{plugins.length !== 1 ? 's' : ''}
          </div>
          <div className={styles.grid}>
            {filteredPlugins.map((plugin) => (
              <ExtensionCard
                key={plugin.id}
                plugin={plugin}
                onToggle={handleToggle}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

