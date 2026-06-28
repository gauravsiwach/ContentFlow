# ContentFlow - Development Guidelines

This document defines the engineering standards, development workflow, coding conventions, and best practices for ContentFlow. Every contributor (human or AI) must follow these guidelines.

---

## Project Context

ContentFlow is a **Proof of Concept (POC)** and **Minimum Viable Product (MVP)** for a local-first AI content creation platform. It serves a single developer and single user.

**Goal:** Validate the product idea quickly while maintaining clean, maintainable code.

**Key Characteristics:**
- Local-first architecture
- Single developer project
- Single user application
- AI-assisted, human-controlled
- Minimal operating cost

---

## Core Principles

1. **Simplicity over complexity** - Choose the simplest solution that works
2. **Readability over cleverness** - Write code that others (and future you) can understand
3. **Working software over perfect software** - Ship functional features first
4. **Build only what is required today** - Avoid speculative features
5. **Avoid premature optimization** - Optimize only when there's a proven problem
6. **Keep the architecture simple** - Modular Monolith, not microservices
7. **Human review for all AI-generated code** - Never commit AI code without review

---

## Development Methodology

### Vertical Slice Development

Each phase must deliver a complete, runnable, testable feature slice:

- Backend API
- Frontend UI
- Database schema
- AI integration (when applicable)
- Testing

**Do not move to the next phase until the current phase is complete and tested.**

### Phase Completion Checklist

- [ ] Backend endpoints implemented and tested
- [ ] Frontend UI implemented and tested
- [ ] Database migrations applied
- [ ] AI integration (if applicable) tested
- [ ] Manual testing scenarios verified
- [ ] No blocking bugs or known issues

---

## Engineering Standards

### Project Structure

```
ContentFlow/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app initialization
│   │   ├── config.py       # Application configuration
│   │   ├── database.py     # Database connection and session
│   │   ├── modules/        # Feature modules (project, script, scene, image, voice, reel)
│   │   ├── workflow/       # Workflow orchestration
│   │   └── shared/         # Shared utilities (AI, storage, exceptions, prompts)
│   ├── requirements.txt
│   └── .env
├── frontend/                # React frontend
│   ├── src/
│   │   ├── api/            # API client functions
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   └── App.jsx         # Main app with routing
│   ├── package.json
│   └── vite.config.js
├── storage/                 # Generated assets (gitignored)
└── Docs/                    # Documentation
```

### Feature-Based Organization

Each feature module in `backend/app/modules/` contains:

```
modules/{feature}/
├── router.py       # API endpoints
├── service.py      # Business logic
├── models.py       # SQLAlchemy database models
└── schemas.py      # Pydantic request/response schemas
```

**Module Boundary Rules:**
- Modules communicate through direct imports or Shared layer
- No circular dependencies
- Each module has a single entry point (service class or functions)

### Naming Conventions

**Python (Backend):**
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

