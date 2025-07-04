import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

/// A facade over the analytics and crash reporting platforms.
///
/// This abstraction provides a single, consistent interface for logging events,
/// user properties, and errors. It decouples the application from specific
/// SDKs (like Firebase), allowing for easier testing and potential future
/// swapping of analytics providers.
abstract class AnalyticsService {
  /// Logs a custom event.
  ///
  /// - [name]: The name of the event (e.g., 'project_created').
  /// - [parameters]: A map of key-value pairs with additional event data.
  Future<void> logEvent({required String name, Map<String, Object>? parameters});

  /// Associates a user ID with all subsequent events and crash reports.
  ///
  /// - [id]: A unique identifier for the user.
  Future<void> setUserId(String id);

  /// Records a non-fatal error or exception.
  ///
  /// These errors will be reported to the crash reporting tool (e.g., Crashlytics)
  /// and can be analyzed to find bugs.
  ///
  /// - [exception]: The exception object.
  /// - [stackTrace]: The stack trace associated with the exception.
  /// - [reason]: An optional string providing context for the error.
  Future<void> logError(dynamic exception, StackTrace stackTrace, {String? reason});
}

/// The concrete implementation of [AnalyticsService] using Firebase.
class AnalyticsServiceImpl implements AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  @override
  Future<void> logEvent({
    required String name,
    Map<String, Object>? parameters,
  }) async {
    if (kDebugMode) {
      print('[ANALYTICS] Event: $name, Params: $parameters');
    }
    await _analytics.logEvent(
      name: name,
      parameters: parameters,
    );
  }

  @override
  Future<void> setUserId(String id) async {
    if (kDebugMode) {
      print('[ANALYTICS] Set User ID: $id');
    }
    await _analytics.setUserId(id: id);
    await _crashlytics.setUserIdentifier(id);
  }

  @override
  Future<void> logError(
    dynamic exception,
    StackTrace stackTrace, {
    String? reason,
    bool fatal = false,
  }) async {
    if (kDebugMode) {
      print('[ANALYTICS] Logging Error: $exception');
    }
    await _crashlytics.recordError(
      exception,
      stackTrace,
      reason: reason,
      fatal: fatal,
    );
  }
}