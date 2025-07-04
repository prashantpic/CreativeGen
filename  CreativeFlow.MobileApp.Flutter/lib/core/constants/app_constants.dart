import 'package:flutter/material.dart';

/// Defines globally used constant values to avoid magic numbers and strings,
/// ensuring consistency and maintainability across the application.
class AppConstants {
  // Private constructor to prevent instantiation of this class.
  AppConstants._();

  // --- UI & Animation Constants ---

  /// Default padding value used throughout the app (e.g., for containers, screens).
  static const double defaultPadding = 16.0;

  /// Default border radius for elements like cards and buttons.
  static const double defaultBorderRadius = 8.0;

  /// Duration for short, subtle animations (e.g., fade-in, button taps).
  static const Duration shortAnimationDuration = Duration(milliseconds: 300);

  /// Duration for longer animations (e.g., screen transitions, dialog pop-ups).
  static const Duration longAnimationDuration = Duration(milliseconds: 600);


  // --- Feature-Specific Constants ---

  /// The maximum number of projects that can be stored locally for offline access.
  /// Requirement: REQ-019
  static const int maxOfflineProjects = 10;
  
  /// The maximum size for an image upload in bytes (10 MB).
  static const int maxImageUploadSizeBytes = 10 * 1024 * 1024;


  // --- Local Storage & Preferences Keys ---

  /// Key for storing the selected theme (e.g., 'light', 'dark', 'system') in SharedPreferences.
  static const String prefKeyTheme = 'app_theme';

  /// Key for storing the selected locale (e.g., 'en', 'es') in SharedPreferences.
  static const String prefKeyLocale = 'app_locale';

  /// Key for storing the user's ID in SharedPreferences or Secure Storage.
  static const String prefKeyUserId = 'user_id';

  /// Key for storing the authentication JWT in Secure Storage.
  static const String prefKeyAuthToken = 'auth_token';

  /// Key for storing the refresh token in Secure Storage.
  static const String prefKeyRefreshToken = 'refresh_token';


  // --- Database Constants ---

  /// The current version of the local SQLite database schema.
  /// Increment this value when the schema changes to trigger a migration.
  static const int localDbVersion = 1;

  /// The filename for the local SQLite database.
  static const String localDbName = 'creative_flow_local.db';


  // --- Network Constants ---

  /// Default timeout for API requests in milliseconds (30 seconds).
  static const int defaultApiTimeoutMs = 30000;
}