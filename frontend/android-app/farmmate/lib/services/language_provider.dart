import 'package:flutter/material.dart';

class LanguageProvider extends InheritedWidget {
  final Function(Locale) setLocale;

  const LanguageProvider({
    super.key,
    required this.setLocale,
    required super.child,
  });

  static LanguageProvider of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<LanguageProvider>()!;
  }

  @override
  bool updateShouldNotify(LanguageProvider oldWidget) => true;
}
