import os
import subprocess

def docker_stop(here):
    try:
        docker_command = f"docker-compose down -v --remove-orphans"
        result=subprocess.run(docker_command, shell=True, check=True, capture_output=True)
        # Print stdout and stderr for debugging
        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())
        print("Containers and associated resources have been forcefully shut down and removed.")        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")