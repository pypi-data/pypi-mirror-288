import os
import subprocess
def docker_start(here):
    try:
        print("here:",here)
        docker_command = f"docker-compose -f {os.join(here,"docker-compose.yml")} up -d --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")