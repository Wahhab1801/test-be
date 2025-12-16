# Constants used by the voice agent.

import os

# Default to the value injected by LiveKit Cloud; fall back to a local name for dev.
AGENT_NAME: str = (
    os.getenv("LIVEKIT_AGENT_NAME") or os.getenv("LK_AGENT_NAME") or "my-voice-agent"
)

GREETING = "Hey, how can I help you today?"
INSTRUCTIONS = (
    "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
    "You should use short and concise responses, and avoid unpronounceable punctuation."
)
