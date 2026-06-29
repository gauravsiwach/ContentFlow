# ==========================================================
# Scene Generation Prompt (Optimized)
# ==========================================================

SCENE_SYSTEM_PROMPT = """
Convert the script into a JSON array of scenes for a short video.

Each scene object must have:
- title: Brief scene name
- description: What happens (1 sentence)
- duration: Seconds (integer)
- voiceover_text: Script portion for this scene
- image_prompt: Detailed AI image prompt
- camera_directions: Shot type (e.g. "Medium shot, static")
- visual_description: Setting and mood

Create 3-5 scenes. Total duration should match target.

Return ONLY valid JSON array. No markdown. No explanations.

Example:
[{"title":"Hook","description":"Person speaks","duration":8,"voiceover_text":"Script text here","image_prompt":"Person talking, bright room","camera_directions":"Medium shot","visual_description":"Bright room, friendly"}]
"""

# ==========================================================
# Scene Refinement Prompt (Optimized)
# ==========================================================

SCENE_REFINE_PROMPT = """
Refine the scenes based on user feedback.

Apply the feedback while keeping the same JSON format.

Return only the refined JSON array. No markdown. No explanations.
"""
