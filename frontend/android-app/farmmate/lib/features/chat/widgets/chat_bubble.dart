import 'dart:io';
import 'dart:ui';
import 'package:farmmate/features/chat/models/chat_message.dart';
import 'package:flutter/material.dart';

/// A widget that displays a single chat message in a bubble.
class ChatBubble extends StatelessWidget {
  /// The chat message to be displayed.
  final ChatMessage message;

  /// Creates a [ChatBubble] widget.
  const ChatBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final isUserMessage = message.sender == MessageSender.user;
    return AnimatedPadding(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
      child: Align(
        alignment: isUserMessage ? Alignment.centerRight : Alignment.centerLeft,
        child: Container(
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.75,
          ),
          margin: EdgeInsets.only(
            left: isUserMessage ? 50 : 0,
            right: isUserMessage ? 0 : 50,
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.only(
              topLeft: const Radius.circular(24),
              topRight: const Radius.circular(24),
              bottomLeft: Radius.circular(isUserMessage ? 24 : 8),
              bottomRight: Radius.circular(isUserMessage ? 8 : 24),
            ),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: isUserMessage
                        ? [
                            const Color(0xFF2F7FF4).withOpacity(0.8),
                            const Color(0xFF2F7FF4).withOpacity(0.6),
                          ]
                        : [
                            Colors.white.withOpacity(0.8),
                            Colors.white.withOpacity(0.6),
                          ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  border: Border.all(
                    color: isUserMessage
                        ? Colors.white.withOpacity(0.2)
                        : const Color(0xFF2F7FF4).withOpacity(0.1),
                    width: 1,
                  ),
                  borderRadius: BorderRadius.only(
                    topLeft: const Radius.circular(24),
                    topRight: const Radius.circular(24),
                    bottomLeft: Radius.circular(isUserMessage ? 24 : 8),
                    bottomRight: Radius.circular(isUserMessage ? 8 : 24),
                  ),
                ),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (message.files != null && message.files!.isNotEmpty)
                        Container(
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(16),
                          ),
                          height: 120,
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(16),
                            child: BackdropFilter(
                              filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
                              child: ListView.builder(
                                scrollDirection: Axis.horizontal,
                                itemCount: message.files!.length,
                                itemBuilder: (context, index) {
                                  final file = message.files![index];
                                  final isImage =
                                      file.extension?.toLowerCase() == 'png' ||
                                      file.extension?.toLowerCase() == 'jpg' ||
                                      file.extension?.toLowerCase() == 'jpeg';
                                  return Container(
                                    margin: const EdgeInsets.only(right: 8),
                                    child: isImage && file.path != null
                                        ? ClipRRect(
                                            borderRadius: BorderRadius.circular(
                                              12,
                                            ),
                                            child: Image.file(
                                              File(file.path!),
                                              height: 120,
                                              width: 120,
                                              fit: BoxFit.cover,
                                            ),
                                          )
                                        : Container(
                                            padding: const EdgeInsets.all(12),
                                            decoration: BoxDecoration(
                                              color: Colors.white.withOpacity(
                                                0.1,
                                              ),
                                              borderRadius:
                                                  BorderRadius.circular(12),
                                              border: Border.all(
                                                color: Colors.white.withOpacity(
                                                  0.2,
                                                ),
                                                width: 1,
                                              ),
                                            ),
                                            child: Column(
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                Icon(
                                                  Icons.insert_drive_file,
                                                  color: isUserMessage
                                                      ? Colors.white70
                                                      : Colors.black54,
                                                  size: 32,
                                                ),
                                                const SizedBox(height: 8),
                                                Text(
                                                  file.name,
                                                  style: TextStyle(
                                                    color: isUserMessage
                                                        ? Colors.white70
                                                        : Colors.black54,
                                                    fontSize: 12,
                                                    fontWeight: FontWeight.w500,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                  );
                                },
                              ),
                            ),
                          ),
                        ),
                      if (message.text.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: Text(
                            message.text,
                            style: TextStyle(
                              fontSize: 16,
                              color: isUserMessage
                                  ? Colors.white
                                  : Colors.black87,
                              height: 1.4,
                              letterSpacing: 0.2,
                            ),
                          ),
                        ),
                      Padding(
                        padding: const EdgeInsets.only(top: 6),
                        child: Text(
                          '${DateTime.now().hour}:${DateTime.now().minute}',
                          style: TextStyle(
                            fontSize: 11,
                            color: isUserMessage
                                ? Colors.white.withOpacity(0.6)
                                : Colors.black45,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
