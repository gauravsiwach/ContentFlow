# ContentFlow - Technical Architecture

## 1. Executive Summary

ContentFlow is a local-first AI-powered content creation platform that transforms a topic into a complete reel package. The system is designed as a Modular Monolith — a single deployable application with clearly separated internal modules.

This architecture serves a single developer building and maintaining a POC/MVP for personal use. Every decision prioritizes simplicity, clarity, and speed of development over scalability or enterprise readiness.

The platform orchestrates a linear content pipeline:

Topic → Script → Scenes → Images → Voice → Reel

Each stage requires explicit human approval before proceeding.

---

## 2. Architecture Goals

| Goal | Description |
|------|-------------|
| Simplicity | Minimal moving parts. One backend, one frontend, one database. |
| Local-First | All processing happens on the local machine. No cloud dependencies. |
| Human Control | Every AI output requires human review before advancing. |
| Low Cost | Use local AI models. No API billing. |
| Maintainability | A single developer can understand and modify the entire system. |
| Fast Development | Ship the MVP quickly without architectural ceremony. |

---

## 3. Architecture Principles

1. **Modular Monolith** — Logical separation without physical separation.
2. **Single Process** — One backend server, one frontend dev server.
3. **Direct Calls** — Modules communicate via direct function calls. No message queues. No event bus.
4. **Simple State Machine** — Project progresses through a linear set of statuses.
5. **File System as Storage** — Binary assets stored on disk. Metadata in SQLite.
6. **Synchronous by Default** — Use background tasks only where AI processing time requires it.
7. **Convention Over Configuration** — Standard project structure. Predictable file paths.
8. **No Premature Abstraction** — Build concrete implementations. Abstract only when duplication becomes painful.

---

## 4. System Context

```
┌─────────────────────────────────────────────────────────────┐
│                        User (Gaurav)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ Browser (localhost)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ContentFlow Frontend                       │
│                   (React + TypeScript)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST API (HTTP)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ContentFlow Backend                        │
│                   (Python + FastAPI)                         │
├─────────────────────────────────────────────────────────────┤
│  Modules: Project | Script | Scene | Image | Voice | Reel   │
└───────┬──────────┬──────────┬──────────┬────────────────────┘
        │          │          │          │
        ▼          ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ SQLite │ │ Ollama │ │  FLUX  │ │ Kokoro │
   │   DB   │ │ (Qwen) │ │        │ │  TTS   │
   └────────┘ └────────┘ └────────┘ └────────┘
                                          │
                                     ┌────────┐
                                     │ FFmpeg │
                                     └────────┘
```

External Dependencies (all local):
- **Ollama** — Local LLM inference server (Qwen model)
- **FLUX** — Local image generation model
- **Kokoro TTS** — Local text-to-speech engine
- **FFmpeg** — Video processing CLI tool

---

## 5. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                          │
│  ┌──────────┐ ┌──────────────────────────────────────────────┐  │
│  │Dashboard │ │          Project Workspace                    │  │
│  │          │ │  ┌────────┐ ┌──────────┐ ┌────────────────┐ │  │
│  │          │ │  │Progress│ │  Stage   │ │  AI Panel      │ │  │
│  │          │ │  │ Panel  │ │  Content │ │  (Instructions │ │  │
│  │          │ │  │        │ │  Panel   │ │   + Feedback)  │ │  │
│  │          │ │  └────────┘ └──────────┘ └────────────────┘ │  │
│  └──────────┘ └──────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────┴───────────────────────────────────┐
│                         Backend (FastAPI)                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Workflow Service                           │  │
│  │        (State validation, transitions, orchestration)      │  │
│  └───────────────────────────┬───────────────────────────────┘  │
│                               │                                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ Project │ │ Script  │ │  Scene  │ │  Image  │ │  Voice  │  │
│  │ Module  │ │ Module  │ │ Module  │ │ Module  │ │ Module  │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│  ┌─────────┐ ┌─────────┐                                        │
│  │  Reel   │ │Template │                                        │
│  │ Module  │ │ Module  │                                        │
│  └─────────┘ └─────────┘                                        │
│                               │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                    Shared Layer                             │  │
│  │  ┌──────────────────┐  ┌─────────┐  ┌──────────────────┐ │  │
│  │  │    AI Layer       │  │ Storage │  │   Config + DB    │ │  │
│  │  │  (Orchestrator,   │  │         │  │                  │ │  │
│  │  │   Prompt Builder, │  │         │  │                  │ │  │
│  │  │   Validator,      │  │         │  │                  │ │  │
│  │  │   Clients)        │  │         │  │                  │ │  │
│  │  └──────────────────┘  └─────────┘  └──────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Module Architecture

Each module owns:
- Its API routes
- Its service logic
- Its database models
- Its schemas (request/response)

### Module Boundary Rules

1. Modules communicate through the **Shared** layer or direct imports of other module services.
2. No circular dependencies between modules.
3. Each module has a single entry point (its service class or functions).

### Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| **Project** | Project lifecycle (create, list, delete, status tracking) |
| **Script** | Script generation, refinement, approval |
| **Scene** | Scene breakdown generation, refinement, approval |
| **Image** | Image prompt generation, image generation, approval |
| **Voice** | Voice generation per scene, approval |
| **Reel** | Final video assembly from approved assets |
| **Template** | Template CRUD, template application to projects |
| **Workflow** | State validation, transitions, orchestration across stages |
| **Shared** | AI layer, database access, configuration, file storage, common utilities |

### Module Dependency Direction

```
Project → Script → Scene → Image → Voice → Reel
    ↓        ↓        ↓       ↓       ↓       ↓
                      Shared
                    (DB, AI, Storage, Config)
```

Pipeline modules depend on Shared. Upstream modules do not depend on downstream modules.

---

## 7. Frontend Architecture

### Approach

Single Page Application with a simple page-based routing structure.

### Technology

- React 18+
- TypeScript
- React Router (page navigation)
- Fetch API (HTTP calls)
- CSS Modules or Tailwind CSS (styling)

### Page Structure

| Page | Purpose |
|------|---------|
| Dashboard | List projects, create new, resume existing, delete |
| Project Workspace | Unified workspace for all stages (see layout below) |

### Project Workspace Layout

The Project Workspace is a single unified view that minimizes navigation and keeps the creator focused. Instead of separate pages per stage, all interactions happen within one workspace.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Project Workspace                               │
├───────────────┬─────────────────────────────────┬───────────────────────┤
│               │                                  │                       │
│   Left Panel  │         Center Panel             │    Right Panel        │
│               │                                  │                       │
│  ┌─────────┐  │  ┌───────────────────────────┐  │  ┌─────────────────┐ │
│  │ Project │  │  │     Current Stage          │  │  │ AI Instructions │ │
│  │Progress │  │  │                            │  │  │                 │ │
│  │         │  │  │  - Script Editor           │  │  │ Refinement      │ │
│  │ ○ Script│  │  │  - Scene Cards             │  │  │ Feedback Input  │ │
│  │ ○ Scene │  │  │  - Image Gallery           │  │  │                 │ │
│  │ ○ Image │  │  │  - Audio Player            │  │  │ Activity Log    │ │
│  │ ○ Voice │  │  │  - Video Preview           │  │  │                 │ │
│  │ ○ Reel  │  │  │                            │  │  │                 │ │
│  │         │  │  └───────────────────────────┘  │  └─────────────────┘ │
│  └─────────┘  │                                  │                       │
│               │  ┌───────────────────────────┐  │                       │
│               │  │  Actions: Generate |       │  │                       │
│               │  │  Approve | Refine          │  │                       │
│               │  └───────────────────────────┘  │                       │
│               │                                  │                       │
├───────────────┴─────────────────────────────────┴───────────────────────┤
└─────────────────────────────────────────────────────────────────────────┘
```

#### Panel Responsibilities

| Panel | Content |
|-------|---------|
| **Left** | Project progress stepper showing all stages. Current stage highlighted. Completed stages marked. Allows navigation to view (not edit) previous stages. |
| **Center** | Active content area. Displays the current stage editor/viewer. Actions (Generate, Approve, Refine) appear contextually. |
| **Right** | AI interaction panel. Refinement instructions input. Generation activity/status. Prompt context display (optional). |

**Why unified workspace:** Separate pages require full-page navigation between stages. A workspace keeps context visible — the user always sees progress, the current artifact, and available actions in one view.

### State Management

- **React Context** for global app state (current project, user preferences)
- **Local component state** for UI interactions
- **Server state** as source of truth — frontend fetches current state from backend on navigation

No Redux. No Zustand. No complex client-side state management.

**Why:** The backend holds all state. The frontend is a thin presentation layer. Fetching current state on navigation is simple and eliminates synchronization bugs.

### Frontend-Backend Communication

- REST API calls using native Fetch
- Polling for long-running AI tasks (simple `setInterval` with status endpoint)
- No WebSockets in MVP

---

## 8. Backend Architecture

### Framework

FastAPI with:
- Automatic OpenAPI documentation
- Pydantic for request/response validation
- Background tasks for AI processing

### Application Structure

```
app/
├── main.py                 # FastAPI app initialization, router registration
├── config.py               # Application configuration
├── database.py             # SQLite connection and session management
│
├── modules/
│   ├── project/
│   │   ├── router.py       # API endpoints
│   │   ├── service.py      # Business logic
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   │
│   ├── script/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── scene/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── image/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── voice/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── reel/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── template/
│       ├── router.py
│       ├── service.py
│       ├── models.py
│       └── schemas.py
│
├── workflow/
│   └── workflow_service.py  # Workflow orchestration, state transitions
│
└── shared/
    ├── ai/
    │   ├── __init__.py
    │   ├── orchestrator.py      # Coordinates AI calls per stage
    │   ├── ollama_client.py     # Ollama/Qwen text generation
    │   ├── image_client.py      # FLUX image generation
    │   ├── voice_client.py      # Kokoro TTS
    │   ├── video_client.py      # FFmpeg wrapper
    │   ├── prompt_builder.py    # Prompt assembly from components
    │   └── response_validator.py # Validates and parses AI outputs
    ├── storage.py          # File system operations
    ├── exceptions.py       # Custom exceptions
    └── prompts/            # Prompt templates per stage
        ├── script.py
        ├── scene.py
        └── image.py
