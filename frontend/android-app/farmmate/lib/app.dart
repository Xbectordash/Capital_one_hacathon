import 'package:farmmate/features/home/screens/home_screen.dart';
import 'package:farmmate/features/settings/screens/settings_screen.dart';
import 'package:farmmate/features/settings/screens/location_settings_screen.dart';
import 'package:flutter/material.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

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
    );
  }
}
