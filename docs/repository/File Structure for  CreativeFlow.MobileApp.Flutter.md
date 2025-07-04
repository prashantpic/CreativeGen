# Specification

# 1. Files

- **Path:** pubspec.yaml  
**Description:** Flutter project manifest file. Defines project metadata, dependencies (e.g., provider, bloc, drift, firebase_core, firebase_messaging, camera, http, intl, flutter_localizations, shared_preferences), and assets (images, fonts).  
**Template:** Flutter Project Manifest  
**Dependency Level:** 0  
**Name:** pubspec  
**Type:** Configuration  
**Relative Path:** ../pubspec.yaml  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    - Asset Declaration
    
**Requirement Ids:**
    
    - Section 2.1 (Mobile Tech)
    - REQ-019
    - REQ-020
    - INT-004
    
**Purpose:** Declares project dependencies, assets, and general Flutter project configuration.  
**Logic Description:** List all necessary third-party libraries like flutter_bloc, drift, firebase_core, firebase_messaging, camera, http, intl, shared_preferences. Declare paths to assets like images and fonts. Configure flutter_lints and other linters.  
**Documentation:**
    
    - **Summary:** Manages project dependencies and fundamental configuration for the Flutter application.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** analysis_options.yaml  
**Description:** Static analysis configuration for Dart. Enforces coding standards, linting rules (e.g., from flutter_lints, effective_dart), and code metrics to maintain code quality.  
**Template:** Dart Analysis Configuration  
**Dependency Level:** 0  
**Name:** analysis_options  
**Type:** Configuration  
**Relative Path:** ../analysis_options.yaml  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Code Style Enforcement
    - Static Analysis
    
**Requirement Ids:**
    
    - NFR-008 (REQ-SDS-001 from SRS)
    
**Purpose:** Configures Dart static analysis options, linters, and code style rules.  
**Logic Description:** Include recommended lint sets like `flutter_lints`. Customize rules as per project coding standards, aligning with 'Effective Dart' practices. Enable stricter type checks and analysis options.  
**Documentation:**
    
    - **Summary:** Defines static analysis rules to ensure code quality and consistency.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** lib/main.dart  
**Description:** Main entry point for the Flutter application. Initializes essential services (Firebase, Dependency Injection, Logging), sets up the root application widget, and potentially handles initial routing or splash screen logic.  
**Template:** Flutter App Entry Point  
**Dependency Level:** 10  
**Name:** main  
**Type:** Application  
**Relative Path:** main.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** void  
    
**Implemented Features:**
    
    - App Initialization
    - Service Setup
    - Root Widget Invocation
    
**Requirement Ids:**
    
    - NFR-001 (Mobile App Launch)
    - Section 5.2.1
    
**Purpose:** Initializes the Flutter application, sets up global dependencies, and runs the main app widget.  
**Logic Description:** Ensure `WidgetsFlutterBinding.ensureInitialized()` is called. Initialize FirebaseApp, dependency injector (e.g., GetIt), logging. Potentially show a splash screen while initializations occur to meet NFR-001. Run the `CreativeFlowApp` widget.  
**Documentation:**
    
    - **Summary:** The main function that bootstraps and runs the Flutter application.
    
**Namespace:** CreativeFlow.MobileApp  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** lib/app.dart  
**Description:** The root widget of the Flutter application. Configures global theme, localization, navigation (router), and provides top-level BLoC providers or state management setup.  
**Template:** Flutter Root Widget  
**Dependency Level:** 9  
**Name:** CreativeFlowApp  
**Type:** Widget  
**Relative Path:** app.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - MVVM-like with BLoC
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Global Theming
    - Localization Setup
    - Root Navigation
    - Global State Providers
    
**Requirement Ids:**
    
    - UI-006
    - NFR-007 (Mobile Usability)
    - Section 6.2
    
**Purpose:** Defines the root structure of the application, including theme, localization, and navigation.  
**Logic Description:** Return a MaterialApp (or CupertinoApp). Configure `theme` and `darkTheme` using `AppTheme`. Set up `localizationsDelegates` and `supportedLocales` for UI-006. Define `onGenerateRoute` or use a Navigator 2.0 router from `core/navigation`. Wrap with global BLoC providers (e.g., AuthBloc, ThemeBloc, ConnectivityBloc).  
**Documentation:**
    
    - **Summary:** The main application widget that sets up the overall app structure and global configurations.
    