```

### Request Lifecycle

1. Request hits FastAPI router
2. Router validates input via Pydantic schema
3. Router calls module service
4. Service executes business logic (may call Shared utilities)
5. Service returns result
6. Router serializes response via Pydantic schema

### Background Tasks

AI generation tasks (script, scene, image, voice) may take 10–60+ seconds.

Strategy:
- FastAPI `BackgroundTasks` for fire-and-forget generation
- Status polling from frontend
- Task status stored in SQLite (pending, processing, completed, failed)

**Why not Celery/RQ:** Single user, single machine. BackgroundTasks with status polling is sufficient. Adding a task queue adds operational complexity without benefit for this use case.

---

## 9. AI Architecture

### AI Layer Overview

The AI layer is a small, focused subsystem within `shared/ai/` that handles all interactions with AI models. It provides a consistent interface for every module that needs AI generation.

```
┌─────────────────────────────────────────────────────────────┐
│                    Module Service                             │
│              (Script / Scene / Image / Voice)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ calls
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI Orchestrator                          │
│               (shared/ai/orchestrator.py)                     │
├─────────────────────────────────────────────────────────────┤
│  1. Build prompt (prompt_builder)                            │
│  2. Call model (ollama_client / image_client / voice_client) │
│  3. Validate response (response_validator)                   │
│  4. Return standardized output                               │
└─────────────────────────────────────────────────────────────┘
```

### AI Layer Components

| Component | File | Responsibility |
|-----------|------|---------------|
| **Orchestrator** | `orchestrator.py` | Coordinates the generate/refine flow for any stage. Calls prompt builder → client → validator in sequence. |
| **Ollama Client** | `ollama_client.py` | HTTP calls to Ollama API. Handles connection errors, timeouts, retries. |
| **Image Client** | `image_client.py` | HTTP calls to FLUX. Submits prompts, retrieves generated images. |
| **Voice Client** | `voice_client.py` | HTTP calls to Kokoro TTS. Submits text, retrieves audio files. |
| **Video Client** | `video_client.py` | Subprocess calls to FFmpeg. Assembles images + audio into video. |
| **Prompt Builder** | `prompt_builder.py` | Assembles complete prompts from components (system prompt, template, context, artifact, instructions). |
| **Response Validator** | `response_validator.py` | Validates AI output structure (JSON parsing, required fields, length checks). Returns clean data or error. |

### AI Processing Contract

Every AI-powered module (Script, Scene, Image, Voice) follows the same processing contract:

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `generate()` | Create initial artifact from inputs | User clicks "Generate" |
| `refine()` | Update existing artifact based on user feedback | User provides refinement instructions |
| `approve()` | Mark artifact as approved, advance project state | User clicks "Approve" |
| `validate()` | Verify artifact meets minimum quality/structure requirements | Called internally after generation |

#### Contract Flow

```
generate() / refine()
    │
    ├── prompt_builder.build(stage, context, instructions)
    │
    ├── ollama_client.generate(prompt)  OR  image_client.generate(prompt)
    │
    ├── response_validator.validate(response, stage)
    │
    └── Return structured result OR raise AIGenerationError
```

This contract ensures that Script, Scene, Image, and Voice modules all follow the same pattern. The module service calls the orchestrator; the orchestrator handles the AI interaction details.

### Prompt Builder Strategy

Prompts are assembled from distinct components. Every AI call follows this structure:

```
┌─────────────────────────────────────────┐
│              Final Prompt                 │
├─────────────────────────────────────────┤
│  1. System Prompt                        │
│     (Role, behavior rules, output format)│
│                                          │
│  2. Template Context (if applicable)     │
│     (Audience, tone, language, notes)    │
│                                          │
│  3. Project Context                      │
│     (Topic, duration, content type)      │
│                                          │
│  4. Current Artifact (for refinement)    │
│     (Existing script/scene/prompt)       │
│                                          │
│  5. User Instructions                    │
│     (Refinement feedback or initial ask) │
└─────────────────────────────────────────┘
```

#### Prompt Components

| Component | Source | When Included |
|-----------|--------|--------------|
| System Prompt | `shared/prompts/{stage}.py` | Always |
| Template Context | Template record from DB | When project has a template |
| Project Context | Project record from DB | Always |
| Current Artifact | Script/Scene record from DB | Refinement only |
| User Instructions | Request body | Always (generation prompt or refinement feedback) |

The `prompt_builder.py` receives the stage name and relevant data, selects the appropriate template from `shared/prompts/`, and assembles the final prompt string.

### Response Validation

The `response_validator.py` ensures AI outputs meet expected structure before they are stored:

| Stage | Validation Rules |
|-------|-----------------|
| Script | Non-empty text, minimum length, contains content (not just meta-commentary) |
| Scene | Valid JSON array, each scene has required fields (title, description, duration, voiceover_text, image_prompt) |
| Image Prompt | Non-empty string, reasonable length |

If validation fails, the orchestrator raises an `AIGenerationError` with a descriptive message. The module service can then retry or surface the error to the user.

### Pipeline Stages

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│   Script   │───▶│   Scene    │───▶│   Image    │───▶│   Voice    │───▶│    Reel    │
│ Generation │    │ Generation │    │ Generation │    │ Generation │    │  Assembly  │
└────────────┘    └────────────┘    └────────────┘    └────────────┘    └────────────┘
     │                  │                 │                 │                  │
     ▼                  ▼                 ▼                 ▼                  ▼
  Ollama/Qwen      Ollama/Qwen         FLUX           Kokoro TTS          FFmpeg
```

