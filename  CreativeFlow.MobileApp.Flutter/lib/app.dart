import 'package:creativeflow_mobileapp_flutter/core/bloc/connectivity_bloc.dart';
import 'package:creativeflow_mobileapp_flutter/core/l10n/app_localizations.dart';
import 'package:creativeflow_mobileapp_flutter/core/navigation/app_router.dart';
import 'package:creativeflow_mobileapp_flutter/core/navigation/route_paths.dart';
import 'package:creativeflow_mobileapp_flutter/core/theme/app_theme.dart';
import 'package:creativeflow_mobileapp_flutter/core/widgets/offline_banner.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// Placeholder BLoCs for compilation
class AuthBloc extends Bloc<Object, Object> { AuthBloc() : super(Object()); }
class ThemeBloc extends Bloc<Object, ThemeMode> { ThemeBloc() : super(ThemeMode.system); }
class LocalizationBloc extends Bloc<Object, Locale> { LocalizationBloc() : super(const Locale('en', 'US')); }


/// The root widget of the CreativeFlow application.
///
/// This widget sets up the top-level application structure, including:
/// - Global state management providers (BLoCs).
/// - Application theme (light/dark mode).
/// - Localization and internationalization delegates.
/// - Navigation routing.
/// - A global offline status indicator.
class CreativeFlowApp extends StatelessWidget {
  const CreativeFlowApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Provide global BLoCs to the entire widget tree.
    return MultiBlocProvider(
      providers: [
        BlocProvider<AuthBloc>(
          create: (context) => AuthBloc(),
        ),
        BlocProvider<ThemeBloc>(
          create: (context) => ThemeBloc(),
        ),
        BlocProvider<LocalizationBloc>(
          create: (context) => LocalizationBloc(),
        ),
        BlocProvider<ConnectivityBloc>(
          create: (context) => ConnectivityBloc()..add(ConnectivityCheckRequested()),
          lazy: false, // Start listening to connectivity immediately.
        ),
      ],
      child: BlocBuilder<ThemeBloc, ThemeMode>(
        builder: (context, themeMode) {
          return BlocBuilder<LocalizationBloc, Locale>(
            builder: (context, locale) {
              return MaterialApp(
                title: 'CreativeFlow AI',
                
                // Theme Configuration
                theme: AppTheme.lightTheme,
                darkTheme: AppTheme.darkTheme,
                themeMode: themeMode,

                // Localization Configuration (UI-006)
                locale: locale,
                localizationsDelegates: AppLocalizations.localizationsDelegates,
                supportedLocales: AppLocalizations.supportedLocales,

                // Navigation Configuration (Section 6.2)
                onGenerateRoute: AppRouter.onGenerateRoute,
                initialRoute: RoutePaths.splash,

                // Global UI wrapper for features like the offline banner.
                builder: (context, child) {
                  return Stack(
                    children: [
                      child!,
                      const OfflineBanner(), // Displays when offline (UI-004)
                    ],
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}