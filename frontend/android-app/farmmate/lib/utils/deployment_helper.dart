import 'package:flutter/material.dart';
import '../config/app_config.dart';
import '../services/api_service.dart';

class DeploymentHelper {
  /// Check if all deployed services are running
  static Future<Map<String, dynamic>> checkDeployedServices() async {
    final Map<String, dynamic> results = {
      'backend': false,
      'ai_service': false,
      'websocket': false,
      'overall_status': false,
      'errors': <String>[],
      'environment': AppConfig.isDebugMode ? 'development' : 'production',
      'backend_url': AppConfig.backendUrl,
      'ai_service_url': AppConfig.aiServiceUrl,
      'websocket_url': AppConfig.webSocketUrl,
    };

    try {
      // Check backend health
      final backendHealth = await ApiService.checkBackendHealth();
      results['backend'] = backendHealth;
      
      if (!backendHealth) {
        results['errors'].add('Backend service not responding at ${AppConfig.backendUrl}');
      }

      // Check AI service health
      final aiServiceHealth = await ApiService.checkAIServiceHealth();
      results['ai_service'] = aiServiceHealth;
      
      if (!aiServiceHealth) {
        results['errors'].add('AI service not responding at ${AppConfig.aiServiceUrl}');
      }

      // Overall status
      results['overall_status'] = backendHealth && aiServiceHealth;
      
      if (results['overall_status'] == true) {
        results['message'] = 'All services are running successfully! 🚀';
      } else {
        results['message'] = 'Some services are not responding. Please check deployment.';
      }

    } catch (e) {
      results['errors'].add('Error checking services: $e');
      results['message'] = 'Failed to check service status';
    }

    return results;
  }

  /// Show deployment status dialog
  static Future<void> showDeploymentStatus(BuildContext context) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const DeploymentStatusDialog(),
    );
  }

  /// Get deployment instructions
  static String getDeploymentInstructions() {
    return '''
# FarmMate Deployment Instructions

## Current Configuration:
- Environment: ${AppConfig.isDebugMode ? 'DEVELOPMENT' : 'PRODUCTION'}
- Backend URL: ${AppConfig.backendUrl}
- AI Service URL: ${AppConfig.aiServiceUrl}
- WebSocket URL: ${AppConfig.webSocketUrl}

## For Production Deployment:

### 1. Deploy Backend Services:
   - Deploy Python AI Server to Render/Heroku/Railway
   - Deploy Express.js Backend to Render/Heroku/Railway
   - Update URLs in production_config.dart

### 2. Update Android App:
   - Build app with production flag: flutter build apk --dart-define=DEBUG_MODE=false
   - Test with deployed services

### 3. Service URLs to Update:
   - Backend: https://your-backend.onrender.com
   - AI Service: https://your-ai-service.onrender.com

### 4. Environment Variables:
   - Set DEBUG_MODE=false for production builds
   - Configure proper WebSocket URLs (wss:// for HTTPS)

## Testing:
   - Use the Service Status screen to verify connectivity
   - Check logs for any connection issues
   - Test chat functionality with deployed services
''';
  }
}

class DeploymentStatusDialog extends StatefulWidget {
  const DeploymentStatusDialog({Key? key}) : super(key: key);

  @override
  State<DeploymentStatusDialog> createState() => _DeploymentStatusDialogState();
}

class _DeploymentStatusDialogState extends State<DeploymentStatusDialog> {
  Map<String, dynamic>? _status;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _checkServices();
  }

  Future<void> _checkServices() async {
    setState(() => _isLoading = true);
    final status = await DeploymentHelper.checkDeployedServices();
    setState(() {
      _status = status;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Row(
        children: [
          Icon(Icons.cloud_done, color: Colors.blue),
          SizedBox(width: 8),
          Text('Deployment Status'),
        ],
      ),
      content: SizedBox(
        width: double.maxFinite,
        child: _isLoading
            ? Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Checking deployed services...'),
                ],
              )
            : _buildStatusContent(),
      ),
      actions: [
        TextButton(
          onPressed: _checkServices,
          child: Text('Refresh'),
        ),
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: Text('Close'),
        ),
      ],
    );
  }

  Widget _buildStatusContent() {
    if (_status == null) return Text('Failed to check status');

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Environment info
        Container(
          padding: EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: !AppConfig.isDebugMode ? Colors.green.shade50 : Colors.orange.shade50,
            borderRadius: BorderRadius.circular(4),
          ),
          child: Row(
            children: [
              Icon(
                !AppConfig.isDebugMode ? Icons.cloud : Icons.computer,
                size: 16,
                color: !AppConfig.isDebugMode ? Colors.green : Colors.orange,
              ),
              SizedBox(width: 8),
              Text(
                'Environment: ${_status!['environment']}',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
        
        SizedBox(height: 16),
        
        // Services status
        _buildServiceStatus('Backend', _status!['backend'], _status!['backend_url']),
        _buildServiceStatus('AI Service', _status!['ai_service'], _status!['ai_service_url']),
        
        SizedBox(height: 16),
        
        // Overall status
        Container(
          padding: EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: _status!['overall_status'] ? Colors.green.shade50 : Colors.red.shade50,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: _status!['overall_status'] ? Colors.green : Colors.red,
            ),
          ),
          child: Row(
            children: [
              Icon(
                _status!['overall_status'] ? Icons.check_circle : Icons.error,
                color: _status!['overall_status'] ? Colors.green : Colors.red,
              ),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  _status!['message'] ?? 'Unknown status',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
        ),
        
        // Errors
        if (_status!['errors'].isNotEmpty) ...[
          SizedBox(height: 16),
          Text('Issues:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
          ...(_status!['errors'] as List<String>).map((error) => 
            Padding(
              padding: EdgeInsets.only(left: 16, top: 4),
              child: Text('• $error', style: TextStyle(color: Colors.red.shade700)),
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildServiceStatus(String name, bool status, String url) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(
            status ? Icons.check_circle : Icons.cancel,
            color: status ? Colors.green : Colors.red,
            size: 20,
          ),
          SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: TextStyle(fontWeight: FontWeight.w500),
                ),
                Text(
                  url,
                  style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// Widget to show quick deployment status in the app
class DeploymentStatusWidget extends StatelessWidget {
  final bool showDetails;

  const DeploymentStatusWidget({Key? key, this.showDetails = false}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: DeploymentHelper.checkDeployedServices(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Card(
            child: ListTile(
              leading: SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
              title: Text('Checking Services'),
              subtitle: Text('Verifying deployment status...'),
            ),
          );
        }

        if (!snapshot.hasData) {
          return Card(
            child: ListTile(
              leading: Icon(Icons.error, color: Colors.red),
              title: Text('Service Check Failed'),
              subtitle: Text('Unable to verify deployment status'),
            ),
          );
        }

        final status = snapshot.data!;
        final isHealthy = status['overall_status'] as bool;

        return Card(
          child: ListTile(
            leading: Icon(
              isHealthy ? Icons.cloud_done : Icons.cloud_off,
              color: isHealthy ? Colors.green : Colors.red,
            ),
            title: Text('${status['environment']} Services'),
            subtitle: Text(status['message'] ?? 'Unknown status'),
            trailing: showDetails 
                ? IconButton(
                    icon: Icon(Icons.info_outline),
                    onPressed: () => DeploymentHelper.showDeploymentStatus(context),
                  )
                : null,
            onTap: showDetails 
                ? () => DeploymentHelper.showDeploymentStatus(context)
                : null,
          ),
        );
      },
    );
  }
}
