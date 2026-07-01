# Comedy Children Content Type Specialization

This plan implements a specialized content type system for children's comedy, designed to be easily extensible for future content types while improving quality through phased prompt optimization.

## Overview

Transform the current open-ended `content_type` field into a structured dropdown system starting with "Comedy (Children)" as the only option, with an extensible architecture for adding more content types later.

## Phase 1: Architecture & Content Type System (BE + FE)

### 1.1 Content Type Enum & Configuration (BE)
- Create `ContentType` enum in `app/shared/content_types.py`
- Define content types with metadata:
  ```python
  class ContentType(str, Enum):
    COMEDY_CHILDREN = "comedy_children"
    # Future: EDUCATIONAL = "educational"
    # Future: MARKETING = "marketing"
  ```
- Add content type configuration with:
  - Display name
  - Target audience
  - Description
  - Supported age ranges

### 1.2 Update Database Schema (BE)
- Keep `content_type` column in Project model
- Add constraint to only allow enum values
- Default: `ContentType.COMEDY_CHILDREN`

### 1.3 Update API Schemas (BE)
- Change `content_type` in `ProjectCreate` to use enum
- Add validation for enum values

### 1.4 Frontend Dropdown (FE)
- Change content_type input from text to dropdown
- Show only "Comedy (Children)" option
- Add description: "Humorous content for children (ages 5-10)"
- Display content type in project details view
- Add API endpoint to get available content types

### 1.5 Testing Phase 1
- Create project via UI with dropdown
- Verify content_type is saved as "comedy_children"
- Verify API validation rejects invalid content types

## Phase 2: Prompt Template System (BE)

### 2.1 Create Prompt Template Architecture (BE)
- Create `app/shared/prompts/templates/` directory
- Create base template interface:
  ```python
  class PromptTemplate(ABC):
    @abstractmethod
    def get_script_prompt(self, context: dict) -> str
    @abstractmethod
    def get_scene_prompt(self, context: dict) -> str
  ```

### 2.2 Comedy Children Template Implementation (BE)
- Create `app/shared/prompts/templates/comedy_children.py`
- Implement specialized prompts:
  - **Script Prompt**: Simple language, kid-friendly jokes, short attention span pacing
  - **Scene Prompt**: Cartoon style, bright colors, exaggerated expressions
  - **Image Prompt**: Child-friendly characters, playful settings
  - **Voice Prompt**: Energetic, playful tone

### 2.3 Template Registry (BE)
- Create template registry to map content types to templates
- Allow easy addition of new templates for future content types

### 2.4 Update Prompt Builder (BE)
- Modify `PromptBuilder` to use template system
- Select template based on `content_type`
- Fall back to default if template not found

### 2.5 Testing Phase 2
- Test template retrieval for comedy_children
- Verify fallback to legacy for unknown types
- Test prompt generation with new templates

## Phase 3: Script Prompt Specialization (BE + FE)

### 3.1 Comedy Children Script Prompt (BE)
- Focus on:
  - Simple, age-appropriate vocabulary
  - Short, punchy sentences
  - Relatable situations for children
  - Physical comedy and visual humor
  - Positive, uplifting messages
  - Duration calculation for children's attention (shorter scenes)

### 3.2 Language Style (BE)
- Add `CHILDREN_LANGUAGE_STYLE` constant
- Simple sentence structures
- Avoid complex words
- Use repetition and rhyme where appropriate
- Interactive elements (questions, call-and-response)

### 3.3 Humor Guidelines (BE)
- Slapstick and physical comedy
- Wordplay and simple puns
- Silly situations
- Animal characters
- Everyday scenarios kids relate to

### 3.4 Frontend Script Preview (FE)
- Show script content with highlighting for humor elements
- Display word count and estimated duration
- Show content type specific tips (e.g., "Keep it simple for kids")

### 3.5 Testing Phase 3
- Generate script with comedy_children content type
- Verify simple vocabulary and age-appropriate humor
- Check word count matches duration calculation
- Test script refinement with new prompts

## Phase 4: Scene Prompt Specialization (BE + FE)

### 4.1 Comedy Children Scene Prompt (BE)
- Focus on:
  - Fast-paced scene transitions
  - Clear visual storytelling
  - Exaggerated character expressions
  - Bright, colorful environments
  - Simple, clear actions

### 4.2 Visual Style Guidelines (BE)
- Cartoon/animated style
- Primary colors
- Rounded shapes
- Friendly character designs
- Clear contrast

