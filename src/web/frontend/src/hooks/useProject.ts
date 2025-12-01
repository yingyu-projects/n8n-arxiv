'use client';

import { useState, useEffect } from 'react';
import { projectService, UpdateProjectRequest } from '@/api/projectService';
import type { Project } from '@/types/project';

export function useProject(id: string | null) {
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!id) {
      setProject(null);
      setLoading(false);
      return;
    }

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await projectService.getProject(id);
        setProject(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to load project'));
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [id]);

  const updateProject = async (data: UpdateProjectRequest) => {
    if (!id) throw new Error('Project ID is required');
    try {
      const updated = await projectService.updateProject(id, data);
      setProject(updated);
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update project'));
      throw err;
    }
  };

  const deleteProject = async () => {
    if (!id) throw new Error('Project ID is required');
    await projectService.deleteProject(id);
  };

  return {
    project,
    loading,
    error,
    updateProject,
    deleteProject,
  };
}

