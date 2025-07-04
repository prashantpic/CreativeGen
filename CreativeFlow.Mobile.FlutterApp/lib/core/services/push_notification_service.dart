import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';

/// A top-level function to handle background messages from FCM.
///
/// According to the `firebase_messaging` documentation, this handler must be
/// a top-level function and not an anonymous function to ensure it can be
/// called from a separate isolate.
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  // If you're going to use other Firebase services in the background, you must
  // call `initializeApp` here.
  await Firebase.initializeApp();

  debugPrint("Handling a background message: ${message.messageId}");
  debugPrint("Data payload: ${message.data}");
  // Here, you could process the data payload, e.g., update a local database
  // with new information, without waking up the full application UI.
}

/// Manages the entire lifecycle of push notifications via Firebase Cloud Messaging (FCM).
///
/// This service encapsulates logic for:
/// - Requesting user permissions for notifications.
/// - Handling incoming messages when the app is in the foreground, background, or terminated.
/// - Retrieving the unique FCM device token.
abstract class PushNotificationService {
  /// Initializes the service, sets up message handlers, and requests permissions.
  Future<void> initialize();

  /// Retrieves the unique Firebase Cloud Messaging (FCM) token for the device.
  ///
  /// This token should be sent to your backend server to target this device
  /// for push notifications. Returns `null` if the token cannot be retrieved.
  Future<String?> getFcmToken();

  /// A stream that emits a [RemoteMessage] when the app is opened from a
  /// background or terminated state via a notification tap.
  Stream<RemoteMessage> get onMessageOpenedApp;
}

/// The concrete implementation of [PushNotificationService].
class PushNotificationServiceImpl implements PushNotificationService {
  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

  @override
  Future<void> initialize() async {
    // Request permission from the user on iOS and web.
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      announcement: false,
      badge: true,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
      sound: true,
    );

    if (kDebugMode) {
      print('Push Notification Permission status: ${settings.authorizationStatus}');
    }

    // Set the background message handler.
    FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

    // Handle messages received while the app is in the foreground.
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      debugPrint('Received a foreground message!');
      debugPrint('Message data: ${message.data}');

      if (message.notification != null) {
        debugPrint('Message also contained a notification: ${message.notification}');
        // Here you might want to display a custom in-app notification
        // using a package like `flutter_local_notifications`.
      }
    });
  }

  @override
  Future<String?> getFcmToken() async {
    try {
      final token = await _firebaseMessaging.getToken();
      if (kDebugMode) {
        print('FCM Token: $token');
      }
      return token;
    } catch (e) {
      debugPrint('Error getting FCM token: $e');
      return null;
    }
  }

  @override
  Stream<RemoteMessage> get onMessageOpenedApp {
    return FirebaseMessaging.onMessageOpenedApp;
  }
}