### 4.3 Scene Structure (BE)
- Short scenes (3-8 seconds each)
- Clear beginning, middle, end
- Visual punchlines
- Setup and payoff structure

### 4.4 Frontend Scene Preview (FE)
- Show scene cards with visual descriptions
- Display scene duration and image prompts
- Add scene editing with content type tips
- Show scene sequence with thumbnails

### 4.5 Testing Phase 4
- Generate scenes with comedy_children content type
- Verify cartoon style visual descriptions
- Check scene duration (3-8 seconds)
- Test scene refinement with new prompts

## Phase 5: Image Prompt Specialization (BE + FE)

### 5.1 Comedy Children Image Prompt (BE)
- Focus on:
  - Cartoon/illustration style
  - Bright, saturated colors
  - Expressive characters
  - Playful settings
  - Child-safe content

### 5.2 Character Design (BE)
- Exaggerated expressions
- Distinct silhouettes
- Friendly appearances
- Clear emotions

### 5.3 Environment Design (BE)
- Playful locations (playground, home, school)
- Bright lighting
- Clean compositions
- Age-appropriate props

### 5.4 Frontend Image Preview (FE)
- Show generated images with scene context
- Display image prompts used
- Add image regeneration with style options
- Show image quality indicators

### 5.5 Testing Phase 5
- Generate images with comedy_children content type
- Verify cartoon style and bright colors
- Check character designs are child-friendly
- Test image regeneration with new prompts

## Phase 6: Voice Prompt Specialization (BE + FE)

### 6.1 Comedy Children Voice Prompt (BE)
- Focus on:
  - Energetic delivery
  - Clear enunciation
  - Character voices for different roles
  - Appropriate pacing for children
  - Upbeat tone

### 6.2 Voice Style Guidelines (BE)
- Higher pitch for children's content
- Dynamic range (whisper to shout)
- Clear character differentiation
- Sound effect integration

### 6.3 Frontend Voice Preview (FE)
- Show audio player with voiceover text
- Display voice style and tone indicators
- Add voice regeneration with style options
- Show audio quality indicators

### 6.4 Testing Phase 6
- Generate voices with comedy_children content type
- Verify energetic and clear delivery
- Check appropriate pacing for children
- Test voice regeneration with new prompts

## Phase 7: End-to-End Testing & Validation (BE + FE)

### 7.1 Full Workflow Testing
- Create project with comedy_children content type
- Generate script → verify comedy children prompts
- Generate scenes → verify cartoon style descriptions
- Generate images → verify bright colors and cartoon style
- Generate voices → verify energetic delivery
- Generate reel → verify final output quality

### 7.2 Quality Metrics
- Script: Simple vocabulary, age-appropriate humor
- Scenes: 3-8 second duration, visual comedy structure
- Images: Cartoon style, bright colors, child-friendly
- Voices: Energetic, clear, appropriate pacing
- Reel: Cohesive comedy narrative for children

### 7.3 User Acceptance Testing
- Test with actual children's topics
- Gather feedback on humor appropriateness
- Validate visual appeal for target age group
- Check engagement metrics

## Phase 8: Future Extensibility (BE + FE)

### 8.1 Adding New Content Types
- To add new content type:
  1. Add enum value to `ContentType`
  2. Add configuration to `ContentTypeConfig`
  3. Create new template class
  4. Register in template registry
  5. Add to frontend dropdown
  6. No changes to core logic needed

### 8.2 Content Type Metadata
- Target audience
- Age range
- Language complexity level
- Visual style guidelines
- Voice style preferences

### 8.3 Frontend Extensibility
- Dynamic dropdown population from API
- Content type specific UI elements
- Per-content-type tips and guidelines

## Implementation Order

1. **Phase 1** (Week 1): Architecture + FE dropdown (BE + FE)
2. **Phase 2** (Week 2): Template system (BE only)
3. **Phase 3** (Week 3): Script prompts + FE preview (BE + FE)
4. **Phase 4** (Week 4): Scene prompts + FE preview (BE + FE)
5. **Phase 5** (Week 5): Image prompts + FE preview (BE + FE)
6. **Phase 6** (Week 6): Voice prompts + FE preview (BE + FE)
7. **Phase 7** (Week 7): End-to-end testing (BE + FE)
8. **Phase 8** (Week 8): Extensibility documentation (BE + FE)

## Success Metrics

- Script generation produces age-appropriate humor
- Scene generation creates visual comedy structure
- Image generation produces cartoon-style images
- Voice generation uses appropriate tone
- System can add new content type in < 1 day
- Quality improvement measurable vs generic prompts
