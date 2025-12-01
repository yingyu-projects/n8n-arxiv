export type PluginType = 'output' | 'input' | 'processing';

export interface Plugin {
  id: string;
  name: string;
  type: PluginType;
  version: string;
  config_schema: Record<string, any>;
  enabled: boolean;
  metadata: Record<string, any>;
}

export interface PluginConfigSchema {
  schema: Record<string, any>;
}

