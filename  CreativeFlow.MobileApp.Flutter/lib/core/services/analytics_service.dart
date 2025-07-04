import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

/// Provides a unified interface for tracking user behavior and application events.
///
/// This service abstracts the underlying analytics platform (Firebase), allowing
/// for easier testing and potential replacement of the analytics provider in the future.
/// It also integrates with Firebase Crashlytics for error and crash reporting.
class AnalyticsService {
  final FirebaseAnalytics _firebaseAnalytics = FirebaseAnalytics.instance;
  final FirebaseCrashlytics _firebaseCrashlytics = FirebaseCrashlytics.instance;

  /// Initializes the service.
  ///
  /// Can be used to set up initial configurations, such as enabling
  /// or disabling collection based on user consent.
  Future<void> initialize() async {
    // Enable Crashlytics collection. In a real app, this might depend on
    // user consent provided through a privacy setting.
    await _firebaseCrashlytics.setCrashlyticsCollectionEnabled(true);
  }

  /// Logs a custom analytics event.
  ///
  /// Use this to track specific user interactions or milestones.
  /// [name] should be a unique identifier for the event.
  /// [parameters] can provide additional context.
  Future<void> logEvent({
    required String name,
    Map<String, Object>? parameters,
  }) async {
    await _firebaseAnalytics.logEvent(name: name, parameters: parameters);
  }

  /// Sets a user property to a given value.
  ///
  /// User properties are attributes you define to describe segments of your
  /// user base, such as language preference or geographic location.
  Future<void> setUserProperty({
    required String name,
    String? value,
  }) async {
    await _firebaseAnalytics.setUserProperty(name: name, value: value);
  }

  /// Logs a screen view event.
  ///
  /// This helps you understand what content users are viewing most.
  /// Should be called whenever a new screen becomes visible.
  Future<void> logScreenView({
    required String screenName,
    String? screenClassOverride,
  }) async {
    await _firebaseAnalytics.setCurrentScreen(
      screenName: screenName,
      screenClassOverride: screenClassOverride ?? screenName,
    );
  }

  /// Records a non-fatal error or exception.
  ///
  /// Use this to log caught exceptions to understand error trends.
  /// [fatal] indicates if the error caused the app to crash.
  Future<void> recordError(
    dynamic exception,
    StackTrace stack, {
    bool fatal = false,
  }) async {
    await _firebaseCrashlytics.recordError(exception, stack, fatal: fatal);
  }

  /// Sets a user identifier for analytics and crash reporting.
  ///
  /// This helps associate analytics data and crash reports with a specific user,
  /// aiding in debugging and user journey analysis.
  Future<void> setUserId(String? userId) async {
    await _firebaseAnalytics.setUserId(id: userId);
    await _firebaseCrashlytics.setUserIdentifier(userId ?? 'anonymous');
  }
}