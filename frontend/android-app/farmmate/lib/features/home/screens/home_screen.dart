import 'package:farmmate/utils/constants/app_assets.dart';
import 'package:farmmate/utils/constants/app_sizes.dart';
import 'package:farmmate/utils/constants/app_strings.dart';
import 'package:farmmate/utils/extensions/app_extensions.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
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
                    Navigator.pop(context); // Close drawer
                    // Navigate to home
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.settings),
                  title: const Text('Settings'),
                  onTap: () {
                    Navigator.pop(context); // Close drawer
                    // Navigate to settings
                  },
                ),
              ],
            ),
          ),
          body: Column(
            children: [
              Padding(
                padding: EdgeInsets.symmetric(
                  horizontal: context.screenWidth * 0.05, // 5%
                  vertical: context.screenHeight * 0.015, // 2%
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
                    // Image/Gallery Button
                    Container(
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
                    SizedBox(width: context.screenWidth * 0.02),

                    // Input Field with Mic
                    Expanded(
                      child: Container(
                        padding: EdgeInsets.symmetric(
                          horizontal: AppSizes.padding10,
                        ),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(100),
                          color: Colors.grey.shade300,
                        ),
                        child: Row(
                          children: [
                            Expanded(
                              child: TextField(
                                decoration: InputDecoration(
                                  hintText: AppStrings.askAnythingHint,
                                  border: InputBorder.none,
                                  contentPadding: EdgeInsets.only(
                                    left: 10,
                                    right: 10,
                                  ),
                                ),
                              ),
                            ),
                            const Icon(Icons.mic),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(width: context.screenWidth * 0.02),
                    Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(100),
                        color: Colors.grey.shade300,
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(AppSizes.padding10),
                        child: Image.asset(
                          AppAssets.blackSend,
                          width: 23,
                          height: 23,
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
