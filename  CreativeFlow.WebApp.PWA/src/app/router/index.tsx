import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoutes from './ProtectedRoutes';
import AppLayout from '@/shared/components/layouts/AppLayout';
import PublicLayout from '@/shared/components/layouts/PublicLayout';
import FullPageSpinner from '@/shared/components/molecules/FullPageSpinner';

// Lazy load page components for better code splitting and initial load performance.
const LoginPage = lazy(() => import('@/features/auth/pages/LoginPage'));
const RegisterPage = lazy(() => import('@/features/auth/pages/RegisterPage'));
const EmailVerificationPage = lazy(() => import('@/features/auth/pages/EmailVerificationPage'));
const ForgotPasswordPage = lazy(() => import('@/features/auth/pages/ForgotPasswordPage'));
const ResetPasswordPage = lazy(() => import('@/features/auth/pages/ResetPasswordPage'));

const DashboardPage = lazy(() => import('@/features/dashboard/pages/DashboardPage'));
const ProfilePage = lazy(() => import('@/features/profile/pages/ProfilePage'));
const CreativeEditorPage = lazy(() => import('@/features/creativeEditor/pages/CreativeEditorPage'));
const TemplateGalleryPage = lazy(() => import('@/features/templateGallery/pages/TemplateGalleryPage'));
const WorkbenchListPage = lazy(() => import('@/features/workbench/pages/WorkbenchListPage'));
const ProjectListPage = lazy(() => import('@/features/project/pages/ProjectListPage'));
const DeveloperPortalPage = lazy(() => import('@/features/developer/pages/DeveloperPortalPage'));

const NotFoundPage = lazy(() => import('@/shared/components/pages/NotFoundPage'));

/**
 * Defines the main routing configuration for the application.
 * It uses React Router to handle client-side navigation, separating routes
 * into public (e.g., login, register) and protected (e.g., dashboard, editor) sections.
 *
 * @returns {React.ReactElement} The rendered router component.
 */
const AppRouter: React.FC = () => {
  return (
    <Suspense fallback={<FullPageSpinner />}>
      <Routes>
        {/* Public Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/verify-email" element={<EmailVerificationPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
        </Route>

        {/* Protected Routes */}
        <Route element={<ProtectedRoutes />}>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/profile/*" element={<ProfilePage />} />
            <Route path="/editor/:assetId?" element={<CreativeEditorPage />} />
            <Route path="/templates" element={<TemplateGalleryPage />} />
            <Route path="/workbenches" element={<WorkbenchListPage />} />
            <Route path="/workbenches/:workbenchId/projects" element={<ProjectListPage />} />
            <Route path="/developer/*" element={<DeveloperPortalPage />} />
          </Route>
        </Route>

        {/* Not Found Route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
};

export default AppRouter;