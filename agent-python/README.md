
# Agent Python

This directory contains the Python agent for the Capital One Hackathon project.
         ┌─────────────────────┐
         │ 1. UserContextNode  │
         │  (detect location,  │
         │  language, device)  │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ 2. QueryUnderstanding│
         │  (intent, entities,  │
         │   multi-intent)      │
         └─────────┬───────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ 3. ConditionalRouter │
         │ (route to relevant   │
         │  agent functions)    │
         └───────┬──────────────┘
   ┌─────────────┼─────────────────────────────┐
   ▼             ▼             ▼               ▼
WeatherAgent   SoilAgent   MarketAgent   PolicyAgent
   │             │             │               │
   ▼             ▼             ▼               ▼
CropHealthAgent OfflineAgent (optional)   ... more
   └─────────────┬─────────────────────────────┘
                 ▼
         ┌─────────────────────┐
         │ 4. DecisionSupport  │
         │  (aggregate all     │
         │   agent outputs)    │
         └─────────┬───────────┘
                   ▼
         ┌─────────────────────┐
         │ 5. TranslationNode  │
         │ (final reply in     │
         │  user's language)   │
         └─────────┬───────────┘
                   ▼
                Final
               Response


## Project Structure

```
project-root/
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── venv/
└── src/
    ├── main.py                   # App entrypoint
    ├── config/                   # All config loading
    │   └── settings.py
    ├── core/                     # Base logic shared by all
    │   ├── llm.py                # LLM wrapper (Gemini/OpenAI)
    │   ├── embeddings.py
    │   └── vectorstore.py        # Chroma or other vector db
    ├── agents/                   # Different agents or AI brains
    │   ├── base.py               # Abstract agent class
    │   ├── farmer_agent.py       # Specific use-case: Farmer
    │   └── market_agent.py       # (Example) Market advisor agent
    ├── plugins/                  # Plugin system (for tools, RAG, etc.)
    │   ├── weather_plugin.py
    │   ├── soil_plugin.py
    │   └── pest_plugin.py
    ├── data/                     # Local static or raw data
    │   └── crops.json
    ├── loaders/                  # Load docs, files, etc.
    │   └── pdf_loader.py
    ├── chains/                   # Custom chain logic (RAG, Tool use)
    │   └── retrieval_chain.py
    └── server/                   # Optional: REST API (FastAPI, Flask)
        ├── app.py
        └── routes.py
```

## Setup

1. Build the Docker image:
   ```sh
   docker build -t agent-python .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 agent-python
   ```

## Development
- Main entry point: `main.py`
- Dependencies are listed in `requirements.txt`

## Environment Variables
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`

## Exposed Port
- 8000 (default, adjust as needed)

## License
MIT
