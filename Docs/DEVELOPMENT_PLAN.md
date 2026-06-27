# ContentFlow - Development Plan

## Document Purpose

This document is the execution roadmap for building ContentFlow from zero to a working MVP. It is designed for a single developer working incrementally, with every phase delivering a runnable, testable application.

---

## Development Philosophy

- Build one vertical slice at a time
- Every phase produces a working application
- No placeholder code. No unfinished modules.
- Backend and Frontend evolve together
- Complete and test before moving forward
- Follow the Technical Architecture exactly

---

## Phase Dependencies

```
Phase 0 (Foundation)
    │
    ▼
Phase 1 (Project Module)
    │
    ▼
Phase 2 (Script Module)
    │
    ▼
Phase 3 (Scene Module)
    │
    ▼
Phase 4 (Image Module)
    │
    ▼
Phase 5 (Voice Module)
    │
    ▼
Phase 6 (Reel Module)
    │
    ▼
Phase 7 (Templates)
    │
    ▼
Phase 8 (Polish)
```

Each phase depends on all previous phases being complete.

---

## Phase 0 — Foundation

### Objective

Set up the complete development environment. Establish project structure, tooling, and infrastructure so that development can begin immediately in Phase 1.

### Deliverables

- Monorepo structure with `backend/` and `frontend/` directories
- FastAPI backend running on `localhost:8000`
- React frontend running on `localhost:5173`
- SQLite database initializing on startup
- Storage directory structure created on startup
- Health check endpoint (backend)
- Health check display (frontend)
- All tooling configured (linting, formatting, environment)

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 0.1 | Create project root structure | `ContentFlow/backend/`, `ContentFlow/frontend/`, `ContentFlow/storage/`, `ContentFlow/Docs/` |
| 0.2 | Initialize Python project | Create `backend/requirements.txt` with FastAPI, uvicorn, SQLAlchemy, pydantic, pydantic-settings, python-dotenv, alembic |
| 0.3 | Create virtual environment | `python -m venv backend/.venv` |
| 0.4 | Create `app/main.py` | FastAPI app instance, CORS middleware, router registration |
| 0.5 | Create `app/config.py` | Pydantic BaseSettings class with all configuration values (DATABASE_URL, STORAGE_BASE_PATH, OLLAMA_BASE_URL, OLLAMA_MODEL, FLUX_BASE_URL, KOKORO_BASE_URL, FFMPEG_PATH, LOG_LEVEL) |
| 0.6 | Create `app/database.py` | SQLAlchemy engine, session factory, Base declarative class, `init_db()` function |
| 0.7 | Create `.env` file | Default development values for all config keys |
| 0.8 | Create `app/shared/exceptions.py` | Base `ContentFlowError` and subclasses (ProjectNotFoundError, InvalidStateTransitionError, AIGenerationError, AIServiceUnavailableError, StorageError, ValidationError) |
| 0.9 | Create `app/shared/storage.py` | `ensure_storage_dirs()` function that creates `storage/projects/` on startup |
| 0.10 | Create health check endpoint | `GET /api/v1/health` returning `{ "status": "ok", "database": "connected", "storage": "ready" }` |
| 0.11 | Configure logging | Python logging with format `{timestamp} | {level} | {module} | {message}` |
| 0.12 | Register global exception handler | Catch `ContentFlowError` subclasses, return structured JSON error responses |
| 0.13 | Create startup event | Initialize database tables, create storage directories |
| 0.14 | Create module directory stubs | Empty `__init__.py` files in `app/modules/`, `app/workflow/`, `app/shared/`, `app/shared/ai/`, `app/shared/prompts/` |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 0.15 | Initialize React project | `npm create vite@latest frontend -- --template react` |
| 0.16 | Install dependencies | react-router-dom, tailwindcss (or CSS modules) |
| 0.17 | Configure Vite proxy | Proxy `/api` requests to `localhost:8000` |
| 0.18 | Create `src/api/client.ts` | Base fetch wrapper with error handling, base URL configuration |
| 0.19 | Create `src/App.tsx` | React Router setup with route definitions |
| 0.20 | Create `src/pages/Dashboard.tsx` | Placeholder page with heading |
| 0.21 | Create health check display | Call `GET /api/v1/health` on Dashboard, show connection status |
| 0.22 | Configure React | Setup Vite configuration |

---

### Configuration Files

| # | Task | Details |
|---|------|---------|
| 0.23 | Create `.gitignore` | Python venv, node_modules, __pycache__, .env, storage/, *.db, dist/ |
| 0.24 | Create `backend/.env.example` | Template with all config keys and comments |
| 0.25 | Create `README.md` | Project overview, prerequisites, setup steps, run commands |
| 0.26 | Configure Python formatting | `ruff` for linting and formatting (pyproject.toml or ruff.toml) |
| 0.27 | Configure Frontend formatting | Prettier config, ESLint config |
| 0.28 | Create dev scripts | `backend/run.sh` (uvicorn reload), `frontend/` uses `npm run dev` |

