import 'dart:io';
import 'package:farmmate/utils/constants/app_assets.dart';
import 'package:farmmate/utils/constants/app_sizes.dart';
import 'package:farmmate/utils/constants/app_strings.dart';
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

  // void activateSpeechRecognizer() {
  //   _speech = SpeechRecognition();
  //   _speech.setAvailabilityHandler(onSpeechAvailability);
  //   _speech.setRecognitionStartedHandler(onRecognitionStarted);
  //   _speech.setRecognitionResultHandler(onRecognitionResult);
  //   _speech.setRecognitionCompleteHandler(onRecognitionComplete);
  //   _speech.activate("en_US").then((value) {
  //     setState(() => _currentLocaleId = value);
  //   });
  // }

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

  @override
  Widget build(BuildContext context) {
    return AnnotatedRegion(
      value: SystemUiOverlayStyle(
        statusBarColor: Colors.white,
        statusBarBrightness: Brightness.light,
        statusBarIconBrightness: Brightness.light,
      ),
      child: SafeArea(
        child: Scaffold(
          backgroundColor: Colors.white,
          key: _scaffoldKey,
          drawer: Drawer(
            backgroundColor: Colors.white,
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
          body: Column(
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
              Expanded(child: Container(color: Colors.white)),
              Container(
                width: double.infinity,
                padding: EdgeInsets.symmetric(
                  horizontal: context.screenWidth * 0.05,
                  vertical: context.screenHeight * 0.025,
                ),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(25),
                    topRight: Radius.circular(25),
                  ),
                  color: Colors.grey.shade100,
                ),
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: () async {
                        final pickedFiles = await FilePicker.platform.pickFiles(
                          allowMultiple: true,
                        );
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
                          color: Colors.grey.shade300,
                        ),
                        child: Padding(
                          padding: EdgeInsets.all(AppSizes.padding10),
                          child: Image.asset(
                            AppAssets.blackImageGallery,
                            width: 25,
                            height: 25,
                          ),
                        ),
                      ),
                    ),
                    SizedBox(width: context.screenWidth * 0.02),
                    Expanded(
                      child: Container(
                        padding: EdgeInsets.symmetric(
                          horizontal: AppSizes.padding10,
                        ),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(20),
                          color: Colors.grey.shade300,
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
                                      Image.asset(
                                        AppAssets.blackSend,
                                        width: 23,
                                        height: 23,
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
    );
  }
}
