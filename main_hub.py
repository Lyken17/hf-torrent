import os, sys, os.path as osp
import json
from utils import run_command, FORMAT_NAME

def FORMAT_NAME(s): 
    return s.replace("-", "_").replace("/", "-")

def enumerate_hf_repo(folder_base="bert-base-uncased"):
    exclude = set(
        [
            f"{folder_base}/.git",
        ]
    )
    for root, dirs, files in os.walk(f"{folder_base}", topdown=False):
        # print(dirs)
        # TODO: add more ignore files
        dirs[:] = [d for d in dirs if d not in exclude]
        # [dirs.remove(d) for d in list(dirs) if d in exclude]
        for name in files:
            if root.startswith(f"{folder_base}/.git"):
                continue
            if name.startswith(".DS_Store"):
                continue
            yield osp.join(root, name)


REPO_BASE_DIR = "hf-repository"
TORRENT_BASE_DIR = "hf-torrent-store"


def main(repo = "stabilityai/stable-diffusion-xl-base-1.0"):
    FORMAT_NAME = lambda s: s.replace("-", "_").replace("/", "-")
    
    from huggingface_hub import snapshot_download
    
    model_fpath = snapshot_download(repo)
    hf_cache_base = osp.dirname(osp.dirname(model_fpath))
    
    fpath_mapping = {}
    fpath_mapping["fpath2uuid"] = {}
    fpath_mapping["uuid2fpath"] = {}
    
    for fpath in enumerate_hf_repo(model_fpath):
        print("--" * 50)
        file_name = osp.relpath(fpath, model_fpath)
        file_hash = osp.basename(osp.realpath(fpath))
        repo_name = FORMAT_NAME(repo)
        torrent_name = FORMAT_NAME(file_name)
        
        print(repo_name, "\t", torrent_name, "\t", file_hash)

        uuid = f"{repo_name}-{torrent_name}-{file_hash}"
        
        torrent_path = osp.join(TORRENT_BASE_DIR, repo, f"{uuid}.torrent")
        os.makedirs(osp.dirname(torrent_path), exist_ok=True)
        
        cmd = f"python py3createtorrent.py -t best5 {fpath} \
                --name '{uuid}' \
                --webseed https://huggingface.co/{repo}/resolve/{file_hash}/{file_name} \
                --webseed https://hf-mirror.com/{repo}/resolve/{file_hash}/{file_name} \
                --output {torrent_path} --force"
        stdout, stderr = run_command(cmd)
        print(stdout, stderr)
        print(cmd)
        print("--" * 50)

        rel_fpath = osp.relpath(fpath, model_fpath)
        fpath_mapping["fpath2uuid"][rel_fpath] = f"{uuid}"
        fpath_mapping["uuid2fpath"][f"{uuid}"] = rel_fpath
    
    with open(
        osp.join(TORRENT_BASE_DIR, repo, "_hf_mirror_torrent.json"), "w"
    ) as fp:
        json.dump(fpath_mapping, fp, indent=2)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(prog='HF Torrent Creator')
    parser.add_argument('repo')       # positional argument
    args = parser.parse_args()
    main()