**Namespace:** CreativeFlow.MobileApp  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/config/app_config.dart  
**Description:** Application configuration settings, such as API base URLs, feature flags, and environment-specific parameters (dev, staging, prod).  
**Template:** Dart Configuration Class  
**Dependency Level:** 0  
**Name:** AppConfig  
**Type:** Configuration  
**Relative Path:** core/config/app_config.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - ConfigurationProvider
    
**Members:**
    
    - **Name:** apiBaseUrl  
**Type:** String  
**Attributes:** static final  
    - **Name:** environment  
**Type:** String  
**Attributes:** static final  
    - **Name:** enableOfflineMode  
**Type:** bool  
**Attributes:** static final  
    
**Methods:**
    
    - **Name:** initialize  
**Parameters:**
    
    - String environment
    
**Return Type:** Future<void>  
**Attributes:** static Future  
    
**Implemented Features:**
    
    - Environment Configuration
    - Feature Flag Management
    
**Requirement Ids:**
    
    - REQ-019
    
**Purpose:** Provides centralized access to application configuration values based on the current environment.  
**Logic Description:** Load environment-specific configurations, potentially from .env files or build flavors. Define constants for API endpoints, third-party keys (though these should ideally be injected, not hardcoded here for production), and feature toggles.  
**Documentation:**
    
    - **Summary:** Manages application-wide configuration settings and environment variables.
    
**Namespace:** CreativeFlow.MobileApp.Core.Config  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/constants/app_constants.dart  
**Description:** Application-wide constants, such as default padding, animation durations, storage keys, or numerical limits.  
**Template:** Dart Constants File  
**Dependency Level:** 0  
**Name:** AppConstants  
**Type:** Constants  
**Relative Path:** core/constants/app_constants.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** defaultPadding  
**Type:** double  
**Attributes:** const  
    - **Name:** maxOfflineProjects  
**Type:** int  
**Attributes:** const  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Constants
    
**Requirement Ids:**
    
    - REQ-019
    
**Purpose:** Defines globally used constant values to avoid magic numbers/strings and ensure consistency.  
**Logic Description:** Declare const variables for UI dimensions, timeouts, default settings, shared preference keys, database table/column names etc.  
**Documentation:**
    
    - **Summary:** Contains application-level constant values.
    
**Namespace:** CreativeFlow.MobileApp.Core.Constants  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/navigation/app_router.dart  
**Description:** Manages application navigation logic, defining routes and handling navigation events. May use Navigator 1.0 (onGenerateRoute) or Navigator 2.0 (RouterDelegate, RouteInformationParser).  
**Template:** Flutter Router Class  
**Dependency Level:** 8  
**Name:** AppRouter  
**Type:** Navigation  
**Relative Path:** core/navigation/app_router.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Router
    
**Members:**
    
    
**Methods:**
    
    - **Name:** onGenerateRoute  
**Parameters:**
    
    - RouteSettings settings
    
**Return Type:** Route<dynamic>?  
**Attributes:** static  
    - **Name:** navigateToEditor  
**Parameters:**
    
    - BuildContext context
    - String projectId
    
**Return Type:** void  
**Attributes:** static  
    
**Implemented Features:**
    
    - Route Definition
    - Navigation Handling
    
**Requirement Ids:**
    
    - Section 6.2
    
**Purpose:** Centralizes navigation logic and route definitions for the application.  
**Logic Description:** Define static route names in `RoutePaths`. Implement `onGenerateRoute` to return appropriate `MaterialPageRoute` or `CupertinoPageRoute` for each route. Handle route arguments. Implement helper methods for typed navigation.  
**Documentation:**
    
    - **Summary:** Provides routing and navigation services for the application.
    
