import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/app/store';

/**
 * A route guard component that protects routes requiring user authentication.
 * It checks the authentication status from the global `useAuthStore`.
 * If the user is authenticated, it renders the nested child routes (`<Outlet />`).
 * If not, it redirects the user to the login page, preserving the intended destination
 * for redirection after a successful login.
 *
 * @returns {React.ReactElement} Either the child routes or a redirect to the login page.
 */
const ProtectedRoutes: React.FC = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to. This allows us to send them along to that page after they
    // log in, which is a nicer user experience than dropping them off on the home page.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated, render the nested routes.
  return <Outlet />;
};

export default ProtectedRoutes;