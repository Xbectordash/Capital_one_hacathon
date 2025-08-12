import 'dart:io';
import 'package:farmmate/utils/constants/app_assets.dart';
import 'package:farmmate/utils/constants/app_sizes.dart';
import 'package:farmmate/utils/constants/app_strings.dart';
import 'package:farmmate/features/chat/models/chat_message.dart';
import 'package:farmmate/features/chat/widgets/chat_bubble.dart';
import 'package:farmmate/utils/extensions/app_extensions.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_speech/flutter_speech.dart';
import 'package:logger/web.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  Logger logger = Logger();
  FilePickerResult? result;
  late SpeechRecognition _speech;
  bool _isListening = false;
  bool _isSpeechAvailable = false;
  String _currentLocaleId = '';
  final TextEditingController _textController = TextEditingController();
  final List<ChatMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    activateSpeechRecognizer();
  }

  void activateSpeechRecognizer() {
    _speech = SpeechRecognition();
    _speech.setAvailabilityHandler(onSpeechAvailability);
    _speech.setRecognitionStartedHandler(onRecognitionStarted);
    _speech.setRecognitionResultHandler(onRecognitionResult);
    _speech.setRecognitionCompleteHandler(onRecognitionComplete);

    // The 'activate' method returns a bool to confirm if activation was successful.
    _speech.activate("en_US").then((isActivated) {
      setState(() {
        // Assign the bool result to your new bool variable
        _isSpeechAvailable = isActivated;

        // You already know the locale is "en_US" because you passed it.
        if (isActivated) {
          _currentLocaleId = "en_US";
        }
      });
    });
  }

  void onSpeechAvailability(bool isAvailable) {
    setState(() => _isListening = isAvailable);
  }

  void onRecognitionStarted() {
    setState(() => _isListening = true);
  }

  void onRecognitionResult(String text) {
    setState(() {
      _textController.text = text;
    });
  }

  void onRecognitionComplete(String text) {
    setState(() {
      _isListening = false;
      // If you also want the final recognized text:
      _textController.text = text;
    });
  }

  void startListening() {
    _speech.listen().then((_) {
      print('Started listening...');
    });
  }

  void stopListening() {
    _speech.stop().then((_) {
      setState(() => _isListening = false);
    });
  }

  void _sendMessage() {
    if (_textController.text.isEmpty &&
        (result == null || result!.files.isEmpty)) {
      return;
    }

    final userMessage = ChatMessage(
      text: _textController.text,
      sender: MessageSender.user,
      files: result?.files,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.add(userMessage);
      _textController.clear();
      result = null;
    });

    // Simulate a bot response
    Future.delayed(const Duration(seconds: 1), () {
      final botMessage = ChatMessage(
        text: 'This is a mock response.',
        sender: MessageSender.bot,
        timestamp: DateTime.now(),
      );
      setState(() {
        _messages.add(botMessage);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnnotatedRegion(
      value: const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarBrightness: Brightness.dark,
        statusBarIconBrightness: Brightness.dark,
      ),
      child: SafeArea(
        child: Scaffold(
          backgroundColor: const Color(0xFFF8F9FE),
          key: _scaffoldKey,
          drawer: Drawer(
            backgroundColor: Colors.white.withOpacity(0.95),
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                const SizedBox(height: 50),
                ListTile(
                  leading: const Icon(Icons.home),
                  title: const Text('Home'),
                  onTap: () {
                    Navigator.pop(context);
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.settings),
                  title: const Text('Settings'),
                  onTap: () {
                    Navigator.pop(context);
                  },
                ),
              ],
            ),
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
            child: Column(
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: context.screenWidth * 0.05,
                    vertical: context.screenHeight * 0.015,
                  ),
                  child: Row(
                    children: [
                      GestureDetector(
                        onTap: () {
                          _scaffoldKey.currentState?.openDrawer();
                        },
                        child: Image.asset(
                          AppAssets.blackHamburgur,
                          height: 30,
                          width: 30,
                        ),
                      ),
                      Padding(
                        padding: EdgeInsets.only(
                          left: context.screenWidth * 0.05,
                        ),
                        child: Text(
                          AppStrings.appName,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                      Spacer(),
                      GestureDetector(
                        onTap: () {
                          print('Dot menu');
                        },
                        child: Image.asset(
                          AppAssets.blackMenuDots,
                          height: 25,
                          width: 25,
                        ),
                      ),
                    ],
                  ),
                ),
                Divider(thickness: 0.5),
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.5),
                      borderRadius: const BorderRadius.only(
                        topLeft: Radius.circular(30),
                        topRight: Radius.circular(30),
                      ),
                    ),
                    child: ClipRRect(
                      borderRadius: const BorderRadius.only(
                        topLeft: Radius.circular(30),
                        topRight: Radius.circular(30),
                      ),
                      child: ListView.builder(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        itemCount: _messages.length,
                        itemBuilder: (context, index) {
                          return ChatBubble(message: _messages[index]);
                        },
                      ),
                    ),
                  ),
                ),
                Container(
                  width: double.infinity,
                  padding: EdgeInsets.symmetric(
                    horizontal: context.screenWidth * 0.05,
                    vertical: context.screenHeight * 0.02,
                  ),
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(30),
                      topRight: Radius.circular(30),
                    ),
                    color: Colors.white.withOpacity(0.9),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.05),
                        blurRadius: 10,
                        offset: const Offset(0, -5),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      GestureDetector(
                        onTap: () async {
                          final pickedFiles = await FilePicker.platform
                              .pickFiles(allowMultiple: true);
                          if (pickedFiles == null) {
                            logger.e("No file selected");
                          } else {
                            setState(() {
                              result = pickedFiles;
                            });
                            for (var element in result!.files) {
                              logger.d(element.name);
                            }
                          }
                        },
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(100),
                            color: Colors.blue.withOpacity(0.1),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(12),
                            child: Image.asset(
                              AppAssets.blackImageGallery,
                              width: 22,
                              height: 22,
                            ),
                          ),
                        ),
                      ),
                      SizedBox(width: context.screenWidth * 0.02),
                      Expanded(
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 15),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(25),
                            color: Colors.blue.withOpacity(0.05),
                            border: Border.all(
                              color: Colors.blue.withOpacity(0.1),
                              width: 1,
                            ),
                          ),
                          child: Row(
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    if (result != null &&
                                        result!.files.isNotEmpty)
                                      Padding(
                                        padding: const EdgeInsets.symmetric(
                                          vertical: 8,
                                        ),
                                        child: SizedBox(
                                          height: 50,
                                          child: ListView.separated(
                                            scrollDirection: Axis.horizontal,
                                            itemCount: result!.files.length,
                                            separatorBuilder: (_, __) =>
                                                SizedBox(width: 8),
                                            itemBuilder: (context, index) {
                                              final file = result!.files[index];
                                              final isImage =
                                                  file.extension
                                                          ?.toLowerCase()
                                                          .contains('png') ==
                                                      true ||
                                                  file.extension
                                                          ?.toLowerCase()
                                                          .contains('jpg') ==
                                                      true ||
                                                  file.extension
                                                          ?.toLowerCase()
                                                          .contains('jpeg') ==
                                                      true;

                                              return Stack(
                                                children: [
                                                  Container(
                                                    padding: EdgeInsets.all(5),
                                                    decoration: BoxDecoration(
                                                      color: Colors.white,
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                            8,
                                                          ),
                                                    ),
                                                    child: Row(
                                                      mainAxisSize:
                                                          MainAxisSize.min,
                                                      children: [
                                                        if (isImage &&
                                                            file.path != null)
                                                          Image.file(
                                                            File(file.path!),
                                                            width: 40,
                                                            height: 40,
                                                            fit: BoxFit.cover,
                                                          )
                                                        else
                                                          Icon(
                                                            Icons
                                                                .insert_drive_file,
                                                            size: 30,
                                                            color: Colors.grey,
                                                          ),
                                                      ],
                                                    ),
                                                  ),
                                                  Positioned(
                                                    right: -10,
                                                    top: -10,
                                                    child: IconButton(
                                                      padding: EdgeInsets.zero,
                                                      constraints:
                                                          const BoxConstraints(),
                                                      icon: const Icon(
                                                        Icons.cancel,
                                                        size: 18,
                                                      ),
                                                      onPressed: () {
                                                        setState(() {
                                                          final files = result!
                                                              .files
                                                              .toList();
                                                          files.removeAt(index);
                                                          if (files.isEmpty) {
                                                            result = null;
                                                          } else {
                                                            result =
                                                                FilePickerResult(
                                                                  files,
                                                                );
                                                          }
                                                        });
                                                      },
                                                    ),
                                                  ),
                                                ],
                                              );
                                            },
                                          ),
                                        ),
                                      ),
                                    Row(
                                      children: [
                                        Expanded(
                                          child: TextField(
                                            controller: _textController,
                                            decoration: InputDecoration(
                                              hintText:
                                                  AppStrings.askAnythingHint,
                                              border: InputBorder.none,
                                            ),
                                          ),
                                        ),
                                        GestureDetector(
                                          onTap: () {
                                            if (_isListening) {
                                              stopListening();
                                            } else {
                                              startListening();
                                            }
                                          },
                                          child: Icon(
                                            _isListening
                                                ? Icons.mic_off
                                                : Icons.mic,
                                            color: _isListening
                                                ? Colors.red
                                                : Colors.black,
                                          ),
                                        ),
                                        SizedBox(
                                          width: context.screenWidth * 0.025,
                                        ),
                                        GestureDetector(
                                          onTap: _sendMessage,
                                          child: Image.asset(
                                            AppAssets.blackSend,
                                            width: 23,
                                            height: 23,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
