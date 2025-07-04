import 'dart:async';
import 'package:creativeflow_mobileapp_flutter/core/navigation/app_router.dart';
import 'package:creativeflow_mobileapp_flutter/core/navigation/route_paths.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:uni_links/uni_links.dart';

/// Manages deep linking functionality, allowing the app to respond to external URLs.
///
/// This handler listens for incoming links when the app is launched or running,
/// parses them, and navigates to the appropriate screen.
class DeepLinkHandler {
  // Private constructor to prevent instantiation.
  DeepLinkHandler._();

  static StreamSubscription? _sub;

  /// Initializes the deep link listeners.
  ///
  /// This should be called once in the application's lifecycle, typically
  /// in the `initState` of the main app widget.
  ///
  /// [navigatorKey] is required to perform navigation from outside the widget tree.
  static Future<void> init(GlobalKey<NavigatorState> navigatorKey) async {
    try {
      // Listen for incoming links while the app is running.
      _sub = uriLinkStream.listen(
        (Uri? link) => handleLink(link, navigatorKey),
        onError: (err) {
          if (kDebugMode) {
            print('uni_links stream error: $err');
          }
        },
      );

      // Handle the initial link that launched the app.
      final initialUri = await getInitialUri();
      if (initialUri != null) {
        handleLink(initialUri, navigatorKey);
      }
    } on PlatformException {
      if (kDebugMode) {
        print('Failed to get initial uri.');
      }
    }
  }

  /// Parses the incoming [link] and navigates to the corresponding screen.
  ///
  /// [navigatorKey] is the global navigator key to push new routes.
  static Future<void> handleLink(Uri? link, GlobalKey<NavigatorState> navigatorKey) async {
    if (link == null) return;

    if (kDebugMode) {
      print('Handling deep link: $link');
    }

    // Placeholder for authentication check.
    // Before navigating to a protected route, you would check the state
    // of an AuthBloc. If the user is not authenticated, you could navigate
    // to the login screen and store the deep link to redirect after login.
    // Example:
    // final authState = BLoCProvider.of<AuthBloc>(navigatorKey.currentContext!).state;
    // if (authState is! Authenticated) { /* redirect to login */ }

    final pathSegments = link.pathSegments;
    if (pathSegments.isEmpty) return;

    // Example URI parsing: creativeflow://app/project/project-id-123
    final navigator = navigatorKey.currentState;
    if (navigator == null) return;

    if (pathSegments.first == 'project' && pathSegments.length > 1) {
      final projectId = pathSegments[1];
      AppRouter.navigateToEditor(navigator.context, projectId: projectId);
    } else if (pathSegments.first == 'settings' && pathSegments.length > 1) {
      if (pathSegments[1] == 'accessibility') {
        AppRouter.navigateToAccessibilitySettings(navigator.context);
      }
    } else {
        // Fallback or error handling for unknown deep link paths.
        if (kDebugMode) {
          print('Unknown deep link path: ${link.path}');
        }
    }
  }

  /// Disposes of the stream subscription to prevent memory leaks.
  static void dispose() {
    _sub?.cancel();
  }
}