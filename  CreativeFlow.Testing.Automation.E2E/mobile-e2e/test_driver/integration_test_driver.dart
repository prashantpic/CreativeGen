import 'package:integration_test/integration_test_driver.dart';

/// The driver script required by `flutter_driver` to run the integration tests
/// defined in the `integration_test` directory.
///
/// This is a standard boilerplate file. It acts as the entry point for the
/// test runner, connecting the `flutter_driver` command-line tool to the
/// `integration_test` suite running inside the app.
///
/// To run tests, use the command:
/// `flutter drive --driver=test_driver/integration_test_driver.dart --target=integration_test/journeys/auth_journey_test.dart`
Future<void> main() => integrationDriver();