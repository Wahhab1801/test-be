import logging
import os
import sys

try:
    from dotenv import load_dotenv
    from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
    from livekit.agents.voice import Agent, AgentSession
    from livekit.plugins import openai, silero
except ImportError as e:
    print(f"Error: {e}")
    print("It looks like you're missing some dependencies.")
    print("Please make sure you are running this script with the virtual environment activated.")
    print("Try running: ./run_agent.sh")
    print("Or: source venv/bin/activate && python agent.py dev")
    sys.exit(1)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)
logger = logging.getLogger("voice-agent")
AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME") or os.getenv("LK_AGENT_NAME") or "my-voice-agent"

def prewarm(proc: JobContext):
    logger.info("Prewarming VAD...")
    try:
        proc.userdata["vad"] = silero.VAD.load()
        logger.info("VAD loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load VAD: {e}")

async def entrypoint(ctx: JobContext):
    logger.info(
        "Entrypoint called",
        extra={
            "room": ctx.room.name,
            "room_meta": getattr(ctx.room, "metadata", None),
            "agent_name": getattr(ctx.job, "agent_name", None),
        },
    )

    try:
        logger.info("Connecting to room %s", ctx.room.name)
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        logger.info("Connected to room %s", ctx.room.name)
    except Exception as e:
        logger.error("Failed to connect to room %s: %s", ctx.room.name, e, exc_info=True)
        raise

    try:
        participant = await ctx.wait_for_participant()
        logger.info("First participant detected: %s", participant.identity)
    except Exception as e:
        logger.error("Failed while waiting for participant: %s", e, exc_info=True)
        raise

    instructions = (
        "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
        "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
    )

    agent = Agent(
        instructions=instructions,
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    session = AgentSession()
    try:
        logger.info("Starting agent session...")
        await session.start(agent, room=ctx.room)
        logger.info("Agent session started")

        logger.info("Agent saying hello...")
        await session.say("Hey, how can I help you today?", allow_interruptions=True)
        logger.info("Agent said hello")
    except Exception as e:
        logger.error("Error in agent session: %s", e, exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting agent with name '%s'", AGENT_NAME)
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, agent_name=AGENT_NAME))
