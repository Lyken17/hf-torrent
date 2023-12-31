import time
import datetime
import os, os.path as osp
import subprocess
import json
import argparse
import fire


def run():
    parser = argparse.ArgumentParser()
    # facebook/opt-125m
    parser.add_argument("repo", type=str, nargs="?")
    parser.add_argument("--get-torrent", action="store_true", default=False)
    parser.add_argument("--hf-models", type=str, default="~/.cache/hf-torrent/downloads")
    parser.add_argument(
        "--download-folder", type=str, default="hf-torrent-models"
    )
    args = parser.parse_args()
    from hf_torrent.download import main as download_main

    download_main(args.repo, args.hf_models, args.download_folder, args.get_torrent)


if __name__ == "__main__":
    run()
