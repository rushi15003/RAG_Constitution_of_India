import subprocess
import time

CONTAINER_NAME = "lucid_wu"

def start_qdrant_container():
    try:
        # Check if Docker is available
        docker_check = subprocess.run(
            ["docker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if docker_check.returncode != 0:
            print(f"❌ Docker is not available: {docker_check.stderr}")
            return

        # Check if container exists
        exists_check = subprocess.run(
            ["docker", "container", "inspect", CONTAINER_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if exists_check.returncode != 0:
            print(f"❌ Container '{CONTAINER_NAME}' doesn't exist. Please create it first using docker run.")
            return

        # Check if container is running
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"name={CONTAINER_NAME}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.stdout.strip() == "":
            print(f"🚀 Qdrant container '{CONTAINER_NAME}' is not running. Starting it...")
            start_result = subprocess.run(
                ["docker", "start", CONTAINER_NAME],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if start_result.returncode == 0:
                print(f"✅ Container '{CONTAINER_NAME}' started.")
                time.sleep(5)
            else:
                print(f"❌ Failed to start container '{CONTAINER_NAME}': {start_result.stderr}")
        else:
            print(f"✅ Qdrant container '{CONTAINER_NAME}' is already running.")

    except Exception as e:
        print("❌ Error while starting Qdrant container:", e)

if __name__ == "__main__":
    start_qdrant_container()