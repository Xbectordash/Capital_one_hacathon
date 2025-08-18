import 'package:farmmate/app.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/chat_provider.dart';
import 'config/app_config.dart';
import 'services/api_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize API service with configuration validation
  ApiService.initialize();
  
  // Validate deployment configuration
  print('🚀 Starting FarmMate');
  AppConfig.printConfig();
  AppConfig.validateConfig();
  
  runApp(
    ChangeNotifierProvider(
      create: (context) => ChatProvider(),
      child: const MyApp(),
    ),
  );
}
