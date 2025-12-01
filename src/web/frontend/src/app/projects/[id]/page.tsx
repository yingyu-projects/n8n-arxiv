'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useProjectContext } from '@/hooks/useProjectContext';
import { workflowService } from '@/api/workflowService';
import { paperService } from '@/api/paperService';
import styles from './page.module.scss';

export default function ProjectDashboard() {
  const { projectId, project, loading: projectLoading } = useProjectContext();
  const [stats, setStats] = useState({
    papersCount: 0,
    workflowsCount: 0,
    loading: true,
  });

  useEffect(() => {
    if (!projectId) return;

    const loadStats = async () => {
      try {
        const [papers, workflows] = await Promise.all([
          paperService.getPapers(undefined, projectId, 100, 0),
          workflowService.getWorkflows(false, projectId),
        ]);
        setStats({
          papersCount: papers.length,
          workflowsCount: workflows.length,
          loading: false,
        });
      } catch (err) {
        console.error('Failed to load stats:', err);
        setStats(prev => ({ ...prev, loading: false }));
      }
    };

    loadStats();
  }, [projectId]);

  if (projectLoading || !project) {
    return <div className={styles.loading}>Loading project...</div>;
  }

  if (!projectId) {
    return <div className={styles.error}>Project not found</div>;
  }

  return (
    <div className={styles.dashboard}>
      <div className={styles.header}>
        <h1>{project.name}</h1>
        {project.description && <p className={styles.description}>{project.description}</p>}
      </div>

      <div className={styles.stats}>
        <div className={styles.statCard}>
          <div className={styles.statValue}>
            {stats.loading ? '...' : stats.papersCount}
          </div>
          <div className={styles.statLabel}>Papers</div>
          <Link href={`/projects/${projectId}/papers`} className={styles.statLink}>
            View Papers →
          </Link>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statValue}>
            {stats.loading ? '...' : stats.workflowsCount}
          </div>
          <div className={styles.statLabel}>Workflows</div>
          <Link href={`/projects/${projectId}/workflows`} className={styles.statLink}>
            View Workflows →
          </Link>
        </div>
      </div>

      <div className={styles.quickActions}>
        <h2>Quick Actions</h2>
        <div className={styles.actions}>
          <Link href={`/projects/${projectId}/papers`} className={styles.actionCard}>
            <h3>Papers</h3>
            <p>View and manage papers in this project</p>
          </Link>
          <Link href={`/projects/${projectId}/workflows`} className={styles.actionCard}>
            <h3>Workflows</h3>
            <p>Create and manage workflows</p>
          </Link>
          <Link href={`/projects/${projectId}/config`} className={styles.actionCard}>
            <h3>Config</h3>
            <p>Configure project settings</p>
          </Link>
        </div>
      </div>
    </div>
  );
}

