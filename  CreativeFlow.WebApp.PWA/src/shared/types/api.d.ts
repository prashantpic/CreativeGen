/**
 * @file This file contains TypeScript declarations for all data transfer objects (DTOs)
 * used in API requests and responses. It serves as the contract between the frontend
 * and backend, ensuring type safety in all API interactions.
 *
 * These types are based on the database design and API specification.
 */

// --- Error ---
export interface ApiErrorResponse {
  message: string;
  errors?: Record<string, string[]>;
}

// --- Auth ---
export interface UserLoginRequest {
  email: string;
  password?: string;
  socialToken?: string; // For social logins
}

export interface UserLoginResponse {
  accessToken: string;
  refreshToken: string;
  user: UserProfile;
}

export interface UserRegistrationRequest {
  email: string;
  password?: string;
  fullName?: string;
  socialToken?: string;
}

// --- User & Profile ---
export interface UserProfile {
  id: string;
  email: string;
  fullName: string | null;
  username: string | null;
  profilePictureUrl: string | null;
  languagePreference: string;
  timezone: string;
  mfaEnabled: boolean;
  subscriptionTier: 'Free' | 'Pro' | 'Team' | 'Enterprise';
  creditBalance: number;
  createdAt: string;
  lastLoginAt: string | null;
}

export interface UpdateUserProfileRequest {
  fullName?: string;
  username?: string;
  languagePreference?: string;
  timezone?: string;
}

// --- Brand Kit ---
export interface BrandKitColor {
  name: string;
  hex: string;
}

export interface BrandKitFont {
  name: string;
  family: string;
  url?: string;
}

export interface BrandKitLogo {
  name: string;
  path: string; // MinIO path
  format: string;
}

export interface BrandKit {
  id: string;
  userId: string;
  name: string;
  colors: BrandKitColor[];
  fonts: BrandKitFont[];
  logos: BrandKitLogo[];
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
}

export type CreateBrandKitRequest = Omit<BrandKit, 'id' | 'userId' | 'createdAt' | 'updatedAt'>;
export type UpdateBrandKitRequest = Partial<CreateBrandKitRequest>;

// --- Workbench & Project ---
export interface Workbench {
  id: string;
  userId: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface Project {
  id: string;
  workbenchId: string;
  userId: string;
  name: string;
  targetPlatform: string | null;
  createdAt: string;
  updatedAt: string;
}

export type CreateProjectRequest = Omit<Project, 'id' | 'workbenchId' | 'userId' | 'createdAt' | 'updatedAt'> & { name: string };


// --- Asset ---
export interface Asset {
  id: string;
  projectId: string | null;
  userId: string;
  name: string;
  type: 'Uploaded' | 'AIGenerated' | 'Derived';
  filePath: string; // MinIO path
  mimeType: string;
  isFinal: boolean;
  metadata?: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export interface UploadAssetResponse {
  asset: Asset;
}

// --- AI Generation ---
export interface GenerationRequestPayload {
  projectId: string;
  inputPrompt: string;
  styleGuidance?: string;
  inputParameters?: {
    format?: string;
    resolution?: string;
    numSamples?: number;
  };
}

export interface GenerationStatusResponse {
  jobId: string;
  status: 'Pending' | 'ProcessingSamples' | 'AwaitingSelection' | 'ProcessingFinal' | 'Completed' | 'Failed' | 'Cancelled' | 'ContentRejected';
  progress?: number;
  errorMessage?: string;
}

export interface GenerationSample {
    id: string; // Asset ID of the sample
    url: string;
}

export interface GenerationSamplesResponse extends GenerationStatusResponse {
  samples?: GenerationSample[];
}

export interface SelectSampleRequest {
    jobId: string;
    selectedSampleId: string; // Asset ID of the selected sample
}

export interface GenerationFinalAssetResponse extends GenerationStatusResponse {
    finalAsset: Asset;
}

// --- Subscription & Billing ---
export interface SubscriptionDetails {
  planId: string;
  status: 'Active' | 'Trial' | 'Suspended' | 'Cancelled' | 'Expired';
  currentPeriodStart: string;
  currentPeriodEnd: string;
  paymentProvider: 'Stripe' | 'PayPal' | 'OdooManual';
}

export interface CreditBalance {
    balance: number;
}

// --- Developer Portal ---
export interface ApiKey {
    id: string;
    name: string;
    apiKey: string; // The key itself, only shown on creation
    createdAt: string;
    isActive: boolean;
}

export interface WebhookConfig {
    id: string;
    url: string;
    events: string[];
    isActive: boolean;
    createdAt: string;
}