**Namespace:** CreativeFlow.MobileApp.Core.Navigation  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/navigation/route_paths.dart  
**Description:** Defines constant strings for all named routes in the application, ensuring type safety and avoiding typos in navigation calls.  
**Template:** Dart Constants File  
**Dependency Level:** 0  
**Name:** RoutePaths  
**Type:** Constants  
**Relative Path:** core/navigation/route_paths.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** login  
**Type:** String  
**Attributes:** const  
    - **Name:** home  
**Type:** String  
**Attributes:** const  
    - **Name:** editor  
**Type:** String  
**Attributes:** const  
    - **Name:** settings  
**Type:** String  
**Attributes:** const  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Route Name Constants
    
**Requirement Ids:**
    
    - Section 6.2
    
**Purpose:** Central repository for all named route paths used in the application.  
**Logic Description:** Define `const String` variables for each screen or navigation destination. This helps prevent typos and makes route management easier.  
**Documentation:**
    
    - **Summary:** Contains string constants for named navigation routes.
    
**Namespace:** CreativeFlow.MobileApp.Core.Navigation  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/navigation/deep_link_handler.dart  
**Description:** Handles incoming deep links, parsing them and navigating to the appropriate screen or content within the application.  
**Template:** Flutter Service Class  
**Dependency Level:** 7  
**Name:** DeepLinkHandler  
**Type:** Service  
**Relative Path:** core/navigation/deep_link_handler.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** init  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** void  
**Attributes:** static  
    - **Name:** handleLink  
**Parameters:**
    
    - Uri link
    - BuildContext context
    
**Return Type:** Future<void>  
**Attributes:** static  
    
**Implemented Features:**
    
    - Deep Link Processing
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** Manages deep linking functionality, allowing the app to respond to external URLs.  
**Logic Description:** Initialize deep link listeners (e.g., using `uni_links` package). Parse incoming URIs to extract route and parameters. Use `AppRouter` to navigate to the correct screen. Handle authentication checks if necessary before navigating.  
**Documentation:**
    
    - **Summary:** Processes deep links to navigate users to specific content within the app.
    
**Namespace:** CreativeFlow.MobileApp.Core.Navigation  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/network/api_client.dart  
**Description:** Provides a wrapper around an HTTP client (e.g., dio or http package) to make API calls to the backend. Handles base URL, headers, interceptors for auth tokens, error handling, and request/response logging.  
**Template:** Dart HTTP Client Wrapper  
**Dependency Level:** 1  
**Name:** ApiClient  
**Type:** Network  
**Relative Path:** core/network/api_client.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - ServiceAgent
    - Gateway
    
**Members:**
    
    - **Name:** _dio  
**Type:** Dio  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** get  
**Parameters:**
    
    - String path
    - Map<String, dynamic>? queryParameters
    
**Return Type:** Future<Response>  
**Attributes:** Future  
    - **Name:** post  
**Parameters:**
    
    - String path
    - dynamic data
    
**Return Type:** Future<Response>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - HTTP Request Handling
    - Authentication Interceptor
    - Error Handling
    
**Requirement Ids:**
    
    - Section 5.2.1
    
**Purpose:** Centralizes network request logic, managing API calls, authentication, and error responses.  
**Logic Description:** Initialize Dio with `BaseOptions` (baseUrl from AppConfig, connectTimeout, receiveTimeout). Add interceptors for: adding JWT tokens to headers, refreshing tokens if necessary, logging requests/responses, and standardizing error handling from API responses.  
**Documentation:**
    
    - **Summary:** A client for making HTTP requests to the backend API, including authentication and error handling.
    
**Namespace:** CreativeFlow.MobileApp.Core.Network  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/storage/local_database.dart  
**Description:** Defines the SQLite database schema using Drift (formerly Moor). Includes table definitions, DAOs (Data Access Objects) for CRUD operations on local data, and database connection setup. This is critical for offline editing (REQ-019).  
**Template:** Drift Database Definition  
**Dependency Level:** 0  
**Name:** AppLocalDatabase  
**Type:** Storage  
**Relative Path:** core/storage/local_database.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - DAO
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Local Data Persistence
    - Offline Storage Schema
    
**Requirement Ids:**
    
    - REQ-019
    - REQ-019.1
    