### Refinement Flow

When the user provides refinement instructions:
1. Prompt builder assembles: system prompt + project context + current artifact + user feedback
2. Orchestrator calls the AI model
3. Response validator checks the output
4. Updated output replaces previous version
5. Previous version is not retained in MVP (no version history)

---

## 10. Workflow Architecture

### Workflow Service

A dedicated `workflow_service.py` owns all workflow orchestration logic. Individual modules (Script, Scene, Image, Voice) do not manage state transitions or validate project readiness — the Workflow Service does.

**Location:** `app/workflow/workflow_service.py`

**Responsibilities:**

| Responsibility | Description |
|---------------|-------------|
| State Validation | Check if the project is in the correct state for a requested action |
| Trigger Generation | Call the appropriate module service to generate content |
| Handle Approvals | Advance project state when user approves an artifact |
| Prevent Invalid Transitions | Reject requests that violate the state machine |
| Coordinate Dependencies | Ensure upstream artifacts exist before downstream generation |

**Why a separate service:** Without this, workflow logic leaks into every module router. Each module would need to check project state, handle approvals, and manage transitions independently — leading to duplication and inconsistency.

#### Workflow Service Interface

```
WorkflowService:
    get_current_stage(project_id) → stage info + available actions
    generate(project_id, stage) → trigger generation for current stage
    refine(project_id, stage, instructions) → refine current artifact
    approve(project_id, stage) → approve and advance to next stage
```

#### Request Flow Through Workflow Service

```
Frontend → Router → WorkflowService → Module Service → AI Orchestrator
                         │
                         ├── Validates project state
                         ├── Delegates to module service
                         └── Updates project status on completion
```

### Project State Machine

```
Draft
  │
  ▼ (generate script)
Script Generated
  │
  ▼ (approve script)
Script Approved
  │
  ▼ (generate scenes)
Scenes Generated
  │
  ▼ (approve scenes)
Scenes Approved
  │
  ▼ (generate images)
Images Generated
  │
  ▼ (approve images)
Images Approved
  │
  ▼ (generate voice)
Voice Generated
  │
  ▼ (approve voice)
Voice Approved
  │
  ▼ (generate reel)
Reel Generated
  │
  ▼ (mark complete)
Completed
```

### State Transitions

- Forward-only in MVP. No going back to a previous stage.
- Each "Generated" state allows: Approve, Edit, Refine.
- Refine returns to the same "Generated" state with updated content.
- Approve advances to the next stage.

### Workflow Enforcement

The backend enforces state transitions. The frontend cannot skip stages.

Example: Cannot generate images unless scenes are approved. The API returns a 409 Conflict if the project is not in the correct state.

---

## 10.1. Asset Pipeline

The Asset Pipeline defines the complete lifecycle of content as it flows through the system. Each stage transforms inputs into outputs that feed the next stage.

### Pipeline Overview

