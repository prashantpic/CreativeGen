# Specification

# 1. Files

- **Path:** pubspec.yaml  
**Description:** Defines project metadata, dependencies, and asset paths for the Flutter application. Lists all external packages from pub.dev (like provider, http, drift, firebase_messaging, camera) and internal shared component repositories, and configures assets like fonts and images.  
**Template:** Flutter Project Template  
**Dependency Level:** 0  
**Name:** pubspec  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management
    - Asset Configuration
    
**Requirement Ids:**
    
    - REQ-019
    - REQ-020
    - UI-005
    
**Purpose:** To manage all project dependencies, fonts, assets, and other configuration required by the Flutter build system.  
**Logic Description:** This file is a YAML configuration. It will list dependencies under `dependencies` and `dev_dependencies`. It will configure the `flutter` section to include paths to `assets/images/`, `assets/icons/`, `assets/fonts/`, and `assets/l10n/`. It will also define the project name, description, and version.  
**Documentation:**
    
    - **Summary:** The core configuration file for the Flutter project, managing dependencies and assets. It is the first file a developer interacts with when setting up the project or adding new packages.
    
**Namespace:** creativeflow_flutter_app  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** lib/main.dart  
**Description:** The main entry point for the Flutter application. Initializes essential services, dependency injection, and runs the root application widget.  
**Template:** Flutter Application EntryPoint  
**Dependency Level:** 1  
**Name:** main  
**Type:** ApplicationEntryPoint  
**Relative Path:** main.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** main  
    
**Implemented Features:**
    
    - App Initialization
    - Service Locator Setup
    - Firebase Initialization
    
**Requirement Ids:**
    
    - REQ-019
    
**Purpose:** To initialize the application, set up dependency injection, configure global services like Firebase, and launch the main `App` widget.  
**Logic Description:** The `main` function will be asynchronous. It will ensure Flutter bindings are initialized. It will call a setup function for dependency injection (e.g., `configureDependencies`). It will initialize Firebase services. Finally, it will run the `App` widget using `runApp()`.  
**Documentation:**
    
    - **Summary:** This file serves as the bootstrap for the entire Flutter application, preparing all necessary services and configurations before the UI is rendered.
    
**Namespace:** CreativeFlow.Mobile  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** lib/app/app.dart  
**Description:** The root widget of the application. Sets up the MaterialApp, including the theme, localization, and the main navigator/router.  
**Template:** Flutter Root Widget  
**Dependency Level:** 2  
**Name:** App  
**Type:** Widget  
**Relative Path:** app/app.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** override  
    
**Implemented Features:**
    
    - Theme Management
    - Navigation Root
    - Localization Setup
    
**Requirement Ids:**
    
    - NFR-007
    - UI-005
    
**Purpose:** To provide the root of the widget tree, configure the overall app theme, define the router, and set up localization delegates.  
**Logic Description:** This stateless or stateful widget will return a `MaterialApp.router`. It will consume the app theme data from a provider or theme definition file. The `routerConfig` will be sourced from the navigation setup. `localizationsDelegates` and `supportedLocales` will be configured for internationalization.  
**Documentation:**
    
    - **Summary:** This is the core UI container for the application, responsible for establishing the look, feel, and navigation structure that all other screens inherit from.
    
**Namespace:** CreativeFlow.Mobile.App  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/navigation/app_router.dart  
**Description:** Defines all application routes and navigation logic using a routing package like GoRouter or AutoRoute. Manages navigation stacks, deep linking, and transitions between screens.  
**Template:** Flutter Router  
**Dependency Level:** 1  
**Name:** AppRouter  
**Type:** Router  
**Relative Path:** core/navigation/app_router.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** router  
**Type:** GoRouter  
**Attributes:** final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Route Configuration
    - Deep Link Handling
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** To centralize all navigation logic, making it easy to manage routes, pass arguments between screens, and handle deep links.  
**Logic Description:** This file will contain the configuration for a routing package (e.g., GoRouter). It will define a list of `GoRoute` objects, mapping URL-like paths to specific screen widgets. It will include logic for handling initial routes, error pages, and parsing deep link URIs.  
**Documentation:**
    
    - **Summary:** Defines the navigational map of the application, controlling how users move between different features and screens.
    
**Namespace:** CreativeFlow.Mobile.Core.Navigation  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/theme/app_theme.dart  
**Description:** Defines the application's visual theme, including color palettes, typography, button styles, and other UI component styling constants.  
**Template:** Flutter Theme  
**Dependency Level:** 0  
**Name:** AppTheme  
**Type:** Configuration  
**Relative Path:** core/theme/app_theme.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
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
    
    - Consistent Design Language
    
