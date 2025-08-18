import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageProvider extends ChangeNotifier {
  static const String _languageKey = 'selected_language';
  
  Locale _currentLocale = const Locale('en');
  
  Locale get currentLocale => _currentLocale;
  
  // Supported languages
  static const List<Locale> supportedLocales = [
    Locale('en', ''), // English
    Locale('hi', ''), // Hindi
    Locale('mr', ''), // Marathi
    Locale('gu', ''), // Gujarati
    Locale('pa', ''), // Punjabi
    Locale('kn', ''), // Kannada
    Locale('ta', ''), // Tamil
    Locale('te', ''), // Telugu
  ];
  
  // Language names map
  static const Map<String, String> languageNames = {
    'en': 'English',
    'hi': 'हिंदी',
    'mr': 'मराठी',
    'gu': 'ગુજરાતી',
    'pa': 'ਪੰਜਾਬੀ',
    'kn': 'ಕನ್ನಡ',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
  };
  
  LanguageProvider() {
    _loadSavedLanguage();
  }
  
  /// Load saved language from SharedPreferences
  Future<void> _loadSavedLanguage() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedLanguage = prefs.getString(_languageKey);
      
      if (savedLanguage != null) {
        _currentLocale = Locale(savedLanguage);
        notifyListeners();
      }
    } catch (e) {
      // If loading fails, keep default language
      print('Error loading saved language: $e');
    }
  }
  
  /// Change the current language
  Future<void> changeLanguage(String languageCode) async {
    if (_currentLocale.languageCode != languageCode) {
      _currentLocale = Locale(languageCode);
      
      // Save to SharedPreferences
      try {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(_languageKey, languageCode);
      } catch (e) {
        print('Error saving language preference: $e');
      }
      
      notifyListeners();
    }
  }
  
  /// Get language name for display
  String getLanguageName(String languageCode) {
    return languageNames[languageCode] ?? languageCode.toUpperCase();
  }
  
  /// Check if a language is supported
  bool isLanguageSupported(String languageCode) {
    return supportedLocales.any((locale) => locale.languageCode == languageCode);
  }
  
  /// Get language code for AI service
  String getLanguageCodeForAI() {
    // Map app language codes to AI service language codes if needed
    switch (_currentLocale.languageCode) {
      case 'en':
        return 'en';
      case 'hi':
        return 'hi';
      case 'mr':
        return 'mr';
      case 'gu':
        return 'gu';
      case 'pa':
        return 'pa';
      case 'kn':
        return 'kn';
      case 'ta':
        return 'ta';
      case 'te':
        return 'te';
      default:
        return 'en'; // Fallback to English
    }
  }
}