**JavaScript (Frontend):**
- Files: `PascalCase.jsx` for components, `snake_case.js` for utilities
- Components: `PascalCase`
- Functions/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`

**Database:**
- Tables: `snake_case` (plural)
- Columns: `snake_case`
- Foreign keys: `{table}_id`

### Folder Conventions

- `backend/app/modules/` - Feature modules only
- `backend/app/shared/` - Cross-cutting concerns only
- `backend/app/workflow/` - Workflow orchestration only
- `frontend/src/api/` - API client functions only
- `frontend/src/pages/` - Page components only
- `frontend/src/components/` - Reusable UI components only

### API Design Standards

**RESTful Conventions:**
- Use HTTP methods correctly (GET, POST, PUT, DELETE)
- Use plural nouns for resource collections: `/api/v1/projects`
- Use singular nouns for single resources: `/api/v1/projects/{id}`
- Use kebab-case for query parameters
- Return appropriate HTTP status codes

**Response Format:**
```json
{
  "data": { ... },
  "error": null
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "type": "ErrorClassName"
}
```

**Status Codes:**
- 200 - OK
- 201 - Created
- 204 - No Content
- 400 - Bad Request
- 404 - Not Found
- 409 - Conflict (invalid state)
- 500 - Internal Server Error

### Database Conventions

**Models:**
- Use SQLAlchemy declarative base
- All models inherit from `Base`
- Include `created_at` and `updated_at` timestamps
- Use UUID for primary keys (TEXT type in SQLite)

**Migrations:**
- Use Alembic for all schema changes
- Never modify database schema directly
- Create migration before changing models
- Review generated migrations before applying

**Queries:**
- Use SQLAlchemy ORM for queries
- Avoid raw SQL unless absolutely necessary
- Use `get_db()` dependency for database sessions

### Error Handling

**Backend:**
- Create custom exceptions in `app/shared/exceptions.py`
- Use descriptive exception names: `ProjectNotFoundError`, `InvalidStateTransitionError`
- Include HTTP status code in exception
- Register global exception handler in `main.py`
- Log errors with context

**Frontend:**
- Catch API errors in client functions
- Display user-friendly error messages
- Log technical errors to console
- Provide retry mechanism where appropriate

### Logging

**Backend:**
- Use Python `logging` module
- Configure log level via environment variable
- Use structured log format: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Include context in log messages

**Frontend:**
- Use `console.log` for debugging (remove before commit)
- Use error boundaries for React error handling

### Configuration Management

**Backend:**
- Use `pydantic-settings` for configuration
- Store configuration in `app/config.py`
- Load environment variables from `.env` file
- Never commit `.env` file
- Provide `.env.example` with defaults

**Frontend:**
- Use Vite environment variables for build-time config
- Store runtime config in a config object
- Never commit secrets

### AI Integration Rules

**AI Layer:**
- All AI interactions go through `shared/ai/` layer
- Use `AI Orchestrator` to coordinate AI calls
- Each AI client handles its own errors and retries
- Validate AI responses before storing

**Prompt Management:**
- Store prompt templates in `shared/prompts/`
- Use `prompt_builder.py` to assemble prompts
- Never hardcode prompts in business logic
- Keep prompts version-controlled

**Error Handling:**
- Raise `AIGenerationError` for AI failures
- Include stage and error details
- Allow retry for transient failures
- Surface clear error messages to user

### Documentation Updates

**When to Update:**
- After completing a phase
- After significant architectural changes
- After adding new features
- After changing API contracts

**What to Update:**
- `DEVELOPMENT_PLAN.md` - Phase progress
- `TECHNICAL_ARCHITECTURE.md` - Architecture changes
- API documentation (auto-generated by FastAPI)

### Git Commit Conventions

**Commit Message Format:**
```
<type>: <subject>

<body>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `docs` - Documentation
- `style` - Code style (formatting)
- `test` - Tests
- `chore` - Maintenance

**Examples:**
- `feat: add project CRUD endpoints`
- `fix: resolve logging format error`
- `docs: update development guidelines`

**Branch Strategy:**
- `main` - Production
- Feature branches for significant work (optional for single developer)

### Code Review Checklist

**Before Committing:**
- [ ] Code follows naming conventions
- [ ] No console.log or debug statements
- [ ] Error handling is appropriate
- [ ] Logging is sufficient
- [ ] No hardcoded values (use config)
- [ ] No sensitive data in code
- [ ] Tests pass (if applicable)
- [ ] Manual testing passes

### Manual Testing Checklist

**Backend:**
- [ ] Start server with `uvicorn app.main:app --reload`
- [ ] Test all endpoints via API docs at `/docs`
- [ ] Verify error handling
- [ ] Check database records created correctly
- [ ] Verify storage directories created

**Frontend:**
- [ ] Start dev server with `npm run dev`
- [ ] Test all user flows
- [ ] Verify API integration
- [ ] Test error states
- [ ] Check responsive design (basic)
- [ ] Verify no console errors

### Definition of Done

A feature is complete when:
- [ ] Backend implementation done
- [ ] Frontend implementation done
- [ ] Database schema updated
- [ ] API documented (auto-generated)
- [ ] Manual testing verified
- [ ] No known bugs
- [ ] Code reviewed (self or peer)
- [ ] Documentation updated

---

## AI Development Guidelines

### Role of AI Assistants

AI assistants (GitHub Copilot, Windsurf, ChatGPT) are tools to **accelerate development**, not replace engineering judgment.

**AI Should:**
- Generate boilerplate code
- Suggest implementations for well-defined problems
- Help with debugging
- Write tests (with review)
- Refactor code (with review)

**AI Should Not:**
- Make architectural decisions
- Design system boundaries
- Choose technology stack
- Generate entire features in one prompt
- Commit code without human review

### AI Code Generation Workflow

1. **Define the task clearly** - Provide context, constraints, and expected output
2. **Generate in small increments** - One function or component at a time
3. **Review every line** - Understand what the code does
4. **Test immediately** - Verify the code works as expected
5. **Refactor if needed** - Adjust to match project conventions
6. **Commit only after review** - Never commit AI code without understanding it

### AI Prompting Best Practices

