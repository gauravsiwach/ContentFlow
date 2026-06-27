# ContentFlow - PRD (Phase 1: Reel Creation)

## Product Name
ContentFlow

## Objective

Build a local-first AI-powered content creation platform that transforms a topic into a complete reel package with human review at every stage.

---

## Target User

Primary User:
- Gaurav

Content Types:
- AI
- Software Development
- .NET
- Azure
- Productivity
- Technology

---

## Goals

- Reduce content creation time from hours to minutes
- Keep human control at every stage
- Minimize operational costs using local AI models
- Generate production-ready reel assets

---

## MVP Scope

### Inputs

- Topic
- Language
- Duration
- Content Type
- Template
- Additional Context

### Outputs

- Script
- Scene Breakdown
- Image Prompts
- Generated Images
- Voice Tracks
- Final Reel

---

## Core Workflow

Create Project
↓
Generate Script
↓
Review Script
↓
Generate Scenes
↓
Review Scenes
↓
Generate Images
↓
Review Images
↓
Generate Voice
↓
Review Voice
↓
Generate Reel
↓
Preview Reel
↓
Download

---

## Human In The Loop

Every stage requires user approval.

Available Actions:
- Approve
- Edit
- Refine With Instructions

No regenerate-from-scratch workflow in MVP.

---

## Refinement Workflow

User can provide feedback at every stage.

Examples:
- Make hook stronger
- Use simple Hindi
- Add more technical details
- Add real-world examples
- Reduce duration

AI updates the existing artifact instead of replacing it.

---

## Scene Generation

AI decides:
- Number of scenes
- Scene duration
- Scene sequencing

Inputs:
- Script
- Duration
- Content Type

---

## Image Generation

Phase 1:
- One image per scene
- AI-generated images only
- FLUX model

Actions:
- Approve
- Refine Prompt
- Regenerate Image

---

## Voice Generation

Voice generated per scene.

Future support:
- Male Voice
- Female Voice
- Custom Voice Profiles

AI may use scene context to determine delivery style.

---

## Reel Generation

Input:
- Approved Images
- Approved Voice Tracks

Output:
- MP4 Reel

Phase 1:
- Automatic reel generation
- No timeline editor

---

## Templates

Template contains:
- Audience
- Tone
- Language
- Creator Notes
- Default Instructions

Project can override template values.

---

## Project Dashboard

Features:
- Create Project
- Resume Project
- Delete Project
- View Status

---

## Project Persistence

Store:
- Project Metadata
- Script
- Scenes
- Images
- Voice Files
- Reel Files
- Approval Status

Statuses:
- Draft
- Script Approved
- Scenes Approved
- Images Approved
- Voice Approved
- Reel Generated
- Completed

---

## Technical Stack

Frontend:
- React

Backend:
- Python
- FastAPI

LLM:
- Ollama
- Qwen

Image Generation:
- FLUX

Voice:
- Kokoro TTS

Video:
- FFmpeg

Database:
- SQLite

---

## Competitor Analysis

Existing Tools:
- InVideo AI
- Runway
- HeyGen
- CapCut
- Veed

Observed Gaps:
- Limited creator control
- Weak review workflow
- No scene-level refinement
- Cloud-first cost model
- Lack of educational content workflow

---

## Differentiators

- Local First
- Human In The Loop
- Creator Controlled Workflow
- Scene-Level Review
- Template Driven
- Low Cost Operation

---

## Out Of Scope

- SaaS Platform
- Multi User Support
- Billing
- Analytics
- Social Publishing
- RAG
- Workflow Engine
- Microservices
- Cloud Architecture

---

## Future Enhancements

- Research Stage
- URL/PDF/YouTube Inputs
- Prompt Management UI
- Camera Motion Metadata
- Timeline Editor
- Stock Media Integration
- Long Form Content
- Blog Generation
- LinkedIn Post Generation
