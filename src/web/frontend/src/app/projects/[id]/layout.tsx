import ProjectSidebar from '@/components/ProjectSidebar/ProjectSidebar';
import styles from './layout.module.scss';

export default function ProjectLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.projectLayout}>
      <ProjectSidebar />
      <main className={styles.mainContent}>{children}</main>
    </div>
  );
}


