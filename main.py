import subprocess
import sys
import time
import webbrowser
import requests
import threading


FASTAPI_URL = "http://127.0.0.1:8000/health"
STREAMLIT_URL = "http://localhost:8501/healthz"
STREAMLIT_OPEN_URL = "http://localhost:8501"
MAX_WAIT_SECONDS = 30


def stream_output(process, label):
    """Stream stdout and stderr from a subprocess to the terminal."""
    def stream(pipe, tag):
        for line in iter(pipe.readline, b""):
            print(f"[{tag}] {line.decode(errors='replace').rstrip()}", flush=True)

    threading.Thread(target=stream, args=(process.stdout, label), daemon=True).start()
    threading.Thread(target=stream, args=(process.stderr, label + " ERR"), daemon=True).start()


def wait_for_url(url: str, label: str, max_wait: int = MAX_WAIT_SECONDS) -> bool:
    """Poll a URL until it returns 200 or timeout is reached."""
    print(f"Waiting for {label} to be ready...")
    for _ in range(max_wait):
        try:
            if requests.get(url, timeout=2).status_code == 200:
                print(f"{label} started successfully.")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)

    print(f"{label} did not start within {max_wait} seconds. Aborting.")
    return False


def start_process(label: str, args: list) -> subprocess.Popen:
    print(f"Starting {label}...")
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stream_output(process, label)
    return process


def monitor_processes(*processes):
    """Watch for unexpected process exits and warn."""
    def watch(proc, label):
        proc.wait()
        print(f"[{label}] Process exited unexpectedly with code {proc.returncode}")

    for proc, label in processes:
        threading.Thread(target=watch, args=(proc, label), daemon=True).start()


def shutdown(processes: list):
    print("\nShutting down...")
    for proc in processes:
        proc.terminate()
    for proc in processes:
        proc.wait()
    print("All processes stopped.")


def main():
    fastapi_process = start_process("FASTAPI", [
        sys.executable, "-m", "uvicorn", "app.api.main:app",
        "--host", "0.0.0.0", "--port", "8000"
    ])

    if not wait_for_url(FASTAPI_URL, "FastAPI"):
        fastapi_process.terminate()
        fastapi_process.wait()
        sys.exit(1)

    streamlit_process = start_process("STREAMLIT", [
        sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"
    ])

    if not wait_for_url(STREAMLIT_URL, "Streamlit"):
        shutdown([fastapi_process, streamlit_process])
        sys.exit(1)

    monitor_processes((fastapi_process, "FASTAPI"), (streamlit_process, "STREAMLIT"))

    webbrowser.open(STREAMLIT_OPEN_URL)
    print("Application started. Press Ctrl+C to stop.")

    try:
        while fastapi_process.poll() is None and streamlit_process.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown([fastapi_process, streamlit_process])


if __name__ == "__main__":
    main()