**Purpose:** Defines the local SQLite database structure and provides access methods using Drift.  
**Logic Description:** Define Drift tables for projects, assets, offline changes queue. Create DAOs for each table with methods for insert, update, delete, query. Initialize the database connection. A `part 'local_database.g.dart';` will be needed for generated code.  
**Documentation:**
    
    - **Summary:** Defines the local SQLite database schema and DAOs using Drift for offline data storage.
    
**Namespace:** CreativeFlow.MobileApp.Core.Storage  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/analytics_service.dart  
**Description:** Abstracts analytics tracking functionality. Integrates with Firebase Analytics or a similar platform (Mixpanel/Amplitude) as per INT-004. Provides methods to log events, user properties, and screen views.  
**Template:** Flutter Service Class  
**Dependency Level:** 1  
**Name:** AnalyticsService  
**Type:** Service  
**Relative Path:** core/services/analytics_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    - **Name:** _firebaseAnalytics  
**Type:** FirebaseAnalytics  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** logEvent  
**Parameters:**
    
    - String name
    - Map<String, Object>? parameters
    
**Return Type:** Future<void>  
**Attributes:** Future  
    - **Name:** setUserProperty  
**Parameters:**
    
    - String name
    - String? value
    
**Return Type:** Future<void>  
**Attributes:** Future  
    - **Name:** logScreenView  
**Parameters:**
    
    - String screenName
    
**Return Type:** Future<void>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - Event Tracking
    - User Property Logging
    - Screen View Tracking
    - Crash Reporting Setup
    
**Requirement Ids:**
    
    - INT-004
    - REQ-8-009
    - NFR-001 (Mobile App Crash-Free Rate implies crash reporting)
    
**Purpose:** Provides a unified interface for tracking user behavior and application events using an analytics platform.  
**Logic Description:** Initialize the chosen analytics SDK (e.g., FirebaseAnalytics.instance). Implement methods to abstract the SDK's event logging, user property setting, and screen view tracking functionalities. Handle potential initialization errors. Set up Firebase Crashlytics integration.  
**Documentation:**
    
    - **Summary:** Manages integration with analytics services like Firebase Analytics for event and user tracking.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/push_notification_service.dart  
**Description:** Handles receiving and processing push notifications from Firebase Cloud Messaging (FCM) or Apple Push Notification service (APNS). Manages token registration, foreground/background message handling, and navigation upon notification tap.  
**Template:** Flutter Service Class  
**Dependency Level:** 1  
**Name:** PushNotificationService  
**Type:** Service  
**Relative Path:** core/services/push_notification_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _firebaseMessaging  
**Type:** FirebaseMessaging  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** initialize  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Future<void>  
**Attributes:** Future  
    - **Name:** getFcmToken  
**Parameters:**
    
    
**Return Type:** Future<String?>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - Push Notification Handling
    - FCM Token Management
    
**Requirement Ids:**
    
    - REQ-020 (derived from REQ-8-006)
    
**Purpose:** Manages push notifications, including token handling and message processing.  
**Logic Description:** Initialize FirebaseMessaging. Request notification permissions. Handle FCM token generation and refresh. Set up listeners for `onMessage` (foreground), `onMessageOpenedApp` (background tap), and initial message. Parse notification payload and navigate or trigger actions accordingly.  
**Documentation:**
    
    - **Summary:** Integrates with Firebase Cloud Messaging to handle push notifications.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/sync_service.dart  
**Description:** Manages data synchronization between the local offline database and the cloud backend. Handles queuing of offline changes, conflict detection, and resolution strategies (REQ-019.1).  
**Template:** Flutter Service Class  
**Dependency Level:** 2  
**Name:** SyncService  
**Type:** Service  
**Relative Path:** core/services/sync_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Repository (for sync queue)
    
**Members:**
    
    - **Name:** _localDb  
**Type:** AppLocalDatabase  
**Attributes:** final  
    - **Name:** _apiClient  
**Type:** ApiClient  
**Attributes:** final  
    - **Name:** _connectivityBloc  
**Type:** ConnectivityBloc  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** queueChange  
**Parameters:**
    
    - OfflineChange change
    
