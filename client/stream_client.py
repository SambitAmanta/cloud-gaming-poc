import subprocess

VIDEO_PORT = 5000
AUDIO_PORT = 5002

GST_CLIENT_COMMAND = (
    'gst-launch-1.0 -e '
    'udpsrc port={video_port} caps="application/x-rtp, media=video, encoding-name=H264, payload=96" '
    '! rtph264depay ! avdec_h264 ! videoconvert ! queue max-size-buffers=1000 ! autovideosink sync=false '
    'udpsrc port={audio_port} caps="application/x-rtp, media=audio, encoding-name=MP4A-LATM, payload=97" '
    '! rtpmp4adepay ! avdec_aac ! audioconvert ! autoaudiosink'
)


def main():
    cmd = GST_CLIENT_COMMAND.format(
        video_port=VIDEO_PORT, audio_port=AUDIO_PORT)
    print(f"🔹 Running GStreamer client:\n{cmd}\n")
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
