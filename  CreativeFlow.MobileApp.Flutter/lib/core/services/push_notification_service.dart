import 'dart:async';
import 'package:creativeflow_mobileapp_flutter/core/navigation/app_router.dart';
import 'package:creativeflow_mobileapp_flutter/core/services/permission_handler_service.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
// For foreground notifications, a local notifications plugin is often used.
// import 'package:flutter_local_notifications/flutter_local_notifications.dart';

/// Manages push notifications using Firebase Cloud Messaging (FCM).
///
/// This service handles token management, permission requests, and processing
/// of incoming messages in different application states (foreground, background, terminated).
class PushNotificationService {
  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  final GlobalKey<NavigatorState> _navigatorKey;

  PushNotificationService({required GlobalKey<NavigatorState> navigatorKey})
      : _navigatorKey = navigatorKey;

  /// Initializes the push notification service.
  ///
  /// Requests permissions, configures message handlers, and retrieves the initial token.
  Future<void> initialize() async {
    // Request permission from the user to receive notifications.
    final settings = await _firebaseMessaging.requestPermission(
      alert: true,
      announcement: false,
      badge: true,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
      sound: true,
    );

    if (kDebugMode) {
      print('Push Notification Authorization status: ${settings.authorizationStatus}');
    }

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      // Get the FCM token and listen for refreshes.
      final token = await getFcmToken();
      if (kDebugMode) {
        print('FCM Token: $token');
      }
      // TODO: Send the token to your backend server to associate it with the user.

      _firebaseMessaging.onTokenRefresh.listen((newToken) {
        if (kDebugMode) {
          print('FCM Token Refreshed: $newToken');
        }
        // TODO: Send the new token to your backend.
      });

      // --- Configure Message Handlers ---

      // Handle messages received while the app is in the foreground.
      FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

      // Handle user tapping on a notification when the app is in the background.
      FirebaseMessaging.onMessageOpenedApp.listen(_handleBackgroundMessageTap);

      // Handle user tapping on a notification that launched the app from a terminated state.
      final initialMessage = await _firebaseMessaging.getInitialMessage();
      if (initialMessage != null) {
        _handleBackgroundMessageTap(initialMessage);
      }
    }
  }

  /// Retrieves the current FCM registration token for this device.
  Future<String?> getFcmToken() async {
    return await _firebaseMessaging.getToken();
  }

  /// Handles a message received while the app is in the foreground.
  void _handleForegroundMessage(RemoteMessage message) {
    if (kDebugMode) {
      print('Foreground Message data: ${message.data}');
      if (message.notification != null) {
        print('Message also contained a notification: ${message.notification}');
      }
    }
    // To display a notification banner/heads-up display when the app is in the foreground,
    // you would typically use a package like `flutter_local_notifications`.
    // The logic would parse `message.notification` and `message.data` and show a local notification.
  }

  /// Handles the user tapping on a notification from the background or terminated state.
  void _handleBackgroundMessageTap(RemoteMessage message) {
    if (kDebugMode) {
      print('Background Message Tapped. Data: ${message.data}');
    }

    final navigatorContext = _navigatorKey.currentState?.context;
    if (navigatorContext == null) return;

    // Parse the data payload to determine where to navigate.
    // Example payload: { "type": "project_invite", "project_id": "123" }
    final String? type = message.data['type'];
    final String? entityId = message.data['project_id']; // or other relevant ID

    if (type == 'project_invite' && entityId != null) {
      // Navigate to the specific project screen.
      AppRouter.navigateToEditor(navigatorContext, projectId: entityId);
    }
    // Add more routing logic for other notification types.
  }
}