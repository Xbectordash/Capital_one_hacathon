import 'dart:io';
import 'dart:ui';
import 'package:farmmate/features/chat/models/chat_message.dart';
import 'package:farmmate/utils/constants/app_colors.dart';
import 'package:flutter/material.dart';

class ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const ChatBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final isUserMessage = message.sender == MessageSender.user;
    final isSystemMessage = message.sender == MessageSender.system;
    
    // System messages get a different style
    if (isSystemMessage) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 16),
        child: Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: AppColors.paleGreen,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppColors.borderColor, width: 1),
            ),
            child: Text(
              message.text,
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.textSecondary,
                fontStyle: FontStyle.italic,
                fontWeight: FontWeight.w500,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      );
    }
    
    return AnimatedPadding(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
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
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: isUserMessage
                    ? [AppColors.primaryGreen, AppColors.lightGreen]
                    : [AppColors.pureWhite, AppColors.offWhite],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.only(
                topLeft: const Radius.circular(20),
                topRight: const Radius.circular(20),
                bottomLeft: Radius.circular(isUserMessage ? 20 : 4),
                bottomRight: Radius.circular(isUserMessage ? 4 : 20),
              ),
              boxShadow: [
                BoxShadow(
                  color: AppColors.shadowColor,
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
              border: Border.all(
                color: isUserMessage
                    ? AppColors.primaryGreen.withOpacity(0.3)
                    : AppColors.borderColor,
                width: 1,
              ),
            ),
            child: Container(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (message.files != null && message.files!.isNotEmpty)
                    Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      decoration: BoxDecoration(
                        color: isUserMessage 
                            ? AppColors.pureWhite.withOpacity(0.2)
                            : AppColors.paleGreen,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isUserMessage
                              ? AppColors.pureWhite.withOpacity(0.3)
                              : AppColors.borderColor,
                          width: 1,
                        ),
                      ),
                      height: 120,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(16),
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
                              margin: const EdgeInsets.all(8),
                              child: isImage && file.path != null
                                  ? ClipRRect(
                                      borderRadius: BorderRadius.circular(12),
                                      child: Image.file(
                                        File(file.path!),
                                        height: 104,
                                        width: 104,
                                        fit: BoxFit.cover,
                                      ),
                                    )
                                  : Container(
                                      width: 104,
                                      padding: const EdgeInsets.all(12),
                                      decoration: BoxDecoration(
                                        color: isUserMessage
                                            ? AppColors.pureWhite.withOpacity(0.9)
                                            : AppColors.pureWhite,
                                        borderRadius: BorderRadius.circular(12),
                                        boxShadow: [
                                          BoxShadow(
                                            color: AppColors.shadowColor,
                                            blurRadius: 4,
                                            offset: const Offset(0, 2),
                                          ),
                                        ],
                                      ),
                                      child: Column(
                                        mainAxisAlignment: MainAxisAlignment.center,
                                        children: [
                                          Icon(
                                            Icons.insert_drive_file_rounded,
                                            color: AppColors.primaryGreen,
                                            size: 32,
                                          ),
                                          const SizedBox(height: 8),
                                          Text(
                                            file.name,
                                            style: const TextStyle(
                                              color: AppColors.textPrimary,
                                              fontSize: 10,
                                              fontWeight: FontWeight.w500,
                                            ),
                                            textAlign: TextAlign.center,
                                            maxLines: 2,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                        ],
                                      ),
                                    ),
                            );
                          },
                        ),
                      ),
                    ),
                  if (message.text.isNotEmpty)
                    Text(
                      message.text,
                      style: TextStyle(
                        fontSize: 15,
                        color: isUserMessage
                            ? AppColors.pureWhite
                            : AppColors.textPrimary,
                        height: 1.4,
                        letterSpacing: 0.3,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Text(
                          '${DateTime.now().hour.toString().padLeft(2, '0')}:${DateTime.now().minute.toString().padLeft(2, '0')}',
                          style: TextStyle(
                            fontSize: 11,
                            color: isUserMessage
                                ? AppColors.pureWhite.withOpacity(0.7)
                                : AppColors.textLight,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        if (isUserMessage) ...[
                          const SizedBox(width: 4),
                          Icon(
                            Icons.done_all_rounded,
                            size: 16,
                            color: AppColors.pureWhite.withOpacity(0.7),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
