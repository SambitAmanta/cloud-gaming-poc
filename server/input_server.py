import asyncio
import json
import websockets
from pynput.keyboard import Controller as KeyController, Key
from pynput.mouse import Controller as MouseController, Button

keyboard = KeyController()
mouse = MouseController()

async def handle_input(websocket):
    print("Client connected for input...")
    async for message in websocket:
        try:
            data = json.loads(message)
            event_type = data.get("type")

            if event_type == "key":
                key = data.get("key")
                action = data.get("action")

                if action == "down":
                    keyboard.press(key)
                elif action == "up":
                    keyboard.release(key)

            elif event_type == "mouse_move":
                dx, dy = data.get("dx"), data.get("dy")
                x, y = mouse.position
                mouse.position = (x + dx, y + dy)

            elif event_type == "mouse_click":
                button = Button.left if data.get("button") == "left" else Button.right
                action = data.get("action")
                if action == "down":
                    mouse.press(button)
                elif action == "up":
                    mouse.release(button)

        except Exception as e:
            print("Error:", e)

async def main():
    async with websockets.serve(handle_input, "0.0.0.0", 9000):
        print("Input WebSocket server running on ws://localhost:9000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())


    