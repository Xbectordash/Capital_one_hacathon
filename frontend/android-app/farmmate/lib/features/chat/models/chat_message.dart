import 'package:file_picker/file_picker.dart';

enum MessageSender { user, bot }

class ChatMessage {
  final String text;
  final MessageSender sender;
  final List<PlatformFile>? files;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.sender,
    this.files,
    required this.timestamp,
  });
}
