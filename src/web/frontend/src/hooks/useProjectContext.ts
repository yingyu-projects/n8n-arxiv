'use client';

import { useParams } from 'next/navigation';
import { useProject } from './useProject';

export function useProjectContext() {
  const params = useParams();
  const projectId = params?.id as string | undefined;
  const { project, loading, error } = useProject(projectId || null);

  return {
    projectId,
    project,
    loading,
    error,
  };
}

