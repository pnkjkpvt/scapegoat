# Test Chatbot for Jailbreaker

A super simple chatbot. Here is all you need to know:

- This chatbot serves as a test target for the jailbreaker and is for development purposes only.
- It can be hosted as a standalone Flask app and is only accessible via API calls (i.e., it does not have a frontend).
- The chatbot uses the GPT-35-Turbo model hosted on Azure for generating responses, and the context is not stored between requests.
- No authentication mechanism is implemented for the chatbot.
- It is built on top of the LangChain framework.

## Installation

1. **Create a virtual environment named `.venv` and activate it:**

    ```bash
    python3 -m venv .venv
    ```
   ```bash
   source .venv/bin/activate
   ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set the OpenAI API key as environment variables:**

    ```bash
    export OPENAI_API_KEY=dummy_api_key
    ```
   Alternatively, you can set these environment variables in a the IDE run configuration.

4. **Run the chatbot server:**
   * **using Docker**
       ```bash
       docker build -t scapegoat-chatbot .
       docker run -d -p 5001:5001 --name <container-name> scapegoat-chatbot
      ```
   * **Local run**
      ```bash
      python app.py
      ```
      or
      ```bash
      flask --app app:app run --host 0.0.0.0 --port 5001
      ```


## Accessing the Chatbot

The server is running on [http://localhost:5001](http://localhost:5001). \
The services running inside docker container can access this at http://host.docker.internal:5001

The chatbot is accessible via a POST request to [http://localhost:5001/chat](http://localhost:5001/chat) and it expects a JSON payload with the following structure:

```json
{
    "message": "Hello"
}
```