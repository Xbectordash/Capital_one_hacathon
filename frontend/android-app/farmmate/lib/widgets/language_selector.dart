import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/language_provider.dart';

class LanguageSelector extends StatelessWidget {
  const LanguageSelector({super.key});

  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);

    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.language, color: Colors.blue),
                const SizedBox(width: 8),
                const Text(
                  'Select Language', // Will be localized later
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: LanguageProvider.supportedLocales.map((locale) {
                final isSelected = languageProvider.currentLocale.languageCode == locale.languageCode;
                final languageName = languageProvider.getLanguageName(locale.languageCode);
                
                return FilterChip(
                  label: Text(
                    languageName,
                    style: TextStyle(
                      color: isSelected ? Colors.white : Colors.black87,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                  selected: isSelected,
                  onSelected: (selected) {
                    if (selected) {
                      languageProvider.changeLanguage(locale.languageCode);
                    }
                  },
                  backgroundColor: Colors.grey[200],
                  selectedColor: Colors.blue,
                  checkmarkColor: Colors.white,
                );
              }).toList(),
            ),
            const SizedBox(height: 8),
            Text(
              'Current: ${languageProvider.getLanguageName(languageProvider.currentLocale.languageCode)}',
              style: TextStyle(
                color: Colors.grey[600],
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
