import 'package:creativeflow_mobileapp_flutter/core/navigation/route_paths.dart';
import 'package:creativeflow_mobileapp_flutter/features/editor/presentation/screens/editor_screen.dart';
import 'package:creativeflow_mobileapp_flutter/features/settings/presentation/screens/accessibility_settings_screen.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

// --- Placeholder Screens for Compilation ---
class SplashScreen extends StatelessWidget { const SplashScreen({super.key}); @override Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Splash Screen'))); }
class LoginScreen extends StatelessWidget { const LoginScreen({super.key}); @override Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Login Screen'))); }
class HomeScreen extends StatelessWidget { const HomeScreen({super.key}); @override Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('Home Screen'))); }
class NotFoundScreen extends StatelessWidget { const NotFoundScreen({super.key}); @override Widget build(BuildContext context) => const Scaffold(body: Center(child: Text('404 - Page Not Found'))); }
// --- End Placeholder Screens ---


/// Centralizes navigation logic and route definitions for the application.
///
/// This router uses named routes (Navigator 1.0) and provides a single place
/// to handle route generation, argument passing, and unknown route handling.
class AppRouter {
  // Private constructor to prevent instantiation.
  AppRouter._();

  /// Generates a route based on the provided [RouteSettings].
  ///
  /// This method is the core of the navigation logic, mapping route names
  /// from [RoutePaths] to the corresponding screen widgets.
  static Route<dynamic>? onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case RoutePaths.splash:
        return MaterialPageRoute(builder: (_) => const SplashScreen());

      case RoutePaths.login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());

      case RoutePaths.home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());

      case RoutePaths.editor:
        // Safely extract the projectId from the arguments.
        final args = settings.arguments;
        if (args is String) {
          return MaterialPageRoute(builder: (_) => EditorScreen(projectId: args));
        }
        // If arguments are invalid, navigate to an error page or a fallback.
        return _errorRoute(message: 'Project ID is required for the editor.');

      case RoutePaths.accessibilitySettings:
        return MaterialPageRoute(builder: (_) => const AccessibilitySettingsScreen());

      // ... other routes would be added here
      // e.g., case RoutePaths.projectDetails:
      
      default:
        // Handle unknown routes gracefully.
        return _errorRoute();
    }
  }

  /// Returns a `MaterialPageRoute` to a generic "Not Found" screen.
  static Route<dynamic> _errorRoute({String message = 'Page not found'}) {
    return MaterialPageRoute(
      builder: (_) => Scaffold(
        appBar: AppBar(title: const Text('Error')),
        body: Center(child: Text(message)),
      ),
    );
  }

  // --- Typed Navigation Helper Methods ---

  /// Navigates to the login screen and removes all previous routes from the stack.
  static void navigateToLogin(BuildContext context) {
    Navigator.of(context).pushNamedAndRemoveUntil(RoutePaths.login, (route) => false);
  }

  /// Navigates to the home screen and removes all previous routes.
  static void navigateToHome(BuildContext context) {
    Navigator.of(context).pushNamedAndRemoveUntil(RoutePaths.home, (route) => false);
  }

  /// Navigates to the editor screen with a specific project ID.
  static Future<dynamic> navigateToEditor(BuildContext context, {required String projectId}) {
    return Navigator.of(context).pushNamed(RoutePaths.editor, arguments: projectId);
  }

  /// Navigates to the accessibility settings screen.
  static Future<dynamic> navigateToAccessibilitySettings(BuildContext context) {
    return Navigator.of(context).pushNamed(RoutePaths.accessibilitySettings);
  }
}