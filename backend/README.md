# Backend

This directory contains the backend service for the Capital One Hackathon project.

## Setup

1. Build the Docker image:
   ```sh
   docker build -t backend .
   ```
2. Run the container:
   ```sh
   docker run -p 3000:3000 backend
   ```

## Development
- Main entry point: see `package.json` scripts
- Dependencies are managed via `package.json`

## Exposed Port
- 3000 (default, adjust as needed)

## License
MIT
