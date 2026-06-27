# AI Content Creator - Context Document

## Overview

AI Content Creator is a personal-first content creation platform designed to automate the process of creating short-form videos (Reels, Shorts, TikTok videos).

The primary goal is not to build a SaaS product initially. The goal is to create an internal tool that significantly reduces the time required to create content.

Target outcome:
- Topic to Reel in under 10 minutes
- Local-first architecture
- Minimal operating cost
- Human review at every important stage

## Vision

Build an AI-powered content factory that transforms a simple topic into a complete reel package.

Input:
- Topic
- Language
- Duration
- Content Style

Output:
- Script
- Scene Breakdown
- Image Prompts
- Voiceover Script
- Images
- Voice
- Final Reel Video

## Problem Statement

Current content creation workflow is fragmented.

1. Research topic
2. Write script
3. Create scenes
4. Create image prompts
5. Generate images
6. Generate voiceover
7. Edit video
8. Add captions
9. Export reel

Goal: Reduce this process to a few minutes.

## Primary User

Gaurav

Content Areas:
- AI
- Software Development
- .NET
- Azure
- Productivity
- Technology

Languages:
- English
- Hindi

## Guiding Principles

- Local First
- Low Cost
- Human Review Required
- Modular Architecture
- AI Assisted, Not AI Controlled
- Creator Owns Final Decision

## Existing Market Solutions

### InVideo AI
Strengths:
- Script to video generation
- Large media library

Weaknesses:
- Limited control over scenes
- Generic output

### Runway
Strengths:
- High quality AI video generation

Weaknesses:
- Expensive
- Not optimized for educational content workflows

### HeyGen
Strengths:
- Avatar generation
- Voice generation

Weaknesses:
- Focused on talking-head videos

### CapCut
Strengths:
- Excellent editing experience

Weaknesses:
- Limited AI planning workflow

## Market Gap

Most tools focus on one stage:
- Script Generation
- Video Generation
- Editing
- Voice Generation

Missing:
Idea → Script Review → Scene Review → Asset Generation → Reel Assembly

## MVP Scope

Input:
- Topic
- Language
- Duration
- Content Type

Generate:
- Script
- Scene Breakdown
- Image Prompts
- Voiceover Script

Export:
- JSON
- Markdown

## Technical Direction

Frontend:
- React

Backend:
- Python
- FastAPI

AI:
- Ollama
- Qwen

Image Generation:
- FLUX

Voice Generation:
- Kokoro TTS

Video Processing:
- FFmpeg

Storage:
- SQLite
