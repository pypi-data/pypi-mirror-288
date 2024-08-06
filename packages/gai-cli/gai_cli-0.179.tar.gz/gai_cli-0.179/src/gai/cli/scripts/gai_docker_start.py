import os
import subprocess
def docker_start(here):
    try:
        dest = os.path.join(here,"../../../.vscode")
        docker_command = f"cd {dest} && docker-compose up -d --build --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")