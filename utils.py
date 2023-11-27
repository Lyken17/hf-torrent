import subprocess

REPO_BASE_DIR = "hf-repository"
TORRENT_BASE_DIR = "hf-torrent-store"


def run_command(cmd):
    out = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = out.stdout.decode()
    stderr = out.stderr.decode()
    return stdout, stderr
