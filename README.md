# ContentFlow

AI-powered content creation platform that transforms a topic into a complete reel package with human review at every stage.

## Overview

ContentFlow is a local-first, personal content creation tool designed to automate the process of creating short-form videos (Reels, Shorts, TikTok videos). The goal is to reduce content creation time from hours to minutes while maintaining human control at every important stage.

## Tech Stack

**Backend:**
- Python 3.x
- FastAPI
- SQLAlchemy
- SQLite

**Frontend:**
- React
- Vite
- React Router

**AI Services (Local):**
- Ollama (Qwen model) - Text generation
- FLUX - Image generation
- Kokoro TTS - Voice generation
- FFmpeg - Video processing

## Project Structure

```
ContentFlow/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── modules/      # Feature modules
│   │   ├── workflow/     # Workflow orchestration
│   │   └── shared/       # Shared utilities
│   ├── requirements.txt
│   └── .env
├── frontend/         # React frontend
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── storage/          # Generated assets storage
└── Docs/             # Documentation
```

## Getting Started

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Development

**Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Documentation

- [ContentFlow Context](Docs/ContentFlow_CONTEXT.md)
- [Development Plan](Docs/DEVELOPMENT_PLAN.md)
- [Product Requirements](Docs/PRD_ContentFlow_Phase1.md)
- [Technical Architecture](Docs/TECHNICAL_ARCHITECTURE.md)

## License

Personal use project.
