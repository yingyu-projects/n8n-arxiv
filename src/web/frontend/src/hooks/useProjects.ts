'use client';

import { useState, useEffect } from 'react';
import { projectService, CreateProjectRequest, UpdateProjectRequest } from '@/api/projectService';
import type { Project } from '@/types/project';

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const reload = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await projectService.getProjects();
      setProjects(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load projects'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    reload();
  }, []);

  const createProject = async (data: CreateProjectRequest) => {
    try {
      const newProject = await projectService.createProject(data);
      setProjects([newProject, ...projects]);
      return newProject;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create project'));
      throw err;
    }
  };

  const updateProject = async (id: string, data: UpdateProjectRequest) => {
    try {
      const updated = await projectService.updateProject(id, data);
      setProjects(projects.map(p => p.id === id ? updated : p));
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update project'));
      throw err;
    }
  };

  const deleteProject = async (id: string) => {
    try {
      await projectService.deleteProject(id);
      setProjects(projects.filter(p => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete project'));
      throw err;
    }
  };

  return {
    projects,
    loading,
    error,
    reload,
    createProject,
    updateProject,
    deleteProject,
  };
}

