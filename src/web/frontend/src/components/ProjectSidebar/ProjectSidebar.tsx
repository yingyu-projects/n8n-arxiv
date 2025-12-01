'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useProjectContext } from '@/hooks/useProjectContext';
import { HiHome, HiDocumentText, HiCog, HiCollection, HiPuzzle } from 'react-icons/hi';
import styles from './ProjectSidebar.module.scss';

export default function ProjectSidebar() {
  const pathname = usePathname();
  const { projectId, project } = useProjectContext();

  if (!projectId) {
    return null;
  }

  const basePath = `/projects/${projectId}`;

  // Dashboard should only be active on exact match
  const isDashboardActive = pathname === basePath;
  
  // Other items should be active on exact match or when pathname starts with their path
  const isActive = (path: string) => {
    return pathname === path || pathname?.startsWith(path + '/');
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.header}>
        <h2 className={styles.projectName}>{project?.name || 'Project'}</h2>
        {project?.description && (
          <p className={styles.projectDescription}>{project.description}</p>
        )}
      </div>
      <nav className={styles.nav}>
        <Link
          href={basePath}
          className={`${styles.navItem} ${isDashboardActive ? styles.active : ''}`}
        >
          <HiHome className={styles.icon} />
          Dashboard
        </Link>
        <Link
          href={`${basePath}/papers`}
          className={`${styles.navItem} ${isActive(`${basePath}/papers`) ? styles.active : ''}`}
        >
          <HiDocumentText className={styles.icon} />
          Papers
        </Link>
        <Link
          href={`${basePath}/workflows`}
          className={`${styles.navItem} ${isActive(`${basePath}/workflows`) ? styles.active : ''}`}
        >
          <HiCollection className={styles.icon} />
          Workflows
        </Link>
        <Link
          href={`${basePath}/extensions`}
          className={`${styles.navItem} ${isActive(`${basePath}/extensions`) ? styles.active : ''}`}
        >
          <HiPuzzle className={styles.icon} />
          Extensions
        </Link>
        <div className={styles.spacer}></div>
        <Link
          href={`${basePath}/config`}
          className={`${styles.navItem} ${styles.configItem} ${isActive(`${basePath}/config`) ? styles.active : ''}`}
        >
          <HiCog className={styles.icon} />
          Config
        </Link>
      </nav>
    </div>
  );
}

