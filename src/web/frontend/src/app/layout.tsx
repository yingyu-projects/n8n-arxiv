import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.scss';
import styles from './layout.module.scss';

export const metadata: Metadata = {
  title: 'arXiv Parser',
  description: 'Parse and summarize arXiv papers',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div id="app">
          <nav className={styles.navbar}>
            <div className={styles.container}>
              <h1 className={styles.logo}>
                <Link href="/">arXiv Parser</Link>
              </h1>
              <ul className={styles.navLinks}>
                <li>
                  <Link href="/">Papers</Link>
                </li>
                <li>
                  <Link href="/workflow">Workflow</Link>
                </li>
                <li>
                  <Link href="/config">Config</Link>
                </li>
              </ul>
            </div>
          </nav>
          <main className={styles.mainContent}>{children}</main>
        </div>
      </body>
    </html>
  );
}