```
Topic + Context
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Script    │────▶│   Scenes    │────▶│   Images    │────▶│   Voice     │────▶│    Reel     │
│             │     │             │     │             │     │             │     │             │
│ Input:      │     │ Input:      │     │ Input:      │     │ Input:      │     │ Input:      │
│  - Topic    │     │  - Script   │     │  - Image    │     │  - Voiceover│     │  - Images   │
│  - Language │     │  - Duration │     │    Prompts  │     │    Text     │     │  - Voice    │
│  - Duration │     │  - Content  │     │             │     │  - Language │     │    Tracks   │
│  - Template │     │    Type     │     │ Output:     │     │             │     │  - Scene    │
│  - Context  │     │             │     │  - PNG per  │     │ Output:     │     │    Durations│
│             │     │ Output:     │     │    scene    │     │  - WAV per  │     │             │
│ Output:     │     │  - Scene[]  │     │             │     │    scene    │     │ Output:     │
│  - Script   │     │    (title,  │     │ Depends On: │     │             │     │  - MP4 Reel │
│    (text)   │     │    desc,    │     │  - Scenes   │     │ Depends On: │     │             │
│             │     │    duration,│     │    Approved │     │  - Scenes   │     │ Depends On: │
│ Depends On: │     │    voiceover│     │             │     │    Approved │     │  - Images   │
│  - None     │     │    image    │     │             │     │             │     │    Approved │
│             │     │    prompt)  │     │             │     │             │     │  - Voice    │
│             │     │             │     │             │     │             │     │    Approved │
│             │     │ Depends On: │     │             │     │             │     │             │
│             │     │  - Script   │     │             │     │             │     │             │
│             │     │    Approved │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Stage Details

| Stage | Input | Output | AI Model | Dependencies |
|-------|-------|--------|----------|--------------|
| **Script** | Topic, Language, Duration, Content Type, Template, Additional Context | Script text | Ollama/Qwen | None |
| **Scenes** | Approved Script, Duration, Content Type | Array of scene objects (title, description, duration, voiceover_text, image_prompt) | Ollama/Qwen | Script Approved |
| **Images** | Image prompt (from scene) | PNG image file per scene | FLUX | Scenes Approved |
| **Voice** | Voiceover text (from scene), Language | WAV audio file per scene | Kokoro TTS | Scenes Approved |
| **Reel** | Approved images, Approved voice tracks, Scene durations | MP4 video file | FFmpeg | Images Approved + Voice Approved |

### Artifact Storage

| Stage | Storage Type | Location |
|-------|-------------|----------|
| Script | Database (text column) | `scripts` table |
| Scenes | Database (structured records) | `scenes` table |
| Images | File system | `storage/projects/{id}/images/scene_XX.png` |
| Voice | File system | `storage/projects/{id}/voice/scene_XX.wav` |
| Reel | File system | `storage/projects/{id}/reel/final.mp4` |

---

## 11. Database Architecture

### Database Choice

SQLite — single-file database, zero configuration, sufficient for single-user workload.

**Why not PostgreSQL:** No concurrent users. No need for advanced querying. SQLite is simpler to deploy and maintain.

### ORM

SQLAlchemy with synchronous sessions.

**Why not async SQLAlchemy:** SQLite does not benefit from async. Synchronous code is simpler to debug and maintain.

### Core Tables

```
projects
├── id (UUID, PK)
├── title
├── topic
├── language
├── duration
├── content_type
├── template_id (FK, nullable)
├── additional_context
├── status
├── created_at
└── updated_at

scripts
├── id (UUID, PK)
├── project_id (FK)
├── content (text)
├── refinement_instructions (text, nullable)
├── is_approved (boolean)
├── created_at
└── updated_at

scenes
├── id (UUID, PK)
├── project_id (FK)
├── scene_number (integer)
├── title
├── description
├── duration (seconds)
├── voiceover_text
├── image_prompt
├── is_approved (boolean)
├── created_at
└── updated_at

images
├── id (UUID, PK)
├── scene_id (FK)
├── project_id (FK)
├── file_path (relative path)
├── prompt_used
├── is_approved (boolean)
├── created_at
└── updated_at

voice_tracks
├── id (UUID, PK)
├── scene_id (FK)
├── project_id (FK)
├── file_path (relative path)
├── is_approved (boolean)
├── created_at
└── updated_at

reels
├── id (UUID, PK)
├── project_id (FK)
├── file_path (relative path)
├── created_at
└── updated_at

templates
├── id (UUID, PK)
├── name
├── audience
├── tone
├── language
├── creator_notes
├── default_instructions
├── created_at
└── updated_at

