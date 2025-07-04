import 'dart:io';

import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

/// An abstraction for interacting with the device's camera and photo gallery.
///
/// This service provides a clean and testable interface for capturing new
/// images or picking existing ones, decoupling feature logic from the specific
/// plugin (`image_picker`) implementation.
abstract class CameraService {
  /// Opens the device camera to take a new picture.
  ///
  /// Returns a [File] object of the captured image, or `null` if the
  /// user cancels the operation. Throws a [PlatformException] if camera
  /// access is denied or another platform-specific error occurs.
  Future<File?> takePicture();

  /// Opens the device's photo gallery to select an existing image.
  ///
  /// Returns a [File] object of the selected image, or `null` if the
  /// user cancels the operation. Throws a [PlatformException] if gallery
  /// access is denied or another platform-specific error occurs.
  Future<File?> pickImageFromGallery();
}

/// The concrete implementation of [CameraService] using the `image_picker` package.
class CameraServiceImpl implements CameraService {
  final ImagePicker _picker;

  // Allows injecting a mock picker for testing.
  CameraServiceImpl({ImagePicker? picker}) : _picker = picker ?? ImagePicker();

  @override
  Future<File?> takePicture() async {
    try {
      final XFile? imageFile = await _picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 85, // Compress image slightly for performance
      );

      return imageFile != null ? File(imageFile.path) : null;
    } on PlatformException catch (e) {
      // Potentially handle permission errors specifically
      print('Failed to take picture: ${e.message}');
      rethrow;
    }
  }

  @override
  Future<File?> pickImageFromGallery() async {
    try {
      final XFile? imageFile = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
      );

      return imageFile != null ? File(imageFile.path) : null;
    } on PlatformException catch (e) {
      // Potentially handle permission errors specifically
      print('Failed to pick image from gallery: ${e.message}');
      rethrow;
    }
  }
}