---

### Database Changes

- SQLAlchemy `Base.metadata.create_all()` on startup
- No tables yet (created in Phase 1)

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Start backend with `uvicorn app.main:app --reload` | Server starts on port 8000, no errors |
| `GET http://localhost:8000/api/v1/health` | Returns 200 with status "ok" |
| Start frontend with `npm run dev` | Dev server starts on port 5173 |
| Open `http://localhost:5173` | Dashboard page loads, shows "Connected" status from health API |
| Check `storage/` directory | `storage/projects/` directory exists |
| Check database | `contentflow.db` file created |

---

### Definition of Done

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Frontend successfully calls backend health endpoint
- [ ] Database file is created on startup
- [ ] Storage directories are created on startup
- [ ] Health endpoint returns correct response
- [ ] All configuration loads from `.env`
- [ ] Logging outputs to console with correct format
- [ ] `.gitignore` excludes appropriate files
- [ ] README contains setup instructions

---

## Phase 1 — Project Module

### Objective

Deliver a fully working Project feature. Users can create, view, list, and delete projects. The Project Dashboard and Project Workspace UI are functional.

### Deliverables

- Project CRUD (Create, Read, List, Delete)
- Project Dashboard page with project cards
- Project Workspace page with 3-panel layout (empty panels)
- Project status tracking
- Database schema for projects and tasks tables

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 1.1 | Create `modules/project/models.py` | SQLAlchemy model for `projects` table (id, title, topic, language, duration, content_type, template_id, additional_context, status, created_at, updated_at) |
| 1.2 | Create `modules/project/schemas.py` | Pydantic schemas: ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse |
| 1.3 | Create `modules/project/service.py` | Functions: create_project, get_project, list_projects, delete_project, update_project_status |
| 1.4 | Create `modules/project/router.py` | Endpoints: POST /projects, GET /projects, GET /projects/{id}, DELETE /projects/{id}, GET /projects/{id}/status |
| 1.5 | Create `tasks` model | SQLAlchemy model for `tasks` table (id, project_id, task_type, status, error_message, created_at, updated_at) |
| 1.6 | Register project router | Add to `main.py` with prefix `/api/v1` |
| 1.7 | Create Alembic migration | Initial migration with projects and tasks tables |
| 1.8 | Implement project deletion | Delete project record + delete project storage directory |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 1.9 | Create project types | JavaScript objects/types for Project, ProjectCreate, ProjectStatus |
| 1.10 | Create `src/api/projects.ts` | API functions: createProject, getProjects, getProject, deleteProject |
| 1.11 | Build Dashboard page | Grid/list of project cards showing title, status, created date. "New Project" button. |
| 1.12 | Create "New Project" form | Modal or inline form with fields: title, topic, language, duration, content_type, additional_context |
| 1.13 | Create Project Workspace page | 3-panel layout: Left (ProgressPanel), Center (ContentPanel), Right (AIPanel). Load project data on mount. |
| 1.14 | Build ProgressPanel component | Stepper showing stages (Script, Scene, Image, Voice, Reel) with current stage highlighted |
| 1.15 | Build ContentPanel component | Shows "Ready to generate script" message for Draft projects |
| 1.16 | Build AIPanel component | Empty panel with "Instructions" heading (populated in Phase 2) |
| 1.17 | Implement project deletion | Confirm dialog, call delete API, refresh list |
| 1.18 | Add routing | `/` → Dashboard, `/project/:id` → Project Workspace |
| 1.19 | Create AppContext | React Context providing current project data to workspace components |

---

### Database Changes

```
projects
├── id (TEXT, PK, UUID)
├── title (TEXT, NOT NULL)
├── topic (TEXT, NOT NULL)
├── language (TEXT, NOT NULL, default: "English")
├── duration (INTEGER, NOT NULL, default: 60)
├── content_type (TEXT, NOT NULL, default: "Technology")
├── template_id (TEXT, FK, nullable)
├── additional_context (TEXT, nullable)
├── status (TEXT, NOT NULL, default: "draft")
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)

tasks
├── id (TEXT, PK, UUID)
├── project_id (TEXT, FK, NOT NULL)
├── task_type (TEXT, NOT NULL)
├── status (TEXT, NOT NULL, default: "pending")
├── error_message (TEXT, nullable)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects` | Create a new project |
| GET | `/api/v1/projects` | List all projects |
| GET | `/api/v1/projects/{project_id}` | Get project details |
| DELETE | `/api/v1/projects/{project_id}` | Delete project and its assets |
| GET | `/api/v1/projects/{project_id}/status` | Get current project status and available actions |

---

### AI Integration

None in this phase.

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Create project via API | Returns 201 with project data, status "draft" |
| List projects | Returns array of projects |
| Get project by ID | Returns project details |
| Delete project | Returns 204, project removed from list |
| Delete project with storage | Storage directory cleaned up |
| Create project via UI | Form submits, project appears in dashboard |
| Click project card | Navigates to workspace, loads project data |
| Workspace shows correct status | Progress panel shows "Draft" stage |

