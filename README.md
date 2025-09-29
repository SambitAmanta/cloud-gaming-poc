# Cloud Gaming Proof of Concept

This project is a prototype cloud gaming system using **GStreamer + WebRTC**.  
It streams a game window with audio from a host machine to a client.  

### Goals
- Capture game window (video + audio)  
- Encode and stream over the network  
- Play in browser via WebRTC  
- Send back controls (keyboard/mouse)

### Tech Stack
- GStreamer
- Node.js / Python (for signaling server)
- WebRTC (for browser client)

### Setup
1. Install [GStreamer](https://gstreamer.freedesktop.org/download/).
2. Verify installation:
   ```sh
   gst-launch-1.0 --version
