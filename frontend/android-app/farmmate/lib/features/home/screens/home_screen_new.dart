import 'dart:io';
import 'dart:ui'; // Needed for BackdropFilter blur effect
import 'package:farmmate/utils/constants/app_assets.dart';
import 'package:farmmate/utils/constants/app_strings.dart';
import 'package:farmmate/utils/constants/app_colors.dart';
import 'package:farmmate/features/chat/widgets/chat_bubble.dart';
import 'package:farmmate/utils/extensions/app_extensions.dart';
import 'package:farmmate/providers/chat_provider.dart';
import 'package:farmmate/screens/test_screen.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:logger/web.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:provider/provider.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  Logger logger = Logger();
  FilePickerResult? result;
  final TextEditingController _textController = TextEditingController();
  final SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  bool _isListening = false;

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

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

  void _stopListening() async {
    await _speechToText.stop();
    setState(() {
      _isListening = false;
    });
  }

  void _sendMessage() async {
    if (_textController.text.isEmpty &&
        (result == null || result!.files.isEmpty)) {
      return;
    }

    final chatProvider = Provider.of<ChatProvider>(context, listen: false);
    
    // Convert FilePickerResult to List<File>
    List<File>? files;
    if (result != null && result!.files.isNotEmpty) {
      files = result!.files
          .where((file) => file.path != null)
          .map((file) => File(file.path!))
          .toList();
    }

    await chatProvider.sendMessage(
      text: _textController.text,
      files: files,
    );

    setState(() {
      _textController.clear();
      result = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnnotatedRegion(
      value: const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarBrightness: Brightness.light,
        statusBarIconBrightness: Brightness.dark,
      ),
      child: SafeArea(
        child: Scaffold(
          backgroundColor: AppColors.warmWhite,
          key: _scaffoldKey,
          drawer: _buildModernDrawer(),
          body: Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  AppColors.gradientStart,
                  AppColors.gradientMiddle,
                  AppColors.gradientEnd,
                ],
                stops: [0.0, 0.5, 1.0],
              ),
            ),
            child: Column(
              children: [
                _buildModernAppBar(context),
                _buildChatArea(),
                _buildModernInputArea(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildModernDrawer() {
    return Drawer(
      backgroundColor: Colors.transparent,
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppColors.primaryGreen.withOpacity(0.95),
              AppColors.darkGreen.withOpacity(0.98),
            ],
          ),
          borderRadius: const BorderRadius.only(
            topRight: Radius.circular(30),
            bottomRight: Radius.circular(30),
          ),
          boxShadow: [
            BoxShadow(
              color: AppColors.shadowColor,
              blurRadius: 20,
              offset: const Offset(5, 0),
            ),
          ],
        ),
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const SizedBox(height: 60),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CircleAvatar(
                    radius: 30,
                    backgroundColor: AppColors.pureWhite,
                    child: Icon(
                      Icons.agriculture,
                      size: 30,
                      color: AppColors.primaryGreen,
                    ),
                  ),
                  SizedBox(height: 16),
                  Text(
                    'FarmMate AI',
                    style: TextStyle(
                      color: AppColors.pureWhite,
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'Your Agricultural Assistant',
                    style: TextStyle(
                      color: AppColors.textLight,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
            const Divider(color: AppColors.textLight, thickness: 0.5),
            _modernDrawerItem(Icons.home_rounded, 'Home', () => Navigator.pop(context)),
            _modernDrawerItem(Icons.chat_bubble_rounded, 'New Chat', () => Navigator.pop(context)),
            _modernDrawerItem(Icons.history_rounded, 'Chat History', () => Navigator.pop(context)),
            _modernDrawerItem(Icons.bookmark_rounded, 'Saved Responses', () => Navigator.pop(context)),
            _modernDrawerItem(Icons.person_rounded, 'Profile', () => Navigator.pop(context)),
            _modernDrawerItem(Icons.settings_rounded, 'Settings', () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/settings');
            }),
            _modernDrawerItem(Icons.language_rounded, 'Language Test', () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (context) => const TestScreen()));
            }),
            _modernDrawerItem(Icons.info_rounded, 'About App', () => Navigator.pop(context)),
            const SizedBox(height: 20),
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 20),
              child: Divider(color: AppColors.textLight.withOpacity(0.3), thickness: 0.5),
            ),
            _modernDrawerItem(Icons.logout_rounded, 'Logout', () => Navigator.pop(context), AppColors.error),
          ],
        ),
      ),
    );
  }

  Widget _modernDrawerItem(IconData icon, String title, VoidCallback onTap, [Color? color]) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: color != null ? color.withOpacity(0.1) : Colors.transparent,
      ),
      child: ListTile(
        leading: Icon(
          icon,
          color: color ?? AppColors.pureWhite,
          size: 24,
        ),
        title: Text(
          title,
          style: TextStyle(
            color: color ?? AppColors.pureWhite,
            fontWeight: FontWeight.w500,
            fontSize: 16,
          ),
        ),
        onTap: onTap,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }

  Widget _buildModernAppBar(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: context.screenWidth * 0.05,
        vertical: context.screenHeight * 0.02,
      ),
      decoration: BoxDecoration(
        color: AppColors.pureWhite.withOpacity(0.9),
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(25),
          bottomRight: Radius.circular(25),
        ),
        boxShadow: [
          BoxShadow(
            color: AppColors.shadowColor,
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            decoration: BoxDecoration(
              color: AppColors.primaryGreen,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: AppColors.shadowColor,
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: IconButton(
              onPressed: () => _scaffoldKey.currentState?.openDrawer(),
              icon: const Icon(
                Icons.menu_rounded,
                color: AppColors.pureWhite,
                size: 24,
              ),
            ),
          ),
          Expanded(
            child: Container(
              margin: EdgeInsets.only(left: context.screenWidth * 0.04),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'FarmMate AI',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  Text(
                    'Smart Farming Assistant',
                    style: TextStyle(
                      fontSize: 12,
                      color: AppColors.textSecondary,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
          ),
          Container(
            decoration: BoxDecoration(
              color: AppColors.paleGreen,
              borderRadius: BorderRadius.circular(12),
            ),
            child: IconButton(
              onPressed: () => print('More options'),
              icon: const Icon(
                Icons.more_vert_rounded,
                color: AppColors.primaryGreen,
                size: 24,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChatArea() {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: AppColors.pureWhite.withOpacity(0.8),
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: AppColors.shadowColor,
              blurRadius: 15,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(25),
          child: Consumer<ChatProvider>(
            builder: (context, chatProvider, _) {
              return Column(
                children: [
                  // Connection status indicator
                  if (chatProvider.useWebSocket)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      decoration: const BoxDecoration(
                        color: AppColors.paleGreen,
                        borderRadius: BorderRadius.only(
                          topLeft: Radius.circular(25),
                          topRight: Radius.circular(25),
                        ),
                      ),
                      child: Row(
                        children: [
                          Container(
                            width: 8,
                            height: 8,
                            decoration: BoxDecoration(
                              color: chatProvider.isConnected ? AppColors.success : AppColors.error,
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text(
                            chatProvider.isConnected ? 'Connected to FarmMate AI' : 'Disconnected',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: chatProvider.isConnected ? AppColors.success : AppColors.error,
                            ),
                          ),
                          const Spacer(),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: AppColors.primaryGreen,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              '${chatProvider.languages[chatProvider.selectedLanguage]}',
                              style: const TextStyle(
                                fontSize: 10,
                                color: AppColors.pureWhite,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  
                  // Chat messages
                  Expanded(
                    child: chatProvider.messages.isEmpty
                        ? _buildWelcomeScreen()
                        : ListView.builder(
                            padding: const EdgeInsets.all(20),
                            itemCount: chatProvider.messages.length,
                            itemBuilder: (context, index) {
                              return ChatBubble(message: chatProvider.messages[index]);
                            },
                          ),
                  ),
                  
                  // Loading indicator
                  if (chatProvider.isLoading)
                    Container(
                      padding: const EdgeInsets.all(20),
                      child: Row(
                        children: [
                          SpinKitThreeBounce(
                            color: AppColors.primaryGreen,
                            size: 20,
                          ),
                          const SizedBox(width: 12),
                          const Text(
                            'FarmMate is thinking...',
                            style: TextStyle(
                              color: AppColors.textSecondary,
                              fontStyle: FontStyle.italic,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeScreen() {
    return Container(
      padding: const EdgeInsets.all(40),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 100,
            height: 100,
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [AppColors.lightGreen, AppColors.primaryGreen],
              ),
              borderRadius: BorderRadius.circular(50),
              boxShadow: [
                BoxShadow(
                  color: AppColors.shadowColor,
                  blurRadius: 20,
                  offset: const Offset(0, 8),
                ),
              ],
            ),
            child: const Icon(
              Icons.agriculture_rounded,
              size: 50,
              color: AppColors.pureWhite,
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Welcome to FarmMate!',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 12),
          const Text(
            'Your AI-powered agricultural assistant',
            style: TextStyle(
              fontSize: 16,
              color: AppColors.textSecondary,
              fontWeight: FontWeight.w500,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          const Text(
            'Ask me anything about farming, crops, weather, or soil management',
            style: TextStyle(
              fontSize: 14,
              color: AppColors.textLight,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 32),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            alignment: WrapAlignment.center,
            children: [
              _buildSuggestionChip('Weather forecast', Icons.wb_sunny_rounded),
              _buildSuggestionChip('Crop advice', Icons.eco_rounded),
              _buildSuggestionChip('Soil testing', Icons.landscape_rounded),
              _buildSuggestionChip('Pest control', Icons.bug_report_rounded),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSuggestionChip(String text, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.paleGreen,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: AppColors.primaryGreen),
          const SizedBox(width: 8),
          Text(
            text,
            style: const TextStyle(
              color: AppColors.textPrimary,
              fontSize: 12,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildModernInputArea(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(
        horizontal: context.screenWidth * 0.05,
        vertical: context.screenHeight * 0.02,
      ),
      decoration: BoxDecoration(
        color: AppColors.pureWhite.withOpacity(0.95),
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(25),
          topRight: Radius.circular(25),
        ),
        boxShadow: [
          BoxShadow(
            color: AppColors.shadowColor,
            blurRadius: 15,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: Row(
        children: [
          // File picker button
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [AppColors.lightGreen, AppColors.primaryGreen],
              ),
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(
                  color: AppColors.shadowColor,
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: IconButton(
              onPressed: () async {
                final pickedFiles = await FilePicker.platform.pickFiles(allowMultiple: true);
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
              icon: const Icon(
                Icons.attach_file_rounded,
                color: AppColors.pureWhite,
                size: 24,
              ),
            ),
          ),
          SizedBox(width: context.screenWidth * 0.03),
          
          // Input field
          Expanded(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              decoration: BoxDecoration(
                color: AppColors.paleGreen,
                borderRadius: BorderRadius.circular(25),
                border: Border.all(color: AppColors.borderColor, width: 1),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // File preview
                  if (result != null && result!.files.isNotEmpty)
                    Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      height: 50,
                      child: ListView.separated(
                        scrollDirection: Axis.horizontal,
                        itemCount: result!.files.length,
                        separatorBuilder: (_, __) => const SizedBox(width: 8),
                        itemBuilder: (context, index) {
                          final file = result!.files[index];
                          final isImage = file.extension?.toLowerCase().contains('png') == true ||
                              file.extension?.toLowerCase().contains('jpg') == true ||
                              file.extension?.toLowerCase().contains('jpeg') == true;

                          return Stack(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: AppColors.pureWhite,
                                  borderRadius: BorderRadius.circular(12),
                                  boxShadow: [
                                    BoxShadow(
                                      color: AppColors.shadowColor,
                                      blurRadius: 4,
                                      offset: const Offset(0, 2),
                                    ),
                                  ],
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    if (isImage && file.path != null)
                                      ClipRRect(
                                        borderRadius: BorderRadius.circular(8),
                                        child: Image.file(
                                          File(file.path!),
                                          width: 34,
                                          height: 34,
                                          fit: BoxFit.cover,
                                        ),
                                      )
                                    else
                                      Container(
                                        width: 34,
                                        height: 34,
                                        decoration: BoxDecoration(
                                          color: AppColors.paleGreen,
                                          borderRadius: BorderRadius.circular(8),
                                        ),
                                        child: const Icon(
                                          Icons.insert_drive_file_rounded,
                                          size: 20,
                                          color: AppColors.primaryGreen,
                                        ),
                                      ),
                                  ],
                                ),
                              ),
                              Positioned(
                                right: -8,
                                top: -8,
                                child: Container(
                                  decoration: const BoxDecoration(
                                    color: AppColors.error,
                                    shape: BoxShape.circle,
                                  ),
                                  child: IconButton(
                                    padding: EdgeInsets.zero,
                                    constraints: const BoxConstraints(
                                      minWidth: 20,
                                      minHeight: 20,
                                    ),
                                    icon: const Icon(
                                      Icons.close_rounded,
                                      size: 16,
                                      color: AppColors.pureWhite,
                                    ),
                                    onPressed: () {
                                      setState(() {
                                        final files = result!.files.toList();
                                        files.removeAt(index);
                                        if (files.isEmpty) {
                                          result = null;
                                        } else {
                                          result = FilePickerResult(files);
                                        }
                                      });
                                    },
                                  ),
                                ),
                              ),
                            ],
                          );
                        },
                      ),
                    ),
                  
                  // Text input row
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _textController,
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 16,
                          ),
                          decoration: InputDecoration(
                            hintText: AppStrings.askAnythingHint,
                            hintStyle: const TextStyle(
                              color: AppColors.textLight,
                              fontSize: 16,
                            ),
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.zero,
                          ),
                          maxLines: null,
                        ),
                      ),
                      const SizedBox(width: 12),
                      
                      // Voice input button
                      Container(
                        decoration: BoxDecoration(
                          color: _speechEnabled 
                              ? (_isListening ? AppColors.error : AppColors.primaryGreen)
                              : AppColors.textLight,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: IconButton(
                          padding: EdgeInsets.zero,
                          constraints: const BoxConstraints(
                            minWidth: 36,
                            minHeight: 36,
                          ),
                          onPressed: _speechEnabled
                              ? () {
                                  if (!_isListening) {
                                    _startListening();
                                  } else {
                                    _stopListening();
                                  }
                                }
                              : null,
                          icon: Icon(
                            _isListening ? Icons.mic_off_rounded : Icons.mic_rounded,
                            color: AppColors.pureWhite,
                            size: 20,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      
                      // Send button
                      Container(
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: [AppColors.lightGreen, AppColors.primaryGreen],
                          ),
                          borderRadius: BorderRadius.circular(12),
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.shadowColor,
                              blurRadius: 8,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: IconButton(
                          padding: EdgeInsets.zero,
                          constraints: const BoxConstraints(
                            minWidth: 36,
                            minHeight: 36,
                          ),
                          onPressed: _sendMessage,
                          icon: const Icon(
                            Icons.send_rounded,
                            color: AppColors.pureWhite,
                            size: 20,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
