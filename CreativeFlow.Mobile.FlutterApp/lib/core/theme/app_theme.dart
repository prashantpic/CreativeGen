import 'package:flutter/material.dart';

/// Defines the application's visual themes.
///
/// This class provides a single source of truth for all UI styling, ensuring
/// a consistent look and feel. It defines `ThemeData` for both light and dark
/// modes, including color palettes, typography, and component styles.
class AppTheme {
  static const _fontFamily = 'Inter';

  /// The light theme configuration for the application.
  static final ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    fontFamily: _fontFamily,
    brightness: Brightness.light,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF673AB7), // Deep Purple
      brightness: Brightness.light,
      primary: const Color(0xFF673AB7),
      secondary: const Color(0xFF03DAC6), // Teal
      background: const Color(0xFFF5F5F7),
      surface: Colors.white,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
      elevation: 0.5,
      surfaceTintColor: Colors.transparent,
    ),
    scaffoldBackgroundColor: const Color(0xFFF5F5F7),
    textTheme: _textTheme,
    elevatedButtonTheme: _elevatedButtonTheme,
  );

  /// The dark theme configuration for the application.
  static final ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    fontFamily: _fontFamily,
    brightness: Brightness.dark,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF673AB7), // Deep Purple
      brightness: Brightness.dark,
      primary: const Color(0xFFD0BCFF), // Lighter Purple for dark mode
      secondary: const Color(0xFF03DAC6), // Teal
      background: Colors.black,
      surface: const Color(0xFF1C1C1E),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Color(0xFF1C1C1E),
      foregroundColor: Colors.white,
      elevation: 0,
    ),
    scaffoldBackgroundColor: Colors.black,
    textTheme: _textTheme,
    elevatedButtonTheme: _elevatedButtonTheme,
  );

  /// Defines the core typography for the application.
  static const TextTheme _textTheme = TextTheme(
    displayLarge: TextStyle(fontFamily: _fontFamily, fontSize: 57.0, fontWeight: FontWeight.bold),
    displayMedium: TextStyle(fontFamily: _fontFamily, fontSize: 45.0, fontWeight: FontWeight.bold),
    displaySmall: TextStyle(fontFamily: _fontFamily, fontSize: 36.0, fontWeight: FontWeight.bold),
    headlineLarge: TextStyle(fontFamily: _fontFamily, fontSize: 32.0, fontWeight: FontWeight.bold),
    headlineMedium: TextStyle(fontFamily: _fontFamily, fontSize: 28.0, fontWeight: FontWeight.bold),
    headlineSmall: TextStyle(fontFamily: _fontFamily, fontSize: 24.0, fontWeight: FontWeight.bold),
    titleLarge: TextStyle(fontFamily: _fontFamily, fontSize: 22.0, fontWeight: FontWeight.w600),
    titleMedium: TextStyle(fontFamily: _fontFamily, fontSize: 16.0, fontWeight: FontWeight.w600),
    titleSmall: TextStyle(fontFamily: _fontFamily, fontSize: 14.0, fontWeight: FontWeight.w500),
    bodyLarge: TextStyle(fontFamily: _fontFamily, fontSize: 16.0),
    bodyMedium: TextStyle(fontFamily: _fontFamily, fontSize: 14.0),
    bodySmall: TextStyle(fontFamily: _fontFamily, fontSize: 12.0),
    labelLarge: TextStyle(fontFamily: _fontFamily, fontSize: 14.0, fontWeight: FontWeight.w600),
    labelMedium: TextStyle(fontFamily: _fontFamily, fontSize: 12.0, fontWeight: FontWeight.w600),
    labelSmall: TextStyle(fontFamily: _fontFamily, fontSize: 11.0, fontWeight: FontWeight.w500),
  );

  /// Defines the default style for all elevated buttons.
  static final ElevatedButtonThemeData _elevatedButtonTheme = ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8.0),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      textStyle: const TextStyle(
        fontFamily: _fontFamily,
        fontWeight: FontWeight.bold,
      ),
    ),
  );
}