import 'package:flutter/material.dart';

/// ------------------------------
/// BuildContext Extensions
/// ------------------------------
extension ContextExtensions on BuildContext {
  Size get screenSize => MediaQuery.of(this).size;
  double get screenWidth => screenSize.width;
  double get screenHeight => screenSize.height;

  void hideKeyboard() => FocusScope.of(this).unfocus();
}