# Data Model: Physical AI & Humanoid Robotics Textbook

## Content Entities

### Chapter
- **Fields**:
  - id: string (e.g., "chapter-1", "chapter-2")
  - title: string (e.g., "Introduction to Physical AI and Humanoid Robotics")
  - description: string (brief overview of chapter content)
  - lessons: array of Lesson objects
  - prerequisites: array of string (knowledge needed before this chapter)
  - learningObjectives: array of string (what students will learn)
  - estimatedTime: number (in minutes)

### Lesson
- **Fields**:
  - id: string (e.g., "lesson-1.1", "lesson-2.3")
  - title: string (e.g., "Foundations of Physical AI")
  - description: string (brief overview of lesson content)
  - chapterId: string (reference to parent chapter)
  - content: string (main content in MDX format)
  - learningObjectives: array of string (specific objectives for this lesson)
  - prerequisites: array of string (specific knowledge needed)
  - handsOnExercises: array of Exercise objects
  - codeExamples: array of CodeExample objects
  - verificationSteps: array of string (how to verify completion)
  - furtherResources: array of string (additional reading/resources)

### Exercise
- **Fields**:
  - id: string (e.g., "exercise-1.1.1")
  - title: string (e.g., "Basic Robot Movement")
  - description: string (what the exercise involves)
  - lessonId: string (reference to parent lesson)
  - difficulty: enum ("beginner", "intermediate", "advanced")
  - estimatedTime: number (in minutes)
  - steps: array of string (step-by-step instructions)
  - requiredEquipment: array of string (what hardware/software needed)
  - expectedOutcome: string (what success looks like)
  - troubleshootingTips: array of string (common issues and solutions)

### CodeExample
- **Fields**:
  - id: string (e.g., "code-example-1.1.1")
  - title: string (e.g., "Basic Movement Controller")
  - lessonId: string (reference to parent lesson)
  - language: string (e.g., "python", "cpp", "javascript")
  - code: string (the actual code)
  - description: string (what the code does)
  - explanation: string (detailed explanation of code)
  - dependencies: array of string (what libraries/packages needed)

### UserProgress
- **Fields**:
  - userId: string (identifier for the user)
  - lessonId: string (which lesson this progress relates to)
  - status: enum ("not-started", "in-progress", "completed")
  - completionDate: date (when completed)
  - exerciseCompletions: array of object (tracking exercise completion)
  - notes: string (user's personal notes)

## Relationships
- Chapter contains many Lessons (1-to-many)
- Lesson contains many Exercises (1-to-many)
- Lesson contains many CodeExamples (1-to-many)
- UserProgress relates to one Lesson (many-to-one)