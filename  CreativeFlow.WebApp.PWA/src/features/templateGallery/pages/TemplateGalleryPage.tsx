import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useDocumentTitle } from '@/shared/hooks/useDocumentTitle';
import styles from './TemplateGalleryPage.module.css';
import { useTemplateStore } from '@/app/store';

// Placeholder components
const TemplateCard = ({ template }: { template: any }) => <div className={styles.templateCard}>{template.name}</div>;
const TemplateFilters = ({ onFilterChange }: { onFilterChange: (filters: any) => void }) => <div>Filters Placeholder</div>;
const TemplateSearchBar = ({ onSearch }: { onSearch: (term: string) => void }) => <div>Search Bar Placeholder</div>;
const InspirationGallerySection = () => <div>Inspiration Gallery Placeholder</div>;
const LoadingSpinner = () => <div>Loading...</div>;

/**
 * Displays a gallery of creative templates for users to browse, search, and filter.
 * Users can select a template to start a new creative project.
 *
 * @returns {React.ReactElement} The rendered template gallery page.
 */
const TemplateGalleryPage: React.FC = () => {
  const { t } = useTranslation('templates');
  useDocumentTitle(t('pageTitle'));

  const { templates, loading, error, fetchTemplates } = useTemplateStore((state) => ({
    templates: state.templates,
    loading: state.loading,
    error: state.error,
    fetchTemplates: state.fetchTemplates,
  }));

  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch templates when the component mounts or when filters/search change
    fetchTemplates({ ...filters, search: searchTerm });
  }, [filters, searchTerm, fetchTemplates]);

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
  };

  const handleSearch = (newSearchTerm: string) => {
    setSearchTerm(newSearchTerm);
  };

  return (
    <div className={styles.galleryContainer}>
      <header className={styles.header}>
        <h1 className={styles.title}>{t('title')}</h1>
        <p className={styles.subtitle}>{t('subtitle')}</p>
        <TemplateSearchBar onSearch={handleSearch} />
      </header>
      <div className={styles.mainContent}>
        <aside className={styles.filters}>
          <TemplateFilters onFilterChange={handleFilterChange} />
        </aside>
        <main className={styles.templateGridContainer}>
          {loading && <LoadingSpinner />}
          {error && <p className={styles.errorMessage}>{error}</p>}
          {!loading && !error && (
            <div className={styles.templateGrid}>
              {templates.map((template) => (
                <TemplateCard key={template.id} template={template} />
              ))}
            </div>
          )}
          {!loading && templates.length === 0 && !error && (
            <p className={styles.noResults}>{t('noTemplatesFound')}</p>
          )}
        </main>
      </div>
      <section className={styles.inspirationSection}>
        <InspirationGallerySection />
      </section>
    </div>
  );
};

export default TemplateGalleryPage;