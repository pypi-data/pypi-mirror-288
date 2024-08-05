# APIFixer

APIFixer is a powerful automation tool built for API developers. It starts an API server using Uvicorn, analyzes its routes, generates detailed documentation using OpenAI, and performs automated tests of API endpoints. Key features include:

1. API Server Startup: Allows you to easily start the server with minimal configuration.
2. API Documentation Generation: Uses OpenAI to generate detailed documentation based on API routes.
3. Automatic testing of API routes: Checks for errors and writes the results to a log file.
4. Support for auto-close server: Ability to automatically close the server after all tasks are completed.
5. This tool simplifies the API development and testing process, minimizes errors, and creates easy-to-use documentation.

Developed by Bohdan Terskow (c) 2024

## Usage Process

### Parameter Setup:

Define parameters when initializing the APIFixer class, such as resource (resource), host (host), port (port), and the OpenAI API key (openai_api_key).

### Start the server and generate documentation:

Call the run method to start the server. This method also starts the route validation process, which automatically generates documentation and performs API testing.

### Testing and Logging:

API route validation and testing occurs in the background and the results are written to a log file.

### Auto-close server:

If auto_close_server=True is set, the server will automatically close after all tasks are completed.

```python
fixer = APIFixer(
    resource='main:app',
    host='127.0.0.1',
    port=8000,
    openai_api_key='your_openai_api_key'
)

fixer.run(auto_close_server=True)
```