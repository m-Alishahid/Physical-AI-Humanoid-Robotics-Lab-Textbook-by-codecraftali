# Data Model: Robotic Nervous System (ROS 2) Textbook Module 1

This document outlines the key entities and their relationships for the content of Module 1 of the ROS 2 textbook. This data model focuses on the logical structure of the pedagogical content and features, rather than database schema.

## Entities

### 1. Chapter
Represents a self-contained unit of learning within the textbook module. Each chapter focuses on a specific topic and progresses in complexity.

**Attributes**:
- **Title**: (String) The name of the chapter (e.g., "ROS 2 Fundamentals").
- **Level**: (Enum: Beginner, Intermediate, Advanced, Expert) The target learning level of the chapter.
- **Content**: (Markdown/Structured Text) The main theoretical explanations, descriptions, and prose of the chapter.
- **LearningObjectives**: (List of LearningObjective) A collection of learning goals for the chapter.
- **CodeExamples**: (List of CodeExample) References to executable Python code snippets.
- **HandsOnExercises**: (List of HandsOnExercise) A collection of practical tasks for learners.
- **RAGIntegrationPoints**: (List of RAGIntegrationMarker) Locations within the content where the RAG chatbot can be integrated.
- **PersonalizationSections**: (List of PersonalizationSection) Prompts or areas for learner customization.
- **WordCount**: (Integer) Estimated word count of the chapter's core content.

**Relationships**:
- Contains many LearningObjectives.
- Contains many CodeExamples.
- Contains many HandsOnExercises.
- Contains many RAGIntegrationMarkers.
- Contains many PersonalizationSections.

### 2. LearningObjective
A concise, actionable statement describing what a learner should be able to achieve or understand after completing a specific section or the entire chapter.

**Attributes**:
- **Description**: (String) The objective statement (e.g., "Understand the ROS 2 graph architecture").
- **AssociatedSection**: (String) Reference to the textbook section this objective pertains to.

**Relationships**:
- Belongs to a Chapter.

### 3. CodeExample
A runnable Python script that demonstrates a ROS 2 concept. It includes the code itself, explanations, and expected output.

**Attributes**:
- **Title**: (String) A brief title for the example.
- **FilePath**: (String) The relative or absolute path to the Python script file.
- **Description**: (Markdown/String) Explanation of the code, its purpose, and how it relates to ROS 2 concepts.
- **ExpectedOutput**: (String) The anticipated console output or behavior when the code is executed.
- **Difficulty**: (Enum: Easy, Medium, Hard) The complexity level of the example.

**Relationships**:
- Belongs to a Chapter.

### 4. HandsOnExercise
A practical task or problem designed for learners to apply the concepts learned in a chapter. These range in difficulty and may involve coding, simulation, or conceptual challenges.

**Attributes**:
- **Title**: (String) A brief title for the exercise.
- **Description**: (Markdown/String) Detailed instructions for the exercise.
- **ExpectedOutcome**: (String) What the learner should achieve or demonstrate.
- **Difficulty**: (Enum: Easy, Medium, Hard) The complexity level of the exercise.
- **Hints/SolutionPath**: (String) Optional path to hints or solutions (if provided separately).

**Relationships**:
- Belongs to a Chapter.

### 5. RAGIntegrationMarker
A specific tag or annotation embedded within the textbook content that signals a point where the RAG chatbot can provide supplementary information, answer questions, or offer interactive explanations.

**Attributes**:
- **ID**: (String) A unique identifier for the integration point.
- **Topic**: (String) The main subject or keyword for which the chatbot should provide context.
- **ContextSnippet**: (String) A short snippet of the surrounding text to provide context to the chatbot.

**Relationships**:
- Embedded within Chapter content.

### 6. UrduTranslationTag
An inline marker associated with an English technical term or concept, providing its equivalent translation in Urdu for accessibility.

**Attributes**:
- **EnglishTerm**: (String) The original English technical term.
- **UrduTranslation**: (String) The Urdu translation of the term.

**Relationships**:
- Embedded within Chapter content.
- Can be centrally managed in `translation_tags.json`.

### 7. PersonalizationSection
A designated area within a chapter that prompts learners to connect the learned concepts to their own interests, projects, or existing knowledge, thereby personalizing their learning experience.

**Attributes**:
- **Prompt**: (Markdown/String) A question or suggestion to encourage personalization.
- **Type**: (Enum: Reflective, Project-Based, Discussion) The nature of the personalization activity.

**Relationships**:
- Belongs to a Chapter.
