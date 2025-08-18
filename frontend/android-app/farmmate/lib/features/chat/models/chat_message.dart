import 'package:file_picker/file_picker.dart';

/// An enumeration representing the sender of a chat message.
enum MessageSender {
  /// The message was sent by the user.
  user,

  /// The message was sent by the bot.
  bot
}

/// A class representing a single chat message.
class ChatMessage {
  /// The text content of the message.
  final String text;

  /// The sender of the message.
  final MessageSender sender;

  /// A list of files attached to the message.
  final List<PlatformFile>? files;

  /// The timestamp of when the message was sent.
  final DateTime timestamp;

  /// Creates a [ChatMessage] object.
  ChatMessage({
    required this.text,
    required this.sender,
    this.files,
    required this.timestamp,
  });
}
