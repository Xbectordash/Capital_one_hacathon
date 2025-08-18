import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:geolocator/geolocator.dart';
import '../../../providers/chat_provider.dart';
import '../../../services/location_service.dart';
import '../../../utils/extensions/app_extensions.dart';

class LocationSettingsScreen extends StatefulWidget {
  const LocationSettingsScreen({super.key});

  @override
  State<LocationSettingsScreen> createState() => _LocationSettingsScreenState();
}

class _LocationSettingsScreenState extends State<LocationSettingsScreen> {
  final TextEditingController _locationController = TextEditingController();
  bool _isLoadingLocation = false;
  bool _isSettingCustomLocation = false;
  String? _currentLocationDetails;

  @override
  void initState() {
    super.initState();
    _loadCurrentLocation();
  }

  Future<void> _loadCurrentLocation() async {
    final chatProvider = Provider.of<ChatProvider>(context, listen: false);
    _locationController.text = chatProvider.currentLocation;
    await _getLocationDetails();
  }

  Future<void> _getLocationDetails() async {
    setState(() {
      _isLoadingLocation = true;
    });

    try {
      final savedLocation = await LocationService.getSavedLocation();
      if (savedLocation != null) {
        setState(() {
          _currentLocationDetails = 
              'Lat: ${savedLocation['latitude'].toStringAsFixed(4)}, '
              'Lng: ${savedLocation['longitude'].toStringAsFixed(4)}';
        });
      }
    } catch (e) {
      print('Error getting location details: $e');
    } finally {
      setState(() {
        _isLoadingLocation = false;
      });
    }
  }

  Future<void> _getCurrentLocation() async {
    setState(() {
      _isLoadingLocation = true;
    });

    try {
      // Check and request permissions
      bool hasPermission = await LocationService.hasLocationPermission();
      if (!hasPermission) {
        hasPermission = await LocationService.requestLocationPermission();
        if (!hasPermission) {
          _showPermissionDialog();
          return;
        }
      }

      // Check if location services are enabled
      bool isLocationEnabled = await LocationService.isLocationServiceEnabled();
      if (!isLocationEnabled) {
        _showLocationServiceDialog();
        return;
      }

      Position? position = await LocationService.getCurrentPosition();
      if (position != null) {
        String? address = await LocationService.getAddressFromCoordinates(
          position.latitude,
          position.longitude,
        );
        
        if (address != null) {
          await LocationService.saveLocation(position, address);
          _locationController.text = address;
          
          final chatProvider = Provider.of<ChatProvider>(context, listen: false);
          await chatProvider.refreshLocation();
          
          await _getLocationDetails();
          
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('📍 Location updated successfully!'),
                backgroundColor: Colors.green,
              ),
            );
          }
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ Error getting location: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isLoadingLocation = false;
      });
    }
  }

  Future<void> _setCustomLocation() async {
    if (_locationController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('❌ Please enter a location'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() {
      _isSettingCustomLocation = true;
    });

    try {
      final chatProvider = Provider.of<ChatProvider>(context, listen: false);
      await chatProvider.setCustomLocation(_locationController.text.trim());
      
      await _getLocationDetails();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('📍 Custom location set successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('❌ Error setting location: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isSettingCustomLocation = false;
      });
    }
  }

  void _showPermissionDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Location Permission Required'),
        content: const Text(
          'This app needs location permission to provide location-based farming advice. '
          'Please grant location permission in app settings.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              LocationService.openLocationSettings();
            },
            child: const Text('Open Settings'),
          ),
        ],
      ),
    );
  }

  void _showLocationServiceDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Location Services Disabled'),
        content: const Text(
          'Location services are disabled. Please enable location services to get your current location.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              LocationService.openLocationSettings();
            },
            child: const Text('Enable'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FE),
      appBar: AppBar(
        title: const Text('Location Settings'),
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
        child: Padding(
          padding: EdgeInsets.all(context.screenWidth * 0.05),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Current Location Section
              Card(
                elevation: 2,
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
                          const Icon(Icons.location_on, color: Colors.blue),
                          const SizedBox(width: 8),
                          const Text(
                            'Current Location',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Consumer<ChatProvider>(
                        builder: (context, chatProvider, _) {
                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                chatProvider.currentLocation.isEmpty
                                    ? 'No location set'
                                    : chatProvider.currentLocation,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              if (_currentLocationDetails != null) ...[
                                const SizedBox(height: 4),
                                Text(
                                  _currentLocationDetails!,
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                              ],
                            ],
                          );
                        },
                      ),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 20),
              
              // Get Current Location Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _isLoadingLocation ? null : _getCurrentLocation,
                  icon: _isLoadingLocation
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.my_location),
                  label: Text(_isLoadingLocation 
                      ? 'Getting Location...' 
                      : 'Use Current Location'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 15),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                ),
              ),
              
              const SizedBox(height: 20),
              
              // Custom Location Section
              Card(
                elevation: 2,
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
                          const Icon(Icons.edit_location, color: Colors.green),
                          const SizedBox(width: 8),
                          const Text(
                            'Set Custom Location',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        controller: _locationController,
                        decoration: InputDecoration(
                          hintText: 'Enter city, state, or address',
                          prefixIcon: const Icon(Icons.search),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                          filled: true,
                          fillColor: Colors.grey[50],
                        ),
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _isSettingCustomLocation ? null : _setCustomLocation,
                          icon: _isSettingCustomLocation
                              ? const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(strokeWidth: 2),
                                )
                              : const Icon(Icons.check),
                          label: Text(_isSettingCustomLocation 
                              ? 'Setting Location...' 
                              : 'Set Location'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 15),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 20),
              
              // Information Card
              Card(
                elevation: 1,
                color: Colors.blue[50],
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                child: const Padding(
                  padding: EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue),
                      SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'Your location helps FarmMate provide accurate weather, soil, and regional farming advice.',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.blue,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _locationController.dispose();
    super.dispose();
  }
}
