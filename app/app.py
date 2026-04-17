from flask import Flask, request
import time
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running!"

# CPU stress endpoint
@app.route("/cpu")
def cpu_stress():
    duration = int(request.args.get("duration", 10))

    def burn_cpu():
        end_time = time.time() + duration
        while time.time() < end_time:
            pass  # tight loop = CPU usage

    thread = threading.Thread(target=burn_cpu)
    thread.start()

    return f"CPU stress started for {duration} seconds\n"

# Memory stress endpoint
memory_holder = []

@app.route("/memory")
def memory_stress():
    size_mb = int(request.args.get("size", 100))
    memory_holder.append(" " * (size_mb * 1024 * 1024))
    return f"Allocated {size_mb} MB memory\n"

@app.route("/health")
def health():
    return "OK"

# New endpoint for ConfigMap data
@app.route("/config")
def config():
    config_value = os.getenv('APP_CONFIG', 'default_config')
    return f"Config value: {config_value}\n"

# New endpoint for Secret data
@app.route("/secret")
def secret():
    try:
        with open('/mnt/secrets/secret.txt', 'r') as f:
            secret_value = f.read().strip()
        return f"Secret value: {secret_value}\n"
    except FileNotFoundError:
        return "Secret file not found\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)