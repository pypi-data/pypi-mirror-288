import os
import subprocess
def docker_start(here):
    try:
        docker_command = f"docker-compose up -d --build --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")