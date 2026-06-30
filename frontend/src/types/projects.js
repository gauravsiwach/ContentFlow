// Project status constants
export const PROJECT_STATUS = {
  DRAFT: 'draft',
  SCRIPT_GENERATED: 'script_generated',
  SCRIPT_APPROVED: 'script_approved',
  SCENES_GENERATED: 'scenes_generated',
  SCENES_APPROVED: 'scenes_approved',
  IMAGES_GENERATED: 'images_generated',
  IMAGES_APPROVED: 'images_approved',
  VOICE_GENERATED: 'voice_generated',
  VOICE_APPROVED: 'voice_approved',
  REEL_GENERATED: 'reel_generated',
  COMPLETED: 'completed',
};

// Project type definition
export const ProjectCreate = {
  title: '',
  topic: '',
  language: 'English',
  duration: 60,
  content_type: '',
  template_id: null,
  additional_context: '',
};

// Content type options
export const CONTENT_TYPES = [
  'Technology',
  'AI',
  'Software Development',
  '.NET',
  'Azure',
  'Productivity',
];

// Language options
export const LANGUAGES = [
  'English',
  'Hindi',
];

// Duration options (in seconds)
export const DURATIONS = [10, 30, 60];