**Requirement Ids:**
    
    - NFR-007
    
**Purpose:** To provide a single source of truth for all UI styling, ensuring a consistent look and feel across the entire application and supporting both light and dark modes.  
**Logic Description:** This class will contain static `ThemeData` objects for light and dark themes. Each `ThemeData` object will define properties like `primaryColor`, `scaffoldBackgroundColor`, `textTheme` (with different font sizes and weights), `elevatedButtonTheme`, etc.  
**Documentation:**
    
    - **Summary:** Centralizes the application's design system, defining colors, fonts, and component styles to be used globally.
    
**Namespace:** CreativeFlow.Mobile.Core.Theme  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/database/app_database.dart  
**Description:** Defines the local SQLite database schema and Data Access Objects (DAOs) using the Drift (formerly Moor) package. Specifies tables for offline projects, assets, and queued changes.  
**Template:** Drift Database Definition  
**Dependency Level:** 1  
**Name:** AppDatabase  
**Type:** Database  
**Relative Path:** core/database/app_database.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    - DataAccessObject
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Local Database Schema
    - Offline Data Persistence
    
**Requirement Ids:**
    
    - REQ-019
    
**Purpose:** To define the structure of the local database for offline storage and provide type-safe methods for data access.  
**Logic Description:** This file will be an abstract class extending `DriftDatabase`. It will use annotations to declare tables (e.g., `OfflineProjects`, `QueuedChanges`). It will also define abstract getters for DAOs (e.g., `ProjectDao get projectDao;`). A part file (`app_database.g.dart`) will be generated by the build runner to provide the implementation.  
**Documentation:**
    
    - **Summary:** The blueprint for the application's local SQLite database, defining tables, columns, and relationships for offline data persistence.
    
**Namespace:** CreativeFlow.Mobile.Core.Database  
**Metadata:**
    
    - **Category:** Data
    
- **Path:** lib/features/offline_sync/domain/services/conflict_resolution_service.dart  
**Description:** Contains the business logic for handling data synchronization conflicts between local offline changes and server-side data.  
**Template:** Dart Service Class  
**Dependency Level:** 3  
**Name:** ConflictResolutionService  
**Type:** Service  
**Relative Path:** features/offline_sync/domain/services/conflict_resolution_service.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** resolveConflicts  
**Parameters:**
    
    - List<LocalChange> localChanges
    - List<ServerChange> serverChanges
    
**Return Type:** Future<ResolutionResult>  
**Attributes:** abstract  
    
**Implemented Features:**
    
    - Offline Data Conflict Resolution
    
**Requirement Ids:**
    
    - REQ-019.1
    
**Purpose:** To implement strategies for merging data, such as 'last-write-wins' for simple cases, and flagging complex conflicts for manual user intervention.  
**Logic Description:** The implementation of this service will compare timestamps and data structures of local and server changes. For non-collaborative projects, it will implement a 'last-write-wins' policy. For collaborative projects, it will attempt to merge changes using CRDT principles if applicable, or flag the conflict by creating a new version and notifying the user.  
**Documentation:**
    
    - **Summary:** The core logic engine for reconciling differences between data edited offline and the authoritative data from the server upon reconnection.
    
**Namespace:** CreativeFlow.Mobile.Features.OfflineSync.Domain.Services  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** lib/features/offline_sync/presentation/bloc/sync_cubit.dart  
**Description:** Manages the state for the data synchronization process, providing UI components with information about sync status (e.g., syncing, synced, error, conflicts).  
**Template:** Flutter Cubit/Bloc  
**Dependency Level:** 4  
**Name:** SyncCubit  
**Type:** StateManagement  
**Relative Path:** features/offline_sync/presentation/bloc/sync_cubit.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    - BLoC
    
**Members:**
    
    
**Methods:**
    
    - **Name:** startSync  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** public  
    - **Name:** resolveConflictManually  
**Parameters:**
    
    - Conflict conflict
    - ResolutionChoice choice
    
**Return Type:** Future<void>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Synchronization State Management
    
**Requirement Ids:**
    
    - REQ-019.1
    - UI-004
    
**Purpose:** To orchestrate the synchronization flow, communicate with the `ConflictResolutionService`, and emit states that the UI can react to, such as showing progress indicators or conflict resolution dialogs.  
**Logic Description:** This Cubit will have states like `SyncInitial`, `SyncInProgress`, `SyncSuccess`, `SyncFailure`, and `SyncConflictDetected`. The `startSync` method will call the relevant domain use cases. If a conflict is detected, it will emit the `SyncConflictDetected` state with the conflict details, pausing the sync until the user resolves it.  
**Documentation:**
    
    - **Summary:** Handles the presentation logic for the data synchronization feature, managing its state and responding to user actions related to resolving conflicts.
    
