import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpApi from 'i18next-http-backend';

/**
 * Initializes and configures the i18next library for internationalization (i18n).
 *
 * This setup includes:
 * - `HttpApi`: A backend plugin to load translation files from a server.
 * - `LanguageDetector`: A plugin to automatically detect the user's language from
 *   the browser (e.g., from `localStorage`, `navigator`).
 * - `initReactI18next`: A plugin that passes the i18n instance down to React components
 *   using React Context, enabling the use of hooks like `useTranslation`.
 *
 * The configuration specifies supported languages, a fallback language, and paths
 * for loading translation resources.
 */
i18n
  .use(HttpApi)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    // Languages required by PLI-001 to PLI-007
    supportedLngs: ['en-US', 'en-GB', 'es-ES', 'es-MX', 'fr-FR', 'de-DE'],
    fallbackLng: 'en-US',
    
    // Set debug to true in development for console logs
    debug: import.meta.env.DEV,

    // Language detection options
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag', 'path', 'subdomain'],
      caches: ['localStorage'],
    },

    // Backend options for loading translation files
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    // React-i18next specific options
    react: {
      useSuspense: true, // Recommended for modern React apps
    },

    interpolation: {
      escapeValue: false, // React already protects from XSS
    },
  });

export default i18n;