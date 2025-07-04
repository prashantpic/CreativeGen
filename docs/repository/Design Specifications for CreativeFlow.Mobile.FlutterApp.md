# Software Design Specification (SDS): CreativeFlow.Mobile.FlutterApp

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `CreativeFlow.Mobile.FlutterApp` repository. This application serves as the native mobile client for the CreativeFlow AI platform on both iOS and Android. It is designed to provide a seamless, touch-optimized experience for creative generation, project management, and collaboration, with a strong emphasis on offline capabilities and native device integration.

### 1.2. Scope
The scope of this document is limited to the mobile application's internal architecture, component design, state management, service integrations, and data handling. It details the implementation of features such as the creative editor, offline synchronization, native API usage (camera, voice), and push notifications. It assumes the existence of and defines the interaction with backend services via a central API Gateway.

## 2. System Overview

### 2.1. Architecture
The mobile application will be built using a layered architecture to ensure a clean separation of concerns, enhance testability, and improve maintainability. The primary layers are:

*   **Presentation Layer:** Contains all UI elements (Widgets, Screens) and state management logic (BLoC/Cubit). This layer is responsible for rendering the UI and handling user input. It is reactive to state changes from the Business Logic Layer.
*   **Business Logic Layer (BLoC/Cubit):** Acts as the intermediary between the Presentation and Domain layers. It receives events from the UI, executes business logic by invoking Domain services, and emits new states for the UI to consume.
*   **Domain Layer:** Contains the core business logic, entities, and service abstractions (interfaces). This layer is independent of any UI or data source implementation details. It defines the "what" of the application's capabilities.
*   **Data Layer:** Responsible for all data operations. It includes repository implementations that fetch data from remote sources (API Client) or local sources (Local Database) and provides a single source of truth to the Domain layer.

This architecture will be supported by a centralized **Dependency Injection** (DI) mechanism, likely using the `get_it` package, to provide services and repositories throughout the application.

### 2.2. Technology Stack
*   **Framework:** Flutter 3.19+
*   **Language:** Dart
*   **State Management:** `flutter_bloc` / `cubit`
*   **Routing:** `go_router`
*   **Local Database:** `drift` (atop SQLite)
*   **API Communication:** `http` or `dio`
*   **Dependency Injection:** `get_it`
*   **Native Integration:**
    *   Camera: `camera`
    *   Voice-to-Text: `speech_to_text`
    *   Push Notifications: `firebase_messaging`
*   **Analytics:** `firebase_analytics`, `firebase_crashlytics`
*   **Connectivity:** `connectivity_plus`

## 3. Core Services & Abstractions

This section defines the contracts for core, reusable services within the application.

### 3.1. Local Database Service (`AppDatabase`)
*   **File:** `lib/core/database/app_database.dart`
*   **Framework:** `drift`
*   **Description:** Defines the local SQLite database schema.
*   **Schema Tables:**
    *   `OfflineProjects`: Caches project data for offline access. Columns: `id` (string), `name` (string), `workbenchId` (string), `lastModified` (datetime), `syncStatus` (enum: synced, pending, conflict), `data` (JSON text).
    *   `OfflineAssets`: Caches asset metadata and local file paths. Columns: `id` (string), `projectId` (string), `name` (string), `localPath` (string), `remoteUrl` (string, nullable), `type` (enum), `lastModified` (datetime).
    *   `QueuedChanges`: A log of user actions performed offline that need to be sent to the server. Columns: `id` (int, auto-increment), `timestamp` (datetime), `actionType` (string, e.g., 'update_project'), `payload` (JSON text).
*   **DAOs (Data Access Objects):**
    *   `ProjectDao`: Provides CRUD operations for the `OfflineProjects` table.
    *   `AssetDao`: Provides CRUD operations for the `OfflineAssets` table.
    *   `ChangeQueueDao`: Provides methods to enqueue, dequeue, and clear the `QueuedChanges` table.

### 3.2. Native Feature Services

#### 3.2.1. Camera Service (`CameraService`)
*   **File:** `lib/core/services/camera_service.dart`
*   **Interface:**
    dart
    abstract class CameraService {
      Future<File?> takePicture();
      Future<File?> pickImageFromGallery();
    }
    
*   **Implementation:** Will use the `camera` and `image_picker` packages. It will encapsulate logic for permission handling, initializing the camera controller, and returning the file path of the captured/selected image.

#### 3.2.2. Voice Recognition Service (`VoiceRecognitionService`)
*   **File:** `lib/core/services/voice_recognition_service.dart`
*   **Interface:**
    dart
    abstract class VoiceRecognitionService {
      Future<bool> initialize();
      void startListening({required Function(String) onResult});
      void stopListening();
      bool get isListening;
    }
    