---

### Definition of Done

- [ ] Projects can be created via API and UI
- [ ] Projects appear in Dashboard
- [ ] Projects can be deleted
- [ ] Project Workspace loads with 3-panel layout
- [ ] Progress panel shows project stages
- [ ] Status is correctly displayed
- [ ] Storage directory created per project
- [ ] Database migrations work cleanly

---

### Dependencies

- Phase 0 complete

---

## Phase 2 — Script Module

### Objective

Deliver script generation, editing, refinement, and approval. This is the first AI-powered stage and establishes the pattern for all subsequent modules.

### Deliverables

- Script generation via Ollama/Qwen
- Script display in workspace
- Script editing (manual)
- Script refinement (AI-assisted with user instructions)
- Script approval (advances project to next stage)
- AI layer foundation (orchestrator, prompt builder, response validator, ollama client)
- Workflow service foundation

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 2.1 | Create `shared/ai/ollama_client.py` | HTTP client for Ollama API. Methods: `generate(prompt, model)`. Handle connection errors, timeouts. |
| 2.2 | Create `shared/ai/prompt_builder.py` | `build(stage, project_context, template_context, current_artifact, user_instructions)` → assembled prompt string |
| 2.3 | Create `shared/ai/response_validator.py` | `validate(response, stage)` → validated content or raise error. Script validation: non-empty, minimum length. |
| 2.4 | Create `shared/ai/orchestrator.py` | `generate(stage, context)` and `refine(stage, context, instructions)` → coordinates prompt_builder → client → validator |
| 2.5 | Create `shared/prompts/script.py` | System prompt template for script generation. Include role, output format rules, content guidelines. |
| 2.6 | Create `modules/script/models.py` | SQLAlchemy model for `scripts` table |
| 2.7 | Create `modules/script/schemas.py` | ScriptResponse, ScriptGenerateRequest, ScriptRefineRequest |
| 2.8 | Create `modules/script/service.py` | generate_script, refine_script, approve_script, get_script, update_script |
| 2.9 | Create `modules/script/router.py` | Endpoints for script operations |
| 2.10 | Create `workflow/workflow_service.py` | validate_state, advance_state, get_current_stage. Enforce: can only generate script when status is "draft". |
| 2.11 | Integrate workflow with script | Script router calls workflow_service to validate before generation |
| 2.12 | Implement background task for generation | Script generation runs as BackgroundTask. Create task record. Update on completion/failure. |
| 2.13 | Create task status endpoint | `GET /api/v1/projects/{id}/tasks/{task_id}` for polling |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 2.14 | Create `src/api/script.ts` | API functions: generateScript, getScript, refineScript, approveScript, updateScript |
| 2.15 | Create `src/api/tasks.ts` | API function: pollTaskStatus (with setInterval wrapper) |
| 2.16 | Build ScriptStage component | Display script content in editable textarea. Show when project is at script stage. |
| 2.17 | Add "Generate Script" button | Visible when status is "draft". Triggers generation. Shows loading state. |
| 2.18 | Implement polling for generation | After triggering generate, poll task status. Show progress indicator. Display script when complete. |
| 2.19 | Add "Approve" button | Visible when script exists. Calls approve endpoint. Advances stage in UI. |
| 2.20 | Add "Refine" action | Input field in AIPanel for refinement instructions. Submit calls refine endpoint. |
| 2.21 | Add inline editing | Allow direct text editing of script content. Save button calls update endpoint. |
| 2.22 | Update ProgressPanel | Reflect script stage states (generating, generated, approved) |
| 2.23 | Handle errors | Display error messages from failed generations. Show retry option. |

---

### Database Changes

```
scripts
├── id (TEXT, PK, UUID)
├── project_id (TEXT, FK, NOT NULL, UNIQUE)
├── content (TEXT, NOT NULL)
├── refinement_instructions (TEXT, nullable)
├── is_approved (BOOLEAN, NOT NULL, default: false)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects/{id}/script/generate` | Trigger script generation (async) |
| GET | `/api/v1/projects/{id}/script` | Get current script |
| PUT | `/api/v1/projects/{id}/script` | Update script content (manual edit) |
| POST | `/api/v1/projects/{id}/script/refine` | Refine script with instructions (async) |
| POST | `/api/v1/projects/{id}/script/approve` | Approve script, advance state |
| GET | `/api/v1/projects/{id}/tasks/{task_id}` | Poll task status |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Model | Ollama / Qwen |
| Prompt | System prompt (role + rules) + Project context (topic, language, duration, content_type) + User instructions |
| Validation | Non-empty response, minimum 100 characters, contains actual content |
| Refinement | Current script + user feedback → updated script |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Generate script (Ollama running) | Task created, status transitions to "processing", script generated, status "completed" |
| Generate script (Ollama down) | Task fails, error message stored, 503 returned to user |
| Get script | Returns script content |
| Edit script manually | Content updated in database |
| Refine script | New script generated incorporating feedback |
| Approve script | Project status advances to "script_approved" |
| Generate when not in "draft" | Returns 409 Conflict |
| Poll task status | Returns current task state |
| UI shows loading during generation | Spinner/progress shown while polling |
| UI shows script after generation | Script text displayed in ContentPanel |

