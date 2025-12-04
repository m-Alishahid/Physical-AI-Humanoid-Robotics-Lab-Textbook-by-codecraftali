# Code Verification API Contract

This document defines the API contract for a service responsible for verifying and executing code examples within the textbook. This service ensures technical integrity of code snippets.

## Endpoint: `/verify_code`

**Description**: Receives a code snippet and executes it within a controlled environment, returning the output and any errors.

**Method**: `POST`

**Request Body** (`application/json`):

```json
{
  "code_content": "string", // The full Python code snippet to execute
  "language": "string",   // e.g., "python" (can be extended for other languages)
  "ros_version": "string", // e.g., "jazzy", "humble" (for ROS 2 specific execution environment)
  "timeout_seconds": "integer" // Max execution time in seconds
}
```

**Response Body** (`application/json`):

```json
{
  "status": "string",     // "success" or "failure"
  "stdout": "string",     // Standard output from code execution
  "stderr": "string",     // Standard error output (if any)
  "exit_code": "integer", // Exit code of the executed process
  "error_message": "string" // Populated if status is "failure"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input (e.g., unsupported `language`).
- `408 Request Timeout`: Code execution exceeded the `timeout_seconds`.
- `500 Internal Server Error`: An issue occurred with the verification service.

## Endpoint: `/lint_code`

**Description**: Analyzes a code snippet for style violations and potential issues based on defined coding standards (e.g., PEP 8 for Python).

**Method**: `POST`

**Request Body** (`application/json`):

```json
{
  "code_content": "string", // The full Python code snippet to lint
  "language": "string"    // e.g., "python"
}
```

**Response Body** (`application/json`):

```json
{
  "status": "string",     // "success" or "failure"
  "linting_results": [
    {
      "line": "integer",
      "column": "integer",
      "code": "string",     // Linting error code (e.g., "E501")
      "message": "string",  // Description of the linting issue
      "severity": "string"  // "warning" or "error"
    }
  ],
  "error_message": "string" // Populated if status is "failure" (e.g., couldn't parse code)
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input (e.g., unsupported `language`).
- `500 Internal Server Error`: An issue occurred with the linting service.