**Return Type:** Future<void>  
**Attributes:** Future  
    - **Name:** processSyncQueue  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** Future  
    - **Name:** resolveConflict  
**Parameters:**
    
    - ConflictData conflict
    - ResolutionStrategy strategy
    
**Return Type:** Future<void>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - Offline Data Synchronization
    - Conflict Resolution Logic
    
**Requirement Ids:**
    
    - REQ-019
    - REQ-019.1
    - UI-004
    
**Purpose:** Orchestrates synchronization of local offline data with the backend server.  
**Logic Description:** Listen to connectivity changes. When online, iterate through queued local changes (stored in Drift). Send changes to the backend API. Handle API responses: success (remove from queue), failure (retry logic), conflict (trigger UI for user resolution or apply strategy like last-write-wins). Implements logic described in REQ-019.1 for merging and conflict resolution, potentially interacting with a collaboration service for CRDTs.  
**Documentation:**
    
    - **Summary:** Manages synchronization of offline data changes with the cloud backend, including conflict resolution.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/camera_service.dart  
**Description:** Provides an interface to interact with the device's native camera for capturing images and videos as per REQ-020.  
**Template:** Flutter Service Class  
**Dependency Level:** 1  
**Name:** CameraService  
**Type:** Service  
**Relative Path:** core/services/camera_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** pickImageFromCamera  
**Parameters:**
    
    
**Return Type:** Future<XFile?>  
**Attributes:** Future  
    - **Name:** pickVideoFromCamera  
**Parameters:**
    
    
**Return Type:** Future<XFile?>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - Camera Integration
    
**Requirement Ids:**
    
    - REQ-020
    - UI-004
    
**Purpose:** Abstracts device camera functionalities for capturing media.  
**Logic Description:** Use the `camera` or `image_picker` plugin. Request camera permissions. Provide methods to open the camera, allow user to capture image/video, and return the file path/object.  
**Documentation:**
    
    - **Summary:** Handles integration with the device camera to capture images and videos.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/voice_input_service.dart  
**Description:** Integrates with device's speech-to-text capabilities for voice prompt input (REQ-020).  
**Template:** Flutter Service Class  
**Dependency Level:** 1  
**Name:** VoiceInputService  
**Type:** Service  
**Relative Path:** core/services/voice_input_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** startListening  
**Parameters:**
    
    - Function(String) onResult
    
**Return Type:** Future<bool>  
**Attributes:** Future  
    - **Name:** stopListening  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** void  
    
**Implemented Features:**
    
    - Voice-to-Text Input
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** Provides voice-to-text functionality for inputting creative prompts.  
**Logic Description:** Use a speech-to-text plugin (e.g., `speech_to_text`). Request microphone permissions. Implement methods to start and stop listening, and provide callbacks for recognized text.  
**Documentation:**
    
    - **Summary:** Integrates with native speech recognition for voice input.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/theme/app_theme.dart  
**Description:** Defines the application's visual theme, including color schemes (light/dark), typography, button styles, and other UI component styling, adhering to UI-005 accessibility.  
**Template:** Flutter Theme Definition  
**Dependency Level:** 0  
**Name:** AppTheme  
**Type:** Theme  
**Relative Path:** core/theme/app_theme.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** lightTheme  
**Type:** ThemeData  
**Attributes:** static final  
    - **Name:** darkTheme  
**Type:** ThemeData  
**Attributes:** static final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - App Theming
    - Light/Dark Mode Support
    - Accessible Color Contrasts
    
**Requirement Ids:**
    
    - UI-005
    - NFR-007 (Mobile Usability)
    - Section 6.2
    
**Purpose:** Centralizes theme definitions for consistent UI styling and theming capabilities.  
**Logic Description:** Define `ThemeData` for both light and dark modes. Specify primary colors, accent colors, typography (using `AppTypography`), button themes, input decoration themes, etc. Ensure color contrasts meet WCAG 2.1 AA (UI-005).  
**Documentation:**
    
    - **Summary:** Contains theme data for light and dark modes, defining the app's visual appearance.
    
