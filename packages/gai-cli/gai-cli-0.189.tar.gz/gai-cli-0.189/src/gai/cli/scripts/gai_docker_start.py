import os
import subprocess
def docker_start(here):
    try:
        docker_compose_path = os.path.join(here,"docker-compose.yml")
        print("docker-compose:",docker_compose_path)
        docker_command = f"docker-compose -f {docker_compose_path} up -d --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")