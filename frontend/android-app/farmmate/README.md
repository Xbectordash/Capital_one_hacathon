# FarmMate Flutter App

This is the FarmMate Flutter application for the Capital One Hackathon project.

## Setup & Build (Docker)

1. Build the Docker image:
   ```sh
   docker build -t farmmate-web -f ../dockerfile .
   ```
2. Run the container:
   ```sh
   docker run -p 8080:80 farmmate-web
   ```
3. Access the app at [http://localhost:8080](http://localhost:8080)

## Development
- Main entry point: `lib/main.dart`
- To build locally, use:
  ```sh
  flutter build web
  ```
- The web build output is in `build/web/`

## License
MIT
# farmmate

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
