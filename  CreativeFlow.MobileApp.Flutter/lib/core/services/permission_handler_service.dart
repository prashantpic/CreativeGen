import 'package:permission_handler/permission_handler.dart';

/// Provides a centralized and simplified interface for requesting and checking
/// device permissions as required by REQ-020.
///
/// This service abstracts the `permission_handler` plugin, making permission
/// logic consistent and easy to manage across the application.
class PermissionHandlerService {
  // Private constructor to prevent instantiation.
  PermissionHandlerService._();

  /// Requests permission to access the device's camera.
  ///
  /// Returns the resulting [PermissionStatus].
  static Future<PermissionStatus> requestCameraPermission() async {
    return await Permission.camera.request();
  }

  /// Checks the current status of the camera permission.
  static Future<PermissionStatus> checkCameraPermission() async {
    return await Permission.camera.status;
  }

  /// Requests permission to access the device's microphone.
  ///
  /// Returns the resulting [PermissionStatus].
  static Future<PermissionStatus> requestMicrophonePermission() async {
    return await Permission.microphone.request();
  }

  /// Checks the current status of the microphone permission.
  static Future<PermissionStatus> checkMicrophonePermission() async {
    return await Permission.microphone.status;
  }

  /// Requests permission to show notifications.
  ///
  /// Returns the resulting [PermissionStatus].
  static Future<PermissionStatus> requestNotificationPermission() async {
    return await Permission.notification.request();
  }

  /// Checks the current status of the notification permission.
  static Future<PermissionStatus> checkNotificationPermission() async {
    return await Permission.notification.status;
  }

  /// Requests permission to access device storage.
  ///
  /// On modern iOS, `Permission.photos` might be more appropriate. This is a general
  /// starting point.
  /// Returns the resulting [PermissionStatus].
  static Future<PermissionStatus> requestStoragePermission() async {
    // For modern Android (API 33+), granular permissions like photos/videos are needed.
    // This is a simplified approach. A real app might have more logic here.
    return await Permission.storage.request();
  }

  /// Opens the application's settings screen on the device.
  ///
  /// This is useful for prompting the user to manually enable a permission
  /// if they have permanently denied it. Returns `true` if the settings
  /// screen could be opened.
  static Future<bool> openAppSettings() async {
    return await openAppSettings();
  }
}