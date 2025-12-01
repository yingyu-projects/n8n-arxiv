import { useState, useEffect, useCallback } from 'react';
import { projectService } from '@/api/projectService';
import type { ProjectPluginConfig } from '@/types/plugin';

export function useProjectPluginConfig(projectId: string | null | undefined) {
  const [configs, setConfigs] = useState<Map<string, ProjectPluginConfig>>(new Map());
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState<Map<string, boolean>>(new Map());
  const [error, setError] = useState<string | null>(null);

  const loadConfigs = useCallback(async () => {
    if (!projectId) {
      setConfigs(new Map());
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const allConfigs = await projectService.getProjectPluginConfigs(projectId);
      const configMap = new Map<string, ProjectPluginConfig>();
      allConfigs.forEach((config) => {
        configMap.set(config.plugin_id, config);
      });
      setConfigs(configMap);
    } catch (err: any) {
      setError(err.message || 'Failed to load plugin configs');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    loadConfigs();
  }, [loadConfigs]);

  const getConfig = useCallback(
    (pluginId: string): Record<string, any> | null => {
      const config = configs.get(pluginId);
      return config ? config.config : null;
    },
    [configs]
  );

  const saveConfig = useCallback(
    async (pluginId: string, config: Record<string, any>): Promise<void> => {
      if (!projectId) {
        throw new Error('Project ID is required');
      }

      setSaving((prev) => new Map(prev).set(pluginId, true));
      setError(null);
      try {
        const saved = await projectService.updateProjectPluginConfig(projectId, pluginId, config);
        setConfigs((prev) => {
          const updated = new Map(prev);
          updated.set(pluginId, saved);
          return updated;
        });
      } catch (err: any) {
        setError(err.message || 'Failed to save plugin config');
        throw err;
      } finally {
        setSaving((prev) => {
          const updated = new Map(prev);
          updated.set(pluginId, false);
          return updated;
        });
      }
    },
    [projectId]
  );

  const isSaving = useCallback(
    (pluginId: string): boolean => {
      return saving.get(pluginId) || false;
    },
    [saving]
  );

  return {
    configs,
    loading,
    error,
    getConfig,
    saveConfig,
    isSaving,
    reload: loadConfigs,
  };
}

