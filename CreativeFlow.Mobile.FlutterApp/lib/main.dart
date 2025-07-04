import 'package:creativeflow_flutter_app/app/app.dart';
import 'package:creativeflow_flutter_app/core/services/analytics_service.dart';
import 'package:creativeflow_flutter_app/core/services/camera_service.dart';
import 'package:creativeflow_flutter_app/core/services/push_notification_service.dart';
import 'package:creativeflow_flutter_app/core/services/voice_recognition_service.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';

// Global service locator
final getIt = GetIt.instance;

/// Configures all dependencies for the application.
///
/// This function sets up the dependency injection container using `get_it`.
/// It registers all core services as lazy singletons, meaning they are
/// instantiated only when they are first requested.
Future<void> configureDependencies() async {
  // Core Native Feature Services
  getIt.registerLazySingleton<CameraService>(() => CameraServiceImpl());
  getIt.registerLazySingleton<VoiceRecognitionService>(() => VoiceRecognitionServiceImpl());
  getIt.registerLazySingleton<PushNotificationService>(() => PushNotificationServiceImpl());
  getIt.registerLazySingleton<AnalyticsService>(() => AnalyticsServiceImpl());

  // Data Layer Services (e.g., Database, API Client) would be registered here
  // getIt.registerLazySingleton<AppDatabase>(() => AppDatabase());
  // getIt.registerLazySingleton<ApiClient>(() => ApiClientImpl());

  // Domain Layer Services (e.g., Repositories) would be registered here
  // getIt.registerLazySingleton<ProjectRepository>(() => ProjectRepositoryImpl(getIt(), getIt()));

  // Business Logic Layer (Cubits) are typically created via BlocProvider,
  // but can be registered here if they need to be accessed globally.
}

/// The main entry point of the application.
Future<void> main() async {
  // Ensure that Flutter bindings are initialized before any Flutter-specific code.
  WidgetsFlutterBinding.ensureInitialized();

  // Set up the dependency injection container.
  await configureDependencies();

  // Initialize Firebase services.
  await Firebase.initializeApp();

  // Initialize the push notification service to set up background and foreground handlers.
  final pushNotificationService = getIt<PushNotificationService>();
  await pushNotificationService.initialize();

  // Run the root widget of the application.
  runApp(const App());
}