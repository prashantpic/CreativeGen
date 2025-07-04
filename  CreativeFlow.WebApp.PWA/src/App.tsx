import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import i18n from './app/i18n';
import AppRouter from './app/router';
import { ThemeProvider } from './app/theme/ThemeProvider';
import { NotificationContainer } from './shared/components/molecules/NotificationToast';

/**
 * The root component of the application.
 * It sets up all the global context providers that are needed across the app,
 * such as the theme, internationalization (i18n), and routing.
 *
 * @returns {React.ReactElement} The rendered App component.
 */
function App(): React.ReactElement {
  return (
    <I18nextProvider i18n={i18n}>
      <ThemeProvider>
        <BrowserRouter>
          <AppRouter />
          <NotificationContainer />
        </BrowserRouter>
      </ThemeProvider>
    </I18nextProvider>
  );
}

export default App;