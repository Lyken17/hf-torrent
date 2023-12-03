import os, sys, os.path as osp
import json

from utils import run_command, FORMAT_NAME, enumerate_hf_repo


REPO_BASE_DIR = "hf-repository"
TORRENT_BASE_DIR = "hf-torrent-store"


def main(repo="bert-base-uncased"):
    FORMAT_NAME = lambda s: s.replace("-", "_").replace("/", "-")

    from huggingface_hub import snapshot_download, hf_hub_url, get_hf_file_metadata

    model_fpath = snapshot_download(repo)
    hf_cache_base = osp.dirname(osp.dirname(model_fpath))

    fpath_mapping = {}
    fpath_mapping["fpath2uuid"] = {}
    fpath_mapping["uuid2fpath"] = {}

    # Create torrent for folder
    print("--" * 50)
    git_hash = osp.basename(model_fpath)
    """
    python py3createtorrent.py -t best5 \
        $HOME/.cache/huggingface/hub/models--bert-base-uncased/snapshots/1dbc166cf8765166998eff31ade2eb64c8a40076  \
        --output bert-base-uncased.torrent \
        --name 1dbc166cf8765166998eff31ade2eb64c8a40076 --webseed https://huggingface.co/bert-base-uncased/resolve/
    """
    torrent_path = osp.join(TORRENT_BASE_DIR, repo, f"_all.torrent")
    os.makedirs(osp.dirname(torrent_path), exist_ok=True)
    repo_name = FORMAT_NAME(repo)
    cmd = f"python py3createtorrent.py -t best5 {model_fpath} \
        --name '{git_hash}' \
        --webseed https://huggingface.co/{repo}/resolve/ \
        --webseed https://hf-mirror.com/{repo}/resolve/ \
        --output {torrent_path} --force"
    stdout, stderr = run_command(cmd)
    print(stdout, stderr)
    print(cmd)
    print("--" * 50)
    # Create torrent for single-file
    for fpath in enumerate_hf_repo(model_fpath):
        print("--" * 50)
        file_name = osp.relpath(fpath, model_fpath)
        etag_hash = osp.basename(osp.realpath(fpath))
        repo_name = FORMAT_NAME(repo)
        torrent_name = FORMAT_NAME(file_name)

        print(repo_name, "\t", torrent_name, "\t", etag_hash)

        uuid = f"{repo_name}-{torrent_name}-{etag_hash}"

        torrent_path = osp.join(TORRENT_BASE_DIR, repo, f"{uuid}.torrent")
        os.makedirs(osp.dirname(torrent_path), exist_ok=True)

        hf_meta = get_hf_file_metadata(hf_hub_url(repo_id=repo, filename=file_name))
        commit_hash = hf_meta.commit_hash

        rel_fpath = osp.relpath(fpath, model_fpath)
        fpath_mapping["fpath2uuid"][rel_fpath] = f"{uuid}"
        fpath_mapping["uuid2fpath"][f"{uuid}"] = rel_fpath

        if osp.exists(torrent_path):
            print(f"Skipping {torrent_path} as it already exists.")
            print("--" * 50)
            continue

        cmd = f"python py3createtorrent.py -t best5 {fpath} \
                --name '{uuid}' \
                --webseed https://huggingface.co/{repo}/resolve/{commit_hash}/{file_name} \
                --webseed https://hf-mirror.com/{repo}/resolve/{commit_hash}/{file_name} \
                --output {torrent_path} --force"
        stdout, stderr = run_command(cmd)
        print(stdout, stderr)
        print(cmd)
        print("--" * 50)

    with open(osp.join(TORRENT_BASE_DIR, repo, "_hf_mirror_torrent.json"), "w") as fp:
        json.dump(fpath_mapping, fp, indent=2)


if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(prog='HF Torrent Creator')
    # parser.add_argument('repo')       # positional argument
    # args = parser.parse_args()
    main()
