import asyncio
import subprocess
import sys

USER_ID = "a9c0963f-337c-5884-885c-8c8f8f8d3d82"
WS_URL = f"ws://localhost:8001/penny/v1/ws/{USER_ID}/chat"


def check_wscat():
    try:
        subprocess.run(["wscat", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def chat_with_wscat():
    print(f"Connecting to agent at: {WS_URL}")
    print("Type your message and press Enter. Type 'exit' or Ctrl+C to quit.\n")

    try:
        process = subprocess.Popen(
            ["wscat", "-c", WS_URL],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        process.wait()
    except KeyboardInterrupt:
        print("\nDisconnected.")
        process.terminate()


async def chat_with_websockets():
    try:
        import websockets
    except ImportError:
        print("Installing websockets...")
        subprocess.run([sys.executable, "-m", "pip", "install", "websockets"], check=True)
        import websockets

    print(f"Connecting to agent at: {WS_URL}")
    print("Type your message and press Enter. Type 'exit' or Ctrl+C to quit.\n")

    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected!\n")

            async def receive_loop():
                async for message in ws:
                    print(message, flush=True)

            receive_task = asyncio.create_task(receive_loop())

            while True:
                user_input = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
                if user_input.strip().lower() in ("exit", "quit"):
                    break
                if user_input.strip():
                    await ws.send(user_input)

            receive_task.cancel()

    except ConnectionRefusedError:
        print(f"Could not connect to {WS_URL}")
        print("Make sure the agent server is running: python api/agent/main.py")
    except KeyboardInterrupt:
        print("\nDisconnected.")


if __name__ == "__main__":
    if check_wscat():
        chat_with_wscat()
    else:
        print("wscat not found — using Python websockets fallback.\n")
        asyncio.run(chat_with_websockets())
