# Software Design Specification: CreativeFlow.MobileApp.Flutter

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `CreativeFlow.MobileApp.Flutter` repository. This mobile application serves as the cross-platform (iOS and Android) frontend for the CreativeFlow AI platform, enabling users to engage in creative workflows, manage assets, and interact with platform features on the go. It emphasizes mobile-optimized interactions, offline capabilities, and native device integrations.

### 1.2 Scope
This SDS covers the design of the Flutter-based mobile application, including:
*   User Interface (UI) and User Experience (UX) components.
*   State management strategy.
*   Local data storage and offline capabilities.
*   Data synchronization with the backend.
*   Integration with native device features (camera, voice input, push notifications, deep linking).
*   Communication with backend services via the API Gateway.
*   Implementation of accessibility and localization features.
*   Adherence to specified non-functional requirements like performance and usability.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **API:** Application Programming Interface
*   **APNS:** Apple Push Notification service
*   **BLoC:** Business Logic Component (State Management Pattern)
*   **CI/CD:** Continuous Integration / Continuous Deployment
*   **CRUD:** Create, Read, Update, Delete
*   **DAO:** Data Access Object
*   **FCM:** Firebase Cloud Messaging
*   **Flutter:** UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.
*   **Dart:** Programming language used by Flutter.
*   **Drift:** Reactive persistence library for Dart & Flutter (SQLite wrapper).
*   **Firebase:** Mobile and web application development platform by Google.
*   **Intl:** Internationalization
*   **L10n:** Localization
*   **NFR:** Non-Functional Requirement
*   **PWA:** Progressive Web App (Mentioned for web, but mobile app is native Flutter)
*   **REQ:** Requirement
*   **RTL:** React Testing Library (Not directly applicable here, but analogous to Flutter widget testing)
*   **SDS:** Software Design Specification
*   **SQLite:** Lightweight, file-based relational database.
*   **UI:** User Interface
*   **UX:** User Experience
*   **WCAG:** Web Content Accessibility Guidelines
*   **XFile:** A cross-platform file representation from Flutter plugins like `image_picker` or `camera`.

## 2. Overall Architecture

The `CreativeFlow.MobileApp.Flutter` application will follow a feature-first directory structure with a layered architecture within each feature, primarily leveraging the **BLoC (Business Logic Component)** pattern for state management. This promotes separation of concerns, testability, and scalability within the monolithic mobile application structure.

**Key Architectural Layers/Components:**

1.  **Presentation Layer:**
    *   **Screens (UI):** User-facing views built with Flutter widgets.
    *   **Widgets (UI):** Reusable UI components.
    *   **BLoCs/Cubits (State Management):** Manage the state of screens and features, handling user interactions and communicating with the domain/data layer.
2.  **Domain Layer (Implicit within BLoCs/Repositories):**
    *   Contains business logic, use cases, and domain entities. Often, this logic resides within BLoCs or is coordinated by them through repositories.
3.  **Data Layer:**
    *   **Repositories:** Abstract data sources, providing a clean API for BLoCs to access data. They decide whether to fetch data from local or remote sources.
    *   **Data Sources:**
        *   **Remote:** Handles communication with the backend API Gateway (e.g., `ApiClient`).
        *   **Local:** Manages local data persistence using SQLite via Drift (e.g., `CreativeLocalDataSource`).
    *   **Models:** Data structures representing entities (e.g., Project, Asset).
4.  **Core Services/Utils:**
    *   Cross-cutting concerns like navigation, networking, local storage setup, theme, localization, analytics, push notifications, permissions, device integrations (camera, voice), and synchronization.