---

### Definition of Done

- [ ] Script generates successfully from Ollama
- [ ] Script displays in workspace
- [ ] Script can be edited manually
- [ ] Script can be refined with instructions
- [ ] Script approval advances project state
- [ ] Workflow service prevents invalid state transitions
- [ ] Background task with polling works end-to-end
- [ ] Error states handled (AI unavailable, generation failed)
- [ ] AI layer (orchestrator, prompt builder, validator, client) established

---

### Dependencies

- Phase 1 complete
- Ollama installed and running locally
- Qwen model pulled (`ollama pull qwen2.5:7b`)

---

## Phase 3 — Scene Module

### Objective

Generate scene breakdowns from an approved script. Scenes include title, description, duration, voiceover text, and image prompts. The AI determines the number of scenes and their sequencing.

### Deliverables

- Scene generation from approved script
- Scene cards display in workspace
- Individual scene editing
- Scene refinement (all scenes regenerated with instructions)
- Scene approval (advances project state)

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 3.1 | Create `shared/prompts/scene.py` | System prompt for scene generation. Output format: JSON array of scene objects. |
| 3.2 | Create `modules/scene/models.py` | SQLAlchemy model for `scenes` table |
| 3.3 | Create `modules/scene/schemas.py` | SceneResponse, SceneListResponse, SceneGenerateRequest, SceneRefineRequest |
| 3.4 | Create `modules/scene/service.py` | generate_scenes, refine_scenes, approve_scenes, get_scenes, update_scene |
| 3.5 | Create `modules/scene/router.py` | Endpoints for scene operations |
| 3.6 | Update response_validator | Add scene validation: valid JSON array, required fields per scene (title, description, duration, voiceover_text, image_prompt) |
| 3.7 | Update workflow_service | Add scene stage transitions. Require "script_approved" to generate scenes. |
| 3.8 | Handle scene parsing | Parse AI JSON response into individual scene records. Store each scene as separate row. |
| 3.9 | Implement scene refinement | Send all scenes + user feedback to AI. Replace all scene records with new output. |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 3.10 | Create `src/api/scenes.ts` | API functions: generateScenes, getScenes, refineScenes, approveScenes, updateScene |
| 3.11 | Build SceneStage component | List of scene cards. Each card shows: scene number, title, duration, voiceover text, image prompt. |
| 3.12 | Add "Generate Scenes" button | Visible when status is "script_approved". Triggers generation with polling. |
| 3.13 | Add scene card editing | Click scene card to expand/edit individual fields |
| 3.14 | Add "Refine" action | Input in AIPanel. Refines all scenes together. |
| 3.15 | Add "Approve" button | Approves all scenes. Advances project state. |
| 3.16 | Update ProgressPanel | Reflect scene stage states |
| 3.17 | Show scene count and total duration | Summary bar above scene cards |

---

### Database Changes

```
scenes
├── id (TEXT, PK, UUID)
├── project_id (TEXT, FK, NOT NULL)
├── scene_number (INTEGER, NOT NULL)
├── title (TEXT, NOT NULL)
├── description (TEXT, NOT NULL)
├── duration (INTEGER, NOT NULL)
├── voiceover_text (TEXT, NOT NULL)
├── image_prompt (TEXT, NOT NULL)
├── is_approved (BOOLEAN, NOT NULL, default: false)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects/{id}/scenes/generate` | Generate scenes from script (async) |
| GET | `/api/v1/projects/{id}/scenes` | Get all scenes |
| PUT | `/api/v1/projects/{id}/scenes/{scene_id}` | Update individual scene |
| POST | `/api/v1/projects/{id}/scenes/refine` | Refine all scenes with instructions (async) |
| POST | `/api/v1/projects/{id}/scenes/approve` | Approve all scenes |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Model | Ollama / Qwen |
| Prompt | System prompt (JSON output format) + Approved script + Project context (duration, content_type) + User instructions |
| Validation | Valid JSON array, each object has: title (string), description (string), duration (integer), voiceover_text (string), image_prompt (string) |
| Output | AI determines scene count and sequencing based on script and duration |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Generate scenes from approved script | JSON parsed, scenes stored as individual records |
| Scene count determined by AI | Multiple scenes created, durations sum to approximate target |
| Edit individual scene | Single scene record updated |
| Refine scenes | All scenes regenerated with feedback incorporated |
| Approve scenes | Project status advances to "scenes_approved" |
| Generate when script not approved | Returns 409 |
| Invalid JSON from AI | Error surfaced, user can retry |
| UI displays scene cards | Each card shows all fields |

---

### Definition of Done

