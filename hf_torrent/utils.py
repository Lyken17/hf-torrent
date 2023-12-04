import os, os.path as osp
import subprocess

REPO_BASE_DIR = "hf-repository"
TORRENT_BASE_DIR = "hf-torrent-store"


def download_fn(url, fpath):
    from huggingface_hub.file_download import http_get, _chmod_and_replace
    import tempfile
    from functools import partial

    if osp.exists(fpath):
        return fpath
    
    cache_dir = osp.dirname(".cache")
    temp_file_manager = partial(  # type: ignore
        tempfile.NamedTemporaryFile, mode="wb", dir=cache_dir, delete=False
    )

    with temp_file_manager() as temp_file:
        http_get(url, temp_file)
    os.makedirs(osp.dirname(fpath), exist_ok=True)
    _chmod_and_replace(temp_file.name, fpath)
    return fpath


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


def run_command(cmd):
    out = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = out.stdout.decode()
    stderr = out.stderr.decode()
    return stdout, stderr
