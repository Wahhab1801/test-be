import os
import asyncio
from livekit import api
from dotenv import load_dotenv

load_dotenv()

async def dispatch_agent():
    lkapi = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )

    # Create an explicit dispatch for the agent
    dispatch_service = lkapi.agent_dispatch

    room_name = "test-room-3"
    agent_name = "my-voice-agent"
    
    print(f"Creating explicit dispatch for agent '{agent_name}' in room '{room_name}'...")
    
    try:
        # Ensure room exists first
        await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
        
        req = api.CreateAgentDispatchRequest(
            room=room_name,
            agent_name=agent_name
        )
        dispatch = await dispatch_service.create_dispatch(req)
        print(f"Dispatch created: {dispatch}")
        
    except Exception as e:
        print(f"Error creating dispatch: {e}")

    except Exception as e:
        print(f"Error: {e}")
    
    await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(dispatch_agent())
