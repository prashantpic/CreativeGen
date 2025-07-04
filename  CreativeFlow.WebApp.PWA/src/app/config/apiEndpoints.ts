/**
 * A centralized configuration object for all backend API endpoints.
 * Using a frozen object prevents accidental modification at runtime and provides
 * a single source of truth for API paths, making them easier to manage and update.
 */
export const apiEndpoints = Object.freeze({
  // Authentication
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    socialLogin: (provider: 'google' | 'facebook' | 'apple') => `/auth/social-login/${provider}`,
    verifyEmail: '/auth/verify-email',
    requestPasswordReset: '/auth/password/request-reset',
    resetPassword: '/auth/password/reset',
    refreshToken: '/auth/token/refresh',
    setupMfa: '/auth/mfa/setup',
    verifyMfa: '/auth/mfa/verify',
  },

  // User Profile & Account
  user: {
    me: '/users/me',
    profile: '/users/me/profile',
    preferences: '/users/me/preferences',
    brandKits: '/users/me/brand-kits',
    brandKitById: (kitId: string) => `/users/me/brand-kits/${kitId}`,
    dataPortability: '/users/me/data-portability',
    consent: '/users/me/consent',
    activeSessions: '/users/me/sessions',
  },

  // Workbenches & Projects
  workbenches: {
    list: '/workbenches',
    create: '/workbenches',
    details: (id: string) => `/workbenches/${id}`,
    projects: (id: string) => `/workbenches/${id}/projects`,
  },
  projects: {
    create: '/projects',
    details: (id: string) => `/projects/${id}`,
    assets: (id: string) => `/projects/${id}/assets`,
  },

  // Assets
  assets: {
    list: '/assets',
    upload: '/assets',
    details: (id: string) => `/assets/${id}`,
    versions: (id: string) => `/assets/${id}/versions`,
  },

  // Templates
  templates: {
    list: '/templates',
    categories: '/templates/categories',
    userTemplates: '/users/me/templates',
    details: (id: string) => `/templates/${id}`,
  },

  // Creative Generation
  generation: {
    request: '/generate/request',
    status: (jobId: string) => `/generate/status/${jobId}`,
    samples: (jobId: string) => `/generate/samples/${jobId}`,
    select: '/generate/select',
  },

  // Subscription & Billing
  billing: {
    subscription: '/billing/subscription',
    credits: '/billing/credits',
    usage: '/billing/usage',
    createCheckoutSession: '/billing/create-checkout-session',
    portal: '/billing/portal',
  },

  // Developer Platform
  developer: {
    apiKeys: '/developer/api-keys',
    apiKeyById: (id: string) => `/developer/api-keys/${id}`,
    webhooks: '/developer/webhooks',
    webhookById: (id: string) => `/developer/webhooks/${id}`,
  },
  
  // Social Integrations
  social: {
    connect: (platform: string) => `/social/connect/${platform}`,
    connections: '/social/connections',
    publish: '/social/publish'
  }
});