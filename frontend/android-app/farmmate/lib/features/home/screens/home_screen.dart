import 'dart:io';
import 'dart:ui'; // Needed for BackdropFilter blur effect
import 'package:farmmate/l10n/app_localizations.dart';
import 'package:farmmate/services/language_provider.dart';
import 'package:farmmate/utils/constants/app_assets.dart';
import 'package:farmmate/features/chat/models/chat_message.dart';
import 'package:farmmate/features/chat/widgets/chat_bubble.dart';
import 'package:farmmate/utils/extensions/app_extensions.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:logger/web.dart';
import 'package:speech_to_text/speech_to_text.dart';

/// The main screen of the application, displaying the chat interface and drawer menu.
class HomeScreen extends StatefulWidget {
  /// Creates a [HomeScreen] widget.
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  /// A global key to control the scaffold, used for opening the drawer.
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  /// A logger for debugging purposes.
  Logger logger = Logger();

  /// The result of a file picker operation.
  FilePickerResult? result;

  /// A controller for the text input field.
  final TextEditingController _textController = TextEditingController();

  /// A list of chat messages to be displayed.
  final List<ChatMessage> _messages = [];

  /// An instance of the speech-to-text plugin.
  final SpeechToText _speechToText = SpeechToText();

  /// A flag to indicate whether speech recognition is enabled.
  bool _speechEnabled = false;

  /// A flag to indicate whether the app is currently listening for speech.
  bool _isListening = false;

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  /// Initializes the speech-to-text functionality.
  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

  /// Starts listening for speech input.
  void _startListening() async {
    await _speechToText.listen(
      onResult: (result) {
        setState(() {
          _textController.text = result.recognizedWords;
        });
      },
    );
    setState(() {
      _isListening = true;
    });
  }

  /// Stops listening for speech input.
  void _stopListening() async {
    await _speechToText.stop();
    setState(() {
      _isListening = false;
    });
  }

  /// Sends a chat message.
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

  Widget _drawerItem(
    IconData icon,
    String title,
    VoidCallback onTap, [
    Color color = Colors.white,
  ]) {
    return ListTile(
      leading: Icon(icon, color: color),
      title: Text(
        title,
        style: TextStyle(color: color, fontWeight: FontWeight.w500),
      ),
      onTap: onTap,
    );
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
            backgroundColor: Colors.transparent,
            child: Stack(
              children: [
                ClipRRect(
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.15),
                        borderRadius: const BorderRadius.only(
                          topRight: Radius.circular(30),
                          bottomRight: Radius.circular(30),
                        ),
                        border: Border.all(
                          color: Colors.white.withOpacity(0.3),
                          width: 1.5,
                        ),
                      ),
                    ),
                  ),
                ),
                ListView(
                  padding: EdgeInsets.zero,
                  children: [
                    const SizedBox(height: 50),
                    _drawerItem(
                      Icons.home,
                      AppLocalizations.of(context)!.home,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.chat,
                      AppLocalizations.of(context)!.newChat,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.history,
                      AppLocalizations.of(context)!.chatHistory,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.bookmark,
                      AppLocalizations.of(context)!.savedResponses,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.person,
                      AppLocalizations.of(context)!.profile,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.settings,
                      AppLocalizations.of(context)!.settings,
                      () => Navigator.pop(context),
                    ),
                    _drawerItem(
                      Icons.info,
                      AppLocalizations.of(context)!.aboutApp,
                      () => Navigator.pop(context),
                    ),
                    const Divider(color: Colors.white54, thickness: 0.8),
                    _drawerItem(
                      Icons.logout,
                      AppLocalizations.of(context)!.logout,
                      () => Navigator.pop(context),
                      Colors.redAccent,
                    ),
                  ],
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
                          AppLocalizations.of(context)!.appName,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                      Spacer(),
                      GestureDetector(
                        onTap: () {
                          showDialog(
                            context: context,
                            builder: (_) => AlertDialog(
                              title: const Text("Select Language"),
                              content: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  ListTile(
                                    title: const Text("English"),
                                    onTap: () {
                                      LanguageProvider.of(
                                        context,
                                      ).setLocale(const Locale('en'));
                                      Navigator.pop(context);
                                    },
                                  ),
                                  ListTile(
                                    title: const Text("मराठी"),
                                    onTap: () {
                                      LanguageProvider.of(
                                        context,
                                      ).setLocale(const Locale('mr'));
                                      Navigator.pop(context);
                                    },
                                  ),
                                  ListTile(
                                    title: const Text("हिंदी"),
                                    onTap: () {
                                      LanguageProvider.of(
                                        context,
                                      ).setLocale(const Locale('hi'));
                                      Navigator.pop(context);
                                    },
                                  ),
                                  ListTile(
                                    title: const Text("ಕನ್ನಡ"),
                                    onTap: () {
                                      LanguageProvider.of(
                                        context,
                                      ).setLocale(const Locale('kn'));
                                      Navigator.pop(context);
                                    },
                                  ),
                                  ListTile(
                                    title: const Text("ગુજરાતી"),
                                    onTap: () {
                                      LanguageProvider.of(
                                        context,
                                      ).setLocale(const Locale('gu'));
                                      Navigator.pop(context);
                                    },
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                        child: Image.asset(
                          AppAssets.languageIcon,
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
                                              hintText: AppLocalizations.of(
                                                context,
                                              )!.askAnythingHint,
                                              border: InputBorder.none,
                                            ),
                                          ),
                                        ),
                                        GestureDetector(
                                          onTap: _speechEnabled
                                              ? () {
                                                  if (!_isListening) {
                                                    _startListening();
                                                  } else {
                                                    _stopListening();
                                                  }
                                                }
                                              : null,
                                          child: Icon(
                                            _isListening
                                                ? Icons.mic_off
                                                : Icons.mic,
                                            color: _speechEnabled
                                                ? (_isListening
                                                      ? Colors.red
                                                      : Colors.black)
                                                : Colors.grey,
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
