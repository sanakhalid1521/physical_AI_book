# Research Document: Physical AI & Humanoid Robotics Textbook

## Docusaurus Setup and Configuration Research

### Decision: Docusaurus Version and Setup
- **Chosen**: Docusaurus v3+ with TypeScript configuration
- **Rationale**: Latest version with best features, TypeScript provides better type safety for custom components, aligns with constitution requirement
- **Alternatives considered**:
  - Docusaurus v2: Would work but lacks newer features
  - Nextra: Alternative static site generator but less focused on documentation
  - GitBook: Commercial solution with less customization

### Decision: Project Structure
- **Chosen**: Standard Docusaurus structure with docs/ folder for textbook content
- **Rationale**: Follows Docusaurus best practices, enables easy navigation and search functionality as required by constitution
- **Alternatives considered**:
  - Custom React app: More complex, loses Docusaurus features
  - Next.js with custom MDX: Would require rebuilding Docusaurus features

### Decision: Content Organization
- **Chosen**: docs/chapters/[chapter-number]/[lesson-number].mdx structure
- **Rationale**: Enables clear hierarchical navigation, supports the 5 chapters with 3 lessons each requirement
- **Alternatives considered**:
  - Flat structure: Would not support proper navigation hierarchy
  - Blog format: Not appropriate for textbook structure

### Decision: Code and Exercise Integration
- **Chosen**: MDX components for interactive elements, separate code examples directory
- **Rationale**: Supports hands-on learning principle from constitution, allows for reproducible examples
- **Alternatives considered**:
  - External code repositories: Would make examples less accessible
  - Inline code only: Would not support complex examples

### Decision: Math and Diagram Support
- **Chosen**: MathJax for mathematical notation, Mermaid for diagrams
- **Rationale**: Supports constitution requirement for mathematical notation and image integration
- **Alternatives considered**:
  - KaTeX: Alternative math rendering, but MathJax more comprehensive
  - Static images: Less flexible than dynamic diagrams

### Decision: Search and Navigation
- **Chosen**: Algolia search integration with custom sidebar navigation
- **Rationale**: Meets Docusaurus-specific requirement for search functionality and hierarchical navigation
- **Alternatives considered**:
  - Built-in search: Less powerful than Algolia
  - Custom search: More complex to implement