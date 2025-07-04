import 'package:creativeflow_mobileapp_flutter/core/services/camera_service.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

/// A widget providing a UI element (e.g., a button) for users to access
/// the device camera and capture media.
///
/// This widget integrates with the [CameraService] to handle the logic
/// of camera access and permission requests.
class CameraInputWidget extends StatelessWidget {
  /// A callback function that is invoked when media has been successfully captured.
  final Function(XFile mediaFile) onMediaCaptured;

  const CameraInputWidget({
    super.key,
    required this.onMediaCaptured,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      icon: const Icon(Icons.camera_alt),
      label: const Text('Camera'),
      onPressed: () async {
        // Use the centralized CameraService to pick an image.
        final XFile? mediaFile = await CameraService.pickImageFromCamera();

        if (mediaFile != null) {
          // If a file was captured, invoke the callback.
          onMediaCaptured(mediaFile);
        } else {
          // If mediaFile is null, the user either cancelled the operation
          // or denied permissions.
          // The UI could show a SnackBar or dialog here.
          // For example:
          if (context.mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Camera access was denied or cancelled.')),
            );
          }
        }
      },
      style: ElevatedButton.styleFrom(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}