import { useAuthStore } from '@/app/store';

/**
 * Custom hook for accessing and managing authentication state and actions.
 * This hook acts as a facade over the `useAuthStore`, abstracting the underlying
 * state management logic from the components that use it. It provides a clean,
 * concise API for authentication-related operations.
 *
 * @returns An object containing authentication status, user data, and action handlers.
 */
export const useAuth = () => {
  const {
    isAuthenticated,
    user,
    token,
    loading,
    error,
    mfaRequired,
    login,
    register,
    logout,
    verifyEmail,
    requestPasswordReset,
    resetPassword,
    handleMfa,
    refreshToken,
    loadUserFromToken,
  } = useAuthStore((state) => ({
    isAuthenticated: state.isAuthenticated,
    user: state.user,
    token: state.token,
    loading: state.loading,
    error: state.error,
    mfaRequired: state.mfaRequired,
    login: state.login,
    register: state.register,
    logout: state.logout,
    verifyEmail: state.verifyEmail,
    requestPasswordReset: state.requestPasswordReset,
    resetPassword: state.resetPassword,
    handleMfa: state.handleMfa,
    refreshToken: state.refreshToken,
    loadUserFromToken: state.loadUserFromToken,
  }));

  return {
    isAuthenticated,
    user,
    token,
    loading,
    error,
    mfaRequired,
    login,
    register,
    logout,
    verifyEmail,
    requestPasswordReset,
    resetPassword,
    handleMfa,
    refreshToken,
    loadUserFromToken,
  };
};