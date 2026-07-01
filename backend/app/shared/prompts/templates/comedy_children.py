from typing import Dict, Any
from .base import PromptTemplate


# Language style constants for children's content
CHILDREN_LANGUAGE_STYLE = """
LANGUAGE STYLE GUIDELINES:
- Use simple sentence structures (subject-verb-object)
- Maximum 8 words per sentence
- Avoid complex words (use "happy" instead of "elated", "big" instead of "enormous")
- Use repetition and rhyme where appropriate for memorability
- Include interactive elements (questions: "Can you guess what happens next?")
- Use onomatopoeia for sound effects (boom, crash, meow, woof)
- Keep sentences under 12 syllables
- Use present tense primarily
- Avoid abstract concepts
- Use concrete, visual descriptions
"""

# Visual style constants for children's content
CHILDREN_VISUAL_STYLE = """
VISUAL STYLE GUIDELINES:
- Cartoon/illustration style (not realistic)
- Use bright, saturated colors (red, blue, yellow, green)
- Create exaggerated character expressions (big smiles, surprised faces)
- Design playful, child-friendly settings (playground, classroom, home)
- Ensure all content is safe and appropriate for children
- Use rounded shapes and friendly character designs
- Make characters look approachable and cute
- Use clear emotions on faces (happy, surprised, silly)
- Use clean, simple compositions
- Add age-appropriate props (toys, school supplies, playground equipment)
- Ensure good lighting (bright and cheerful)
- Avoid any scary or dark elements

CHARACTER DESIGN:
- Exaggerated expressions for emotions
- Distinct silhouettes (easy to recognize)
- Friendly appearances (no sharp edges or scary features)
- Clear emotions visible at a glance

ENVIRONMENT:
- Playful locations kids recognize
- Bright, cheerful lighting
- Clean, uncluttered compositions
- Age-appropriate props and background elements
"""

# Humor guidelines for children's comedy
CHILDREN_HUMOR_GUIDELINES = """
HUMOR STYLE GUIDELINES:
- Slapstick and physical comedy (falling, tripping, silly movements)
- Simple wordplay and puns (cat-astrophe, paw-some)
- Silly situations (animals doing human things)
- Animal characters (cats, dogs, rabbits are favorites)
- Everyday scenarios kids relate to (school, playground, home, friends)
- Visual humor (funny faces, exaggerated expressions)
- Repetition for comedic effect
- Surprise endings with happy twists
- No scary or dark humor
- Always positive and uplifting
"""


