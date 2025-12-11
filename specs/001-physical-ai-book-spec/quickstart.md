# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Basic familiarity with command line

## Setup Instructions

### 1. Clone and Initialize
```bash
# If starting from scratch
npx create-docusaurus@latest textbook-physical-ai classic
cd textbook-physical-ai
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Docusaurus
Update `docusaurus.config.ts` with the following settings:
- Enable MathJax for mathematical notation
- Configure Algolia search
- Set up sidebar navigation for 5 chapters and 15 lessons
- Add Mermaid diagram support

### 4. Add Content Structure
```bash
# Create the chapter directories
mkdir -p docs/chapters/01-introduction
mkdir -p docs/chapters/02-perception
mkdir -p docs/chapters/03-control
mkdir -p docs/chapters/04-intelligence
mkdir -p docs/chapters/05-applications
```

### 5. Start Development Server
```bash
npm run start
# or
yarn start
```

Your textbook will be available at http://localhost:3000

## Content Creation Workflow

### Adding a New Lesson
1. Create a new MDX file in the appropriate chapter directory
2. Follow the standardized lesson format from the specification
3. Include hands-on exercises with code examples
4. Add proper frontmatter with metadata
5. Update the sidebar configuration to include the new lesson

### Example Lesson Structure
```mdx
---
title: Foundations of Physical AI
sidebar_position: 1
description: Understanding the intersection of artificial intelligence and physical systems
---

# Foundations of Physical AI

## Learning Objectives
- Understand the basic concepts of Physical AI
- Identify key differences between traditional AI and embodied AI
- Recognize applications of Physical AI in robotics

## Introduction
[Lesson content here...]

## Hands-on Exercise
[Practical exercise with code examples...]

## Summary
[Key takeaways...]
```

## Key Features Implemented
- Responsive design for all devices
- Full-text search across all content
- Mathematical notation support
- Code syntax highlighting
- Diagram and image integration
- Navigation between related concepts