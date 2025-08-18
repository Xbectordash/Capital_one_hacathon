import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/language_provider.dart';

class TestScreen extends StatelessWidget {
  const TestScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Language Test'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Current Language: ${languageProvider.getLanguageName(languageProvider.currentLocale.languageCode)}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            const Text(
              'Test Messages:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            ...LanguageProvider.supportedLocales.map((locale) {
              final messages = _getTestMessages(locale.languageCode);
              return Card(
                margin: const EdgeInsets.symmetric(vertical: 8),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${languageProvider.getLanguageName(locale.languageCode)} (${locale.languageCode})',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Text('Welcome: ${messages['welcome']}'),
                      Text('Chat: ${messages['chat']}'),
                      Text('Settings: ${messages['settings']}'),
                    ],
                  ),
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  Map<String, String> _getTestMessages(String languageCode) {
    final messages = {
      'en': {'welcome': 'Welcome to FarmMate', 'chat': 'Chat', 'settings': 'Settings'},
      'hi': {'welcome': 'FarmMate में आपका स्वागत है', 'chat': 'चैट', 'settings': 'सेटिंग्स'},
      'mr': {'welcome': 'FarmMate मध्ये आपले स्वागत आहे', 'chat': 'चॅट', 'settings': 'सेटिंग्ज'},
      'gu': {'welcome': 'FarmMate માં આપનું સ્વાગત છે', 'chat': 'ચેટ', 'settings': 'સેટિંગ્સ'},
      'pa': {'welcome': 'FarmMate ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ', 'chat': 'ਚੈਟ', 'settings': 'ਸੈਟਿੰਗਾਂ'},
      'kn': {'welcome': 'FarmMate ಗೆ ಸ್ವಾಗತ', 'chat': 'ಚಾಟ್', 'settings': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು'},
      'ta': {'welcome': 'FarmMate க்கு வரவேற்கிறோம்', 'chat': 'அரட்டை', 'settings': 'அமைப்புகள்'},
      'te': {'welcome': 'FarmMate కు స్వాగతం', 'chat': 'చాట్', 'settings': 'సెట్టింగులు'},
    };
    
    return messages[languageCode] ?? messages['en']!;
  }
}
