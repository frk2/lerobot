import modal

# how to run:
# modal run modal_deploy.py
# modal run --detach modal_deploy.py

image = (
    modal.Image.from_registry("nvidia/cuda:12.2.0-devel-ubuntu22.04", add_python="3.11")
    .pip_install("transformers","pytest")
    .apt_install("software-properties-common")
    .run_commands("add-apt-repository -y ppa:ubuntuhandbook1/ffmpeg7")
    .run_commands("apt update")
    .apt_install("ffmpeg", "build-essential", "clang")
    .pip_install_from_pyproject("pyproject.toml")
    .pip_install("opencv-python-headless")
    .pip_install("huggingface_hub")
    .add_local_python_source("lerobot")
    

)

app = modal.App(name="lerobot-train", image=image)

@app.function(gpu="A100-80GB", volumes={"/out": modal.Volume.from_name("lerobot")}, timeout=86400)
def train_lerobot():
    import subprocess
    command = [
        "python", "lerobot/scripts/train.py",
        f"--dataset.repo_id=frk2/smallactionspace",
        "--policy.path=lerobot/pi0",
        "--output_dir=/out/smallactionspace",
        "--job_name=pi0small_env",
        "--policy.device=cuda",
        # "--wandb.enable=true"
    ]

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as process:
        for line in process.stdout:
            print(line, end='')  # Print each line as it is received
        process.wait()  # Wait for the process to complete




@app.local_entrypoint()
def main():
    return train_lerobot.remote()