class ComedyChildrenTemplate(PromptTemplate):
    """Prompt template for children's comedy content"""

    def get_script_prompt(self, context: Dict[str, Any]) -> str:
        """Generate script prompt for children's comedy"""
        topic = context.get('topic', '')
        duration = context.get('duration', 60)
        
        # Calculate target word count based on duration (150 words per minute)
        target_words = int((duration / 60) * 150)
        
        return f"""You are writing a humorous narration for children aged 5-10. The topic is: {topic}

{CHILDREN_LANGUAGE_STYLE}

{CHILDREN_HUMOR_GUIDELINES}

NARRATION STRUCTURE:
1. Hook - Start with something exciting to grab attention
2. Setup - Introduce the funny situation or characters
3. Escalation - Build the comedy with silly moments
4. Twist - A funny surprise or unexpected turn
5. Punchline - End with the funniest line

DURATION REQUIREMENT:
- Target word count: approximately {target_words} words
- This should take approximately {duration} seconds when spoken
- Keep it concise to match the duration

CONTENT GUIDELINES:
- Focus on ONE main funny situation
- Use simple, relatable scenarios kids understand
- Include animal characters when possible (kids love animals)
- Make it sound like you're talking directly to kids
- Use sound effects in your narration (Boom! Crash! Meow!)
- Ask questions to engage young viewers
- Keep it positive and uplifting
- End with a memorable punchline

Remember: This is ONLY the spoken narration. No scene headers, no character names, no camera directions. Just the words that will be spoken."""

    def get_scene_prompt(self, context: Dict[str, Any]) -> str:
        """Generate scene prompt for children's comedy"""
        script_content = context.get('script', '')
        duration = context.get('duration', 60)
        
        # Calculate number of scenes based on duration (3-8 seconds per scene for children)
        estimated_scenes = max(2, min(10, duration // 5))
        
        return f"""You are creating scene descriptions for a children's comedy video based on this script:

{script_content}

{CHILDREN_VISUAL_STYLE}

SCENE STRUCTURE:
- Create {estimated_scenes} short scenes (3-8 seconds each)
- Fast-paced transitions to keep kids engaged
- Each scene must have a clear beginning, middle, and end
- Include visual punchlines (funny moments that land the joke)
- Use setup and payoff structure for each scene
- Total duration should be approximately {duration} seconds

SCENE DESCRIPTIONS:
For each scene, provide:
- Scene number and duration
- Visual description of the setting (cartoon style, bright colors)
- Character positions and actions (exaggerated movements)
- Camera angle suggestions (keep it simple and dynamic)
- Visual humor elements (slapstick, funny movements, silly faces)
- Transition to next scene (quick cuts for energy)
- voiceover_text: MUST include the exact narration text for this scene from the script above

IMPORTANT: Each scene MUST have a voiceover_text field containing the exact narration text for that scene. Split the script narration naturally across scenes.

VISUAL STORYTELLING:
- Show, don't just tell (visual humor is key)
- Exaggerated character expressions for emotions
- Clear contrast between characters and background
- Use movement to keep attention (kids love action)
- Make the action easy to follow
- Include visual callbacks to earlier scenes

Remember: This is for children aged 5-10. Keep it colorful, fun, and visually engaging."""

    def get_image_prompt(self, context: Dict[str, Any]) -> str:
        """Generate image prompt for children's comedy"""
        scene_description = context.get('scene_description', '')
        
        return f"""Create an image for a children's comedy scene based on this description:

{scene_description}

{CHILDREN_VISUAL_STYLE}

ADDITIONAL IMAGE GUIDELINES:
- Focus on the main action or emotion of the scene
- Ensure the image tells a clear visual story
- Use composition that guides the eye to the focal point
- Include background elements that support the scene (toys, playground equipment)
- Make sure characters are the center of attention
- Use color to convey emotion (warm colors for happy, cool for calm)
- Ensure good contrast between characters and background
- Keep the overall composition balanced and harmonious

Remember: This image will be used in a video for children aged 5-10. Make it colorful, engaging, and visually clear."""

    def get_voice_prompt(self, context: Dict[str, Any]) -> str:
        """Generate voice prompt for children's comedy"""
        script_content = context.get('script_content', '')
        
        return f"""You are providing voiceover instructions for a children's comedy script:

{script_content}

Voice Style Requirements:
- Use energetic delivery (keep kids engaged)
- Ensure clear enunciation (easy for children to understand)
- Use appropriate pacing for children (not too fast, not too slow)
- Maintain an upbeat, cheerful tone throughout
- Use higher pitch for children's content (sounds more friendly)
- Include dynamic range (whisper to shout for dramatic effect)
- Create clear character differentiation (different voices for different characters)
- Add appropriate sound effects integration (funny sounds, cartoon effects)
- Keep the tone playful and fun
- Avoid any scary or harsh sounds

Character Voices:
- Main character: Friendly, energetic, clear
- Supporting characters: Distinct voices with fun personalities
- Narrator: Warm, engaging, clear pronunciation

Pacing Guidelines:
- Pause slightly after jokes to let them land
- Speed up slightly during action scenes
- Slow down for important moments or lessons
- Maintain consistent rhythm throughout

Tone:
- Always positive and encouraging
- Never scary or negative
- Include laughter and joy in the delivery"""
