import { useState, useEffect } from 'react';
import { pluginService } from '@/api/pluginService';
import type { Plugin, PluginType } from '@/types/plugin';

export function usePlugins(pluginType?: PluginType, enabledOnly: boolean = false) {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPlugins = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await pluginService.getPlugins(pluginType, enabledOnly);
      setPlugins(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load plugins');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlugins();
  }, [pluginType, enabledOnly]);

  const updatePlugin = async (id: string, enabled: boolean) => {
    try {
      const updated = await pluginService.updatePlugin(id, { enabled });
      setPlugins(prev => prev.map(p => p.id === id ? updated : p));
      return updated;
    } catch (err: any) {
      setError(err.message || 'Failed to update plugin');
      throw err;
    }
  };

  const discoverPlugins = async () => {
    try {
      await pluginService.discoverPlugins();
      await loadPlugins();
    } catch (err: any) {
      setError(err.message || 'Failed to discover plugins');
      throw err;
    }
  };

  return {
    plugins,
    loading,
    error,
    reload: loadPlugins,
    updatePlugin,
    discoverPlugins,
  };
}

