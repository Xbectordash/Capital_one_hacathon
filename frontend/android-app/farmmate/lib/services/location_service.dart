import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:logger/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocationService {
  static final Logger _logger = Logger();
  static const String _locationKey = 'user_location';
  static const String _locationNameKey = 'user_location_name';
  
  /// Check if location permissions are granted
  static Future<bool> hasLocationPermission() async {
    LocationPermission permission = await Geolocator.checkPermission();
    
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return false;
      }
    }
    
    if (permission == LocationPermission.deniedForever) {
      return false;
    }
    
    return true;
  }
  
  /// Request location permissions
  static Future<bool> requestLocationPermission() async {
    try {
      PermissionStatus status = await Permission.location.request();
      return status.isGranted;
    } catch (e) {
      _logger.e('Error requesting location permission: $e');
      return false;
    }
  }
  
  /// Get current position
  static Future<Position?> getCurrentPosition() async {
    try {
      bool hasPermission = await hasLocationPermission();
      if (!hasPermission) {
        _logger.w('Location permission not granted');
        return null;
      }
      
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      
      _logger.i('Current position: ${position.latitude}, ${position.longitude}');
      return position;
    } catch (e) {
      _logger.e('Error getting current position: $e');
      return null;
    }
  }
  
  /// Get address from coordinates
  static Future<String?> getAddressFromCoordinates(
    double latitude,
    double longitude,
  ) async {
    try {
      List<Placemark> placemarks = await placemarkFromCoordinates(
        latitude,
        longitude,
      );
      
      if (placemarks.isNotEmpty) {
        Placemark place = placemarks[0];
        String address = '';
        
        if (place.subLocality != null && place.subLocality!.isNotEmpty) {
          address += '${place.subLocality}, ';
        }
        if (place.locality != null && place.locality!.isNotEmpty) {
          address += '${place.locality}, ';
        }
        if (place.administrativeArea != null && place.administrativeArea!.isNotEmpty) {
          address += '${place.administrativeArea}, ';
        }
        if (place.country != null && place.country!.isNotEmpty) {
          address += place.country!;
        }
        
        // Remove trailing comma and space
        if (address.endsWith(', ')) {
          address = address.substring(0, address.length - 2);
        }
        
        _logger.i('Address: $address');
        return address;
      }
    } catch (e) {
      _logger.e('Error getting address: $e');
    }
    return null;
  }
  
  /// Get coordinates from address
  static Future<Position?> getCoordinatesFromAddress(String address) async {
    try {
      List<Location> locations = await locationFromAddress(address);
      
      if (locations.isNotEmpty) {
        Location location = locations[0];
        Position position = Position(
          latitude: location.latitude,
          longitude: location.longitude,
          timestamp: DateTime.now(),
          accuracy: 0,
          altitude: 0,
          altitudeAccuracy: 0,
          heading: 0,
          headingAccuracy: 0,
          speed: 0,
          speedAccuracy: 0,
        );
        
        _logger.i('Coordinates for $address: ${position.latitude}, ${position.longitude}');
        return position;
      }
    } catch (e) {
      _logger.e('Error getting coordinates from address: $e');
    }
    return null;
  }
  
  /// Save location to local storage
  static Future<void> saveLocation(Position position, String address) async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString(_locationKey, '${position.latitude},${position.longitude}');
      await prefs.setString(_locationNameKey, address);
      _logger.i('Location saved: $address');
    } catch (e) {
      _logger.e('Error saving location: $e');
    }
  }
  
  /// Get saved location
  static Future<Map<String, dynamic>?> getSavedLocation() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      String? locationCoords = prefs.getString(_locationKey);
      String? locationName = prefs.getString(_locationNameKey);
      
      if (locationCoords != null && locationName != null) {
        List<String> coords = locationCoords.split(',');
        if (coords.length == 2) {
          return {
            'latitude': double.parse(coords[0]),
            'longitude': double.parse(coords[1]),
            'address': locationName,
          };
        }
      }
    } catch (e) {
      _logger.e('Error getting saved location: $e');
    }
    return null;
  }
  
  /// Clear saved location
  static Future<void> clearSavedLocation() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.remove(_locationKey);
      await prefs.remove(_locationNameKey);
      _logger.i('Saved location cleared');
    } catch (e) {
      _logger.e('Error clearing saved location: $e');
    }
  }
  
  /// Get location for farming queries
  static Future<String> getLocationForQuery() async {
    try {
      // First try to get saved location
      Map<String, dynamic>? savedLocation = await getSavedLocation();
      if (savedLocation != null) {
        return savedLocation['address'];
      }
      
      // If no saved location, get current location
      Position? position = await getCurrentPosition();
      if (position != null) {
        String? address = await getAddressFromCoordinates(
          position.latitude,
          position.longitude,
        );
        
        if (address != null) {
          // Save the current location for future use
          await saveLocation(position, address);
          return address;
        }
      }
      
      // Fallback to a default location
      return 'भारत'; // India in Hindi
    } catch (e) {
      _logger.e('Error getting location for query: $e');
      return 'भारत'; // India in Hindi
    }
  }
  
  /// Check if location services are enabled
  static Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }
  
  /// Open location settings
  static Future<void> openLocationSettings() async {
    await Geolocator.openLocationSettings();
  }
}
