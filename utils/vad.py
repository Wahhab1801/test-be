# Helper for initializing and caching VAD.

from typing import Any, Dict


def load_vad(proc_userdata: Dict[str, Any], logger) -> None:
    # Load and cache VAD in process userdata so subsequent jobs reuse it.
    if "vad" in proc_userdata:
        return
    logger.info("Prewarming VAD...")
    try:
        from livekit.plugins import silero

        proc_userdata["vad"] = silero.VAD.load()
        logger.info("VAD loaded successfully")
    except Exception:
        logger.exception("Failed to load VAD")
        raise
