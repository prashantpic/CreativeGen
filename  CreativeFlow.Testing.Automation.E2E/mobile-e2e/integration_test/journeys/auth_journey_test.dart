import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
// It's crucial that the main app (`creative_flow_app`) is a dependency or located correctly
// for this import to work.
import 'package:creative_flow_app/main.dart' as app;

void main() {
  // Ensure the IntegrationTest service is initialized.
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Authentication Journey', () {
    testWidgets('User can log in and log out successfully', (tester) async {
      // 1. Pump the main app widget.
      app.main();
      await tester.pumpAndSettle();

      // Define keys for widgets to make finding them reliable.
      const emailFieldKey = Key('login_email_field');
      const passwordFieldKey = Key('login_password_field');
      const loginButtonKey = Key('login_button');
      const dashboardWelcomeKey = Key('dashboard_welcome_message');
      const logoutButtonKey = Key('dashboard_logout_button');

      // 2. Find the email and password TextField widgets.
      final emailField = find.byKey(emailFieldKey);
      final passwordField = find.byKey(passwordFieldKey);
      expect(emailField, findsOneWidget);
      expect(passwordField, findsOneWidget);

      // 3. Enter text using tester.enterText().
      // Use credentials from environment variables for security.
      const email = String.fromEnvironment('TEST_USER_EMAIL', defaultValue: 'test@example.com');
      const password = String.fromEnvironment('TEST_USER_PASSWORD', defaultValue: 'password123');

      await tester.enterText(emailField, email);
      await tester.enterText(passwordField, password);
      await tester.pumpAndSettle();

      // 4. Find and tap the login button.
      final loginButton = find.byKey(loginButtonKey);
      expect(loginButton, findsOneWidget);
      await tester.tap(loginButton);

      // 5. Pump and settle to wait for animations and screen transitions.
      await tester.pumpAndSettle(const Duration(seconds: 5));

      // 6. Expect to find a widget unique to the dashboard screen.
      expect(find.byKey(dashboardWelcomeKey), findsOneWidget);

      // 7. Find and tap the logout button.
      // This might be inside a menu, requiring additional taps.
      // For this example, we assume it's directly accessible.
      final logoutButton = find.byKey(logoutButtonKey);
      expect(logoutButton, findsOneWidget);
      await tester.tap(logoutButton);

      // 8. Pump and settle.
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // 9. Expect to find a widget unique to the login screen again.
      expect(find.byKey(loginButtonKey), findsOneWidget);
    });
  });
}