**Good Prompts:**
- Include context (what you're building, why)
- Specify constraints (technology, conventions)
- Provide examples (similar code patterns)
- Ask for explanations (not just code)
- Request incremental changes (not full implementations)

**Bad Prompts:**
- "Build the entire project"
- "Write a complete authentication system"
- "Generate all the code for Phase 1"
- Vague requests without context

### Code Review Checklist for AI-Generated Code

- [ ] I understand every line of code
- [ ] Code follows project conventions
- [ ] No unnecessary complexity
- [ ] Error handling is appropriate
- [ ] No security vulnerabilities
- [ ] No hardcoded values
- [ ] Performance is acceptable
- [ ] Tests are adequate

---

## POC Constraints

**Intentionally Avoided in MVP:**

The following are **out of scope** for the MVP. They may be considered only after the product is validated and the need is proven.

### Architecture Patterns
- ❌ Microservices
- ❌ Kubernetes
- ❌ CQRS (Command Query Responsibility Segregation)
- ❌ Event Sourcing
- ❌ Message Queues (RabbitMQ, Kafka, etc.)
- ❌ Plugin Architecture

### Infrastructure
- ❌ Cloud Infrastructure (AWS, GCP, Azure)
- ❌ Container Orchestration
- ❌ Load Balancers
- ❌ CDN integration

### AI Services
- ❌ Multiple AI Providers (use one per category)
- ❌ AI Model Versioning (use latest stable)
- ❌ A/B Testing of AI Models
- ❌ Custom Model Fine-tuning

### Design Patterns
- ❌ Enterprise Design Patterns (unless clearly needed)
- ❌ Repository Pattern (use SQLAlchemy directly)
- ❌ Service Locator Pattern
- ❌ Dependency Injection Frameworks

### Features
- ❌ Multi-tenancy
- ❌ Real-time collaboration
- ❌ WebSockets (use polling in MVP)
- ❌ Advanced caching (use basic caching if needed)
- ❌ Analytics and metrics

### Premature Optimizations
- ❌ Database sharding
- ❌ Read replicas
- ❌ Async processing for simple operations
- ❌ Complex caching strategies
- ❌ Code splitting (unless needed)

**When to Consider These:**
Only after:
1. MVP is validated with real users
2. Specific bottleneck is identified
3. Simpler solution is proven insufficient
4. Benefit clearly outweighs complexity cost

---

## Testing Strategy

### Phase 0-1 Testing
- Manual testing only
- Test via API docs (`/docs`)
- Test via UI flows
- Verify database state

### Future Testing (Post-MVP)
- Unit tests for complex business logic
- Integration tests for critical paths
- E2E tests for key user flows

**Why no automated tests initially:** Speed of development > test coverage for POC. Add tests when they provide clear value.

---

## Performance Guidelines

### Backend
- Keep API response times under 2 seconds for simple operations
- Use database indexes for frequently queried fields
- Avoid N+1 queries
- Use pagination for list endpoints

### Frontend
- Avoid unnecessary re-renders
- Use React.memo for expensive components
- Lazy load images
- Debounce user input where appropriate

**When to optimize:** Only when there's a measurable performance problem.

---

## Security Guidelines

### Backend
- Validate all input via Pydantic schemas
- Use parameterized queries (SQLAlchemy handles this)
- Never expose stack traces to users
- Sanitize error messages before displaying

### Frontend
- Never expose API keys or secrets
- Validate user input before sending to API
- Use HTTPS in production

### Data
- Never commit `.env` file
- Never commit sensitive data
- Use environment variables for secrets

---

## Deployment Guidelines

### Local Development
- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev`
- Database: SQLite (no separate server needed)

### Production (Future)
- Use production ASGI server (Gunicorn + Uvicorn)
- Use production build of frontend
- Configure proper logging levels
- Set up backups for SQLite database

---

## Communication Guidelines

### When to Ask for Help
- Unclear requirements
- Blocked on a technical decision
- Unsure about architectural approach
- Need clarification on existing code

### When to Proceed Independently
- Clear requirements and constraints
- Well-defined problem
- Following established patterns
- Routine implementation

---

## Continuous Improvement

### Review Frequency
- Review these guidelines monthly
- Update based on lessons learned
- Solicit feedback after each phase

### What to Track
- Time spent per phase
- Common blockers
- Frequent errors
- Areas of confusion

---

## Summary

**The Golden Rule:** If you're unsure whether to add complexity, don't. Build the simplest thing that works, validate it, and only then consider adding sophistication.

ContentFlow is a POC. The goal is to learn quickly, not to build a perfect system. Keep it simple, ship it, and iterate based on real feedback.
