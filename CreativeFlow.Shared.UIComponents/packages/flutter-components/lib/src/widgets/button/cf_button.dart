```dart
import 'package:flutter/material.dart';

/// An enum to define the visual style of the [CfButton].
enum CfButtonVariant {
  /// For the main call-to-action on a page.
  primary,

  /// For secondary actions that are less prominent.
  secondary,

  /// For the least prominent actions, often in dialogs or cards.
  text,
}

/// A versatile and themeable button widget for Flutter, offering multiple style
/// variants and states to be used across the mobile application.
/// It ensures visual and behavioral consistency with its React web counterpart.
class CfButton extends StatelessWidget {
  /// The text content displayed inside the button.
  final String label;

  /// The callback that is called when the button is tapped.
  /// If null, the button will be disabled.
  final VoidCallback? onPressed;

  /// The visual style of the button.
  /// Defaults to [CfButtonVariant.primary].
  final CfButtonVariant variant;

  /// If `true`, the button shows a loading indicator and is disabled.
  /// Defaults to `false`.
  final bool isLoading;

  /// Creates a CreativeFlow standard button.
  const CfButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.variant = CfButtonVariant.primary,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    // The actual onPressed handler is null if loading or if the provided
    // onPressed is null, effectively disabling the button.
    final effectiveOnPressed = isLoading ? null : onPressed;

    final Widget child = isLoading
        ? const SizedBox(
            width: 20,
            height: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2.5,
              color: Colors.white, // This could be themed as well
            ),
          )
        : Text(label);

    switch (variant) {
      case CfButtonVariant.primary:
        return ElevatedButton(
          onPressed: effectiveOnPressed,
          child: child,
        );
      case CfButtonVariant.secondary:
        return OutlinedButton(
          onPressed: effectiveOnPressed,
          child: child,
        );
      case CfButtonVariant.text:
        return TextButton(
          onPressed: effectiveOnPressed,
          child: child,
        );
    }
  }
}
```