**Technology Stack:**
*   **Language:** Dart (SDK 3.4.3 or later)
*   **Framework:** Flutter (SDK 3.22.2 or later)
*   **State Management:** `flutter_bloc`
*   **Local Database:** SQLite via `drift`
*   **Networking:** `http` package (or `dio` if complex interceptors are heavily needed, but `http` is simpler for basic needs)
*   **Analytics:** `firebase_core`, `firebase_analytics`
*   **Push Notifications:** `firebase_messaging`
*   **Camera Integration:** `camera` (or `image_picker`)
*   **Localization:** `intl`, `flutter_localizations`
*   **Shared Preferences:** `shared_preferences` (for simple key-value storage)
*   **Deep Linking:** `uni_links` (or Flutter's built-in deep linking support)
*   **Permissions:** `permission_handler`

## 3. Module Design Specifications

This section details the design for each file defined in the repository's `file_structure_json`.

### 3.1 Configuration Files

#### 3.1.1 `pubspec.yaml`
*   **Purpose:** Declares project metadata, dependencies, and assets.
*   **Implemented Features:** Dependency Management, Asset Declaration.
*   **Requirements:** Section 2.1 (Mobile Tech), REQ-019, REQ-020, INT-004.
*   **Logic Description:**
    *   Define `name`, `description`, `version`, `environment` (Dart SDK constraints).
    *   **Dependencies:**
        *   `flutter` (from SDK)
        *   `flutter_localizations` (from SDK, for UI-006)
        *   `intl: ^0.19.0` (or latest, for UI-006)
        *   `flutter_bloc: ^8.1.0` (or latest, for state management)
        *   `equatable: ^2.0.0` (or latest, for BLoC states/events)
        *   `drift: ^2.10.0` (or latest, for REQ-019)
        *   `sqlite3_flutter_libs: ^0.5.0` (or latest, for Drift on mobile)
        *   `path_provider: ^2.0.0` (or latest, for Drift)
        *   `path: ^1.8.0` (or latest, for Drift)
        *   `firebase_core: ^2.15.0` (or latest, for INT-004, REQ-020)
        *   `firebase_analytics: ^10.4.0` (or latest, for INT-004)
        *   `firebase_messaging: ^14.6.0` (or latest, for REQ-020)
        *   `firebase_crashlytics: ^3.3.0` (or latest, for NFR-001 crash reporting)
        *   `camera: ^0.10.0` (or latest, for REQ-020)
        *   `image_picker: ^1.0.0` (alternative/supplement to `camera`)
        *   `http: ^1.1.0` (or latest, for API communication)
        *   `shared_preferences: ^2.1.0` (or latest, for simple key-value storage)
        *   `connectivity_plus: ^5.0.0` (or latest, for UI-004)
        *   `permission_handler: ^11.0.0` (or latest, for REQ-020)
        *   `uni_links: ^0.5.0` (or latest, for REQ-020 deep linking, if not using Flutter's Router based deep linking directly)
        *   `flutter_svg: ^2.0.0` (or latest, if SVG assets are used)
        *   `get_it: ^7.6.0` (Optional, for dependency injection if not solely relying on BLoC providers)
    *   **Dev Dependencies:**
        *   `flutter_test` (from SDK)
        *   `bloc_test: ^9.1.0` (or latest)
        *   `drift_dev: ^2.10.0` (or latest)
        *   `build_runner: ^2.4.0` (or latest)
        *   `flutter_lints: ^3.0.0` (or latest)
    *   **Flutter Configuration:**
        *   `uses-material-design: true`
        *   Declare asset paths for images (e.g., `assets/images/`), fonts.
        *   Define font families and their variants.
*   **Documentation:** Standard pubspec.yaml comments.

#### 3.1.2 `analysis_options.yaml`
*   **Purpose:** Configures Dart static analysis options, linters, and code style rules.
*   **Implemented Features:** Code Style Enforcement, Static Analysis.
*   **Requirements:** NFR-008 (from SRS, implies REQ-SDS-001).
*   **Logic Description:**
    yaml
    include: package:flutter_lints/flutter.yaml

    analyzer:
      strong-mode:
        implicit-casts: false
        implicit-dynamic: false
      errors:
        # treat certain warnings as errors
        # missing_required_param: error
        # unnecessary_null_comparison: error
        # prefer_const_constructors: error # example, enable more
        # todo: error # to ensure todos are addressed
      # exclude:
      #   - "lib/generated_plugin_registrant.dart"

    linter:
      rules:
        # Core Effective Dart rules are often included by flutter_lints
        # Add specific rules or overrides here
        - prefer_final_fields
        - prefer_const_constructors
        - prefer_const_constructors_in_immutables
        - prefer_const_declarations
        - prefer_const_literals_to_create_immutables
        - avoid_print # Encourage use of a proper logger
        - avoid_redundant_argument_values
        - avoid_returning_null_for_void
        - avoid_unused_constructor_parameters
        - curly_braces_in_flow_control_structures
        - no_duplicate_case_values
        # Accessibility related (if linters exist)
        # - semantic_label_instead_of_hint (example)
        # Custom rules based on team agreement
    
*   **Documentation:** Comments within the YAML explaining rule choices.

### 3.2 Application Entry & Root

#### 3.2.1 `lib/main.dart`
*   **Purpose:** Initializes the Flutter application, sets up global dependencies, and runs the main app widget.
*   **Implemented Features:** App Initialization, Service Setup, Root Widget Invocation.
*   **Requirements:** NFR-001 (Mobile App Launch), Section 5.2.1.
*   **Methods:**
    *   `Future<void> main()`:
        *   Call `WidgetsFlutterBinding.ensureInitialized()`.
        *   **Firebase Initialization:** `await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);` (Requires `firebase_options.dart` generated by FlutterFire CLI).
        *   **Crashlytics Error Handling:**
            dart
            FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
            PlatformDispatcher.instance.onError = (error, stack) {
              FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
              return true;
            };
            
        *   **Dependency Injection Setup (Example using GetIt):**
            dart
            // Example:
            // final getIt = GetIt.instance;
            // getIt.registerSingleton<AppConfig>(AppConfig());
            // getIt.registerLazySingleton<ApiClient>(() => ApiClient(getIt<AppConfig>()));
            // getIt.registerSingletonAsync<AppLocalDatabase>(() async {
            //   final db = AppLocalDatabase();
            //   // any async setup for db if needed
            //   return db;
            // });
            // await getIt.allReady(); // if using async singletons
            
            (Alternatively, BLoCs can be provided higher up in the widget tree using `MultiBlocProvider`).
        *   **Logging Initialization:** Setup a global logger instance (e.g., using `logging` package).
        *   **Run App:** `runApp(CreativeFlowApp());` (This can be wrapped with `BlocProvider` for global BLoCs if not using GetIt for them).
*   **Dependencies:** `CreativeFlowApp`, Firebase, (Optional: GetIt, Logging package).
*   **Documentation:** Comments explaining initialization steps.

#### 3.2.2 `lib/app.dart`
*   **Purpose:** Defines the root structure of the application, including theme, localization, and navigation.
*   **Implemented Features:** Global Theming, Localization Setup, Root Navigation, Global State Providers.
*   **Requirements:** UI-006, NFR-007 (Mobile Usability), Section 6.2.
*   **Class:** `CreativeFlowApp extends StatelessWidget`
*   **Methods:**
    *   `Widget build(BuildContext context)`:
        *   Return `MultiBlocProvider` to provide global BLoCs:
            *   `AuthBloc` (manages authentication state).
            *   `ThemeBloc` (manages light/dark theme).
            *   `LocalizationBloc` (manages current locale, for UI-006).
            *   `ConnectivityBloc` (for UI-004 offline status).
        *   Inside, use a `BlocBuilder<ThemeBloc, ThemeState>` to get the current `ThemeData`.
        *   Use a `BlocBuilder<LocalizationBloc, LocalizationState>` to get the current `Locale`.
        *   Return `MaterialApp` (or `CupertinoApp` if strictly iOS-styled):
            *   `title: 'CreativeFlow AI'`
            *   `theme: AppTheme.lightTheme` (or dynamically from ThemeBloc)
            *   `darkTheme: AppTheme.darkTheme` (or dynamically from ThemeBloc)
            *   `themeMode: themeState.themeMode` (from ThemeBloc)
            *   `locale: localizationState.locale` (from LocalizationBloc)
            *   `localizationsDelegates: AppLocalizations.localizationsDelegates` (list from `app_localizations.dart`)
            *   `supportedLocales: AppLocalizations.supportedLocales` (list from `app_localizations.dart`)
            *   `onGenerateRoute: AppRouter.onGenerateRoute` (or use Navigator 2.0 setup)
            *   `initialRoute: RoutePaths.splash` (or dynamically based on AuthBloc state)
            *   `builder: (context, child)`: Wrap child with an `OfflineBanner` listener.
*   **Dependencies:** `AppTheme`, `AppLocalizations`, `AppRouter`, `RoutePaths`, global BLoCs (`AuthBloc`, `ThemeBloc`, `LocalizationBloc`, `ConnectivityBloc`), `OfflineBanner`.
*   **Documentation:** Comments explaining the setup of global providers and MaterialApp properties.

### 3.3 Core Module

#### 3.3.1 Configuration

##### 3.3.1.1 `lib/core/config/app_config.dart`
*   **Purpose:** Provides centralized access to application configuration values based on the current environment.
*   **Implemented Features:** Environment Configuration, Feature Flag Management.
*   **Requirements:** REQ-019 (implies config for offline features).
*   **Class:** `AppConfig`
*   **Members (static final):**
    *   `String apiBaseUrl`
    *   `String environmentName` (e.g., 'dev', 'staging', 'prod')
    *   `bool enableOfflineMode` (Feature Toggle for REQ-019)
    *   `bool enableCollaborationFeatures`
    *   `bool enableVoiceInput` (Feature Toggle for REQ-020)
    *   `bool enableAdvancedAnalyticsTracking` (Feature Toggle for INT-004)
    *   `String firebaseApiKeyAndroid` (loaded from environment)
    *   `String firebaseAppIdAndroid` (loaded from environment)
    *   `String firebaseMessagingSenderIdAndroid` (loaded from environment)
    *   `String firebaseProjectIdAndroid` (loaded from environment)
    *   `String firebaseApiKeyIos` (loaded from environment)
    *   `String firebaseAppIdIos` (loaded from environment)
    *   `String firebaseMessagingSenderIdIos` (loaded from environment)
    *   `String firebaseProjectIdIos` (loaded from environment)
    *   _Other API keys if absolutely necessary here, but prefer backend proxy._
*   **Methods (static):**
    *   `Future<void> initialize()`:
        *   Determine current build environment (e.g., using `String.fromEnvironment` or build flavors).
        *   Load corresponding configuration (e.g., from different `.env` files or a map).
        *   Set the static members.
*   **Logic Description:**
    *   Use Flutter's build flavors or `--dart-define` to pass environment specific variables at build time.
    *   Example:
      dart
      class AppConfig {
        static late String _apiBaseUrl;
        static String get apiBaseUrl => _apiBaseUrl;
        // ... other properties

        static Future<void> initialize() async {
          const env = String.fromEnvironment('APP_ENV', defaultValue: 'dev');
          environmentName = env;
          if (env == 'prod') {
            _apiBaseUrl = 'https://api.creativeflow.ai/v1';
            enableOfflineMode = true;
            // load prod firebase options
          } else if (env == 'staging') {
            _apiBaseUrl = 'https://staging-api.creativeflow.ai/v1';
            enableOfflineMode = true;
            // load staging firebase options
          } else { // dev
            _apiBaseUrl = 'http://localhost:8000/api/v1'; // Example
            enableOfflineMode = true;
            // load dev firebase options
          }
          // Load Firebase options based on environment (or use DefaultFirebaseOptions if flavors handle it)
        }
      }
      
*   **Documentation:** Comments explaining each configuration key and how to set up environments.

#### 3.3.2 Constants

##### 3.3.2.1 `lib/core/constants/app_constants.dart`
*   **Purpose:** Defines globally used constant values.
*   **Implemented Features:** Centralized Constants.
*   **Requirements:** REQ-019 (e.g., max offline items).
*   **Class:** `AppConstants` (or just a library file with top-level consts)
*   **Members (const):**
    *   `double defaultPadding = 16.0;`
    *   `Duration shortAnimationDuration = Duration(milliseconds: 300);`
    *   `Duration longAnimationDuration = Duration(milliseconds: 600);`
    *   `int maxOfflineProjects = 10;` (for REQ-019)
    *   `String prefKeyTheme = 'app_theme';`
    *   `String prefKeyLocale = 'app_locale';`
    *   `String prefKeyUserId = 'user_id';`
    *   `String prefKeyAuthToken = 'auth_token';`
    *   `String prefKeyRefreshToken = 'refresh_token';`
    *   `int localDbVersion = 1;`
    *   `String localDbName = 'creative_flow_local.db';`
    *   `int defaultApiTimeoutMs = 30000;`
    *   `int maxImageUploadSizeBytes = 10 * 1024 * 1024; // 10MB`
*   **Documentation:** Comments explaining the purpose of each constant.

#### 3.3.3 Navigation

##### 3.3.3.1 `lib/core/navigation/route_paths.dart`
*   **Purpose:** Central repository for all named route paths.
*   **Implemented Features:** Route Name Constants.
*   **Requirements:** Section 6.2.
*   **Class:** `RoutePaths`
*   **Members (const String):**
    *   `static const String splash = '/';`
    *   `static const String login = '/login';`
    *   `static const String register = '/register';`
    *   `static const String home = '/home';` // Dashboard
    *   `static const String editor = '/editor'; // e.g., /editor/:projectId`
    *   `static const String projectDetails = '/project'; // e.g., /project/:projectId`
    *   `static const String workbenchDetails = '/workbench'; // e.g., /workbench/:workbenchId`
    *   `static const String settings = '/settings';`
    *   `static const String accountSettings = '/settings/account';`
    *   `static const String accessibilitySettings = '/settings/accessibility';` (UI-005)
    *   `static const String brandKitList = '/brand-kits';`
    *   `static const String brandKitDetails = '/brand-kit'; // e.g., /brand-kit/:kitId`
    *   `static const String templateGallery = '/templates';`
*   **Documentation:** Comments clarifying what each route represents.

##### 3.3.3.2 `lib/core/navigation/app_router.dart`
*   **Purpose:** Centralizes navigation logic and route definitions.
*   **Implemented Features:** Route Definition, Navigation Handling.
*   **Requirements:** Section 6.2.
*   **Class:** `AppRouter`
*   **Methods (static):**
    *   `static Route<dynamic>? onGenerateRoute(RouteSettings settings)`:
        *   Use a `switch` statement on `settings.name`.
        *   For each `RoutePaths` constant, return a `MaterialPageRoute` (or `CupertinoPageRoute`) wrapping the corresponding screen widget.
        *   Extract and pass arguments from `settings.arguments` to screens.
        *   Handle unknown routes gracefully (e.g., navigate to a "Not Found" screen or Home).
        *   Example:
          dart
          switch (settings.name) {
            case RoutePaths.splash:
              return MaterialPageRoute(builder: (_) => SplashScreen());
            case RoutePaths.login:
              return MaterialPageRoute(builder: (_) => LoginScreen());
            case RoutePaths.home:
              return MaterialPageRoute(builder: (_) => HomeScreen());
            case RoutePaths.editor:
              final projectId = settings.arguments as String?; // Or a specific args class
              if (projectId != null) {
                 return MaterialPageRoute(builder: (_) => EditorScreen(projectId: projectId));
              }
              return _errorRoute(); // Or navigate to selection screen
            // ... other routes
            default:
              return _errorRoute(); // A simple screen saying "Page not found"
          }
          
    *   Typed navigation helper methods:
        *   `static void navigateToLogin(BuildContext context) => Navigator.of(context).pushNamedAndRemoveUntil(RoutePaths.login, (route) => false);`
        *   `static Future<void> navigateToEditor(BuildContext context, {required String projectId}) => Navigator.of(context).pushNamed(RoutePaths.editor, arguments: projectId);`
        *   ... and so on for frequently used routes, especially those requiring arguments.
    *   `static Route<dynamic> _errorRoute()`: Returns a `MaterialPageRoute` to a generic error/not found screen.
*   **Dependencies:** `RoutePaths`, all Screen widgets.
*   **Documentation:** Comments explaining route generation logic and argument handling.

##### 3.3.3.3 `lib/core/navigation/deep_link_handler.dart`
*   **Purpose:** Manages deep linking functionality for REQ-020.
*   **Implemented Features:** Deep Link Processing.
*   **Requirements:** REQ-020.
*   **Class:** `DeepLinkHandler`
*   **Dependencies:** `uni_links` package, `AppRouter`, `AuthBloc` (to check auth state before navigating).
*   **Methods:**
    *   `static Future<void> init(GlobalKey<NavigatorState> navigatorKey)`:
        *   To be called in `main.dart` or `app.dart`'s `initState`.
        *   Listen to `getInitialUri()` and `uriLinkStream` from `uni_links`.
        *   On receiving a link, call `handleLink`.
    *   `static Future<void> handleLink(Uri? link, GlobalKey<NavigatorState> navigatorKey)`:
        *   If `link` is null, do nothing.
        *   Parse `link.pathSegments` and `link.queryParameters`.
        *   Determine the target route and arguments (e.g., project ID, content ID).
        *   Check authentication status if the target route requires login. If not logged in, navigate to login, possibly storing the deep link to redirect after login.
        *   Use `navigatorKey.currentState?.pushNamed(...)` or custom logic with `AppRouter` to navigate.
        *   Example path: `/project/123`, `/collab/abc`.
*   **Documentation:** Comments on URI parsing logic and handling different deep link schemes.

#### 3.3.4 Network

##### 3.3.4.1 `lib/core/network/api_client.dart`
*   **Purpose:** Centralizes network request logic, managing API calls, authentication, and error responses.
*   **Implemented Features:** HTTP Request Handling, Authentication Interceptor, Error Handling.
*   **Requirements:** Section 5.2.1 (Mobile App interaction with API Gateway).
*   **Dependencies:** `http` package, `AppConfig`, `AuthTokenRepository` (or similar to get auth token), `shared_preferences` (potentially for token storage if not handled by a dedicated secure storage).
*   **Class:** `ApiClient`
*   **Members:**
    *   `final http.Client _client;`
    *   `final String _baseUrl;`
    *   `final AuthTokenRepository _authTokenRepository;` (injected)
*   **Constructor:** `ApiClient(this._client, this._baseUrl, this._authTokenRepository)`
*   **Methods:**
    *   `Future<Map<String, String>> _getHeaders({bool requiresAuth = true}) async`:
        *   Base headers: `{'Content-Type': 'application/json', 'Accept': 'application/json'}`.
        *   If `requiresAuth`, retrieve JWT token from `_authTokenRepository` and add `Authorization: Bearer <token>` header.
        *   Handle token expiry/refresh logic here or delegate to an interceptor-like pattern if using `dio`.
    *   `Future<http.Response> get(String path, {Map<String, String>? queryParameters, bool requiresAuth = true})`:
        *   Construct URI: `Uri.parse('$_baseUrl$path').replace(queryParameters: queryParameters)`.
        *   Call `_client.get(uri, headers: await _getHeaders(requiresAuth: requiresAuth))`.
        *   Handle response: check status code, parse JSON, throw custom exceptions for API errors (e.g., `ApiException(statusCode, message)`).
    *   `Future<http.Response> post(String path, {required Map<String, dynamic> body, bool requiresAuth = true})`: Similar to `get`, but uses `_client.post` and `jsonEncode(body)`.
    *   `Future<http.Response> put(String path, {required Map<String, dynamic> body, bool requiresAuth = true})`: Similar to `post`.
    *   `Future<http.Response> delete(String path, {Map<String, dynamic>? body, bool requiresAuth = true})`: Similar to `post`.
    *   Private helper `_handleResponse(http.Response response)` to centralize status code checking and error throwing.
*   **Error Handling:** Define custom exception classes (`ApiException`, `NetworkException`, `UnauthorizedException`, etc.) to be thrown based on response status codes or network issues.
*   **Documentation:** Comments on API interaction patterns, error handling, and authentication.

#### 3.3.5 Storage

##### 3.3.5.1 `lib/core/storage/local_database.dart`
*   **Purpose:** Defines the local SQLite database structure and provides access methods using Drift for offline data (REQ-019).
*   **Implemented Features:** Local Data Persistence, Offline Storage Schema.
*   **Requirements:** REQ-019, REQ-019.1.
*   **Dependencies:** `drift`, `path_provider`, `path`, `sqlite3_flutter_libs`.
*   **File Content:**
    dart
    import 'package:drift/drift.dart';
    import 'package.path_provider/path_provider.dart';
    import 'package:path/path.dart' as p;
    import 'package:drift/native.dart';
    import 'dart:io';

    // Import DAOs and Table definitions from feature directories
    // e.g., import '../../features/editor/data/models/local/project_table.dart';
    // e.g., import '../../features/editor/data/datasources/daos/project_dao.dart';

    part 'local_database.g.dart'; // Drift generated file

    // Define tables (example - actual tables will be more detailed and spread across features)
    class LocalProjects extends Table {
      TextColumn get id => text()();
      TextColumn get workbenchId => text()();
      TextColumn get name => text()();
      TextColumn get collaborationStateJson => text().nullable()(); // For CRDT data or simple JSON
      DateTimeColumn get lastSyncedAt => dateTime().nullable()();
      DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
      DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
      BoolColumn get isSynced => boolean().withDefault(Constant(false))();

      @override
      Set<Column> get primaryKey => {id};
    }

    class LocalAssets extends Table {
      TextColumn get id => text()();
      TextColumn get projectId => text().nullable().references(LocalProjects, #id)();
      TextColumn get name => text()();
      TextColumn get localPath => text()(); // Path to asset stored on device
      TextColumn get remotePath => text().nullable()(); // Path on MinIO once synced
      TextColumn get mimeType => text()();
      DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
      BoolColumn get isSynced => boolean().withDefault(Constant(false))();
       @override
      Set<Column> get primaryKey => {id};
    }
    
    class OfflineSyncQueueItems extends Table {
      IntColumn get id => integer().autoIncrement()();
      TextColumn get entityType => text()(); // e.g., 'project', 'asset'
      TextColumn get entityId => text()();
      TextColumn get operationType => text()(); // 'create', 'update', 'delete'
      TextColumn get payloadJson => text()(); // JSON of the changes
      DateTimeColumn get queuedAt => dateTime().withDefault(currentDateAndTime)();
      IntColumn get attemptCount => integer().withDefault(Constant(0))();
    }

    @DriftDatabase(tables: [LocalProjects, LocalAssets, OfflineSyncQueueItems], 
                   daos: [/* ProjectDao, AssetDao, OfflineSyncQueueDao - to be defined in feature dirs */])
    class AppLocalDatabase extends _$AppLocalDatabase {
      AppLocalDatabase() : super(_openConnection());

      @override
      int get schemaVersion => AppConstants.localDbVersion; // From app_constants.dart

      // Migration strategy can be added here if needed
      @override
      MigrationStrategy get migration => MigrationStrategy(
        onCreate: (Migrator m) async {
          await m.createAll();
          // Seed initial data if necessary
        },
        onUpgrade: (Migrator m, int from, int to) async {
          // Handle schema upgrades
          if (from < 2) {
            // example: await m.addColumn(projects, projects.newColumn);
          }
        },
      );
    }

    LazyDatabase _openConnection() {
      return LazyDatabase(() async {
        final dbFolder = await getApplicationDocumentsDirectory();
        final file = File(p.join(dbFolder.path, AppConstants.localDbName));
        return NativeDatabase.createInBackground(file);
      });
    }
    
*   **DAOs:** DAOs for `LocalProjects`, `LocalAssets`, `OfflineSyncQueueItems` should be defined in their respective feature data layers (e.g., `features/editor/data/datasources/daos/`).
*   **Documentation:** Comments detailing table structures, relationships, and DAO responsibilities.

#### 3.3.6 Core Services

##### 3.3.6.1 `lib/core/services/analytics_service.dart`
*   **Purpose:** Abstract analytics tracking (INT-004, REQ-8-009).
*   **Implemented Features:** Event Tracking, User Property Logging, Screen View Tracking, Crash Reporting Setup.
*   **Requirements:** INT-004, REQ-8-009, NFR-001 (Crash-Free Rate implies crash reporting).
*   **Dependencies:** `firebase_core`, `firebase_analytics`, `firebase_crashlytics`.
*   **Class:** `AnalyticsService`
*   **Members:**
    *   `final FirebaseAnalytics _firebaseAnalytics = FirebaseAnalytics.instance;`
    *   `final FirebaseCrashlytics _firebaseCrashlytics = FirebaseCrashlytics.instance;`
*   **Methods:**
    *   `Future<void> initialize()`:
        *   `await _firebaseCrashlytics.setCrashlyticsCollectionEnabled(true);` (based on user consent if applicable)
    *   `Future<void> logEvent({required String name, Map<String, Object>? parameters})`:
        *   `await _firebaseAnalytics.logEvent(name: name, parameters: parameters);`
    *   `Future<void> setUserProperty({required String name, String? value})`:
        *   `await _firebaseAnalytics.setUserProperty(name: name, value: value);`
        *   Common properties: `userId`, `subscriptionTier`.
    *   `Future<void> logScreenView({required String screenName, String? screenClassOverride})`:
        *   `await _firebaseAnalytics.setCurrentScreen(screenName: screenName, screenClassOverride: screenClassOverride ?? screenName);`
    *   `Future<void> recordError(dynamic exception, StackTrace stack, {bool fatal = false})`:
        *   `await _firebaseCrashlytics.recordError(exception, stack, fatal: fatal);`
    *   `Future<void> setUserId(String? userId)`:
        *   `await _firebaseAnalytics.setUserId(id: userId);`
        *   `await _firebaseCrashlytics.setUserIdentifier(userId ?? 'anonymous');`
*   **Documentation:** Comments on event naming conventions and parameter usage.

##### 3.3.6.2 `lib/core/services/push_notification_service.dart`
*   **Purpose:** Manages push notifications (REQ-020, derived from REQ-8-006).
*   **Implemented Features:** Push Notification Handling, FCM Token Management.
*   **Requirements:** REQ-020 (from REQ-8-006).
*   **Dependencies:** `firebase_messaging`, `flutter_local_notifications` (optional, for custom foreground notifications), `AppRouter`, `PermissionHandlerService`.
*   **Class:** `PushNotificationService`
*   **Members:**
    *   `final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;`
    *   `final GlobalKey<NavigatorState> navigatorKey;` (injected or passed)
*   **Constructor:** `PushNotificationService({required this.navigatorKey})`
*   **Methods:**
    *   `Future<void> initialize()`:
        *   Request permission: `await PermissionHandlerService.requestNotificationPermission();`
        *   `NotificationSettings settings = await _firebaseMessaging.requestPermission(...)`
        *   If authorized:
            *   `String? token = await getFcmToken();` // Send token to backend.
            *   `_firebaseMessaging.onTokenRefresh.listen((newToken) { /* Send to backend */ });`
            *   `FirebaseMessaging.onMessage.listen(_handleForegroundMessage);`
            *   `FirebaseMessaging.onMessageOpenedApp.listen(_handleBackgroundMessageTap);`
            *   `RemoteMessage? initialMessage = await _firebaseMessaging.getInitialMessage(); if (initialMessage != null) { _handleBackgroundMessageTap(initialMessage); }`
    *   `Future<String?> getFcmToken()`: `return await _firebaseMessaging.getToken();`
    *   `void _handleForegroundMessage(RemoteMessage message)`:
        *   Display a local notification (e.g., using `flutter_local_notifications`) or update UI.
        *   Parse `message.data` for navigation or action.
    *   `void _handleBackgroundMessageTap(RemoteMessage message)`:
        *   Parse `message.data` (e.g., `type`, `entity_id`).
        *   Navigate to the relevant screen using `navigatorKey.currentState?.pushNamed(...)` and `AppRouter`.
*   **Documentation:** Details on payload structure and navigation logic from notifications.

##### 3.3.6.3 `lib/core/services/sync_service.dart`
*   **Purpose:** Orchestrates synchronization of local offline data with the backend (REQ-019, REQ-019.1).
*   **Implemented Features:** Offline Data Synchronization, Conflict Resolution Logic.
*   **Requirements:** REQ-019, REQ-019.1, UI-004.
*   **Dependencies:** `AppLocalDatabase` (specifically `OfflineSyncQueueDao`), `ApiClient`, `ConnectivityBloc`, (potentially `CollaborationService` if CRDTs are involved directly).
*   **Class:** `SyncService`
*   **Members:**
    *   `final AppLocalDatabase _localDb;`
    *   `final ApiClient _apiClient;`
    *   `final ConnectivityBloc _connectivityBloc;`
    *   `StreamSubscription? _connectivitySubscription;`
    *   `bool _isSyncing = false;`
*   **Constructor:** `SyncService(this._localDb, this._apiClient, this._connectivityBloc)`
*   **Methods:**
    *   `void initialize()`:
        *   Subscribe to `_connectivityBloc.stream`. If online and not already syncing, call `processSyncQueue()`.
    *   `Future<void> queueChange({required String entityType, required String entityId, required String operationType, required Map<String, dynamic> payload})`:
        *   Adds an item to `OfflineSyncQueueItems` table via DAO.
        *   If online, could attempt immediate sync or just queue.
    *   `Future<void> processSyncQueue()`:
        *   If `_isSyncing` or offline, return. Set `_isSyncing = true;`.
        *   Fetch items from `OfflineSyncQueueItems` ordered by `queuedAt`.
        *   For each item:
            *   Attempt to send to `_apiClient` based on `operationType` and `entityType`.
            *   On success: Delete item from queue.
            *   On conflict (e.g., 409 status):
                *   Invoke conflict resolution logic (REQ-019.1). This might involve:
                    *   Fetching latest server version.
                    *   Applying "last-write-wins" for simple changes (update local with server, then re-queue if local was truly later).
                    *   Prompting user via a UI event/state update for complex conflicts.
                    *   If collaborative (using CRDTs from a `CollaborationService`), attempt merge.
            *   On other errors: Increment `attemptCount`. If max attempts reached, flag for manual review or notify user.
        *   Set `_isSyncing = false;`. If queue still has items and online, schedule another `processSyncQueue`.
    *   `Future<void> resolveConflict(...)`: Placeholder for user-driven conflict resolution.
    *   `void dispose()`: Cancel `_connectivitySubscription`.
*   **Documentation:** Detailed explanation of sync strategies, conflict resolution rules for different entities, and retry mechanisms.

##### 3.3.6.4 `lib/core/services/camera_service.dart`
*   **Purpose:** Abstracts device camera functionalities for REQ-020, UI-004.
*   **Implemented Features:** Camera Integration.
*   **Requirements:** REQ-020, UI-004.
*   **Dependencies:** `image_picker` package (preferred for simplicity over `camera` unless fine-grained control is needed), `PermissionHandlerService`.
*   **Class:** `CameraService`
*   **Methods (static or instance-based if configuration needed):**
    *   `static Future<XFile?> pickImageFromCamera()`:
        *   `PermissionStatus status = await PermissionHandlerService.requestCameraPermission();`
        *   If `status.isGranted`: `return await ImagePicker().pickImage(source: ImageSource.camera);`
        *   Else, handle permission denied (e.g., show a dialog).
    *   `static Future<XFile?> pickVideoFromCamera()`:
        *   Similar permission check.
        *   `return await ImagePicker().pickVideo(source: ImageSource.camera);`
*   **Documentation:** Notes on permission handling and returned `XFile` usage.

##### 3.3.6.5 `lib/core/services/voice_input_service.dart`
*   **Purpose:** Provides voice-to-text functionality for REQ-020.
*   **Implemented Features:** Voice-to-Text Input.
*   **Requirements:** REQ-020.
*   **Dependencies:** `speech_to_text` package, `PermissionHandlerService`.
*   **Class:** `VoiceInputService`
*   **Members:**
    *   `final SpeechToText _speechToText = SpeechToText();`
    *   `bool _isListening = false;`
    *   `String _lastRecognizedWords = "";`
*   **Methods:**
    *   `Future<bool> initialize()`:
        *   `bool available = await _speechToText.initialize( onError: _onError, onStatus: _onStatus);`
        *   Request microphone permission: `await PermissionHandlerService.requestMicrophonePermission();`
        *   Return `available`.
    *   `Future<void> startListening({required Function(String words) onResult, required Function(String status) onStatusChange})`:
        *   If not initialized or already listening, return.
        *   `_isListening = true;`
        *   `_speechToText.listen(onResult: (result) { _lastRecognizedWords = result.recognizedWords; onResult(_lastRecognizedWords); if (result.finalResult) _isListening = false; }, listenFor: Duration(seconds:30), onDevice: true );` // Example settings
        *   `onStatusChange(_speechToText.lastStatus);`
    *   `void stopListening()`:
        *   `_speechToText.stop(); _isListening = false;`
    *   `void cancelListening()`:
        *   `_speechToText.cancel(); _isListening = false;`
    *   `void _onError(SpeechRecognitionError error)`: Log error, update UI state.
    *   `void _onStatus(String status)`: Update UI state based on listening status.
    *   `bool get isListening => _isListening;`
    *   `String get lastWords => _lastRecognizedWords;`
*   **Documentation:** Instructions for platform-specific setup (e.g., Info.plist, AndroidManifest.xml) and error handling.

##### 3.3.6.6 `lib/core/services/permission_handler_service.dart`
*   **Purpose:** Centralized way to request and check device permissions for REQ-020.
*   **Implemented Features:** Device Permission Management.
*   **Requirements:** REQ-020.
*   **Dependencies:** `permission_handler` package.
*   **Class:** `PermissionHandlerService`
*   **Methods (static Future<PermissionStatus>):**
    *   `static Future<PermissionStatus> requestCameraPermission()`: `return await Permission.camera.request();`
    *   `static Future<PermissionStatus> checkCameraPermission()`: `return await Permission.camera.status;`
    *   `static Future<PermissionStatus> requestMicrophonePermission()`: `return await Permission.microphone.request();`
    *   `static Future<PermissionStatus> checkMicrophonePermission()`: `return await Permission.microphone.status;`
    *   `static Future<PermissionStatus> requestNotificationPermission()`: `return await Permission.notification.request();`
    *   `static Future<PermissionStatus> checkNotificationPermission()`: `return await Permission.notification.status;`
    *   `static Future<PermissionStatus> requestStoragePermission()`: (Consider specific needs, e.g., `Permission.storage` or `Permission.photos` for iOS) `return await Permission.storage.request();`
    *   `static Future<bool> openAppSettings()`: `return await openAppSettings();` (from permission_handler)
*   **Documentation:** Notes on when to call these methods and how to interpret `PermissionStatus`.

#### 3.3.7 Theme

##### 3.3.7.1 `lib/core/theme/app_theme.dart`
*   **Purpose:** Centralizes theme definitions for UI-005, NFR-007.
*   **Implemented Features:** App Theming, Light/Dark Mode Support, Accessible Color Contrasts.
*   **Requirements:** UI-005, NFR-007 (Mobile Usability), Section 6.2.
*   **Dependencies:** `AppTypography`, `AppColors` (separate files for color constants and typography definitions).
*   **Class:** `AppTheme`
*   **Members (static final ThemeData):**
    *   `static final ThemeData lightTheme = ThemeData(...)`
    *   `static final ThemeData darkTheme = ThemeData(...)`
*   **Logic Description:**
    *   Define `lightTheme`:
        *   `brightness: Brightness.light`
        *   `primaryColor: AppColors.primaryLight`
        *   `scaffoldBackgroundColor: AppColors.backgroundLight`
        *   `textTheme: AppTypography.textThemeLight`
        *   `appBarTheme: AppBarTheme(...)`
        *   `buttonTheme: ButtonThemeData(...)`
        *   `inputDecorationTheme: InputDecorationTheme(...)`
        *   Ensure color contrasts meet WCAG 2.1 AA (e.g., primary text on background).
    *   Define `darkTheme`:
        *   `brightness: Brightness.dark`
        *   `primaryColor: AppColors.primaryDark`
        *   `scaffoldBackgroundColor: AppColors.backgroundDark`
        *   `textTheme: AppTypography.textThemeDark`
        *   Ensure color contrasts meet WCAG 2.1 AA.
*   **Helper files:**
    *   `lib/core/theme/app_colors.dart`: Define `AppColors` class with static `Color` constants.
    *   `lib/core/theme/app_typography.dart`: Define `AppTypography` class with static `TextTheme` and individual `TextStyle` constants. Implement support for dynamic font sizes (UI-005) by providing base text styles that scale appropriately or respond to `MediaQuery.textScaleFactorOf(context)`.
*   **Documentation:** Overview of theme structure and how to use defined styles.

#### 3.3.8 Localization

##### 3.3.8.1 `lib/core/l10n/app_localizations.dart`
*   **Purpose:** Provides localized strings and supports multiple languages for UI-006.
*   **Implemented Features:** Multilingual Support.
*   **Requirements:** UI-006.
*   **Dependencies:** `intl` package, `flutter_localizations`.
*   **Class:** `AppLocalizations`
*   **Methods:**
    *   `static AppLocalizations? of(BuildContext context)`: Standard method to get instance.
    *   `static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();`
    *   `static const List<LocalizationsDelegate<dynamic>> localizationsDelegates = [...]` (includes `delegate`, `GlobalMaterialLocalizations.delegate`, etc.)
    *   `static const List<Locale> supportedLocales = [...]` (e.g., `Locale('en', 'US')`, `Locale('en', 'GB')`, `Locale('es', 'ES')`, etc. for UI-006)
    *   Accessor methods for each translatable string key defined in ARB files (generated by `intl_utils` or manually written based on ARB).
      dart
      // Example:
      // String get appTitle => Intl.message('CreativeFlow AI', name: 'appTitle', desc: 'The title of the application');
      // String get loginButton => Intl.message('Login', name: 'loginButton', desc: 'Label for login button');
      
*   **ARB files:**
    *   `lib/core/l10n/intl_en.arb` (and `intl_en_US.arb`, `intl_en_GB.arb` if region-specific overrides needed)
    *   `lib/core/l10n/intl_es.arb` (and `intl_es_ES.arb`, `intl_es_MX.arb`)
    *   `lib/core/l10n/intl_fr.arb` (and `intl_fr_FR.arb`)
    *   `lib/core/l10n/intl_de.arb` (and `intl_de_DE.arb`)
    *   Each ARB file contains key-value pairs for translations.
*   **Localization BLoC (`lib/core/bloc/localization_bloc.dart`):**
    *   Manages current `Locale`.
    *   Events: `ChangeLocaleEvent(Locale newLocale)`.
    *   States: `LocalizationState(Locale currentLocale)`.
    *   Persists chosen locale using `shared_preferences`.
*   **Documentation:** Instructions on adding new strings and new languages, managing ARB files.

#### 3.3.9 Core Widgets

##### 3.3.9.1 `lib/core/widgets/offline_banner.dart`
*   **Purpose:** Visually informs the user about offline network status (UI-004).
*   **Implemented Features:** Offline Status Indication.
*   **Requirements:** UI-004.
*   **Dependencies:** `ConnectivityBloc`.
*   **Class:** `OfflineBanner extends StatelessWidget`
*   **Methods:**
    *   `Widget build(BuildContext context)`:
        *   Use `BlocBuilder<ConnectivityBloc, ConnectivityState>`.
        *   If `state is ConnectivityOffline`, return a visible banner (e.g., `Container` with distinct background color, `Text` widget saying "You are offline").
        *   If `state is ConnectivityOnline` or initial, return `SizedBox.shrink()` or an empty `Container`.
        *   Ensure the banner is accessible (UI-005): sufficient contrast, screen reader announcements.
*   **Documentation:** How to integrate into the main app layout.

#### 3.3.10 Core BLoCs

##### 3.3.10.1 `lib/core/bloc/connectivity_bloc.dart`
*   **Purpose:** Monitors and broadcasts network connectivity status (UI-004).
*   **Implemented Features:** Network Status Monitoring.
*   **Requirements:** UI-004.
*   **Dependencies:** `connectivity_plus` package, `flutter_bloc`.
*   **Events:**
    *   `_ConnectivityChanged(ConnectivityResult result)` (private internal event)
*   **States:**
    *   `ConnectivityInitial`
    *   `ConnectivityOnline`
    *   `ConnectivityOffline`
*   **Class:** `ConnectivityBloc extends Bloc<ConnectivityEvent, ConnectivityState>`
*   **Constructor:**
    *   Initialize with `ConnectivityInitial`.
    *   Subscribe to `Connectivity().onConnectivityChanged`. On new `ConnectivityResult`, add `_ConnectivityChanged` event.
    *   Perform an initial connectivity check.
*   **`mapEventToState` logic:**
    *   On `_ConnectivityChanged`: if `result == ConnectivityResult.none`, emit `ConnectivityOffline`. Else, emit `ConnectivityOnline`.
*   **`close()` method:** Cancel the stream subscription.
*   **Documentation:** How to use this BLoC to react to connectivity changes.


### 3.4 Feature Modules (Example: Editor)

#### 3.4.1 Editor - Presentation Layer

##### 3.4.1.1 `lib/features/editor/presentation/screens/editor_screen.dart`
*   **Purpose:** Provides the UI for creating and editing creatives (REQ-019, UI-004).
*   **Implemented Features:** Creative Editing UI, Touch Workflows, Gesture Handling, Offline/Sync UI for Editor.
*   **Requirements:** REQ-019, UI-004, Section 6.2, REQ-020 (camera/voice input).
*   **Dependencies:** `EditorBloc`, `OfflineSyncBloc` (if editor sync is separate), `CanvasWidget`, `ToolPaletteWidget`, `AssetPickerWidget`, `CameraInputWidget`, `VoiceInputWidget`.
*   **Class:** `EditorScreen extends StatefulWidget` (or `StatelessWidget` if state is fully in BLoC and passed down)
    *   `final String projectId;`
*   **State (`_EditorScreenState`):**
    *   Initialize `EditorBloc` (e.g., `context.read<EditorBloc>().add(LoadEditorProject(projectId))`).
*   **`build(BuildContext context)`:**
    *   `BlocConsumer<EditorBloc, EditorState>` for main content and listening to side effects (saving, errors).
    *   `BlocBuilder<ConnectivityBloc, ConnectivityState>` to show offline hints within the editor context if needed.
    *   Layout: `Scaffold` with `AppBar` (actions: Save, Share, etc.). Body containing:
        *   `CanvasWidget`: Renders the creative, handles gestures.
        *   `ToolPaletteWidget`: Displays available editing tools.
        *   `AssetPickerWidget`: Allows selection of assets.
        *   `CameraInputWidget`: Button/icon to launch camera (REQ-020).
        *   `VoiceInputWidget`: Button/icon for voice prompt input (REQ-020).
    *   Gesture Detectors on `CanvasWidget` for pinch-to-zoom, drag, tap (UI-004).
    *   Display loading indicators, error messages from `EditorBloc`.
    *   Offline Indicator: May show a specific "Offline Editing Mode" message derived from `ConnectivityBloc` and `EditorBloc` state.
*   **Documentation:** Description of UI elements and user flows.

##### 3.4.1.2 `lib/features/editor/presentation/bloc/editor_bloc.dart`
*   **Purpose:** Handles business logic and state for the creative editor (REQ-019, REQ-019.1).
*   **Implemented Features:** Editor State Management, Load/Save Project Logic, Offline Change Queuing.
*   **Requirements:** REQ-019, REQ-019.1.
*   **Dependencies:** `CreativeRepository` (abstract), `SyncService`, `ConnectivityBloc`.
*   **Events:**
    *   `LoadEditorProject(String projectId)`
    *   `SaveEditorProject(Project projectData)`
    *   `AddElementToCanvas(EditorElement element)`
    *   `UpdateElementOnCanvas(EditorElement element)`
    *   `DeleteElementFromCanvas(String elementId)`
    *   `UndoCanvasChange`
    *   `RedoCanvasChange`
    *   `ApplyVoicePrompt(String promptText)`
    *   `MediaCaptured(XFile mediaFile, MediaType type)`
*   **States:**
    *   `EditorInitial`
    *   `EditorLoading`
    *   `EditorLoaded(Project project, List<EditorElement> canvasElements, bool isOffline)`
    *   `EditorSaving`
    *   `EditorSaveSuccess`
    *   `EditorError(String message)`
*   **Class:** `EditorBloc extends Bloc<EditorEvent, EditorState>`
*   **Constructor:** `EditorBloc({required this.creativeRepository, required this.syncService, required this.connectivityBloc})`
*   **`mapEventToState` logic:**
    *   `LoadEditorProject`: Fetch from `creativeRepository`. If offline, load local. Emit `EditorLoaded`.
    *   `SaveEditorProject`:
        *   Check `connectivityBloc.state`.
        *   If `ConnectivityOffline`: `syncService.queueChange(...)` for project update. Emit `EditorLoaded` (optimistic update with offline flag).
        *   If `ConnectivityOnline`: `creativeRepository.saveProjectRemote(...)`. Emit `EditorSaving` then `EditorSaveSuccess` or `EditorError`.
    *   Element manipulations: Update local state (`canvasElements`). Optimistically update UI. Queue changes via `SyncService` if offline or for collaborative updates.
    *   `ApplyVoicePrompt`: Process prompt, potentially trigger AI generation flow (which might be another BLoC or service call).
    *   `MediaCaptured`: Add media to canvas elements, potentially upload to `AssetRepository` via `SyncService` if needed.
*   **Documentation:** State transitions, event handling, and interaction with services.

##### 3.4.1.3 `lib/features/editor/presentation/widgets/camera_input_widget.dart`
*   **Purpose:** UI element for camera access (REQ-020, UI-004).
*   **Implemented Features:** Camera Capture UI.
*   **Requirements:** REQ-020, UI-004.
*   **Dependencies:** `CameraService`, `PermissionHandlerService`.
*   **Class:** `CameraInputWidget extends StatelessWidget`
    *   `final Function(XFile mediaFile) onMediaCaptured;`
*   **`build(BuildContext context)`:**
    *   Return an `IconButton` or `ElevatedButton`.
    *   `onPressed`: async function that:
        *   Calls `CameraService.pickImageFromCamera()` or `pickVideoFromCamera()`.
        *   If `XFile` is returned, call `onMediaCaptured(mediaFile)`.
        *   Handle permissions gracefully using `PermissionHandlerService` and show dialogs if denied.
*   **Documentation:** How to use the widget and handle its callback.

#### 3.4.2 Editor - Data Layer

##### 3.4.2.1 `lib/features/editor/data/datasources/creative_local_datasource.dart`
*   **Purpose:** Implements local data access for creative projects/assets (REQ-019).
*   **Implemented Features:** Local Project/Asset CRUD.
*   **Requirements:** REQ-019.
*   **Dependencies:** `AppLocalDatabase`, DAOs (e.g., `ProjectDao`, `AssetDao` - these would be generated by Drift based on table definitions and DAO abstract classes).
*   **Interface:** `abstract class ICreativeLocalDataSource { ... }`
*   **Class:** `CreativeLocalDataSourceImpl implements ICreativeLocalDataSource`
    *   `final ProjectDao projectDao;`
    *   `final AssetDao assetDao;`
*   **Methods:**
    *   `Future<ProjectData?> getProjectById(String projectId)`: Use `projectDao.getProject(projectId)`. Map Drift `ProjectData` to domain `ProjectModel`.
    *   `Future<void> saveProject(ProjectModel project)`: Map domain `ProjectModel` to Drift `ProjectCompanion` and call `projectDao.insertOrUpdateProject()`.
    *   `Future<List<AssetModel>> getAssetsForProject(String projectId)`
    *   `Future<void> saveAsset(AssetModel asset)`
*   **DAO Definitions (Example - in separate files like `project_dao.dart`):**
    dart
    // In project_dao.dart
    @DriftAccessor(tables: [LocalProjects]) // LocalProjects from local_database.dart
    class ProjectDao extends DatabaseAccessor<AppLocalDatabase> with _$ProjectDaoMixin {
      ProjectDao(AppLocalDatabase db) : super(db);
      Future<LocalProject?> getProject(String id) => (select(localProjects)..where((tbl) => tbl.id.equals(id))).getSingleOrNull();
      Future<int> insertOrUpdateProject(LocalProjectsCompanion project) => into(localProjects).insertOnConflictUpdate(project);
      // ... other methods
    }
    
*   **Documentation:** Methods provided and their interaction with Drift DAOs.


### 3.5 Other Core Components (High-Level Design)

#### 3.5.1 `lib/core/bloc/auth_bloc.dart` (Illustrative)
*   **Purpose:** Manages user authentication state and login/logout/registration processes.
*   **Events:** `LoginRequested`, `LogoutRequested`, `RegistrationAttempted`, `SocialLoginInitiated`.
*   **States:** `AuthInitial`, `AuthLoading`, `Authenticated(User user)`, `Unauthenticated`, `AuthFailure(String error)`.
*   **Dependencies:** `AuthRepository` (which uses `ApiClient` and secure storage for tokens).
*   **Logic:** Handles API calls for auth, token storage/retrieval, updates app-wide auth state.

#### 3.5.2 `lib/core/theme/theme_bloc.dart` (Illustrative)
*   **Purpose:** Manages app theme (light/dark).
*   **Events:** `ToggleThemeEvent`.
*   **States:** `ThemeState(ThemeMode themeMode)`.
*   **Dependencies:** `shared_preferences` to persist theme choice.
*   **Logic:** Loads and saves theme preference. Emits new state for UI to rebuild with new theme.

#### 3.5.3 `lib/features/settings/presentation/screens/accessibility_settings_screen.dart`
*   **Purpose:** UI for customizing accessibility preferences (UI-005).
*   **Implemented Features:** Accessibility Configuration UI.
*   **Requirements:** UI-005.
*   **Dependencies:** `AccessibilitySettingsBloc` (or similar for managing these settings), `shared_preferences`.
*   **Class:** `AccessibilitySettingsScreen extends StatelessWidget`
*   **`build(BuildContext context)`:**
    *   Provide options to:
        *   Adjust font size scaling (e.g., a slider that updates a BLoC state, which then influences `MaterialApp.builder`'s `MediaQuery` wrapping).
        *   Toggle a high-contrast mode (triggers `ThemeBloc` to switch to a pre-defined high-contrast `ThemeData`).
        *   Link to OS-level accessibility settings.
    *   Ensure all elements on this screen are fully accessible (labels, tap targets).
*   **`AccessibilitySettingsBloc` (Illustrative):**
    *   Manages `textScaleFactorMultiplier` and `isHighContrastEnabled` state.
    *   Persists settings to `shared_preferences`.
    *   `ThemeBloc` might listen to `isHighContrastEnabled` from this BLoC or a shared service.

## 4. Data Management

### 4.1 Local Storage (SQLite via Drift)
*   **Schema:** Defined in `lib/core/storage/local_database.dart` (see section 3.3.5.1). Key tables:
    *   `LocalProjects`: Stores project metadata and potentially last known canvas state for offline editing.
    *   `LocalAssets`: Stores metadata and local file paths for assets available offline.
    *   `OfflineSyncQueueItems`: Queues local changes (CRUD operations) that need to be synced to the backend.
*   **Data Access Objects (DAOs):** Defined per entity within feature modules (e.g., `ProjectDao`, `AssetDao`, `OfflineSyncQueueDao`).
*   **Offline Data Strategy (REQ-019):**
    *   Users can perform basic editing tasks offline.
    *   Changes are saved to the local SQLite database.
    *   An entry is added to `OfflineSyncQueueItems` for each change.
*   **Storage Limits:** `AppConstants.maxOfflineProjects` can be used to manage local storage, prompting users if limits are approached.

### 4.2 Synchronization (REQ-019.1)
*   Managed by `SyncService` (`lib/core/services/sync_service.dart`).
*   **Triggers:**
    *   App launch (if online).
    *   Transition from offline to online (via `ConnectivityBloc`).
    *   Periodically (optional, configurable).
    *   After a user explicitly saves content that couldn't be synced immediately.
*   **Process:**
    1.  `SyncService` fetches pending items from `OfflineSyncQueueItems`.
    2.  For each item, attempts to send the operation to the backend via `ApiClient`.
    3.  **Conflict Resolution:**
        *   **Non-Collaborative Projects (Default):**
            *   Simple changes: "Last write wins" (client or server timestamp, to be defined). If client change is later, it might be re-attempted after fetching server state. If server is later, local changes might be overwritten or user prompted.
            *   Complex changes (structural): User prompted via UI event (e.g., show diff, choose version).
        *   **Collaborative Projects (REQ-013, REQ-8-004 - future phase if not MVP):**
            *   Utilize OT/CRDT mechanisms. The `SyncService` would interact with a `CollaborationService` (which might be part of the mobile app or a backend service).
            *   CRDT data from `LocalProjects.collaborationStateJson` would be merged.
            *   If automatic merge fails, flag conflict and notify users for manual resolution (UI-004).
    4.  On successful sync of an item, remove it from `OfflineSyncQueueItems`.
    5.  Handle API errors, retries (with exponential backoff for transient errors), and unrecoverable errors (flag for user/support).
*   **UI Feedback (UI-004):**
    *   Persistent offline/online indicator (`OfflineBanner`).
    *   Progress indicators during active sync.
    *   Clear messages for sync success, failure, and conflicts requiring attention.

### 4.3 Secure Storage for Sensitive Data
*   Auth tokens (`access_token`, `refresh_token`) should be stored securely. `shared_preferences` is generally not secure enough for sensitive tokens. Consider using:
    *   `flutter_secure_storage`: For storing sensitive data like auth tokens.
    *   `AuthTokenRepository` would abstract this.

## 5. State Management Strategy (BLoC)

*   **Primary Pattern:** `flutter_bloc` will be used for managing state across the application.
*   **Global BLoCs:** Provided at the root of the application (`app.dart`) for app-wide concerns:
    *   `AuthBloc`: Manages authentication state, user object.
    *   `ThemeBloc`: Manages light/dark theme preference.
    *   `LocalizationBloc`: Manages current app locale.
    *   `ConnectivityBloc`: Monitors network status.
*   **Feature BLoCs:** Each feature (e.g., Editor, Settings, ProjectList) will have its own BLoCs to manage its specific state and business logic.
    *   Example: `EditorBloc`, `ProjectListBloc`, `BrandKitBloc`.
*   **BLoC Structure:**
    *   **Events:** Represent user interactions or external triggers.
    *   **States:** Represent the UI state; immutable.
    *   **Bloc:** Receives events, processes them (interacts with repositories/services), and emits new states.
*   **Dependency Injection:**
    *   BLoCs will receive dependencies (Repositories, Services) via constructor injection.
    *   `BlocProvider` will be used to make BLoCs available in the widget tree.
    *   `GetIt` can be used for registering and locating services/repositories if preferred over manual DI or deep provider nesting.

## 6. Navigation Strategy

*   **Method:** Primarily Navigator 1.0 with named routes using `onGenerateRoute` in `AppRouter` (as defined in 3.3.3.2).
*   **Route Definitions:** Centralized in `RoutePaths` (3.3.3.1).
*   **Deep Linking:** Handled by `DeepLinkHandler` (3.3.3.3), which parses incoming URIs and uses `AppRouter` to navigate.
*   **Guards:** Route guards can be implemented within `onGenerateRoute` by checking `AuthBloc` state before returning a route to a protected screen. If unauthenticated, redirect to `RoutePaths.login`.

## 7. Error Handling and Logging

*   **API Errors:** `ApiClient` will parse HTTP responses and throw custom, typed exceptions (e.g., `ApiException`, `UnauthorizedException`, `NotFoundException`).
*   **BLoC Error Handling:** BLoCs will catch exceptions from repositories/services and emit specific error states (e.g., `EditorError(message)`). UI will listen to these states and display user-friendly messages.
*   **Global Error Handling (for unhandled Flutter errors):** In `main.dart`:
    *   `FlutterError.onError`: Catches framework errors.
    *   `PlatformDispatcher.instance.onError`: Catches other unhandled Dart errors.
    *   These will log to `FirebaseCrashlytics` via `AnalyticsService.recordError()`.
*   **Logging:**
    *   Use a standard logging package (e.g., `logging`).
    *   Configure different log levels for dev/prod.
    *   Log key events, BLoC transitions, API requests/responses (scrubbed), and errors.
    *   `AnalyticsService` will also be used for logging specific user interaction events to Firebase.

## 8. API Integration (API Gateway)

*   All backend communication will go through the `ApiClient` (`lib/core/network/api_client.dart`).
*   `ApiClient` will target the API Gateway URL specified in `AppConfig`.
*   **Authentication:** `ApiClient` will attach JWT Bearer tokens to authenticated requests. It should include logic to handle token refresh if a 401 is received due to an expired access token (requires refresh token mechanism).
*   **Request/Response Models:** Define Dart classes for request payloads and expected response DTOs for type safety (typically in `features/.../data/models/remote/`).

## 9. Native Integrations (Platform Channels)

While Flutter plugins cover most native functionalities, direct platform channel usage might be needed for highly custom or performance-critical features not available as plugins.
*   **Camera (`camera` or `image_picker` plugin):** Managed by `CameraService` (3.3.6.4).
*   **Push Notifications (`firebase_messaging` plugin):** Managed by `PushNotificationService` (3.3.6.2).
*   **Voice-to-Text (`speech_to_text` plugin):** Managed by `VoiceInputService` (3.3.6.5).
*   **Deep Linking (`uni_links` plugin):** Managed by `DeepLinkHandler` (3.3.3.3).
*   **Permissions (`permission_handler` plugin):** Managed by `PermissionHandlerService` (3.3.6.6).
*   **Generic Platform Channel Invocation:** If a unique native feature is needed:
    1.  Define method channel name (e.g., `com.creativeflow/custom_feature`).
    2.  Implement native code (Swift/Kotlin) to handle method calls.
    3.  Create a Dart wrapper service to invoke platform channel methods.

## 10. Accessibility (UI-005, NFR-007, REQ-14-001)

*   **Semantic Widgets:** Use Flutter's semantic widgets (`Semantics`, `MergeSemantics`, `ExcludeSemantics`) appropriately.
*   **Labels & Hints:** Provide `semanticLabel` for IconButtons and other non-textual interactive elements.
*   **Tap Targets:** Ensure all interactive elements have a minimum tap target size of 48x48 dp (as per Material Design and WCAG recommendations).
*   **Color Contrast:** `AppTheme` will define color schemes with sufficient contrast ratios (AA level).
*   **Font Scaling:** UI should adapt to user's system font size settings. Use responsive layouts and `TextScaler` (or older `textScaleFactor`). `AppTypography` should define scalable text styles.
*   **Focus Management:** Ensure logical focus order for keyboard/switch access users.
*   **Testing:** Manual testing with VoiceOver (iOS) and TalkBack (Android). Use Flutter's accessibility inspector.

## 11. Localization (UI-006)

*   **Framework:** Flutter's built-in localization system using the `intl` package.
*   **String Management:** ARB files (`.arb`) for each supported language/locale (e.g., `intl_en_US.arb`, `intl_es_ES.arb`) located in `lib/core/l10n/`.
*   **`AppLocalizations` class (`lib/core/l10n/app_localizations.dart`):** Generated or manually created delegate and accessor methods for translated strings.
*   **Supported Locales:** Defined in `AppLocalizations.supportedLocales` (en-US, en-GB, es-ES, es-MX, fr-FR, de-DE initially).
*   **Locale Switching:** Managed by `LocalizationBloc`, persisting choice in `shared_preferences`. `MaterialApp.locale` will be set from this BLoC.
*   **Layout Adaptability:** UI widgets must be designed to handle varying text lengths (e.g., using `Expanded`, `Flexible`, `FittedBox`, or text wrapping).
*   **Date/Time/Number Formatting:** Use `intl` package's `DateFormat` and `NumberFormat` with the current locale.

## 12. Performance Considerations

*   **Launch Time (NFR-001):**
    *   Minimize `main.dart` initialization work. Defer non-critical initializations.
    *   Use code splitting (deferred loading of libraries/features) if app size becomes an issue.
    *   Optimize asset sizes.
    *   Monitor with Firebase Performance Monitoring or dev tools.
*   **UI Responsiveness:**
    *   Build widgets efficiently (use `const` constructors, avoid unnecessary rebuilds).
    *   Offload heavy computations to Isolates if they block the UI thread.
    *   Optimize list rendering (`ListView.builder`).
    *   Profile widget rebuilds using Flutter DevTools.
*   **Offline Mode Performance:**
    *   Efficient SQLite queries via Drift.
    *   Optimize local data structures.
*   **Crash-Free Rate (NFR-001):**
    *   Comprehensive error handling.
    *   Integration with `FirebaseCrashlytics`.
    *   Thorough testing.

## 13. Security Considerations

*   **API Communication:** Use HTTPS for all API calls (enforced by `ApiClient` targeting HTTPS URLs).
*   **Token Storage:** Store authentication tokens securely using `flutter_secure_storage` (abstracted by an `AuthTokenRepository`). Do not use `shared_preferences` for sensitive tokens.
*   **Local Data Encryption (SQLite):** While Drift itself doesn't encrypt the SQLite file by default, if highly sensitive data is stored offline (beyond cached project data), consider plugins like `sqlcipher_flutter_libs` for whole database encryption or encrypting specific fields at the application layer before saving. This needs careful consideration of key management. (REQ-DA-009 from overall SRS implies encryption at rest for PostgreSQL/MinIO; similar care should be given to sensitive local data if any).
*   **Input Validation:** Validate user inputs on the client-side for better UX, but always re-validate on the backend.
*   **Deep Link Security:** Validate parameters from deep links carefully to prevent injection or unintended navigation.
*   **Platform Channel Security:** If using platform channels, validate data passed between Dart and native code.
*   **Dependency Management:** Regularly update dependencies to patch known vulnerabilities. Use `flutter pub outdated`.

## 14. Testing Strategy (Brief Overview)

*   **Unit Tests (`flutter_test`, `bloc_test`):**
    *   For BLoCs, utility functions, repository logic (with mocked data sources).
    *   Aim for high coverage, especially for business logic.
*   **Widget Tests (`flutter_test`):**
    *   Test individual widgets in isolation, verifying UI rendering and basic interactions.
*   **Integration Tests (`integration_test` package from `flutter_test` or `flutter_driver` for older style):**
    *   Test feature flows, interactions between widgets, BLoCs, and services (mocking network layer).
    *   Focus on REQ-019 offline/sync scenarios, REQ-020 native features.
*   **E2E Tests (Appium or Flutter's `integration_test` running on devices/emulators):**
    *   For critical user journeys (registration, login, core creative flow). This is mentioned in QA-001.
*   **Manual Testing:** For usability, accessibility (WCAG 2.1 AA), visual consistency, and exploratory testing.

This SDS provides a comprehensive foundation for the development of the `CreativeFlow.MobileApp.Flutter` application. Specific implementation details for each widget, BLoC interaction, and data model will be further refined during the development sprints.