**Namespace:** CreativeFlow.MobileApp.Core.Theme  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/l10n/app_localizations.dart  
**Description:** Manages localization strings and internationalization (i18n) setup for multilingual support as per UI-006.  
**Template:** Flutter Localization Delegate  
**Dependency Level:** 0  
**Name:** AppLocalizations  
**Type:** Localization  
**Relative Path:** core/l10n/app_localizations.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** delegate  
**Type:** LocalizationsDelegate<AppLocalizations>  
**Attributes:** static const  
    
**Methods:**
    
    - **Name:** of  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** AppLocalizations?  
**Attributes:** static  
    - **Name:** translate  
**Parameters:**
    
    - String key
    
**Return Type:** String  
**Attributes:**   
    
**Implemented Features:**
    
    - Multilingual Support
    
**Requirement Ids:**
    
    - UI-006
    
**Purpose:** Provides localized strings and supports multiple languages in the UI.  
**Logic Description:** Use the `intl` package and Flutter's localization system. Define ARB files (e.g., `intl_en.arb`, `intl_es.arb`) for translations. This class will load the appropriate strings based on the current locale. Include methods to access translated strings.  
**Documentation:**
    
    - **Summary:** Handles internationalization and localization of UI strings.
    
**Namespace:** CreativeFlow.MobileApp.Core.L10n  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/widgets/offline_banner.dart  
**Description:** A reusable widget to display a banner or indicator when the application detects an offline network status, as required by UI-004.  
**Template:** Flutter Widget Template  
**Dependency Level:** 1  
**Name:** OfflineBanner  
**Type:** Widget  
**Relative Path:** core/widgets/offline_banner.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Offline Status Indication
    
**Requirement Ids:**
    
    - UI-004
    
**Purpose:** Visually informs the user about the current network connectivity status (offline).  
**Logic Description:** This widget will listen to a `ConnectivityBloc` or similar service providing network status. If offline, it will render a noticeable banner (e.g., at the top or bottom of the screen) indicating no internet connection. Ensure accessibility (UI-005).  
**Documentation:**
    
    - **Summary:** A widget that displays an 'offline' indicator when network connectivity is lost.
    
**Namespace:** CreativeFlow.MobileApp.Core.Widgets  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/features/editor/presentation/screens/editor_screen.dart  
**Description:** The main screen for the creative editor. Hosts the canvas, tool palette, asset pickers, and manages the editor state via EditorBloc. Implements touch-optimized workflows (UI-004) and gesture interactions.  
**Template:** Flutter Screen Template  
**Dependency Level:** 3  
**Name:** EditorScreen  
**Type:** Screen  
**Relative Path:** features/editor/presentation/screens/editor_screen.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - BLoC
    
**Members:**
    
    - **Name:** projectId  
**Type:** String  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Creative Editing UI
    - Touch Workflows
    - Gesture Handling
    - Offline/Sync UI for Editor
    
**Requirement Ids:**
    
    - REQ-019
    - UI-004
    - Section 6.2
    
**Purpose:** Provides the user interface for creating and editing creatives.  
**Logic Description:** Use a `BlocProvider` for `EditorBloc` and `OfflineSyncBloc`. Structure with `Scaffold`, `AppBar`. Include `CanvasWidget`, `ToolPaletteWidget`, `AssetPickerWidget`. Implement gesture detectors for canvas interactions. Display offline status and sync progress from `OfflineSyncBloc`. Integrate camera input (REQ-020) and voice prompt input (REQ-020) widgets.  
**Documentation:**
    
    - **Summary:** The screen where users interact with the creative editing tools and canvas.
    
**Namespace:** CreativeFlow.MobileApp.Features.Editor.Presentation.Screens  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/features/editor/presentation/bloc/editor_bloc.dart  
**Description:** Manages the state for the creative editor, including current project data, selected tools, asset modifications, and interactions with the creative repository for loading/saving projects (both online and offline via SyncService).  
**Template:** Flutter BLoC Template  
**Dependency Level:** 2  
**Name:** EditorBloc  
**Type:** BLoC  
**Relative Path:** features/editor/presentation/bloc/editor_bloc.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - BLoC
    
**Members:**
    
    - **Name:** _creativeRepository  
**Type:** CreativeRepository  
**Attributes:** final  
    - **Name:** _syncService  
