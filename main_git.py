import os, sys, os.path as osp
import json

from hf_torrent.utils import run_command


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


def main(args):
    # repo = "bert-base-uncased"
    # if len(sys.argv) >= 2:
    #     repo = sys.argv[-1]
    repo = args.repo

    if repo[-1] == "/":
        repo = repo[:-1]

    print(repo)
    FORMAT_NAME = lambda s: s.replace("-", "_").replace("/", "-")

    fpath_mapping = {}
    fpath_mapping["fpath2uuid"] = {}
    fpath_mapping["uuid2fpath"] = {}

    # Create torrents for single-file
    for fpath in enumerate_hf_repo(folder_base=repo):
        # folder = fpath.split("/")[0]
        # rel_path = "/".join(fpath.split("/")[1:])
        folder = repo
        fname = fpath.replace(repo, "")[1:]
        # print("DEBUG:", fpath, folder, fname)
        cmd = f"cd {folder}; git log --format=format:%H {fname}"
        stdout, stderr = run_command(cmd)

        sha1_list = stdout.strip().split()
        sha1 = sha1_list[0]

        print(fpath, "git id: ", sha1_list)

        torrent_name = FORMAT_NAME(fname)
        repo_name = FORMAT_NAME(repo)

        rel_fpath = osp.relpath(fpath, REPO_BASE_DIR)
        rel_rpath = osp.relpath(repo, REPO_BASE_DIR)
        # print(rel_fpath, rel_rpath)
        # new_fpath = osp.join("torrent", rel_fpath)
        # torrent_path = new_fpath + ".torrent"

        uuid = f"{repo_name}-{torrent_name}-{sha1}"

        torrent_path = osp.join(TORRENT_BASE_DIR, rel_rpath, f"{uuid}.torrent")
        os.makedirs(osp.dirname(torrent_path), exist_ok=True)

        cmd = f"python py3createtorrent.py -t best5 {osp.join(folder, fname)} \
                --name '{uuid}' \
                --webseed https://huggingface.co/{repo}/resolve/{sha1}/{fname} \
                --webseed https://hf-mirror.com/{repo}/resolve/{sha1}/{fname} \
                --output {torrent_path} --force"
        stdout, stderr = run_command(cmd)
        print(stdout, stderr)
        print(cmd)
        print("--" * 50)

        fpath_mapping["fpath2uuid"][rel_fpath] = f"{uuid}"
        fpath_mapping["uuid2fpath"][f"{uuid}"] = rel_fpath
        # exit(0)

    # Create torrents for folder

    with open(
        osp.join(TORRENT_BASE_DIR, rel_rpath, "_hf_mirror_torrent.json"), "w"
    ) as fp:
        json.dump(fpath_mapping, fp, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="HF Torrent Creator")
    parser.add_argument("repo")  # positional argument
    args = parser.parse_args()
    main(args)
