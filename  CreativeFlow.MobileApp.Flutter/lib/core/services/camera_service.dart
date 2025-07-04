import 'package:creativeflow_mobileapp_flutter/core/services/permission_handler_service.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

/// Provides a simplified and centralized interface for interacting with the
/// device's camera and image gallery.
///
/// This service abstracts the `image_picker` plugin and integrates with
/// `PermissionHandlerService` to ensure necessary permissions are granted.
class CameraService {
  // Private constructor to prevent instantiation.
  CameraService._();

  static final ImagePicker _picker = ImagePicker();

  /// Opens the device's camera to capture a new image.
  ///
  /// It first requests camera permission. If granted, it launches the camera
  /// interface. If the user captures an image, it returns the image as an [XFile].
  /// Returns `null` if the user cancels the operation or if permission is denied.
  static Future<XFile?> pickImageFromCamera() async {
    final status = await PermissionHandlerService.requestCameraPermission();
    if (status.isGranted) {
      try {
        return await _picker.pickImage(source: ImageSource.camera);
      } catch (e) {
        // Handle potential platform exceptions
        return null;
      }
    } else {
      // The user denied permission. The UI layer should handle this,
      // for example by showing a dialog explaining why the permission is needed.
      return null;
    }
  }

  /// Opens the device's camera to record a new video.
  ///
  /// It first requests camera permission. If granted, it launches the video
  /// recording interface. If the user records a video, it returns the video
  /// as an [XFile].
  /// Returns `null` if the user cancels or if permission is denied.
  static Future<XFile?> pickVideoFromCamera() async {
    final status = await PermissionHandlerService.requestCameraPermission();
    if (status.isGranted) {
      try {
        return await _picker.pickVideo(source: ImageSource.camera);
      } catch (e) {
        return null;
      }
    } else {
      return null;
    }
  }

  /// Opens the device's media gallery to select an existing image.
  ///
  /// It may request storage/photo permissions depending on the platform and OS version.
  static Future<XFile?> pickImageFromGallery() async {
    // Note: permission_handler logic might be needed here too for older Android versions
    // or specific iOS photo access levels.
    try {
      return await _picker.pickImage(source: ImageSource.gallery);
    } catch (e) {
      return null;
    }
  }
}