import 'package:farmmate/features/home/screens/home_screen.dart';
import 'package:farmmate/features/settings/screens/settings_screen.dart';
import 'package:farmmate/features/settings/screens/location_settings_screen.dart';
import 'package:farmmate/services/language_provider.dart';
import 'package:farmmate/utils/constants/app_colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:farmmate/l10n/app_localizations.dart';
import 'package:provider/provider.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => LanguageProvider(),
      child: Consumer<LanguageProvider>(
        builder: (context, languageProvider, child) {
          return MaterialApp(
            debugShowCheckedModeBanner: false,
            title: 'FarmMate AI',
            
            // Localization configuration
            localizationsDelegates: const [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: LanguageProvider.supportedLocales,
            locale: languageProvider.currentLocale,
            
            // Enhanced Theme configuration with Green & White
            theme: ThemeData(
              primarySwatch: _createMaterialColor(AppColors.primaryGreen),
              primaryColor: AppColors.primaryGreen,
              primaryColorLight: AppColors.lightGreen,
              primaryColorDark: AppColors.darkGreen,
              scaffoldBackgroundColor: AppColors.warmWhite,
              
              // App Bar Theme
              appBarTheme: const AppBarTheme(
                backgroundColor: AppColors.primaryGreen,
                foregroundColor: AppColors.pureWhite,
                elevation: 0,
                centerTitle: true,
                titleTextStyle: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  color: AppColors.pureWhite,
                ),
              ),
              
              // Color Scheme
              colorScheme: ColorScheme.fromSwatch(
                primarySwatch: _createMaterialColor(AppColors.primaryGreen),
                backgroundColor: AppColors.warmWhite,
              ).copyWith(
                secondary: AppColors.accentGreen,
                surface: AppColors.pureWhite,
                onSurface: AppColors.textPrimary,
                onPrimary: AppColors.pureWhite,
              ),
              
              // Elevated Button Theme
              elevatedButtonTheme: ElevatedButtonThemeData(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryGreen,
                  foregroundColor: AppColors.pureWhite,
                  elevation: 2,
                  shadowColor: AppColors.shadowColor,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                ),
              ),
              
              // Input Decoration Theme
              inputDecorationTheme: InputDecorationTheme(
                filled: true,
                fillColor: AppColors.paleGreen,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.borderColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.borderColor),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.primaryGreen, width: 2),
                ),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              ),
              
              // Card Theme
              cardTheme: const CardThemeData(
                color: AppColors.pureWhite,
                elevation: 4,
                shadowColor: AppColors.shadowColor,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(16)),
                ),
              ),
              
              visualDensity: VisualDensity.adaptivePlatformDensity,
              fontFamily: 'Roboto',
              
              // Text Theme
              textTheme: const TextTheme(
                headlineLarge: TextStyle(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
                headlineMedium: TextStyle(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w600,
                ),
                bodyLarge: TextStyle(
                  color: AppColors.textPrimary,
                ),
                bodyMedium: TextStyle(
                  color: AppColors.textSecondary,
                ),
              ),
            ),
            
            // Routes
            initialRoute: '/home',
            routes: {
              '/home': (context) => const HomeScreen(),
              '/settings': (context) => const SettingsScreen(),
              '/location-settings': (context) => const LocationSettingsScreen(),
            },
          );
        },
      ),
    );
  }
  
  // Helper method to create MaterialColor from Color
  static MaterialColor _createMaterialColor(Color color) {
    List strengths = <double>[.05];
    Map<int, Color> swatch = {};
    final int r = color.red, g = color.green, b = color.blue;

    for (int i = 1; i < 10; i++) {
      strengths.add(0.1 * i);
    }
    for (var strength in strengths) {
      final double ds = 0.5 - strength;
      swatch[(strength * 1000).round()] = Color.fromRGBO(
        r + ((ds < 0 ? r : (255 - r)) * ds).round(),
        g + ((ds < 0 ? g : (255 - g)) * ds).round(),
        b + ((ds < 0 ? b : (255 - b)) * ds).round(),
        1,
      );
    }
    return MaterialColor(color.value, swatch);
  }
}