**Namespace:** CreativeFlow.Mobile.Features.OfflineSync.Presentation.Bloc  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/app/widgets/network_status_indicator.dart  
**Description:** A global UI widget that persistently displays the current network connectivity status (online/offline) to the user.  
**Template:** Flutter Widget  
**Dependency Level:** 3  
**Name:** NetworkStatusIndicator  
**Type:** Widget  
**Relative Path:** app/widgets/network_status_indicator.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** override  
    
**Implemented Features:**
    
    - Offline Status Indication
    
**Requirement Ids:**
    
    - UI-004
    
**Purpose:** To provide clear and constant feedback to the user about their ability to connect to online services, fulfilling a key requirement for offline-capable apps.  
**Logic Description:** This widget will listen to a stream from a network connectivity service (e.g., using the `connectivity_plus` package). Based on the connection status, it will render a small, non-intrusive UI element, like a banner or an icon, indicating 'Online' or 'Offline'.  
**Documentation:**
    
    - **Summary:** A UI component that visually informs the user of their current network connectivity status.
    
**Namespace:** CreativeFlow.Mobile.App.Widgets  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/services/camera_service.dart  
**Description:** An abstraction layer over the native device camera plugin. Provides simple methods to capture photos or videos for use within the application.  
**Template:** Dart Service Class  
**Dependency Level:** 2  
**Name:** CameraService  
**Type:** Service  
**Relative Path:** core/services/camera_service.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** takePicture  
**Parameters:**
    
    
**Return Type:** Future<File?>  
**Attributes:** abstract  
    - **Name:** pickImageFromGallery  
**Parameters:**
    
    
**Return Type:** Future<File?>  
**Attributes:** abstract  
    
**Implemented Features:**
    
    - Camera Integration
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** To provide a clean and testable interface for interacting with the device camera, decoupling feature logic from the specific plugin implementation.  
**Logic Description:** The implementation of this service will use a third-party Flutter plugin like `camera` or `image_picker`. It will handle requesting camera permissions, launching the camera UI, and returning the captured file path to the caller.  
**Documentation:**
    
    - **Summary:** Provides a standardized way for the application to interact with the device's camera and photo gallery.
    
**Namespace:** CreativeFlow.Mobile.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/voice_recognition_service.dart  
**Description:** An abstraction layer over the native speech-to-text plugin. Provides methods to start listening for voice input and receive transcribed text.  
**Template:** Dart Service Class  
**Dependency Level:** 2  
**Name:** VoiceRecognitionService  
**Type:** Service  
**Relative Path:** core/services/voice_recognition_service.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** startListening  
**Parameters:**
    
    - Function(String) onResult
    
**Return Type:** Future<bool>  
**Attributes:** abstract  
    - **Name:** stopListening  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** abstract  
    
**Implemented Features:**
    
    - Voice-to-Text Input
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** To provide a clean interface for using the device's speech recognition capabilities, abstracting the complexities of the underlying plugin.  
**Logic Description:** The implementation will use a plugin like `speech_to_text`. It will handle microphone permissions, initializing the speech recognizer, starting and stopping listening sessions, and streaming back recognized words or final results via callbacks.  
**Documentation:**
    
    - **Summary:** Provides a standardized interface for converting spoken user language into text, used primarily for prompt input.
    
**Namespace:** CreativeFlow.Mobile.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/core/services/push_notification_service.dart  
**Description:** Handles the setup and management of push notifications using Firebase Cloud Messaging (FCM). Processes incoming notifications when the app is in the foreground, background, or terminated.  
**Template:** Dart Service Class  
**Dependency Level:** 2  
**Name:** PushNotificationService  
**Type:** Service  
**Relative Path:** core/services/push_notification_service.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initialize  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** public  
    - **Name:** getFcmToken  
**Parameters:**
    
    
**Return Type:** Future<String?>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Push Notification Handling
    
**Requirement Ids:**
    
    - REQ-020
    
**Purpose:** To manage the entire lifecycle of push notifications, from obtaining a device token to handling user interactions with received notifications.  
**Logic Description:** This service will use the `firebase_messaging` plugin. The `initialize` method will request notification permissions from the user, get the FCM token, and set up listeners for `onMessage`, `onMessageOpenedApp`, and background messages. These listeners will parse the notification payload and trigger appropriate in-app actions, like navigating to a specific screen.  
**Documentation:**
    
    - **Summary:** Manages push notifications via Firebase Cloud Messaging, responsible for receiving and handling alerts for collaboration updates and other events.
    
