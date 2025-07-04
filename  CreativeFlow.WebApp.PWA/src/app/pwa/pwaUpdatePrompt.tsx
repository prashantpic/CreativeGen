import React from 'react';
import { useRegisterSW } from 'vite-plugin-pwa/react';
import styles from './pwaUpdatePrompt.module.css';
import { useTranslation } from 'react-i18next';
import Button from '@/shared/components/atoms/Button';

/**
 * A UI component that prompts the user to update the application when a new version
 * of the PWA is available. It uses the `useRegisterSW` hook from `vite-plugin-pwa`
 * to detect updates and trigger the refresh.
 *
 * @returns {React.ReactElement | null} The rendered prompt component, or null if no update is available.
 */
const PwaUpdatePrompt: React.FC = () => {
  const { t } = useTranslation('common');
  const {
    offlineReady: [offlineReady, setOfflineReady],
    needRefresh: [needRefresh, setNeedRefresh],
    updateServiceWorker,
  } = useRegisterSW({
    onRegistered(r) {
      console.log('Service Worker registered:', r);
    },
    onRegisterError(error) {
      console.error('Service Worker registration error:', error);
    },
  });

  const close = () => {
    setOfflineReady(false);
    setNeedRefresh(false);
  };

  if (offlineReady) {
    return (
      <div className={styles.promptContainer} role="status">
        <div className={styles.message}>
          <span>{t('pwa.offlineReady')}</span>
        </div>
        <Button onClick={close} variant="secondary" size="sm">
          {t('pwa.close')}
        </Button>
      </div>
    );
  }

  if (needRefresh) {
    return (
      <div className={styles.promptContainer} role="alert">
        <div className={styles.message}>
          <span>{t('pwa.newContent')}</span>
        </div>
        <div className={styles.actions}>
          <Button onClick={() => updateServiceWorker(true)} variant="primary" size="sm">
            {t('pwa.reload')}
          </Button>
          <Button onClick={close} variant="secondary" size="sm">
            {t('pwa.close')}
          </Button>
        </div>
      </div>
    );
  }

  return null;
};

export default PwaUpdatePrompt;