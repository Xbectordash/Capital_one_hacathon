# ChromaDB Setup

This directory contains a minimal setup for running ChromaDB in a Docker container, along with Python helper functions and a starter script.

## Files
- `Dockerfile`: Containerizes ChromaDB with Python 3.11.
- `chromadb_helper.py`: Helper functions to interact with ChromaDB.
- `starter.py`: Example script to use the helper functions.

## Usage
1. **Build the Docker image:**
   ```sh
   docker build -t chromadb-app .
   ```
2. **Run the container:**
   ```sh
   docker run --rm -it chromadb-app
   ```
3. **Use the starter script:**
   The container will have `starter.py` and `chromadb_helper.py` for quick experimentation.

## Requirements
- Python 3.11
- ChromaDB (installed via Dockerfile)

---
For more, see the [ChromaDB documentation](https://docs.trychroma.com/).