- [ ] Scenes generate from approved script
- [ ] AI produces valid scene breakdown with correct fields
- [ ] Scenes display as cards in workspace
- [ ] Individual scenes can be edited
- [ ] Scenes can be refined with instructions
- [ ] Scene approval advances project state
- [ ] Scene validation catches malformed AI output
- [ ] Total duration approximately matches target

---

### Dependencies

- Phase 2 complete
- Approved script exists in project

---

## Phase 4 — Image Module

### Objective

Generate one image per scene using FLUX model. Users can review, refine prompts, and regenerate individual images.

### Deliverables

- Image generation for all scenes (batch)
- Image display in gallery format
- Individual image regeneration with refined prompt
- Image approval (advances project state)
- FLUX client integration

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 4.1 | Create `shared/ai/image_client.py` | HTTP client for FLUX API. Methods: `generate(prompt)` → image bytes. Handle timeouts, errors. |
| 4.2 | Create `modules/image/models.py` | SQLAlchemy model for `images` table |
| 4.3 | Create `modules/image/schemas.py` | ImageResponse, ImageListResponse, ImageRefineRequest |
| 4.4 | Create `modules/image/service.py` | generate_images (batch for all scenes), regenerate_image (single scene), approve_images, get_images |
| 4.5 | Create `modules/image/router.py` | Endpoints for image operations |
| 4.6 | Update workflow_service | Add image stage transitions. Require "scenes_approved" to generate images. |
| 4.7 | Implement batch generation | Iterate through scenes, generate image for each using scene's image_prompt. Save to `storage/projects/{id}/images/scene_XX.png`. |
| 4.8 | Implement individual regeneration | Accept refined prompt for a single scene. Regenerate only that image. |
| 4.9 | Create file serving endpoint | `GET /api/v1/projects/{id}/images/{scene_number}` → serves image file |
| 4.10 | Update shared/prompts/image.py | Prompt enhancement template (optional: wraps scene image_prompt with style instructions) |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 4.11 | Create `src/api/images.ts` | API functions: generateImages, getImages, refineImage, approveImages |
| 4.12 | Build ImageStage component | Grid/gallery of generated images. Each image shows scene number and prompt used. |
| 4.13 | Add "Generate Images" button | Visible when scenes approved. Triggers batch generation with polling. |
| 4.14 | Add individual image actions | Per-image: "Refine Prompt" button → input for new prompt → regenerate that image only |
| 4.15 | Add "Approve All" button | Approves all images. Advances project state. |
| 4.16 | Show generation progress | During batch generation, show which scene is currently generating |
| 4.17 | Display images with scene context | Show scene title and prompt alongside each image |

---

### Database Changes

```
images
├── id (TEXT, PK, UUID)
├── scene_id (TEXT, FK, NOT NULL)
├── project_id (TEXT, FK, NOT NULL)
├── file_path (TEXT, NOT NULL)
├── prompt_used (TEXT, NOT NULL)
├── is_approved (BOOLEAN, NOT NULL, default: false)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects/{id}/images/generate` | Generate images for all scenes (async) |
| GET | `/api/v1/projects/{id}/images` | Get all image metadata |
| GET | `/api/v1/projects/{id}/images/{scene_number}` | Serve image file |
| POST | `/api/v1/projects/{id}/images/{scene_id}/refine` | Regenerate single image with new prompt (async) |
| POST | `/api/v1/projects/{id}/images/approve` | Approve all images |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Model | FLUX (local) |
| Input | Image prompt from scene (optionally enhanced by prompt template) |
| Output | PNG image file |
| Storage | `storage/projects/{id}/images/scene_XX.png` |
| Batch | One image per scene, generated sequentially |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Generate images (FLUX running) | One image per scene saved to storage |
| Generate images (FLUX down) | Task fails with descriptive error |
| Get image file | Image served via API |
| Refine single image | New image generated with updated prompt, old image replaced |
| Approve images | Project status advances to "images_approved" |
| Generate when scenes not approved | Returns 409 |
| Image files persist on disk | Files exist at expected paths |
| UI shows image gallery | All images displayed in grid |

---

### Definition of Done

- [ ] Images generate for all scenes via FLUX
- [ ] Images saved to correct file paths
- [ ] Images served via API endpoint
- [ ] Individual images can be regenerated with new prompt
- [ ] Image approval advances project state
- [ ] Gallery display shows all images with context
- [ ] Error handling for FLUX unavailability

---

### Dependencies

- Phase 3 complete
- FLUX model running locally
- Approved scenes with image_prompt fields

---

## Phase 5 — Voice Module

### Objective

Generate voice-over audio for each scene using Kokoro TTS. Users can preview audio and approve.

### Deliverables

