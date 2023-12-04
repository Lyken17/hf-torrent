import time
import datetime
import os, os.path as osp
import subprocess
import json
import argparse
import fire

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=str, nargs="?", default="facebook/opt-125m")
    parser.add_argument("--hf-models", type=str, default="hf-models")
    parser.add_argument("--download", type=str, default="~/.cache/hf-torrent-downloads")
    parser.add_argument("--debug", type=str, default="~/.cache/hf-torrent-downloads")
    args = parser.parse_args()
    from hf_torrent.download import main as download_main
    download_main(args.repo, args.hf_models, args.download)

if __name__ == '__main__':
    run()