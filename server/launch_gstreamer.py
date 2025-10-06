import os

# GStreamer WebRTC pipeline (video + audio to aiortc peer)
pipeline = r"""
    gst-launch-1.0 -v webrtcbin name=sendrecv bundle-policy=max-bundle 
    videotestsrc is-live=true ! videoconvert ! queue ! vp8enc deadline=1 ! rtpvp8pay pt=96 ! sendrecv. 
    audiotestsrc is-live=true ! audioconvert ! audioresample ! opusenc ! rtpopuspay pt=97 ! sendrecv.
"""

print("Starting GStreamer WebRTC pipeline...")
os.system(pipeline)
