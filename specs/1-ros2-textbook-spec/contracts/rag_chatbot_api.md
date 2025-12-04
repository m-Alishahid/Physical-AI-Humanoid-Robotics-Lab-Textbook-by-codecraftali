# RAG Chatbot API Contract

This document defines the API contract for interacting with the Retrieval-Augmented Generation (RAG) chatbot integrated into the textbook. The chatbot provides contextual information and answers based on the textbook content.

## Endpoint: `/query_rag`

**Description**: Submits a user query and relevant context snippet to the RAG system to retrieve an informed response.

**Method**: `POST`

**Request Body** (`application/json`):

```json
{
  "user_query": "string",  // The user's question (e.g., "What is a ROS 2 node?")
  "context_snippet": "string", // An optional snippet of text from the textbook content where the query originated (e.g., "...ROS 2 is built around the concept of nodes..."), used for context grounding
  "chapter_id": "string",  // The ID of the current chapter or section, to scope retrieval
  "user_profile": {        // Optional: for personalization
    "learning_level": "string", // e.g., "Beginner", "Intermediate"
    "previous_topics": ["string"] // e.g., ["ROS 1", "Python basics"]
  }
}
```

**Response Body** (`application/json`):

```json
{
  "response_text": "string", // The RAG chatbot's generated answer
  "sources": [              // List of textbook sections/pages used for the answer
    {
      "title": "string",    // Title of the source section
      "url": "string"       // Internal URL or path to the source in the textbook
    }
  ],
  "suggested_follow_up_questions": ["string"] // Optional: related questions for further exploration
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input (e.g., missing `user_query`).
- `500 Internal Server Error`: An issue occurred with the RAG processing.

## Endpoint: `/feedback`

**Description**: Submits user feedback on a RAG chatbot response to improve future interactions.

**Method**: `POST`

**Request Body** (`application/json`):

```json
{
  "query_id": "string",     // ID of the original query this feedback relates to
  "rating": "integer",      // 1-5 star rating
  "comment": "string"       // Optional: detailed feedback (e.g., "Answer was irrelevant")
}
```

**Response Body** (`application/json`):

```json
{
  "status": "success",
  "message": "Feedback recorded successfully."
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input (e.g., `query_id` not found).
- `500 Internal Server Error`: Failed to record feedback.
