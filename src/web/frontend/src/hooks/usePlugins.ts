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

  return {
    plugins,
    loading,
    error,
    reload: loadPlugins,
  };
}