**Type:** SyncService  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** EditorBloc  
**Parameters:**
    
    - CreativeRepository creativeRepository
    - SyncService syncService
    
**Return Type:**   
**Attributes:**   
    - **Name:** mapEventToState  
**Parameters:**
    
    - EditorEvent event
    
**Return Type:** Stream<EditorState>  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Editor State Management
    - Load/Save Project Logic
    - Offline Change Queuing
    
**Requirement Ids:**
    
    - REQ-019
    - REQ-019.1
    
**Purpose:** Handles business logic and state for the creative editor feature.  
**Logic Description:** Events: LoadProject, SaveProject, AddElement, ModifyElement, Undo, Redo. States: EditorLoading, EditorLoaded, EditorSaving, EditorError. Interacts with `CreativeRepository` to fetch/save project data. For offline saves (REQ-019), it queues changes via `SyncService` if offline, or attempts direct save if online.  
**Documentation:**
    
    - **Summary:** BLoC responsible for managing the state and business logic of the creative editor.
    
**Namespace:** CreativeFlow.MobileApp.Features.Editor.Presentation.Bloc  
**Metadata:**
    
    - **Category:** PresentationLogic
    
- **Path:** lib/features/editor/presentation/widgets/camera_input_widget.dart  
**Description:** A widget that integrates with the CameraService to allow users to capture and import images/videos directly into the editor.  
**Template:** Flutter Widget Template  
**Dependency Level:** 2  
**Name:** CameraInputWidget  
**Type:** Widget  
**Relative Path:** features/editor/presentation/widgets/camera_input_widget.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** onMediaCaptured  
**Type:** Function(XFile)  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Camera Capture UI
    
**Requirement Ids:**
    
    - REQ-020
    - UI-004
    
**Purpose:** Provides a UI element for users to access the device camera and capture media.  
**Logic Description:** Display a button or icon. On tap, use `CameraService` to open the camera. Handle the captured `XFile` and pass it to the `onMediaCaptured` callback. Request permissions if not granted via `PermissionHandlerService`.  
**Documentation:**
    
    - **Summary:** A widget providing an interface to capture media using the device camera.
    
**Namespace:** CreativeFlow.MobileApp.Features.Editor.Presentation.Widgets  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/features/editor/data/datasources/creative_local_datasource.dart  
**Description:** Implements data access for creative projects and assets stored in the local SQLite database via Drift DAOs. Used for offline mode (REQ-019).  
**Template:** Dart Datasource Class  
**Dependency Level:** 1  
**Name:** CreativeLocalDataSource  
**Type:** DataSource  
**Relative Path:** features/editor/data/datasources/creative_local_datasource.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - DAO
    
**Members:**
    
    - **Name:** _projectDao  
**Type:** ProjectDao  
**Attributes:** final  
    - **Name:** _assetDao  
**Type:** AssetDao  
**Attributes:** final  
    
**Methods:**
    
    - **Name:** getProjectById  
**Parameters:**
    
    - String projectId
    
**Return Type:** Future<ProjectModel?>  
**Attributes:** Future  
    - **Name:** saveProject  
**Parameters:**
    
    - ProjectModel project
    
**Return Type:** Future<void>  
**Attributes:** Future  
    
**Implemented Features:**
    
    - Local Project/Asset CRUD
    
**Requirement Ids:**
    
    - REQ-019
    
**Purpose:** Provides methods to interact with locally stored creative data.  
**Logic Description:** Use Drift DAOs (defined in `core/storage/local_database.dart`) to perform CRUD operations on project and asset tables in the local SQLite database. Handle model transformations if local models differ from domain/network models.  
**Documentation:**
    
    - **Summary:** Handles Create, Read, Update, Delete operations for projects and assets on the local device storage.
    
**Namespace:** CreativeFlow.MobileApp.Features.Editor.Data.DataSources  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/core/bloc/connectivity_bloc.dart  
**Description:** A BLoC that monitors network connectivity status and emits states indicating whether the device is online or offline. Used by UI elements (e.g., OfflineBanner) and services (e.g., SyncService).  
**Template:** Flutter BLoC Template  
**Dependency Level:** 1  
**Name:** ConnectivityBloc  
**Type:** BLoC  
**Relative Path:** core/bloc/connectivity_bloc.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - BLoC
    - Observer
    
