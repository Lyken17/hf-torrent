import os, sys, os.path as osp
import time
import subprocess
import json
import argparse

import aria2p
from hf_torrent.utils import enumerate_hf_repo, download_fn, FORMAT_NAME


def main(
    repo,
    hf_models,
    download,
    get_torrent=False,
    BASE_FOLDER="https://raw.githubusercontent.com/Lyken17/hf-torrent-store/master",
    HF_FOLDER="hf-torrent-downloads",
    HF_MODELS="hf-models",
):
    repo_name = repo
    repo_folder = osp.join(BASE_FOLDER, repo_name)

    HF_MODELS = osp.realpath(osp.expanduser(hf_models))
    HF_FOLDER = osp.realpath(osp.expanduser(download))

    def load_remote_or_local_file(fpath, cache_dir="~/.cache/temp"):
        if fpath.startswith("http://") or fpath.startswith("https://"):
            return download_fn(
                fpath,
                osp.join(
                    osp.expanduser(cache_dir),
                    fpath.replace("https://", "").replace("http://", ""),
                ),
            )
        return fpath

    meta_fpath = osp.join(
        BASE_FOLDER,
        repo_name,
        "_hf_torrent.json",
    )
    meta = json.load(open(load_remote_or_local_file(meta_fpath), "r"))

    if get_torrent:
        print("Downloading torrent files")
        meta_fpath = osp.join(
            BASE_FOLDER,
            repo_name,
            "_all.torrent",
        )
        torrent_path = osp.realpath(
            FORMAT_NAME(repo_name) + f"-{meta['lastest-commit']}" + ".torrent"
        )
        return download_fn(meta_fpath, torrent_path)

    # initialization, these are the default values
    aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))

    print("Clean up error downloads")
    [_.remove() for _ in aria2.get_downloads() if _.status == "error"]

    downloading = {}

    for gid in aria2.get_downloads():
        uuid = gid.bittorrent.info["name"]
        downloading[uuid] = gid

    from queue import Queue

    gids = Queue()
    for fpath, uuid in meta["fpath2uuid"].items():
        torrent_path = load_remote_or_local_file(
            osp.join(BASE_FOLDER, repo_name, f"{uuid}.torrent")
        )
        if uuid in downloading:
            # print(f"Skipping {osp.basename(torrent_path)} as already downloadded.")
            gid = downloading[uuid]
        else:
            os.makedirs(osp.join(HF_FOLDER, repo_name), exist_ok=True)
            print(f"Adding {torrent_path}")
            gid = aria2.add_torrent(
                torrent_path,
                options={
                    "follow-torrent": "true",
                    "check-integrity": "true",
                    "dir": osp.join(HF_FOLDER, repo_name),
                },
            )
        gids.put(gid)
        # TODO: add scripts to ensure download is complete

    count = 0
    while not gids.empty():
        gid = aria2.get_download(gids.get().gid)

        if float(gid.progress) >= 100:
            print(f"Finish downloading {gid.bittorrent.info['name']}")
        else:
            assert (
                gid.status != "error"
            ), f"Error downloading {gid.bittorrent.info['name']}"
            gids.put(gid)
            count = (count + 1) % 10

            print(
                f"[{gid.progress_string()}] Waiting for {gid.bittorrent.info['name']} to finish downloading"
            )
            if count == 9:
                time.sleep(5)
                print("--" * 20, "Check backup in 5s", "--" * 20)

    print("All downloading finished. Now link files to hf-models folder")
    # Create sym-links
    for fpath, uuid in meta["fpath2uuid"].items():
        hf_weights_path = osp.join(HF_FOLDER, repo_name, f"{uuid}")
        hf_models_fpath = osp.join(HF_MODELS, repo_name, fpath)
        os.makedirs(osp.dirname(hf_models_fpath), exist_ok=True)
        if osp.exists(hf_models_fpath) or osp.islink(hf_models_fpath):
            # Override to ensure the link is correct
            os.remove(hf_models_fpath)
        os.symlink(osp.realpath(hf_weights_path), osp.realpath(hf_models_fpath))
        # print(f"Linking {hf_weights_path} ==> {hf_models_fpath}")

    print(
        f"""Now, you can use {repo_name} as in {osp.join(HF_MODELS, repo_name)}. For example    

        from transformers import AutoModelForCausalLM
        model = AutoModelForCausalLM.from_pretrained("{osp.join(HF_MODELS, repo_name)}")
        
    Note this assumes you are running LLMs. Change to other AutoClass when necessary.
    """
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, nargs="?", default="facebook/opt-125m")
    parser.add_argument("--hf-models", type=str, default="hf-models")
    parser.add_argument("--download", type=str, default="~/.cache/hf-torrent-downloads")
    args = parser.parse_args()
    main(args.repo, args.hf_models, args.download)
