import psutil
import win32gui
import win32process
import subprocess

PROCESS_NAME = "SuperliminalGOG.exe"

GST_COMMAND_TEMPLATE = (
    'gst-launch-1.0 -e d3d11screencapturesrc window-handle={hwnd} show-cursor=true '
    '! queue ! d3d11download ! videoconvert ! videorate '
    '! video/x-raw,format=I420,width=1920,height=1080,framerate=30/1 '
    '! x264enc tune=zerolatency bitrate=5000 speed-preset=superfast '
    '! h264parse ! queue ! mux. '
    'wasapi2src ! audioconvert ! audioresample ! avenc_aac bitrate=128000 '
    '! aacparse ! queue ! mux. '
    'mp4mux name=mux ! filesink location=game_capture.mp4'
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
    cmd = GST_COMMAND_TEMPLATE.format(hwnd=hwnd)
    print(f"🔹 Running GStreamer:\n{cmd}\n")

    # Run the command
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
