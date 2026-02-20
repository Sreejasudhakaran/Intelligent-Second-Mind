# JARVIS – Decision Intelligence System

> AI-powered 4-layer cognitive architecture for personal decision intelligence.

## Architecture

```
JARVIS/
├── backend/          # FastAPI (Python)
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schema.sql
│   ├── routes/
│   │   ├── decisions.py
│   │   ├── reflections.py
│   │   ├── replay.py
│   │   ├── insights.py
│   │   └── daily.py
│   ├── services/
│   │   ├── embedding_service.py   ← sentence-transformers
│   │   ├── llm_service.py         ← HuggingFace Inference API
│   │   └── rag_service.py         ← pgvector similarity search
│   └── utils/
│       ├── prompts.py
│       └── helpers.py
└── frontend/         # Next.js 14 + TypeScript + Tailwind
    ├── app/
    │   ├── capture/   ← Decision Capture (Memory Layer)
    │   ├── reflection/← Reflection Engine (Learning Layer)
    │   ├── replay/    ← Decision Replay (Recall Layer)
    │   ├── insights/  ← Pattern Intelligence (Insight Layer)
    │   └── daily/     ← Daily Guidance (Cognitive Layer)
    ├── components/
    │   ├── Sidebar.tsx
    │   └── VoiceButton.tsx
    └── lib/
        ├── api.ts
        └── types.ts
```

## Quick Start

### 1. Database Setup (Supabase)
1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Enable the pgvector extension in the SQL editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Run `backend/schema.sql` in the Supabase SQL editor

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Copy and fill in your secrets
copy .env.example .env

# Start the server
uvicorn main:app --reload --port 8000
```

**Required `.env` values:**
- `DATABASE_URL` – your Supabase PostgreSQL connection string
- `HUGGINGFACE_API_KEY` – from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev   # Opens at http://localhost:3000
```

## Cognitive Layers

| Layer | Route | Feature |
|-------|-------|---------|
| Memory | `/capture` | Log decisions + voice input + auto-tagging |
| Learning | `/reflection` | Submit outcomes + AI reflection insight |
| Recall | `/replay` | Vector similarity search + alternative strategies |
| Insight | `/insights` | Weekly pattern analysis + AI coaching |
| Cognitive | `/daily` | Full RAG-powered daily strategic guidance |

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/decisions/` | Create decision (embeds + auto-tags) |
| GET | `/decisions/` | List all decisions |
| POST | `/reflections/` | Submit reflection + get AI insight |
| POST | `/replay/similar` | Semantic similarity search |
| POST | `/replay/alternative` | Generate alternative strategy |
| GET | `/insights/weekly` | Weekly pattern breakdown + AI insight |
| POST | `/daily/guidance` | Full RAG daily guidance |

Open Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)
