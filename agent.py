# LiveKit voice agent entrypoint.
# Started by the LiveKit CLI (`lk agent deploy` or `python agent.py dev`).
# Connects to a room, loads VAD once per process, and runs the voice agent session.

from __future__ import annotations

import logging
import sys

try:
    from dotenv import load_dotenv
    from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
    from livekit.agents.voice import Agent, AgentSession
    from livekit.plugins import openai
except ImportError as e: 
    print(f"Error: {e}")
    print("It looks like you're missing some dependencies.")
    print("Please make sure you are running this script with the virtual environment activated.")
    print("Try running: ./run_agent.sh")
    print("Or: source venv/bin/activate && python agent.py dev")
    sys.exit(1)

load_dotenv()

from utils.constants import AGENT_NAME, GREETING, INSTRUCTIONS
from utils.vad import load_vad

# Configure structured logging up front so every subprocess shares the same format.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)
logger = logging.getLogger("voice-agent")

def prewarm(proc: JobContext) -> None:
    # LiveKit prewarm hook; called once per process before handling jobs.
    # Use this to load heavy assets (like VAD) so every job can reuse them.
    load_vad(proc.userdata, logger)


async def entrypoint(ctx: JobContext) -> None:
    # LiveKit job entrypoint; connects to the room and runs the agent session.
    logger.info(
        "Entrypoint called",
        extra={
            "room": ctx.room.name,
            "room_meta": getattr(ctx.room, "metadata", None),
            "agent_name": getattr(ctx.job, "agent_name", None),
        },
    )

    # Ensure VAD (Voice Activity Detection) is available even if prewarm failed or was skipped.
    # Without VAD, the agent can't detect when to listen, so bail out.
    if "vad" not in ctx.proc.userdata:
        try:
            load_vad(ctx.proc.userdata, logger)
        except Exception:
            logger.error("Unable to initialize VAD; aborting job")
            raise

    # Establish the media connection to the room and subscribe to audio.
    try:
        logger.info("Connecting to room %s", ctx.room.name)
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        logger.info("Connected to room %s", ctx.room.name)
    except Exception as e:
        logger.error("Failed to connect to room %s: %s", ctx.room.name, e, exc_info=True)
        raise

    # Wait for the first remote participant so we know whom to talk to.
    try:
        participant = await ctx.wait_for_participant()
        logger.info("First participant detected: %s", participant.identity)
    except Exception as e:
        logger.error("Failed while waiting for participant: %s", e, exc_info=True)
        raise

    # Assemble the voice agent with STT/LLM/TTS and the shared VAD instance.
    agent = Agent(
        instructions=INSTRUCTIONS,
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    # Run a session bound to the LiveKit room; greet the user once ready.
    session = AgentSession()
    try:
        logger.info("Starting agent session...")
        await session.start(agent, room=ctx.room)
        logger.info("Agent session started")

        logger.info("Agent saying hello...")
        await session.say(GREETING, allow_interruptions=True)
        logger.info("Agent said hello")
    except Exception as e:
        logger.error("Error in agent session: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    logger.info("Starting agent with name '%s'", AGENT_NAME)
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            agent_name=AGENT_NAME,
        )
    )
