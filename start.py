import subprocess
import sys
import time
import webbrowser

print("=" * 50)
print(" Office Environment Monitor")
print("=" * 50)

print("Starting Flask server...")
flask = subprocess.Popen([sys.executable, "app.py"])

time.sleep(3)

print("Starting data logger...")
logger = subprocess.Popen([sys.executable, "logger.py"])

print("Opening dashboard...")
webbrowser.open("http://localhost:5000")

print()
print("System is running!")
print("Dashboard: http://localhost:5000")
print("Press Ctrl+C to stop everything.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping services...")

    flask.terminate()
    logger.terminate()

    flask.wait()
    logger.wait()

    print("Shutdown complete.")