**Namespace:** CreativeFlow.Mobile.Core.Services  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** lib/features/editor/presentation/screens/editor_screen.dart  
**Description:** The main screen for the creative editor, containing the canvas, tool palettes, and property inspectors. This is a touch-optimized UI for mobile.  
**Template:** Flutter Screen  
**Dependency Level:** 4  
**Name:** EditorScreen  
**Type:** Screen  
**Relative Path:** features/editor/presentation/screens/editor_screen.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** override  
    
**Implemented Features:**
    
    - Touch-Optimized Creative Workflow
    - Gesture-Based Interactions
    
**Requirement Ids:**
    
    - UI-004
    - REQ-019
    
**Purpose:** To provide the user with a fluid and intuitive interface for creating and editing visual content on a mobile device.  
**Logic Description:** This screen will be a `StatefulWidget` that uses a `BlocBuilder` or `Consumer` to listen to the `EditorCubit` state. The layout will be a `Stack` containing the main canvas widget and overlayed toolbars. It will instantiate widgets for different tools, layers, and asset panels, designed with mobile ergonomics in mind (e.g., thumb-friendly placement).  
**Documentation:**
    
    - **Summary:** The primary user interface for creative editing, optimized for touch interaction and smaller screens.
    
**Namespace:** CreativeFlow.Mobile.Features.Editor.Presentation.Screens  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/features/editor/presentation/widgets/canvas_gesture_detector.dart  
**Description:** A specialized widget that wraps the creative canvas, handling all touch-based gestures like pinch-to-zoom, pan, tap, and drag-and-drop.  
**Template:** Flutter Widget  
**Dependency Level:** 5  
**Name:** CanvasGestureDetector  
**Type:** Widget  
**Relative Path:** features/editor/presentation/widgets/canvas_gesture_detector.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** override  
    
**Implemented Features:**
    
    - Gesture-Based Interactions
    
**Requirement Ids:**
    
    - UI-004
    
**Purpose:** To centralize and manage complex gesture logic, translating user touch input into commands for the editor's state management.  
**Logic Description:** This widget will use Flutter's `GestureDetector` to listen for various gestures (`onScaleUpdate` for zoom, `onPanUpdate` for panning). It will calculate the transformation delta and call methods on the `EditorCubit` to update the canvas view or the position of a selected element. It will manage the state of the interaction (e.g., which element is being dragged).  
**Documentation:**
    
    - **Summary:** A crucial component for enabling a touch-native editing experience by handling and interpreting all user gestures on the canvas.
    
**Namespace:** CreativeFlow.Mobile.Features.Editor.Presentation.Widgets  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/services/analytics_service.dart  
**Description:** Abstraction for the mobile analytics platform (e.g., Firebase Analytics, Mixpanel). Provides methods to log standard and custom events.  
**Template:** Dart Service Class  
**Dependency Level:** 2  
**Name:** AnalyticsService  
**Type:** Service  
**Relative Path:** core/services/analytics_service.dart  
**Repository Id:** REPO-MOBILE-FLUTTER-001  
**Pattern Ids:**
    
    - Facade
    
**Members:**
    
    
**Methods:**
    
    - **Name:** logEvent  
**Parameters:**
    
    - String name
    - Map<String, Object> parameters
    
**Return Type:** Future<void>  
**Attributes:** abstract  
    - **Name:** setUserId  
**Parameters:**
    
    - String id
    
**Return Type:** void  
**Attributes:** abstract  
    
**Implemented Features:**
    
    - Mobile App Analytics
    - Crash Reporting
    
**Requirement Ids:**
    
    - REQ-019
    - NFR-001
    
**Purpose:** To provide a consistent interface for event tracking across the app, decoupling feature code from the specific analytics SDK being used.  
**Logic Description:** The implementation will use the `firebase_analytics` or `mixpanel_flutter` plugin. The `logEvent` method will map the provided event name and parameters to the SDK's corresponding function call. It will also handle setting user properties and IDs for session-based analysis. It will integrate with Firebase Crashlytics to log non-fatal exceptions.  
**Documentation:**
    
    - **Summary:** Centralizes all interactions with third-party analytics services for tracking user behavior, app performance, and crashes.
    
**Namespace:** CreativeFlow.Mobile.Core.Services  
**Metadata:**
    
    - **Category:** Core
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableOfflineMode
  - enableCollaborationFeatures
  - enableAdvancedAITools
  
- **Database Configs:**
  
  - localDatabaseName
  - databaseVersion
  


---

