# Implementation Plan: Phase II Extensions for Physical AI Textbook

**Branch**: `2-phase2-extensions-spec` | **Date**: 2025-12-04 | **Spec**: specs/2-phase2-extensions-spec/spec.md

## Summary

This plan outlines the implementation of Phase II extensions to the Physical AI textbook, adding four integrated systems: RAG chatbot, authentication, personalization, and Urdu translation. The approach maintains the existing Docusaurus architecture while introducing a new FastAPI backend and modern AI integrations.

## Technical Context

**Language/Version**: Frontend - TypeScript/React (Docusaurus), Backend - Python 3.9+ (FastAPI)
**Primary Dependencies**:
- Frontend: Existing Docusaurus 3.x, React 18+
- Backend: FastAPI, OpenAI SDK, better-auth (Python), Qdrant client, Neon Postgres driver
- AI: OpenAI API (GPT-4 for personalization/chatbot), Qdrant Cloud (vector DB)
- Auth: better-auth with email/password
- Database: Neon Postgres (user profiles), Qdrant (content vectors)
**Storage**: Neon Postgres for relational data, Qdrant for vector embeddings
**Testing**: Frontend - Jest/React Testing Library, Backend - pytest, Integration - Playwright
**Target Platform**: Vercel (frontend), Vercel/Railway (backend), Qdrant Cloud, Neon Postgres
**Performance Goals**: <2s initial page load, <1s API responses, <3s personalization generation
**Constraints**: Must not break existing Docusaurus deployment, maintain SEO, ensure mobile compatibility
**Scale/Scope**: 4 new systems, ~10 new React components, ~15 API endpoints, content chunking for 15+ chapters

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation plan aligns with constitution principles:

- **Maintain Existing Docusaurus Book**: ✓ Plan preserves core Docusaurus functionality, adds features as enhancements
- **Seamless Feature Integration**: ✓ Features integrate via modular components without core modifications
- **Modular Architecture**: ✓ Clear separation between frontend components, backend APIs, and data layers
- **Technical Integrity**: ✓ Production-ready stack with proper security, error handling, and performance considerations
- **User-Centric Design**: ✓ Features directly enhance learning experience with accessibility improvements

All constitution principles are upheld.

## Project Structure

### Documentation (this feature)

```text
specs/2-phase2-extensions-spec/
├── plan.md              # This file
├── research.md          # Technical research findings
├── data-model.md        # Extended data entities
├── quickstart.md        # Integration setup guide
├── contracts/           # API specifications
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
api/                    # New FastAPI backend
├── main.py            # FastAPI application
├── auth.py            # Authentication endpoints
├── chatbot.py         # RAG chatbot logic
├── personalization.py # Content adaptation
├── translation.py     # Urdu translation service
├── database.py        # Neon Postgres connection
├── vector_db.py       # Qdrant integration
├── models.py          # Pydantic models
├── config.py          # Environment configuration
└── requirements.txt   # Python dependencies

src/components/        # New React components
├── ChatWidget/
│   ├── index.tsx
│   └── styles.module.css
├── AuthButtons/
│   ├── index.tsx
│   └── styles.module.css
├── PersonalizeButton/
│   ├── index.tsx
│   └── styles.module.css
└── TranslateButton/
    ├── index.tsx
    └── styles.module.css

src/hooks/            # Custom React hooks
├── useAuth.ts
├── useChatbot.ts
└── usePersonalization.ts

src/utils/            # Utility functions
├── api.ts           # Frontend API client
└── translation.ts   # Translation helpers

docs/i18n/ur/        # Urdu locale files
├── code.json
├── docusaurus-theme-classic
└── current

scripts/             # Utility scripts
├── chunk_content.py # Content chunking for RAG
└── setup_vector_db.py # Vector database initialization
```

**Structure Decision**: The structure maintains the existing Docusaurus layout while adding a new `/api` directory for the backend. Frontend components are organized in the existing `src/components` structure. This ensures clean separation while keeping related code together.

## Complexity Tracking

No constitution violations detected. The modular approach ensures each system can be developed and deployed independently, reducing overall complexity.

## Implementation Phases

### Phase 1: Infrastructure Setup
- Set up FastAPI backend with basic structure
- Configure Neon Postgres and Qdrant connections
- Initialize vector database with textbook content chunks
- Deploy backend to Vercel/Railway

### Phase 2: Authentication System
- Implement better-auth integration
- Create user profile management
- Add signup flow with background collection
- Integrate auth state management in frontend

### Phase 3: RAG Chatbot
- Implement content chunking and vector embedding
- Build chatbot API endpoints
- Create ChatWidget React component
- Integrate widget into chapter layouts

### Phase 4: Personalization System
- Implement OpenAI-powered content adaptation
- Create personalization API
- Build PersonalizeButton component
- Add caching for personalized content

### Phase 5: Translation System
- Set up Docusaurus i18n for Urdu locale
- Implement on-the-fly translation API
- Create TranslateButton component
- Add translation caching

### Phase 6: Integration & Testing
- Connect all systems together
- Implement cross-system data flow
- Comprehensive testing and optimization
- Deploy all components
