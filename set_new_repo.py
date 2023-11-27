import os, sys, os.path as osp
import subprocess
import json

import utils
from utils import run_command

url = "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"

if url[-1] == "/":
    url = url[:-1]

rel_fpath = "/".join(url.strip().split("/")[-2:])
repo_name = url.strip().split("/")[-1]
fpath = osp.join(utils.REPO_BASE_DIR, rel_fpath)

if osp.exists(fpath):
    cmd = f"cd {fpath}; git pull"
    print(cmd)
    run_command(cmd)
else:
    dirpath = osp.dirname(fpath)
    print(dirpath)
    os.makedirs(dirpath, exist_ok=True)
    cmd = f"cd {dirpath}; git clone {url} {repo_name}"
    print(cmd)
    run_command(cmd)