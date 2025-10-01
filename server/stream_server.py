import psutil
import win32gui
import win32process
import subprocess

PROCESS_NAME = "SuperliminalGOG.exe"
STREAM_SERVER = "127.0.0.1"  # Change to your server IP
VIDEO_PORT = 5000
AUDIO_PORT = 5002

GST_COMMAND_TEMPLATE = (
    'gst-launch-1.0 -e '
    'd3d11screencapturesrc window-handle={hwnd} show-cursor=true '
    '! queue ! d3d11download ! videoconvert ! videorate '
    '! video/x-raw,format=I420,width=1920,height=1080,framerate=30/1 '
    '! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast key-int-max=30 byte-stream=true '
    '! h264parse ! rtph264pay config-interval=1 pt=96 '
    '! queue ! udpsink host={server} port={video_port} '
    'wasapisrc loopback=true ! queue ! audioconvert ! audioresample ! avenc_aac bitrate=128000 '
    '! aacparse ! rtpmp4apay pt=97 '
    '! udpsink host={server} port={audio_port}'
)


def get_hwnd_by_process_name(proc_name: str):
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] and proc_name.lower() in proc.info["name"].lower():
            try:
                windows = []

                def callback(hwnd, _):
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                        if win32process.GetWindowThreadProcessId(hwnd)[1] == proc.info["pid"]:
                            windows.append(hwnd)
                win32gui.EnumWindows(callback, None)
                if windows:
                    return windows[0]  # main window
            except Exception:
                pass
    return None


def main():
    hwnd = get_hwnd_by_process_name(PROCESS_NAME)
    if not hwnd:
        print(f"❌ Could not find window for process: {PROCESS_NAME}")
        return

    print(f"✅ Found window handle: {hwnd}")
    cmd = GST_COMMAND_TEMPLATE.format(
        hwnd=hwnd,
        server=STREAM_SERVER,
        video_port=VIDEO_PORT,
        audio_port=AUDIO_PORT
    )
    print(f"🔹 Running GStreamer:\n{cmd}\n")

    # Run the command
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
