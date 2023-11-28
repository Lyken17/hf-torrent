import os, sys, os.path as osp
import subprocess
import json
from utils import enumerate_hf_repo

import aria2p

# initialization, these are the default values
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
"hf-torrent-store/microsoft/resnet-50"
repo_name = "gpt2"

BASE_FOLDER = "hf-torrent-store"
HF_FOLDER = "hf-files"
repo_folder = osp.join(BASE_FOLDER, repo_name)
meta = json.load(open(osp.join(repo_folder, "_hf_mirror_torrent.json"), "r"))

from pprint import pprint

[_.remove() for _ in aria2.get_downloads() if _.status == "error"]
# [_.remove() for _ in aria2.get_downloads() ]
# pprint(meta)

os.makedirs(osp.join(HF_FOLDER, BASE_FOLDER), exist_ok=True)
for fpath, uuid in meta["fpath2uuid"].items():
    torrent_path = osp.join(repo_folder, f"{uuid}.torrent")
    print(f"Adding {torrent_path}")

    aria2.add_torrent(
        torrent_path,
        options={
            "follow-torrent": "true",
            "check-integrity": "true",
            "dir": osp.join(HF_FOLDER, repo_name),
        },
    )

# for enumerate_hf_repo()
