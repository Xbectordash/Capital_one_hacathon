import 'package:farmmate/features/home/screens/home_screen.dart';
import 'package:farmmate/features/settings/screens/settings_screen.dart';
import 'package:farmmate/features/settings/screens/location_settings_screen.dart';
import 'package:farmmate/l10n/app_localizations.dart';
import 'package:farmmate/services/language_provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

/// The main application widget.
class MyApp extends StatefulWidget {
  /// Creates a [MyApp] widget.
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  Locale _locale = const Locale('en');

  void setLocale(Locale locale) {
    setState(() {
      _locale = locale;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/home',
      routes: {
        '/home': (context) => const HomeScreen(),
        '/settings': (context) => const SettingsScreen(),
        '/location-settings': (context) => const LocationSettingsScreen(),
      },
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      locale: _locale,
      builder: (context, child) {
        return LanguageProvider(setLocale: setLocale, child: child!);
      },
    );
  }
}
