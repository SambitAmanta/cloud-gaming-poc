import subprocess
import asyncio
from webrtc_server import app as signaling_app
from input_server import main as input_server

async def run_all():
    # Launch the game
    subprocess.Popen(["/game/LIMBO/limbo.exe"])
    # Run input + signaling concurrently
    await asyncio.gather(
        input_server(),
        signaling_app(),
    )

if __name__ == "__main__":
    asyncio.run(run_all())