tasks
├── id (UUID, PK)
├── project_id (FK)
├── task_type (enum: script, scene, image, voice, reel)
├── status (enum: pending, processing, completed, failed)
├── error_message (nullable)
├── created_at
└── updated_at
```

### Relationships

- Project has one Script
- Project has many Scenes (ordered by scene_number)
- Scene has one Image
- Scene has one Voice Track
- Project has one Reel
- Project optionally references one Template
- Project has many Tasks (for tracking async operations)

---

## 12. File Storage Strategy

### Storage Location

All binary files stored under a configurable base directory:

```
storage/
├── projects/
│   ├── {project_id}/
│   │   ├── images/
│   │   │   ├── scene_01.png
│   │   │   ├── scene_02.png
│   │   │   └── ...
│   │   ├── voice/
│   │   │   ├── scene_01.wav
│   │   │   ├── scene_02.wav
│   │   │   └── ...
│   │   └── reel/
│   │       └── final.mp4
```

### File Naming Convention

- Images: `scene_{number:02d}.png`
- Voice: `scene_{number:02d}.wav`
- Reel: `final.mp4`

### Storage Rules

1. Database stores relative paths (relative to storage base directory)
2. Backend resolves full paths using configuration
3. Frontend accesses files via API endpoints (never direct file system access)
4. Deleting a project deletes its entire directory

### File Serving

FastAPI serves files via static file endpoints or `FileResponse`. No separate file server.

---

## 13. State Management

### Source of Truth

The **backend database** is the single source of truth for all application state.

### Frontend State Strategy

| State Type | Location | Example |
|-----------|----------|---------|
| Server state | Backend (SQLite) | Project data, scripts, scenes, approvals |
| UI state | React component state | Form inputs, modal open/close |
| Navigation state | React Router | Current page, project ID in URL |
| App context | React Context | Active project reference |

### No Offline Support

The frontend does not cache server state. Every page load fetches fresh data from the backend.

**Why:** Single user on local machine. Network latency is negligible (localhost). Caching adds complexity without benefit.

---

## 14. Project Structure

```
ContentFlow/
├── Docs/
│   ├── ContentFlow_CONTEXT.md
│   ├── PRD_ContentFlow_Phase1.md
│   └── TECHNICAL_ARCHITECTURE.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── project/
│   │   │   ├── script/
│   │   │   ├── scene/
│   │   │   ├── image/
│   │   │   ├── voice/
│   │   │   ├── reel/
│   │   │   └── template/
│   │   ├── workflow/
│   │   │   ├── __init__.py
│   │   │   └── workflow_service.py
│   │   └── shared/
│   │       ├── __init__.py
│   │       ├── ai/
│   │       │   ├── __init__.py
│   │       │   ├── orchestrator.py
│   │       │   ├── ollama_client.py
│   │       │   ├── image_client.py
│   │       │   ├── voice_client.py
│   │       │   ├── video_client.py
│   │       │   ├── prompt_builder.py
│   │       │   └── response_validator.py
│   │       ├── storage.py
│   │       ├── exceptions.py
│   │       └── prompts/
│   │           ├── script.py
│   │           ├── scene.py
│   │           └── image.py
│   ├── requirements.txt
│   ├── alembic/              # Database migrations (if needed)
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   └── ProjectWorkspace.tsx
│   │   ├── components/
│   │   │   ├── workspace/
│   │   │   │   ├── ProgressPanel.tsx
│   │   │   │   ├── ContentPanel.tsx
│   │   │   │   └── AIPanel.tsx
│   │   │   ├── stages/
│   │   │   │   ├── ScriptStage.tsx
│   │   │   │   ├── SceneStage.tsx
│   │   │   │   ├── ImageStage.tsx
│   │   │   │   ├── VoiceStage.tsx
│   │   │   │   └── ReelStage.tsx
│   │   │   └── common/
│   │   ├── api/              # API client functions
│   │   ├── context/
│   │   └── types/
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── storage/                  # Generated assets (gitignored)
│   └── projects/
│
└── README.md
```

---

## 15. API Architecture

### API Style

RESTful. Resource-oriented. JSON request/response bodies.

### URL Structure

```
/api/v1/projects
/api/v1/projects/{project_id}
/api/v1/projects/{project_id}/script
/api/v1/projects/{project_id}/script/generate
/api/v1/projects/{project_id}/script/refine
/api/v1/projects/{project_id}/script/approve
/api/v1/projects/{project_id}/scenes
/api/v1/projects/{project_id}/scenes/generate
/api/v1/projects/{project_id}/scenes/refine
/api/v1/projects/{project_id}/scenes/approve
/api/v1/projects/{project_id}/images
/api/v1/projects/{project_id}/images/generate
/api/v1/projects/{project_id}/images/{scene_id}/refine
/api/v1/projects/{project_id}/images/approve
/api/v1/projects/{project_id}/voice
/api/v1/projects/{project_id}/voice/generate
/api/v1/projects/{project_id}/voice/approve
/api/v1/projects/{project_id}/reel
/api/v1/projects/{project_id}/reel/generate
/api/v1/projects/{project_id}/reel/download
/api/v1/projects/{project_id}/status
/api/v1/projects/{project_id}/tasks/{task_id}
/api/v1/templates
/api/v1/templates/{template_id}
```

### HTTP Methods

| Method | Usage |
|--------|-------|
| GET | Retrieve resources |
| POST | Create resources, trigger actions (generate, refine, approve) |
| PUT | Update resources (edit script, edit scene) |
| DELETE | Delete resources (delete project) |

### Response Format

```json
{
  "data": { ... },
  "message": "Success"
}
```

Error response:
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "detail": { ... }
}
```

### Versioning

URL-based versioning (`/api/v1/`). Allows future breaking changes without disrupting existing clients.

---

## 16. Error Handling Strategy

### Backend Error Handling

| Layer | Strategy |
|-------|----------|
| Router | Catch service exceptions, return appropriate HTTP status |
| Service | Raise domain-specific exceptions |
| AI Client | Catch connection/timeout errors, raise wrapped exceptions |
| Database | Let SQLAlchemy exceptions propagate to a global handler |

### Custom Exception Hierarchy

```
ContentFlowError (base)
├── ProjectNotFoundError → 404
├── InvalidStateTransitionError → 409
├── AIGenerationError → 502
├── AIServiceUnavailableError → 503
├── StorageError → 500
└── ValidationError → 422
```

### Global Exception Handler

