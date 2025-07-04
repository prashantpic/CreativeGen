import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuthStore } from '@/app/store';
import Input from '@/shared/components/atoms/Input';
import Button from '@/shared/components/atoms/Button';
import styles from './LoginForm.module.css';

interface LoginFormProps {
  onLoginSuccess: () => void;
}

/**
 * A form component for user email and password login.
 * It handles its own state for input fields, performs basic validation,
 * and calls the global authentication store's login action upon submission.
 *
 * @param {LoginFormProps} props - The component props.
 * @returns {React.ReactElement} The rendered login form.
 */
export const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess }) => {
  const { t } = useTranslation('auth');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');

  const login = useAuthStore((state) => state.login);
  const loading = useAuthStore((state) => state.loading);
  const apiError = useAuthStore((state) => state.error);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormError('');

    if (!email || !password) {
      setFormError(t('login.validation.allFieldsRequired'));
      return;
    }

    // Basic email format validation
    if (!/\S+@\S+\.\S+/.test(email)) {
      setFormError(t('login.validation.invalidEmail'));
      return;
    }

    try {
      await login({ email, password });
      // On success, the parent component (LoginPage) will handle redirection.
      onLoginSuccess();
    } catch (err) {
      // The error is already set in the authStore by the login action,
      // and it's displayed on the LoginPage.
      // We could set a local form error here if needed for more specific messages.
      console.error('Login failed:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form} noValidate>
      <div className={styles.inputGroup}>
        <Input
          id="email"
          name="email"
          type="email"
          label={t('login.emailLabel')}
          placeholder={t('login.emailPlaceholder')}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={loading}
          required
        />
      </div>
      <div className={styles.inputGroup}>
        <Input
          id="password"
          name="password"
          type="password"
          label={t('login.passwordLabel')}
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          required
        />
      </div>
      
      {formError && <p className={styles.formErrorMessage}>{formError}</p>}
      
      {/* API error from the store is displayed in the parent page */}

      <Button type="submit" variant="primary" fullWidth disabled={loading}>
        {loading ? t('login.loggingIn') : t('login.loginButton')}
      </Button>
    </form>
  );
};