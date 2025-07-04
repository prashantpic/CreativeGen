import 'package:creativeflow_flutter_app/features/editor/presentation/screens/editor_screen.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// A placeholder home screen to demonstrate initial routing.
// In a real application, this would be a dashboard or project list screen.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('CreativeFlow Projects')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Welcome to CreativeFlow!'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => context.go('/editor/new-project-123'),
              child: const Text('Open Editor for Project 123'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Centralized navigation configuration for the application.
///
/// This class uses `go_router` to define all available routes, handle
/// deep linking, and manage navigation logic in one place.
class AppRouter {
  /// The singleton instance of the GoRouter configuration.
  static final router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/editor/:projectId',
        name: 'editor',
        builder: (context, state) {
          // Extract the projectId from the route parameters.
          final projectId = state.pathParameters['projectId'];
          if (projectId != null) {
            return EditorScreen(projectId: projectId);
          }
          // Handle the case where projectId is missing, though the route
          // requires it. Redirect to an error page or home.
          return const ErrorScreen(error: 'Project ID is missing.');
        },
      ),
      // Add other routes here, for example:
      // GoRoute(path: '/login', name: 'login', builder: ...),
      // GoRoute(path: '/settings', name: 'settings', builder: ...),
    ],
    // A custom error builder to show a user-friendly page for unknown routes.
    errorBuilder: (context, state) => ErrorScreen(error: state.error.toString()),
  );
}

/// A simple screen to display routing errors.
class ErrorScreen extends StatelessWidget {
  final String error;
  const ErrorScreen({super.key, required this.error});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Page Not Found')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Oops! Something went wrong.',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(error),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => context.go('/'),
              child: const Text('Go to Home'),
            ),
          ],
        ),
      ),
    );
  }
}