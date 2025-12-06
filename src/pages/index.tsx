import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.bookCover}>
        <div className={styles.bookSpine}></div>
        <div className={styles.bookContent}>
          <div className={styles.bookTitle}>
            <Heading as="h1" className="hero__title">
              🤖 Physical AI & Humanoid Robotics Lab Textbook
            </Heading>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
          </div>
          <div className={styles.bookDetails}>
            <div className={styles.edition}>First Edition</div>
            <div className={styles.author}>By Muhammad Ali Shahid (codecraftali)</div>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs">
                📖 Start Reading
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
