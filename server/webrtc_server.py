import asyncio
import json
import os
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole

pcs = set()

routes = web.RouteTableDef()


@routes.post("/offer")
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)
    print("Created peer connection")

    # Handle incoming tracks properly: consume them with MediaBlackhole
    recorders = []

    @pc.on("track")
    def on_track(track):
        print(f"Track received: {track.kind}")
        # Use MediaBlackhole to consume incoming media (replace with MediaRecorder to save)
        bh = MediaBlackhole()
        recorders.append(bh)

        async def start():
            await bh.start()
            bh.addTrack(track)

        asyncio.ensure_future(start())

        @track.on("ended")
        async def on_ended():
            print(f"Track ended: {track.kind}")
            await bh.stop()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

app = web.Application()
app.add_routes(routes)
app.on_shutdown.append(on_shutdown)

web.run_app(app, port=8080)
