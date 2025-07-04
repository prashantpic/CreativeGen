import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useDocumentTitle } from '@/shared/hooks/useDocumentTitle';
import styles from './DashboardPage.module.css';
import { useProjectStore, useSubscriptionStore, useTemplateStore } from '@/app/store';

// Assuming these components will be created later
const QuickActions = () => <div>Quick Actions Placeholder</div>;
const RecentItemsCard = () => <div>Recent Items Placeholder</div>;
const UsageStatsWidget = () => <div>Usage Stats Placeholder</div>;
const ProgressIndicatorsWidget = () => <div>Progress Indicators Placeholder</div>;
const PersonalizedTipsWidget = () => <div>Personalized Tips Placeholder</div>;

/**
 * The main dashboard page for authenticated users.
 * It serves as a central hub providing an overview of recent activity,
 * quick access to core features, and usage statistics. It fetches necessary
 * data from various state stores upon mounting.
 *
 * @returns {React.ReactElement} The rendered dashboard page.
 */
const DashboardPage: React.FC = () => {
  const { t } = useTranslation('dashboard');
  useDocumentTitle(t('pageTitle'));

  // Fetch necessary data on component mount
  const { fetchWorkbenches, fetchRecentProjects } = useProjectStore((state) => ({
    fetchWorkbenches: state.fetchWorkbenches,
    fetchRecentProjects: state.fetchProjects, // This should be a specific action for recent projects
  }));
  const { fetchSubscriptionDetails } = useSubscriptionStore((state) => ({
    fetchSubscriptionDetails: state.fetchSubscriptionDetails,
  }));
  const { fetchTemplates } = useTemplateStore((state) => ({
    fetchTemplates: state.fetchTemplates,
  }));

  useEffect(() => {
    // These fetches should ideally be optimized to avoid re-fetching on every visit
    // e.g., by checking if data already exists in the store.
    fetchWorkbenches();
    fetchRecentProjects(); // This needs a proper implementation in the store
    fetchSubscriptionDetails();
    fetchTemplates({ limit: 5, sort: 'trending' }); // Fetch trending templates for the dashboard
  }, [fetchWorkbenches, fetchRecentProjects, fetchSubscriptionDetails, fetchTemplates]);

  return (
    <div className={styles.dashboardContainer}>
      <header className={styles.header}>
        <h1 className={styles.title}>{t('title')}</h1>
        <div className={styles.headerActions}>
          <QuickActions />
        </div>
      </header>
      <main className={styles.mainGrid}>
        <section className={`${styles.gridItem} ${styles.recentItems}`}>
          <RecentItemsCard />
        </section>
        <aside className={styles.sidebar}>
          <div className={`${styles.gridItem} ${styles.usageStats}`}>
            <UsageStatsWidget />
          </div>
          <div className={`${styles.gridItem} ${styles.progressIndicators}`}>
            <ProgressIndicatorsWidget />
          </div>
          <div className={`${styles.gridItem} ${styles.tips}`}>
            <PersonalizedTipsWidget />
          </div>
        </aside>
      </main>
    </div>
  );
};

export default DashboardPage;