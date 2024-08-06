# requires pip install huggingface-hub
import os
from huggingface_hub import hf_hub_download,snapshot_download

from gai.lib.common.utils import get_app_path
from pathlib import Path

os.environ["HF_HUB_ENABLED_HF_TRANSFER"]="1"
import time
def pull(console, model_name):
    app_dir = get_app_path()
    if not model_name:
        console.print("[red]Model name not provided[/]")
        return
    if model_name == "exllamav2-mistral7b":
        start=time.time()
        console.print(f"[white]Downloading... {model_name}[/]")
        snapshot_download(
            repo_id="bartowski/Mistral-7B-Instruct-v0.3-exl2",
            local_dir=f"{app_dir}/models/exllamav2-mistral7b",
            revision="1a09a351a5fb5a356102bfca2d26507cdab11111",
            )
        #os.removedirs(Path("~/.cache/huggingface").expanduser())
        end=time.time()
        duration=end-start
        model_name="exllamav2-mistral7b"
        download_size=Path(f"{app_dir}/models/{model_name}").stat().st_size

        from rich.table import Table
        table = Table(title="Download Information")
        # Add columns
        table.add_column("Model Name", justify="left", style="bold yellow")
        table.add_column("Time Taken (s)", justify="right", style="bright_green")
        table.add_column("Size (Mb)", justify="right", style="bright_green")
        table.add_column("Location", justify="right", style="bright_green")

        # Add row with data
        table.add_row(model_name, f"{duration:4}", f"{download_size:2}", f"{app_dir}/models/{model_name}")

        # Print the table to the console
        console.print(table)        

    else:
        console.print(f"[red]Model {model_name} not found[/]")