- Voice generation for all scenes (batch)
- Audio playback in workspace
- Voice approval (advances project state)
- Kokoro TTS client integration

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 5.1 | Create `shared/ai/voice_client.py` | HTTP client for Kokoro TTS. Methods: `generate(text, language)` → audio bytes. Handle errors. |
| 5.2 | Create `modules/voice/models.py` | SQLAlchemy model for `voice_tracks` table |
| 5.3 | Create `modules/voice/schemas.py` | VoiceTrackResponse, VoiceListResponse |
| 5.4 | Create `modules/voice/service.py` | generate_voice_tracks (batch), approve_voice, get_voice_tracks |
| 5.5 | Create `modules/voice/router.py` | Endpoints for voice operations |
| 5.6 | Update workflow_service | Add voice stage transitions. Require "scenes_approved" to generate voice. |
| 5.7 | Implement batch voice generation | Iterate scenes, send voiceover_text to Kokoro TTS, save WAV files to `storage/projects/{id}/voice/scene_XX.wav` |
| 5.8 | Create audio serving endpoint | `GET /api/v1/projects/{id}/voice/{scene_number}` → serves audio file |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 5.9 | Create `src/api/voice.ts` | API functions: generateVoice, getVoiceTracks, approveVoice |
| 5.10 | Build VoiceStage component | List of voice tracks per scene. Each shows scene title, voiceover text, and audio player. |
| 5.11 | Add "Generate Voice" button | Visible when scenes approved. Triggers batch generation with polling. |
| 5.12 | Add audio player per scene | HTML5 audio element with play/pause, seek, duration display |
| 5.13 | Add "Approve All" button | Approves all voice tracks. Advances project state. |
| 5.14 | Show generation progress | Indicate which scene's voice is currently generating |

---

### Database Changes

```
voice_tracks
├── id (TEXT, PK, UUID)
├── scene_id (TEXT, FK, NOT NULL)
├── project_id (TEXT, FK, NOT NULL)
├── file_path (TEXT, NOT NULL)
├── is_approved (BOOLEAN, NOT NULL, default: false)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects/{id}/voice/generate` | Generate voice for all scenes (async) |
| GET | `/api/v1/projects/{id}/voice` | Get all voice track metadata |
| GET | `/api/v1/projects/{id}/voice/{scene_number}` | Serve audio file |
| POST | `/api/v1/projects/{id}/voice/approve` | Approve all voice tracks |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Model | Kokoro TTS (local) |
| Input | Voiceover text from scene, language from project |
| Output | WAV audio file |
| Storage | `storage/projects/{id}/voice/scene_XX.wav` |
| Batch | One audio track per scene, generated sequentially |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Generate voice (Kokoro running) | One WAV per scene saved to storage |
| Generate voice (Kokoro down) | Task fails with error |
| Get audio file | Audio served via API |
| Play audio in browser | Audio plays correctly in HTML5 player |
| Approve voice | Project status advances to "voice_approved" |
| Generate when scenes not approved | Returns 409 |

---

### Definition of Done

- [ ] Voice generates for all scenes via Kokoro TTS
- [ ] Audio files saved to correct paths
- [ ] Audio served via API and playable in browser
- [ ] Voice approval advances project state
- [ ] Audio player works in workspace
- [ ] Error handling for TTS unavailability

---

### Dependencies

- Phase 3 complete (scenes must be approved)
- Kokoro TTS running locally
- Note: Voice can run in parallel with Image stage (both depend on scenes_approved). Implementation is sequential for simplicity.

---

## Phase 6 — Reel Module

### Objective

Assemble approved images and voice tracks into a final MP4 video using FFmpeg. Users can preview and download.

### Deliverables

- Reel generation from approved images + voice
- Video preview in workspace
- Video download
- FFmpeg integration

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 6.1 | Create `shared/ai/video_client.py` | FFmpeg wrapper. Method: `assemble_reel(images, audio_tracks, durations, output_path)`. Uses subprocess with list-based arguments. |
| 6.2 | Create `modules/reel/models.py` | SQLAlchemy model for `reels` table |
| 6.3 | Create `modules/reel/schemas.py` | ReelResponse |
| 6.4 | Create `modules/reel/service.py` | generate_reel, get_reel |
| 6.5 | Create `modules/reel/router.py` | Endpoints for reel operations |
| 6.6 | Update workflow_service | Require "images_approved" AND "voice_approved" to generate reel. |
| 6.7 | Implement reel assembly | Gather all scene images + voice tracks in order. Call FFmpeg to create video. Each scene: display image for voice duration. Output to `storage/projects/{id}/reel/final.mp4`. |
| 6.8 | Create video serving endpoint | `GET /api/v1/projects/{id}/reel/stream` → serves video for preview |
| 6.9 | Create download endpoint | `GET /api/v1/projects/{id}/reel/download` → serves video as attachment |
| 6.10 | Mark project complete | After reel generation, update status to "completed" |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 6.11 | Create `src/api/reel.ts` | API functions: generateReel, getReel |
| 6.12 | Build ReelStage component | Video player with preview. Download button. |
| 6.13 | Add "Generate Reel" button | Visible when images and voice approved. Triggers generation with polling. |
| 6.14 | Add video player | HTML5 video element with controls |
| 6.15 | Add "Download" button | Triggers file download of final.mp4 |
| 6.16 | Update ProgressPanel | Show "Completed" state. All stages marked done. |

