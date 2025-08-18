// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appName => 'Farmmate';

  @override
  String get askAnythingHint => 'Ask anything';

  @override
  String get home => 'Home';

  @override
  String get newChat => 'New Chat';

  @override
  String get chatHistory => 'Chat History';

  @override
  String get savedResponses => 'Saved Responses';

  @override
  String get profile => 'Profile';

  @override
  String get settings => 'Settings';

  @override
  String get aboutApp => 'About App';

  @override
  String get logout => 'Logout';
}
