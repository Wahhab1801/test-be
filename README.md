# LiveKit Voice Agent Backend

This is the backend for the LiveKit Voice Agent, built with Python and the LiveKit Agents framework. It uses OpenAI for STT/LLM/TTS and Silero for VAD.

## Prerequisites

- Python 3.9+
- A LiveKit Cloud project (or self-hosted LiveKit server)
- OpenAI API Key

## Installation

1.  **Clone the repository** (if you haven't already).

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    - macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in this directory (copy from `.env.example` if available, or create new).
2.  Add the following environment variables:

    ```env
    LIVEKIT_URL=<your-livekit-url>
    LIVEKIT_API_KEY=<your-api-key>
    LIVEKIT_API_SECRET=<your-api-secret>
    OPENAI_API_KEY=<your-openai-api-key>
    ```

## Usage

### Running the Agent

You can use the provided helper script to run the agent in development mode:

```bash
./run_agent.sh
```

Or run it manually:

```bash
source venv/bin/activate
python agent.py dev
```

This will connect the agent to your LiveKit project. When a user connects to a room, the agent will automatically join and start the voice assistant session.

## File Structure

- `agent.py`: The main entry point for the voice agent worker.
- `requirements.txt`: Python dependencies.
- `run_agent.sh`: Helper script to run the agent.
- `dispatch.py`: (Optional) Script for manual dispatching if needed.