---

### Database Changes

```
reels
├── id (TEXT, PK, UUID)
├── project_id (TEXT, FK, NOT NULL, UNIQUE)
├── file_path (TEXT, NOT NULL)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/projects/{id}/reel/generate` | Generate reel from approved assets (async) |
| GET | `/api/v1/projects/{id}/reel` | Get reel metadata |
| GET | `/api/v1/projects/{id}/reel/stream` | Stream video for preview |
| GET | `/api/v1/projects/{id}/reel/download` | Download video file |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Tool | FFmpeg (subprocess) |
| Input | Ordered list of images + audio tracks + scene durations |
| Output | MP4 video file |
| Logic | For each scene: display scene image for the duration of its voice track |
| Storage | `storage/projects/{id}/reel/final.mp4` |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Generate reel (FFmpeg installed) | MP4 created at expected path |
| Generate reel (FFmpeg missing) | Clear error message |
| Preview reel in browser | Video plays in HTML5 player |
| Download reel | File downloads with correct filename |
| Generate when assets not approved | Returns 409 |
| Reel duration | Approximately matches sum of scene voice durations |
| Project marked complete | Status updated to "completed" |

---

### Definition of Done

- [ ] Reel generates from approved images and voice
- [ ] Video plays in browser preview
- [ ] Video downloadable as MP4
- [ ] Project status advances to "completed"
- [ ] FFmpeg errors handled gracefully
- [ ] Full pipeline works end-to-end (Topic → Reel)

---

### Dependencies

- Phase 4 complete (images approved)
- Phase 5 complete (voice approved)
- FFmpeg installed on system

---

## Phase 7 — Templates

### Objective

Add template support. Templates pre-configure audience, tone, language, and creator notes. Projects can use a template and override individual values.

### Deliverables

- Template CRUD
- Template selection during project creation
- Template values applied to prompt building
- Template override at project level

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 7.1 | Create `modules/template/models.py` | SQLAlchemy model for `templates` table |
| 7.2 | Create `modules/template/schemas.py` | TemplateCreate, TemplateUpdate, TemplateResponse, TemplateListResponse |
| 7.3 | Create `modules/template/service.py` | create_template, get_template, list_templates, update_template, delete_template |
| 7.4 | Create `modules/template/router.py` | CRUD endpoints for templates |
| 7.5 | Update project creation | Accept optional template_id. Store reference. |
| 7.6 | Update prompt_builder | When project has a template, include template context (audience, tone, language, creator_notes, default_instructions) in prompt assembly. |
| 7.7 | Seed default templates | Create 2-3 default templates on first startup (e.g., "Tech Tutorial", "AI Explainer", "Productivity Tips") |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 7.8 | Create `src/api/templates.ts` | API functions: createTemplate, getTemplates, getTemplate, updateTemplate, deleteTemplate |
| 7.9 | Add template management page/section | List templates, create new, edit, delete |
| 7.10 | Add template selector to project creation | Dropdown in "New Project" form to select a template |
| 7.11 | Show template context in workspace | Display applied template info in AIPanel or project header |

---

### Database Changes

```
templates
├── id (TEXT, PK, UUID)
├── name (TEXT, NOT NULL, UNIQUE)
├── audience (TEXT, NOT NULL)
├── tone (TEXT, NOT NULL)
├── language (TEXT, NOT NULL)
├── creator_notes (TEXT, nullable)
├── default_instructions (TEXT, nullable)
├── created_at (DATETIME, NOT NULL)
└── updated_at (DATETIME, NOT NULL)
```

