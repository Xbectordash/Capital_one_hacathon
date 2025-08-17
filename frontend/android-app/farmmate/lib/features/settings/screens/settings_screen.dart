import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../providers/chat_provider.dart';
import '../../../utils/extensions/app_extensions.dart';
import '../../../utils/deployment_helper.dart';
import 'location_settings_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  Map<String, bool>? _serviceStatus;
  bool _isCheckingStatus = false;

  @override
  void initState() {
    super.initState();
    _checkServiceStatus();
  }

  Future<void> _checkServiceStatus() async {
    setState(() {
      _isCheckingStatus = true;
    });

    try {
      final chatProvider = Provider.of<ChatProvider>(context, listen: false);
      final status = await chatProvider.getServiceStatus();
      setState(() {
        _serviceStatus = status;
      });
    } catch (e) {
      print('Error checking service status: $e');
    } finally {
      setState(() {
        _isCheckingStatus = false;
      });
    }
  }

  Widget _buildSettingCard({
    required String title,
    required String subtitle,
    required IconData icon,
    required Widget child,
    Color? iconColor,
  }) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: iconColor ?? Colors.blue, size: 24),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      subtitle,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),
            child,
          ],
        ),
      ),
    );
  }

  Widget _buildLanguageSelector() {
    return Consumer<ChatProvider>(
      builder: (context, chatProvider, _) {
        return Column(
          children: chatProvider.languages.entries.map((entry) {
            return RadioListTile<String>(
              title: Text(entry.value),
              value: entry.key,
              groupValue: chatProvider.selectedLanguage,
              onChanged: (value) {
                if (value != null) {
                  chatProvider.setLanguage(value);
                }
              },
              dense: true,
              contentPadding: EdgeInsets.zero,
            );
          }).toList(),
        );
      },
    );
  }

  Widget _buildConnectionSettings() {
    return Consumer<ChatProvider>(
      builder: (context, chatProvider, _) {
        return Column(
          children: [
            SwitchListTile(
              title: const Text('Use WebSocket'),
              subtitle: Text(
                chatProvider.useWebSocket 
                    ? 'Real-time connection enabled' 
                    : 'Using HTTP requests',
              ),
              value: chatProvider.useWebSocket,
              onChanged: (value) {
                chatProvider.toggleWebSocket();
              },
              dense: true,
              contentPadding: EdgeInsets.zero,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(
                  chatProvider.isConnected ? Icons.wifi : Icons.wifi_off,
                  color: chatProvider.isConnected ? Colors.green : Colors.red,
                  size: 16,
                ),
                const SizedBox(width: 8),
                Text(
                  chatProvider.isConnected ? 'Connected' : 'Disconnected',
                  style: TextStyle(
                    color: chatProvider.isConnected ? Colors.green : Colors.red,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ],
        );
      },
    );
  }

  Widget _buildServiceStatus() {
    if (_isCheckingStatus) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_serviceStatus == null) {
      return Column(
        children: [
          const Text('Unable to check service status'),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: _checkServiceStatus,
            child: const Text('Retry'),
          ),
        ],
      );
    }

    return Column(
      children: [
        _buildServiceStatusItem(
          'Backend Service',
          _serviceStatus!['backend'] ?? false,
        ),
        const SizedBox(height: 8),
        _buildServiceStatusItem(
          'AI Service',
          _serviceStatus!['ai_service'] ?? false,
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: _checkServiceStatus,
            icon: const Icon(Icons.refresh),
            label: const Text('Refresh Status'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue,
              foregroundColor: Colors.white,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildServiceStatusItem(String serviceName, bool isHealthy) {
    return Row(
      children: [
        Icon(
          isHealthy ? Icons.check_circle : Icons.error,
          color: isHealthy ? Colors.green : Colors.red,
          size: 20,
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            serviceName,
            style: const TextStyle(fontSize: 16),
          ),
        ),
        Text(
          isHealthy ? 'Healthy' : 'Offline',
          style: TextStyle(
            color: isHealthy ? Colors.green : Colors.red,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FE),
      appBar: AppBar(
        title: const Text('Settings'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: Colors.black,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              const Color(0xFFE6EEFE),
              const Color(0xFFF7F9FE),
              Colors.white.withOpacity(0.9),
            ],
          ),
        ),
        child: ListView(
          padding: EdgeInsets.all(context.screenWidth * 0.05),
          children: [
            // Language Settings
            _buildSettingCard(
              title: 'Language',
              subtitle: 'Select your preferred language',
              icon: Icons.language,
              iconColor: Colors.green,
              child: _buildLanguageSelector(),
            ),

            // Location Settings
            _buildSettingCard(
              title: 'Location',
              subtitle: 'Manage your location settings',
              icon: Icons.location_on,
              iconColor: Colors.red,
              child: Column(
                children: [
                  Consumer<ChatProvider>(
                    builder: (context, chatProvider, _) {
                      return ListTile(
                        title: const Text('Current Location'),
                        subtitle: Text(
                          chatProvider.currentLocation.isEmpty
                              ? 'No location set'
                              : chatProvider.currentLocation,
                        ),
                        trailing: const Icon(Icons.arrow_forward_ios),
                        contentPadding: EdgeInsets.zero,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const LocationSettingsScreen(),
                            ),
                          );
                        },
                      );
                    },
                  ),
                ],
              ),
            ),

            // Connection Settings
            _buildSettingCard(
              title: 'Connection',
              subtitle: 'Configure connection preferences',
              icon: Icons.settings_ethernet,
              iconColor: Colors.purple,
              child: _buildConnectionSettings(),
            ),

            // Service Status
            _buildSettingCard(
              title: 'Service Status',
              subtitle: 'Check backend service health',
              icon: Icons.health_and_safety,
              iconColor: Colors.orange,
              child: _buildServiceStatus(),
            ),

            // Chat Actions
            _buildSettingCard(
              title: 'Chat Actions',
              subtitle: 'Manage your chat history',
              icon: Icons.chat,
              iconColor: Colors.blue,
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text('Clear Chat History'),
                            content: const Text(
                              'Are you sure you want to clear all chat messages? This action cannot be undone.',
                            ),
                            actions: [
                              TextButton(
                                onPressed: () => Navigator.pop(context),
                                child: const Text('Cancel'),
                              ),
                              TextButton(
                                onPressed: () {
                                  Provider.of<ChatProvider>(context, listen: false)
                                      .clearChat();
                                  Navigator.pop(context);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text('Chat history cleared'),
                                    ),
                                  );
                                },
                                child: const Text('Clear'),
                              ),
                            ],
                          ),
                        );
                      },
                      icon: const Icon(Icons.clear_all),
                      label: const Text('Clear Chat History'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Service Status
            DeploymentStatusWidget(showDetails: true),

            // Service Info Card
            Card(
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Icon(Icons.cloud_done, color: Colors.green, size: 24),
                        SizedBox(width: 12),
                        Text(
                          'Connected to Cloud Services',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.green,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 12),
                    _buildServiceUrl('Backend', 'https://capital-one-hacathon-1.onrender.com'),
                    _buildServiceUrl('AI Service', 'https://capital-one-hacathon.onrender.com'),
                  ],
                ),
              ),
            ),

            // App Info
            Card(
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    const Text(
                      'FarmMate',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Your AI-powered farming assistant',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.grey[600],
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Version 1.0.0',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildServiceUrl(String name, String url) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(Icons.link, size: 16, color: Colors.blue),
          SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: TextStyle(fontWeight: FontWeight.w500, fontSize: 14),
                ),
                Text(
                  url,
                  style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
