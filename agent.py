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

logger = logging.getLogger("voice-agent")

def prewarm(proc: JobContext):
    logger.info("Prewarming VAD...")
    try:
        proc.userdata["vad"] = silero.VAD.load()
        logger.info("VAD loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load VAD: {e}")

async def entrypoint(ctx: JobContext):
    print(f"DEBUG: Entrypoint called for room {ctx.room.name}")
    logger.info(f"Entrypoint called for room {ctx.room.name}")
    


    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("Connected to room")

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

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
        logger.error(f"Error in agent session: {e}", exc_info=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, agent_name="my-voice-agent"))
