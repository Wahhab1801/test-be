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
    LIVEKIT_AGENT_NAME=my-voice-agent  # match this with NEXT_PUBLIC_AGENT_NAME / LK_AGENT_NAME
    ```

When deployed via `lk agent deploy`, LiveKit injects `LK_AGENT_NAME`; the worker now respects that value automatically. Keep the frontend `NEXT_PUBLIC_AGENT_NAME` in sync so explicit dispatch targets the running agent.

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
The accompanying Next.js frontend handles room creation, token issuance, and agent dispatch; no extra backend endpoints are required.

## Deployment to LiveKit Cloud

To deploy this agent to LiveKit Cloud for 24/7 availability with automatic scaling:

### Quick Deploy

```bash
# 1. Authenticate with LiveKit Cloud
lk cloud auth

# 2. Create and configure your agent
lk agent create --region us-west --secrets OPENAI_API_KEY="your-openai-api-key"

# 3. Deploy to LiveKit Cloud
lk agent deploy

# 4. Monitor deployment
lk agent logs --follow
```

### Complete Guide

See the comprehensive **[DEPLOYMENT.md](DEPLOYMENT.md)** guide for:

- Detailed step-by-step instructions
- Managing secrets and environment variables
- Monitoring and troubleshooting
- Updating deployed agents
- Regional deployment options

Once deployed, your agent will:

- Automatically connect to LiveKit Cloud
- Join rooms when users connect

## File Structure

- `agent.py`: The main entry point for the voice agent worker.
- `requirements.txt`: Python dependencies.
- `run_agent.sh`: Helper script to run the agent locally.
- `Dockerfile`: Docker configuration for LiveKit Cloud deployment.
- `DEPLOYMENT.md`: Comprehensive deployment guide for LiveKit Cloud.