*   **Implementation:** Will use the `speech_to_text` package. It will manage microphone permissions, the listening state, and provide transcribed text back to the caller via the `onResult` callback.

### 3.3. Push Notification Service (`PushNotificationService`)
*   **File:** `lib/core/services/push_notification_service.dart`
*   **Description:** Manages the entire lifecycle of push notifications via Firebase Cloud Messaging (FCM).
*   **Methods:**
    *   `Future<void> initialize()`: Sets up background and foreground message handlers. Requests user permission on iOS.
    *   `Future<String?> getFcmToken()`: Retrieves the unique device token to be sent to the backend server.
    *   `Stream<RemoteMessage> get onMessageOpenedApp`: A stream that emits events when the app is opened from a terminated state via a notification tap.
*   **Logic:** The service will listen for incoming messages and, based on the `data` payload, use the `AppRouter` to navigate to the relevant content (e.g., a specific project for a collaboration update).

### 3.4. Analytics Service (`AnalyticsService`)
*   **File:** `lib/core/services/analytics_service.dart`
*   **Description:** A facade over Firebase Analytics and Crashlytics.
*   **Interface:**
    dart
    abstract class AnalyticsService {
      Future<void> logEvent({required String name, Map<String, Object>? parameters});
      Future<void> setUserId(String id);
      Future<void> logError(dynamic exception, StackTrace stackTrace, {String? reason});
    }
    
*   **Implementation:** Will use `firebase_analytics` to log custom events and `firebase_crashlytics` to report errors. This abstraction allows for easier testing and potential future swapping of analytics providers.

## 4. Feature Implementation

### 4.1. Application Initialization (`main.dart`, `app.dart`)
1.  **`main.dart`**:
    *   The `main()` function will be `async`.
    *   It will call `WidgetsFlutterBinding.ensureInitialized()`.
    *   It will initialize Firebase using `Firebase.initializeApp()`.
    *   It will set up the dependency injection container (e.g., `configureDependencies()`).
    *   It will initialize the `PushNotificationService`.
    *   It will run the `App` widget.
2.  **`app.dart`**:
    *   The `App` widget will be a `StatelessWidget`.
    *   It will return a `MaterialApp.router`.
    *   `theme` and `darkTheme` will be sourced from `AppTheme`.
    *   `routerConfig` will be an instance of the `AppRouter`.
    *   `localizationsDelegates` and `supportedLocales` will be configured for i18n.

### 4.2. Offline Mode & Data Synchronization (`REQ-019`, `REQ-019.1`)

#### 4.2.1. Network Status Indication
*   **Widget:** `NetworkStatusIndicator`
*   **Logic:** A global service, `NetworkConnectivityService`, will use the `connectivity_plus` package to provide a `Stream<ConnectivityResult>`. The `NetworkStatusIndicator` widget, likely placed in the main app scaffold, will subscribe to this stream and display a persistent, non-obtrusive UI element (e.g., a small banner at the bottom or top) indicating "Offline" when the stream emits `ConnectivityResult.none`.

#### 4.2.2. Synchronization Logic
*   **Trigger:** Synchronization will be triggered automatically by the `NetworkConnectivityService` when the device transitions from offline to online. It can also be triggered manually by the user.
*   **State Management:** `SyncCubit` (`lib/features/offline_sync/presentation/bloc/sync_cubit.dart`)
    *   **States:**
        *   `SyncInitial`: The default state.
        *   `SyncInProgress`: UI should show a sync progress indicator.
        *   `SyncSuccess(DateTime lastSynced)`: Sync completed successfully.
        *   `SyncFailure(String errorMessage)`: An error occurred during sync.
        *   `SyncConflictDetected(List<Conflict> conflicts)`: Sync is paused, awaiting user resolution.
    *   **Methods:**
        *   `Future<void> startSync()`:
            1.  Emits `SyncInProgress`.
            2.  Fetches all unsynced changes from `ChangeQueueDao`.
            3.  Sends these changes to the backend API.
            4.  Receives server-side changes that occurred during the offline period.
            5.  Invokes `ConflictResolutionService.resolveConflicts()`.
            6.  If conflicts are returned, emits `SyncConflictDetected`.
            7.  If successful, updates local database with server data, clears the queue, and emits `SyncSuccess`.
            8.  Catches exceptions and emits `SyncFailure`.

#### 4.2.3. Conflict Resolution
*   **Service:** `ConflictResolutionService`
*   **Logic:**
    1.  The `resolveConflicts` method receives a list of local (offline) changes and a list of remote (server) changes for the same data entities.
    2.  It iterates through them, comparing entities by ID.
    3.  **For non-collaborative projects (simple data):** It will implement a 'last-write-wins' strategy based on timestamps. The change with the later timestamp is considered authoritative.
    4.  **For collaborative projects (future-proofing):** If the data structure is a CRDT, it will attempt a merge. If a merge is not possible or results in an invalid state, it flags it as a conflict.
    5.  **Conflict Flagging:** When a conflict cannot be resolved automatically, it creates a `Conflict` object containing the local version and the server version and returns it.
