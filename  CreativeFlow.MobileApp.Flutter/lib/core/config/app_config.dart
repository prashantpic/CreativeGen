import 'package:flutter/foundation.dart';

/// Provides centralized access to application configuration values.
///
/// This class loads environment-specific settings and feature flags
/// at startup, ensuring that the application behaves correctly in
/// different environments (dev, staging, prod).
class AppConfig {
  // Private constructor to prevent instantiation.
  AppConfig._();

  // --- Environment ---
  static late final String _environmentName;
  static String get environmentName => _environmentName;

  // --- API Configuration ---
  static late final String _apiBaseUrl;
  static String get apiBaseUrl => _apiBaseUrl;

  // --- Feature Flags ---
  static late final bool _enableOfflineMode;
  static bool get enableOfflineMode => _enableOfflineMode;

  static late final bool _enableCollaborationFeatures;
  static bool get enableCollaborationFeatures => _enableCollaborationFeatures;

  static late final bool _enableVoiceInput;
  static bool get enableVoiceInput => _enableVoiceInput;

  static late final bool _enableAdvancedAnalyticsTracking;
  static bool get enableAdvancedAnalyticsTracking => _enableAdvancedAnalyticsTracking;

  // --- Firebase Configuration (Loaded from environment) ---
  // These should be set using --dart-define at build time.
  // Example: flutter run --dart-define=FIREBASE_API_KEY_ANDROID=...
  static const String firebaseApiKeyAndroid = String.fromEnvironment('FIREBASE_API_KEY_ANDROID');
  static const String firebaseAppIdAndroid = String.fromEnvironment('FIREBASE_APP_ID_ANDROID');
  static const String firebaseMessagingSenderIdAndroid = String.fromEnvironment('FIREBASE_MESSAGING_SENDER_ID_ANDROID');
  static const String firebaseProjectIdAndroid = String.fromEnvironment('FIREBASE_PROJECT_ID_ANDROID');

  static const String firebaseApiKeyIos = String.fromEnvironment('FIREBASE_API_KEY_IOS');
  static const String firebaseAppIdIos = String.fromEnvironment('FIREBASE_APP_ID_IOS');
  static const String firebaseMessagingSenderIdIos = String.fromEnvironment('FIREBASE_MESSAGING_SENDER_ID_IOS');
  static const String firebaseProjectIdIos = String.fromEnvironment('FIREBASE_PROJECT_ID_IOS');


  /// Initializes the application configuration based on the build environment.
  ///
  /// This method must be called once at application startup (e.g., in `main.dart`).
  /// It uses dart-define to determine the environment.
  ///
  /// To run with a specific environment:
  /// `flutter run --dart-define=APP_ENV=prod`
  /// `flutter run --dart-define=APP_ENV=staging`
  static Future<void> initialize() async {
    // Default to 'dev' if no environment is specified.
    _environmentName = const String.fromEnvironment('APP_ENV', defaultValue: 'dev');

    switch (_environmentName) {
      case 'prod':
        _apiBaseUrl = 'https://api.creativeflow.ai/v1';
        _enableOfflineMode = true;
        _enableCollaborationFeatures = true;
        _enableVoiceInput = true;
        _enableAdvancedAnalyticsTracking = true;
        break;
      case 'staging':
        _apiBaseUrl = 'https://staging-api.creativeflow.ai/v1';
        _enableOfflineMode = true;
        _enableCollaborationFeatures = true;
        _enableVoiceInput = true;
        _enableAdvancedAnalyticsTracking = true;
        break;
      case 'dev':
      default:
        _apiBaseUrl = 'http://10.0.2.2:8000/api/v1'; // Android emulator localhost
        _enableOfflineMode = true;
        _enableCollaborationFeatures = false;
        _enableVoiceInput = true;
        _enableAdvancedAnalyticsTracking = false;
        break;
    }

    if (kDebugMode) {
      print('Initialized AppConfig for environment: $_environmentName');
      print('API Base URL: $_apiBaseUrl');
    }
  }
}