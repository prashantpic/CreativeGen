import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { LoginForm } from '../components/LoginForm';
import SocialLoginButtons from '../components/SocialLoginButtons';
import styles from './AuthPages.module.css';
import { useAuthStore } from '@/app/store';
import { useDocumentTitle } from '@/shared/hooks/useDocumentTitle';

/**
 * The login page component.
 * It provides the main UI for users to authenticate with their credentials
 * or via social login providers. It orchestrates the LoginForm and
 * SocialLoginButtons components.
 *
 * @returns {React.ReactElement} The rendered login page.
 */
const LoginPage: React.FC = () => {
  const { t } = useTranslation('auth');
  useDocumentTitle(t('login.pageTitle'));
  const navigate = useNavigate();
  const location = useLocation();
  const { error } = useAuthStore((state) => ({ error: state.error }));

  const from = location.state?.from?.pathname || '/dashboard';

  const onLoginSuccess = () => {
    // Redirect to the page the user was trying to access, or to the dashboard.
    navigate(from, { replace: true });
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authFormWrapper}>
        <h1 className={styles.title}>{t('login.title')}</h1>
        <p className={styles.subtitle}>
          {t('login.subtitle')}{' '}
          <Link to="/register" className={styles.link}>
            {t('login.createAccountLink')}
          </Link>
        </p>
        
        {error && <p className={styles.errorMessage}>{error}</p>}

        <LoginForm onLoginSuccess={onLoginSuccess} />

        <div className={styles.divider}>
          <span>{t('common.or')}</span>
        </div>

        <SocialLoginButtons />

        <div className={styles.footerLinks}>
          <Link to="/forgot-password" className={styles.link}>
            {t('login.forgotPasswordLink')}
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;