*   **UI:** When the `SyncCubit` is in the `SyncConflictDetected` state, a dialog or a dedicated screen will be shown to the user, presenting the conflicting versions side-by-side and allowing them to choose which version to keep.

### 4.3. Creative Editor (`UI-004`)

#### 4.3.1. Editor Screen
*   **File:** `lib/features/editor/presentation/screens/editor_screen.dart`
*   **Layout:** A `Scaffold` will contain a `Stack`. The bottom layer of the stack is the `CanvasGestureDetector`. Overlaid on top are the toolbars (e.g., top app bar with actions, bottom tool palette).
*   **State:** The screen will be a `BlocProvider` for an `EditorCubit`, which manages the state of the creative canvas.

#### 4.3.2. Gesture Handling
*   **Widget:** `CanvasGestureDetector`
*   **Logic:** This widget will wrap the main canvas painting area. It will use a `GestureDetector` to handle:
    *   `onTapDown`/`onTapUp`: To select or deselect elements.
    *   `onPanStart`/`onPanUpdate`: To move selected elements or pan the canvas.
    *   `onScaleStart`/`onScaleUpdate`: To resize selected elements or zoom the canvas.
*   Each gesture will be translated into a method call on the `EditorCubit` (e.g., `editorCubit.selectObjectAt(position)`, `editorCubit.panCanvas(delta)`).

#### 4.3.3. Canvas Rendering
*   The actual canvas will be a `CustomPaint` widget whose `painter` property is a `CustomPainter` implementation.
*   The `CustomPainter`'s `paint` method will receive the list of objects and the canvas transform from the `EditorState` and iterate through them, drawing each one onto the canvas (e.g., `canvas.drawImage`, `canvas.drawParagraph`).

## 5. Testing Strategy

*   **Unit Tests (`/test`):**
    *   **Target:** Cubits, Services, Repositories, and pure Dart models/logic.
    *   **Framework:** `bloc_test`, `mocktail`.
    *   **Goal:** Verify business logic in isolation. Test every state transition in Cubits. Mock dependencies (e.g., mock the `CameraService` when testing a feature that uses it).
*   **Widget Tests (`/test`):**
    *   **Target:** Individual widgets and small screens.
    *   **Framework:** `flutter_test`.
    *   **Goal:** Verify that widgets render correctly based on state and that user interactions trigger the correct BLoC/Cubit methods.
*   **Integration/E2E Tests (`/integration_test`):**
    *   **Target:** Critical user journeys (`REQ-QAS-003`).
    *   **Framework:** `integration_test` package with `flutter_driver` or Patrol.
    *   **Goal:** Verify complete user flows, such as:
        1.  Login -> Create Project -> Edit Creative -> Save (Offline).
        2.  Go Offline -> Make edits -> Go Online -> Trigger Sync -> Verify changes on another device.
        3.  Tap "Add Image" -> Use Camera -> Verify image appears on canvas.

## 6. Configuration (`pubspec.yaml`)

The `pubspec.yaml` will be structured as follows:

yaml
name: creativeflow_flutter_app
description: The native mobile application for CreativeFlow AI.
publish_to: 'none' 
version: 1.0.0+1

environment:
  sdk: '>=3.4.3 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.6
  provider: ^6.1.2 # Often used with BLoC for DI

  # Navigation
  go_router: ^14.1.0

  # Networking
  http: ^1.2.1
  
  # Local Storage
  drift: ^2.18.0
  sqlite3_flutter_libs: ^0.5.22
  path_provider: ^2.1.3
  path: ^1.9.0

  # Native Integrations & Utilities
  firebase_core: ^3.1.1
  firebase_messaging: ^15.0.2
  firebase_analytics: ^11.1.0
  firebase_crashlytics: ^4.0.2
  camera: ^0.11.0+1
  speech_to_text: ^6.6.2
  connectivity_plus: ^6.0.3
  
  # Dependency Injection
  get_it: ^7.7.0

  # Other utilities
  intl: ^0.19.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  
  # Code Generation
  build_runner: ^2.4.11
  drift_dev: ^2.18.0
  
  # Testing
  bloc_test: ^9.1.7
  mocktail: ^1.0.4
  integration_test:
    sdk: flutter

flutter:
  uses-material-design: true

  assets:
    - assets/images/
    - assets/icons/
    - assets/l10n/

  fonts:
    - family: Inter
      fonts:
        - asset: assets/fonts/Inter-Regular.ttf
        - asset: assets/fonts/Inter-Bold.ttf
          weight: 700