**Members:**
    
    - **Name:** _connectivity  
**Type:** Connectivity  
**Attributes:** final  
    - **Name:** _subscription  
**Type:** StreamSubscription<ConnectivityResult>  
**Attributes:** late  
    
**Methods:**
    
    - **Name:** ConnectivityBloc  
**Parameters:**
    
    
**Return Type:**   
**Attributes:**   
    - **Name:** mapEventToState  
**Parameters:**
    
    - ConnectivityEvent event
    
**Return Type:** Stream<ConnectivityState>  
**Attributes:** @override  
    - **Name:** close  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Network Status Monitoring
    
**Requirement Ids:**
    
    - UI-004
    
**Purpose:** Monitors and broadcasts the application's network connectivity status.  
**Logic Description:** Use the `connectivity_plus` package. Subscribe to `onConnectivityChanged` stream. Emit `ConnectivityOnline` or `ConnectivityOffline` states. Handle initial connectivity check.  
**Documentation:**
    
    - **Summary:** BLoC for managing and providing real-time network connectivity status.
    
**Namespace:** CreativeFlow.MobileApp.Core.Bloc  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/permission_handler_service.dart  
**Description:** Manages requests for device permissions like camera, microphone, storage, and notifications. Provides a unified interface to check and request permissions.  
**Template:** Flutter Service Class  
**Dependency Level:** 0  
**Name:** PermissionHandlerService  
**Type:** Service  
**Relative Path:** core/services/permission_handler_service.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** requestCameraPermission  
**Parameters:**
    
    
**Return Type:** Future<PermissionStatus>  
**Attributes:** static Future  
    - **Name:** requestMicrophonePermission  
**Parameters:**
    
    
**Return Type:** Future<PermissionStatus>  
**Attributes:** static Future  
    - **Name:** requestNotificationPermission  
**Parameters:**
    
    
**Return Type:** Future<PermissionStatus>  
**Attributes:** static Future  
    
**Implemented Features:**
    
    - Device Permission Management
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** Provides a centralized way to request and check device permissions.  
**Logic Description:** Use the `permission_handler` plugin. Implement methods for specific permissions (camera, microphone, notifications). Methods should check current status and request permission if not granted. Handle different platform responses.  
**Documentation:**
    
    - **Summary:** Service to handle requesting and checking various device permissions.
    
**Namespace:** CreativeFlow.MobileApp.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/features/settings/presentation/screens/accessibility_settings_screen.dart  
**Description:** Screen allowing users to configure accessibility settings such as font size scaling preferences and high contrast mode toggles, adhering to UI-005.  
**Template:** Flutter Screen Template  
**Dependency Level:** 3  
**Name:** AccessibilitySettingsScreen  
**Type:** Screen  
**Relative Path:** features/settings/presentation/screens/accessibility_settings_screen.dart  
**Repository Id:** REPO-MOBILEAPP-001  
**Pattern Ids:**
    
    - BLoC
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** @override  
    
**Implemented Features:**
    
    - Accessibility Configuration UI
    
**Requirement Ids:**
    
    - UI-005
    
**Purpose:** Provides UI for users to customize accessibility-related preferences.  
**Logic Description:** Use a `SettingsBloc` to manage state. Offer options to adjust text scale factor (which would update `MediaQuery.textScaleFactorOf(context)` effectively or app-wide theme) and toggle a high-contrast theme variant. Ensure all interactive elements are themselves accessible.  
**Documentation:**
    
    - **Summary:** Screen for managing application accessibility settings like font size and contrast.
    
**Namespace:** CreativeFlow.MobileApp.Features.Settings.Presentation.Screens  
**Metadata:**
    
    - **Category:** Presentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableOfflineMode
  - enableCollaborationFeatures
  - enableVoiceInput
  - enableAdvancedAnalyticsTracking
  
- **Database Configs:**
  
  - localDatabaseName: creative_flow_local.db
  - localDatabaseVersion: 1
  


---