FastAPI exception handler catches all `ContentFlowError` subclasses and returns structured JSON error responses.

### Frontend Error Handling

- Display error messages from API responses
- Show retry option for transient failures (AI service unavailable)
- Show user-friendly messages for validation errors

---

## 17. Security Considerations

### Threat Model

This is a local-only, single-user application. The threat surface is minimal.

### Measures

| Concern | Mitigation |
|---------|-----------|
| Input Validation | Pydantic schemas validate all API inputs |
| Path Traversal | Storage module validates file paths against base directory |
| SQL Injection | SQLAlchemy parameterized queries (no raw SQL) |
| CORS | Restrict to localhost origins |
| File Upload | Not applicable in MVP (no user file uploads) |
| Authentication | Not required (single user, localhost only) |
| Subprocess Injection | FFmpeg commands use list-based arguments, not shell strings |

### CORS Configuration

Allow only `http://localhost:5173` (Vite dev server) and `http://localhost:3000` in development.

---

## 18. Configuration Management

### Approach

Environment variables with sensible defaults. Single configuration file.

### Configuration Values

| Key | Default | Description |
|-----|---------|-------------|
| `DATABASE_URL` | `sqlite:///./contentflow.db` | Database connection string |
| `STORAGE_BASE_PATH` | `./storage` | Base directory for file storage |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `qwen2.5:7b` | Default LLM model |
| `FLUX_BASE_URL` | `http://localhost:7860` | FLUX API endpoint |
| `KOKORO_BASE_URL` | `http://localhost:8080` | Kokoro TTS endpoint |
| `FFMPEG_PATH` | `ffmpeg` | Path to FFmpeg binary |
| `LOG_LEVEL` | `INFO` | Logging level |

### Loading

Use Pydantic `BaseSettings` for configuration. Reads from environment variables and `.env` file.

---

## 19. Logging Strategy

### Approach

Python standard `logging` module with structured output.

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed AI prompts, raw responses |
| INFO | Request handling, task status changes, generation start/complete |
| WARNING | Retryable failures, degraded performance |
| ERROR | Failed generations, storage errors, unrecoverable issues |

### Format

```
{timestamp} | {level} | {module} | {message}
```

### What to Log

- Every AI generation request (model, prompt length, duration)
- Every state transition
- Every error with context
- Task lifecycle (created, started, completed, failed)

### What NOT to Log

- Full prompt text at INFO level (use DEBUG)
- Full AI responses at INFO level (use DEBUG)
- Sensitive configuration values

---

## 20. Future Evolution

### Phase 2 Potential Additions

| Feature | Architecture Impact |
|---------|-------------------|
| Research Stage | New module, additional pre-script stage |
| URL/PDF/YouTube Input | New shared clients, input processing pipeline |
| Timeline Editor | Significant frontend complexity, possible canvas library |
| Stock Media | New shared client, image module extension |
| Long Form Content | Extended scene model, chapter concept |
| Blog/LinkedIn Generation | New output modules, parallel to reel |
| Prompt Management UI | Template module extension |

### Architecture Boundaries That Support Evolution

1. Module structure allows adding new modules without modifying existing ones.
2. AI client abstraction allows swapping models (e.g., Qwen → Llama).
3. Storage strategy allows moving to cloud storage later by replacing the storage module.
4. API versioning allows breaking changes in future versions.

---

## 21. Architecture Decision Records (ADR)

### ADR-001: Modular Monolith Over Microservices

**Decision:** Build as a single FastAPI application with logical module boundaries.

**Why:** Single developer, single user, POC/MVP. Physical service separation adds deployment complexity, inter-service communication overhead, and debugging difficulty without any benefit at this scale.

**Alternatives Considered:**
- Microservices: Rejected. Unnecessary operational complexity for a single-user tool.
- Simple monolith (no module structure): Rejected. Some structure prevents the codebase from becoming a tangled mess as features grow.

---

### ADR-002: SQLite Over PostgreSQL

**Decision:** Use SQLite as the database.

**Why:** Zero configuration, single-file database, perfect for single-user local applications. No need to install or manage a database server.

**Alternatives Considered:**
- PostgreSQL: Rejected. Requires running a separate server. Overkill for single-user workloads.
- JSON files: Rejected. No query capability, no relational integrity, harder to manage as data grows.

---

### ADR-003: Background Tasks Over Task Queue

**Decision:** Use FastAPI BackgroundTasks for async AI processing with polling-based status checks.

**Why:** Single user means no task concurrency issues. BackgroundTasks are built into FastAPI. No additional infrastructure required.

**Alternatives Considered:**
- Celery + Redis: Rejected. Requires Redis server, worker processes, and additional configuration. Massive overhead for a single-user tool.
- Python asyncio tasks: Rejected. FastAPI BackgroundTasks provide the same capability with simpler lifecycle management.

---

### ADR-004: REST Over WebSocket for Real-Time Updates

**Decision:** Use HTTP polling for task status updates.

**Why:** Simple to implement. AI tasks take 10–60 seconds. Polling every 2–3 seconds is perfectly adequate.

