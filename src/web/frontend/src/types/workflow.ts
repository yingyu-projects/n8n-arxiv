export interface Workflow {
  id: string;
  name: string;
  description: string | null;
  categories: string[];
  num_papers: number;
  enabled: boolean;
  project_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface WorkflowPluginConfig {
  id: string;
  workflow_id: string;
  plugin_id: string;
  enabled: boolean;
  config: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface WorkflowConfig {
  workflow: Workflow;
  plugin_configs: WorkflowPluginConfig[];
}

export interface CreateWorkflowRequest {
  name: string;
  categories: string[];
  num_papers: number;
  description?: string;
  project_id: string | null;
}

export interface UpdateWorkflowRequest {
  name?: string;
  description?: string;
  categories?: string[];
  num_papers?: number;
  enabled?: boolean;
}

export interface UpdateWorkflowConfigRequest {
  name?: string;
  description?: string;
  categories?: string[];
  num_papers?: number;
  enabled?: boolean;
  plugin_configs?: {
    plugin_id: string;
    enabled: boolean;
    config: Record<string, any>;
  }[];
}

