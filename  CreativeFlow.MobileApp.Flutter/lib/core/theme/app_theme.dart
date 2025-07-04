import 'package:flutter/material.dart';

// --- Placeholder for AppColors ---
// In a real project, this would be in `lib/core/theme/app_colors.dart`
class AppColors {
  AppColors._();
  static const Color primaryLight = Color(0xFF6200EE);
  static const Color primaryDark = Color(0xFFBB86FC);
  static const Color backgroundLight = Color(0xFFFFFFFF);
  static const Color backgroundDark = Color(0xFF121212);
  static const Color surfaceLight = Color(0xFFFFFFFF);
  static const Color surfaceDark = Color(0xFF1E1E1E);
  static const Color textLight = Color(0xFF000000);
  static const Color textDark = Color(0xFFFFFFFF);
}

// --- Placeholder for AppTypography ---
// In a real project, this would be in `lib/core/theme/app_typography.dart`
class AppTypography {
  AppTypography._();

  static const TextTheme textThemeLight = TextTheme(
    displayLarge: TextStyle(fontSize: 96, fontWeight: FontWeight.w300, letterSpacing: -1.5, color: AppColors.textLight),
    headlineMedium: TextStyle(fontSize: 34, fontWeight: FontWeight.w400, letterSpacing: 0.25, color: AppColors.textLight),
    titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.w500, letterSpacing: 0.15, color: AppColors.textLight),
    bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, letterSpacing: 0.5, color: AppColors.textLight),
    bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w400, letterSpacing: 0.25, color: AppColors.textLight),
    labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, letterSpacing: 1.25, color: AppColors.textLight),
  );

  static final TextTheme textThemeDark = textThemeLight.apply(
    bodyColor: AppColors.textDark,
    displayColor: AppColors.textDark,
  );
}


/// Centralizes theme definitions for consistent UI styling.
///
/// This class provides [ThemeData] for both light and dark modes, ensuring
/// the application adheres to the brand's visual identity and supports
/// user preferences for theming. Color contrasts are chosen to meet
/// accessibility standards (WCAG 2.1 AA).
class AppTheme {
  // Private constructor to prevent instantiation.
  AppTheme._();

  /// The theme data for light mode.
  static final ThemeData lightTheme = ThemeData(
    brightness: Brightness.light,
    primaryColor: AppColors.primaryLight,
    scaffoldBackgroundColor: AppColors.backgroundLight,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primaryLight,
      secondary: Colors.amber,
      surface: AppColors.surfaceLight,
      background: AppColors.backgroundLight,
      error: Colors.red,
      onPrimary: Colors.white,
      onSecondary: Colors.black,
      onSurface: Colors.black,
      onBackground: Colors.black,
      onError: Colors.white,
    ),
    textTheme: AppTypography.textThemeLight,
    appBarTheme: const AppBarTheme(
      elevation: 0,
      backgroundColor: AppColors.backgroundLight,
      foregroundColor: AppColors.textLight,
      iconTheme: IconThemeData(color: AppColors.textLight),
    ),
    buttonTheme: const ButtonThemeData(
      buttonColor: AppColors.primaryLight,
      textTheme: ButtonTextTheme.primary,
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
      ),
    ),
  );

  /// The theme data for dark mode.
  static final ThemeData darkTheme = ThemeData(
    brightness: Brightness.dark,
    primaryColor: AppColors.primaryDark,
    scaffoldBackgroundColor: AppColors.backgroundDark,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primaryDark,
      secondary: Colors.amber,
      surface: AppColors.surfaceDark,
      background: AppColors.backgroundDark,
      error: Colors.redAccent,
      onPrimary: Colors.black,
      onSecondary: Colors.black,
      onSurface: Colors.white,
      onBackground: Colors.white,
      onError: Colors.black,
    ),
    textTheme: AppTypography.textThemeDark,
    appBarTheme: const AppBarTheme(
      elevation: 0,
      backgroundColor: AppColors.backgroundDark,
      foregroundColor: AppColors.textDark,
      iconTheme: IconThemeData(color: AppColors.textDark),
    ),
    buttonTheme: const ButtonThemeData(
      buttonColor: AppColors.primaryDark,
      textTheme: ButtonTextTheme.primary,
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
      ),
      focusedBorder: const OutlineInputBorder(
        borderSide: BorderSide(color: AppColors.primaryDark),
      ),
    ),
  );
}