**Alternatives Considered:**
- WebSocket: Rejected. Adds connection management complexity. Not justified for the polling frequency needed.
- Server-Sent Events (SSE): Viable but unnecessary. Polling is simpler and sufficient.

---

### ADR-005: File System Over Object Storage

**Decision:** Store generated assets (images, audio, video) on the local file system.

**Why:** Local-first architecture. No cloud dependency. Simple to implement. Easy to browse generated files manually.

**Alternatives Considered:**
- S3/MinIO: Rejected. Adds cloud dependency or additional service to run.
- Database BLOBs: Rejected. Bloats database. Makes backups slower. SQLite has size limits.

---

### ADR-006: Pydantic BaseSettings for Configuration

**Decision:** Use Pydantic BaseSettings with `.env` file support.

**Why:** Type-safe configuration. Automatic validation. Already a FastAPI dependency. Supports environment variables and `.env` files.

**Alternatives Considered:**
- YAML/TOML config files: Rejected. Additional parsing library. No type validation without extra code.
- Plain environment variables: Rejected. No validation, no defaults, no type coercion.

---

### ADR-007: No Authentication

**Decision:** No authentication or authorization in MVP.

**Why:** Single-user application running on localhost. Adding auth adds complexity with zero security benefit for this use case.

**Alternatives Considered:**
- Basic auth: Rejected. Unnecessary for localhost single-user tool.
- Session-based auth: Rejected. Same reasoning.

---

### ADR-008: React Context Over State Management Libraries

**Decision:** Use React Context for minimal global state. Server is source of truth.

**Why:** The frontend is a thin client. Most state lives on the server. React Context handles the minimal global state (current project) without adding dependencies.

**Alternatives Considered:**
- Redux: Rejected. Massive boilerplate for minimal client state.
- Zustand: Rejected. Another dependency for what Context handles adequately.
- TanStack Query: Worth considering for server state caching, but adds complexity. Simple fetch + useEffect is sufficient for MVP.

---

### ADR-009: Vite for Frontend Build Tool

**Decision:** Use Vite as the frontend build tool and dev server.

**Why:** Fast development experience. Simple configuration. Modern defaults.

**Alternatives Considered:**
- Create React App: Rejected. Deprecated. Slower builds.
- Next.js: Rejected. Server-side rendering is unnecessary for a local SPA.
- Webpack (manual): Rejected. Significant configuration overhead.

---

### ADR-010: Synchronous SQLAlchemy Over Async

**Decision:** Use synchronous SQLAlchemy sessions.

**Why:** SQLite does not benefit from async database access (it's file-based). Synchronous code is simpler to write, debug, and reason about.

**Alternatives Considered:**
- Async SQLAlchemy with aiosqlite: Rejected. Adds complexity without performance benefit for SQLite. Async DB makes sense with PostgreSQL and concurrent users, neither of which apply here.

---

### ADR-011: AI Layer Over Generic Client

**Decision:** Structure AI interactions as a small layered subsystem (`shared/ai/`) with orchestrator, prompt builder, and response validator — instead of a single flat client file.

**Why:** Every AI-powered module needs the same sequence: build prompt → call model → validate response. A single `ai_client.py` would grow into an unmanageable file mixing prompt logic, HTTP calls, and validation. Separating these into focused files keeps each under 100–200 lines.

**Alternatives Considered:**
- Single `ai_client.py`: Rejected. Becomes a god-object as prompt complexity grows.
- LangChain/LangGraph: Rejected. Massive dependency for what amounts to HTTP calls + string formatting. Overkill for this use case.
- Per-module AI logic: Rejected. Duplicates the prompt build → call → validate pattern across every module.

---

### ADR-012: Dedicated Workflow Service Over Distributed State Logic

**Decision:** Centralize workflow orchestration in a single `workflow_service.py` rather than distributing state management across module routers.

**Why:** Workflow logic (state validation, transitions, dependency checks) is cross-cutting. Placing it in each module leads to duplication and inconsistent enforcement. A single service is the natural owner of "what can happen next."

**Alternatives Considered:**
- State checks in each module router: Rejected. Duplicates validation logic. Risk of inconsistent enforcement.
- Workflow engine library (e.g., Prefect, Airflow): Rejected. Massive overhead for a linear 5-stage pipeline.
- State machine library: Considered viable but unnecessary. The state machine is simple enough to implement directly.

---

### ADR-013: Unified Workspace Over Multi-Page Navigation

**Decision:** Use a single Project Workspace view with left/center/right panels instead of separate pages per stage.

**Why:** Content creation is a linear flow where context from previous stages matters. A unified workspace keeps progress visible, reduces navigation clicks, and mirrors the mental model of "working on a project" rather than "visiting different pages."

**Alternatives Considered:**
- Separate page per stage: Rejected. Excessive navigation. Loses context between stages. Each page load requires re-fetching project state.
- Tab-based interface: Viable but adds UI complexity. The panel layout achieves the same goal more simply.
