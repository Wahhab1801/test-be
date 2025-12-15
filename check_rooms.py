import os
import asyncio
from livekit import api
from dotenv import load_dotenv

load_dotenv()

async def list_rooms():
    lkapi = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )

    print(f"Connecting to {os.getenv('LIVEKIT_URL')}...")
    
    try:
        print("Deleting room pre-test-room-3...")
        await lkapi.room.delete_room(api.DeleteRoomRequest(room="pre-test-room-3"))
        print("Room deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
    await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(list_rooms())
