import 'package:creativeflow_flutter_app/core/navigation/app_router.dart';
import 'package:creativeflow_flutter_app/core/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

/// The root widget of the CreativeFlow mobile application.
///
/// This widget sets up the `MaterialApp.router` which is the foundation
/// of the app's UI. It configures:
/// - The application's theme (light and dark modes).
/// - The navigation system using `go_router`.
/// - Localization delegates for internationalization (i18n).
class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'CreativeFlow',
      
      // Configure the app's theme and dark theme.
      // `themeMode` can be set to ThemeMode.system, .light, or .dark.
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,

      // Configure the router using the centralized AppRouter configuration.
      routerConfig: AppRouter.router,

      // Configure localization delegates for i18n support.
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en', ''), // English, no country code
        // Add other supported locales here, e.g., Locale('es', '') for Spanish.
      ],
      
      // Hide the debug banner in the top-right corner.
      debugShowCheckedModeBanner: false,
    );
  }
}