---

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/templates` | Create template |
| GET | `/api/v1/templates` | List all templates |
| GET | `/api/v1/templates/{template_id}` | Get template |
| PUT | `/api/v1/templates/{template_id}` | Update template |
| DELETE | `/api/v1/templates/{template_id}` | Delete template |

---

### AI Integration

| Component | Details |
|-----------|---------|
| Impact | Template context added to prompt builder output |
| Prompt position | Between system prompt and project context |
| Override | Project-level values (language, etc.) override template values if set |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Create template | Template stored, appears in list |
| Edit template | Fields updated |
| Delete template | Template removed, projects using it still work (nullable FK) |
| Create project with template | Template ID stored on project |
| Generate script with template | Prompt includes template context (audience, tone) |
| Generate script without template | Prompt works normally without template section |
| Template values in prompt | Visible in DEBUG-level logs |

---

### Definition of Done

- [ ] Templates CRUD works
- [ ] Templates selectable during project creation
- [ ] Template context included in AI prompts
- [ ] Default templates seeded on first run
- [ ] Projects work with and without templates
- [ ] Template deletion doesn't break existing projects

---

### Dependencies

- Phase 2 complete (prompt builder must exist)
- Can be built any time after Phase 2, placed here to avoid disrupting the core pipeline development

---

## Phase 8 — Polish

### Objective

Harden the application. Add proper error handling, loading states, validation, and documentation. Ensure the MVP is reliable for daily use.

### Deliverables

- Comprehensive error handling across all stages
- Loading states and progress indicators
- Input validation (frontend and backend)
- Application documentation
- Configuration validation on startup
- Performance review

---

### Backend Tasks

| # | Task | Details |
|---|------|---------|
| 8.1 | Audit error handling | Ensure every endpoint has proper try/catch. All AI failures return descriptive errors. |
| 8.2 | Add request validation | Validate all inputs: non-empty topic, valid duration range (15-300 seconds), valid language, valid content_type |
| 8.3 | Add startup checks | Verify Ollama connectivity, FLUX connectivity, Kokoro connectivity, FFmpeg availability on startup. Log warnings for unavailable services (don't fail). |
| 8.4 | Add request logging | Log every API request (method, path, status code, duration) at INFO level |
| 8.5 | Add AI call metrics | Log prompt length, response time, token count (if available) per AI call |
| 8.6 | Review storage cleanup | Ensure project deletion cleans up all files. Handle partial generation cleanup. |
| 8.7 | Add input sanitization | Strip excessive whitespace, validate string lengths |
| 8.8 | Add health check detail | Expand health endpoint to check all external dependencies |

---

### Frontend Tasks

| # | Task | Details |
|---|------|---------|
| 8.9 | Add loading skeletons | Show skeleton UI while data loads |
| 8.10 | Add error boundaries | React error boundaries to prevent white screens |
| 8.11 | Add toast notifications | Success/error notifications for user actions |
| 8.12 | Add form validation | Required fields, character limits, duration range |
| 8.13 | Add empty states | Meaningful messages when no projects, no script, etc. |
| 8.14 | Add confirmation dialogs | Confirm before delete, confirm before overwrite |
| 8.15 | Responsive workspace | Ensure workspace panels work on standard screen sizes |
| 8.16 | Add keyboard shortcuts | Ctrl+Enter to submit forms, Escape to close modals |

---

### Documentation Tasks

| # | Task | Details |
|---|------|---------|
| 8.17 | Update README | Complete setup guide with prerequisites, installation steps, run commands, architecture overview |
| 8.18 | Document API | Verify OpenAPI docs are accurate and complete at `/docs` |
| 8.19 | Add development guide | How to add a new module, how to add a new prompt, how to test |
| 8.20 | Add troubleshooting guide | Common errors, AI service connectivity, FFmpeg issues |

---

### Testing Scenarios

| Test | Expected Result |
|------|----------------|
| Submit empty topic | Validation error shown |
| AI service goes down mid-generation | Graceful error, retry possible |
| Delete project with partial assets | All files cleaned up |
| Rapidly click generate | Only one task created (debounce or disable button) |
| Open workspace for completed project | All stages shown as completed, assets viewable |
| Health check with services down | Reports which services unavailable |

---

### Definition of Done

- [ ] No unhandled errors in normal workflows
- [ ] All loading states implemented
- [ ] Input validation on all forms
- [ ] Confirmation dialogs for destructive actions
- [ ] Health check reports all service statuses
- [ ] README complete and accurate
- [ ] Full pipeline (Topic → Download) works reliably
- [ ] Application suitable for daily use

---

### Dependencies

- All previous phases complete

---

## Summary

| Phase | Focus | Key Outcome |
|-------|-------|-------------|
| 0 | Foundation | Project boots, frontend talks to backend |
| 1 | Project | CRUD projects, workspace layout |
| 2 | Script | First AI generation, workflow service, full vertical slice |
| 3 | Scene | Structured AI output (JSON), batch records |
| 4 | Image | Binary asset generation, file storage, gallery |
| 5 | Voice | Audio generation, playback |
| 6 | Reel | Video assembly, full pipeline complete |
| 7 | Templates | Reusable configurations |
| 8 | Polish | Production quality for personal use |

---

## Estimated Effort Allocation

| Phase | Relative Effort |
|-------|----------------|
| Phase 0 | Small |
| Phase 1 | Medium |
| Phase 2 | Large (establishes all patterns) |
| Phase 3 | Medium |
| Phase 4 | Medium |
| Phase 5 | Small-Medium |
| Phase 6 | Medium |
| Phase 7 | Small |
| Phase 8 | Medium |

Phase 2 is the heaviest because it establishes the AI layer, workflow service, background tasks, and polling — patterns that all subsequent phases reuse.

---

## Prerequisites (Before Phase 0)

| Prerequisite | Purpose |
|-------------|---------|
| Python 3.11+ installed | Backend runtime |
| Node.js 18+ installed | Frontend runtime |
| Ollama installed | LLM inference |
| Qwen model pulled | Text generation |
| FLUX available | Image generation |
| Kokoro TTS available | Voice generation |
| FFmpeg installed | Video assembly |
| Git initialized | Version control |
| VS Code with extensions | Development environment |
