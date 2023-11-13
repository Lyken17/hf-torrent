import os, sys, os.path as osp
import subprocess


def run_command(cmd):
    out = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = out.stdout.decode()
    stderr = out.stderr.decode()
    return stdout, stderr


def enumerate_hf_repo(folder_base="bert-base-uncased"):
    exclude = set(
        [
            f"{folder_base}/.git",
        ]
    )
    for root, dirs, files in os.walk(f"{folder_base}", topdown=False):
        # print(dirs)
        dirs[:] = [d for d in dirs if d not in exclude]
        # [dirs.remove(d) for d in list(dirs) if d in exclude]
        for name in files:
            if root.startswith(f"{folder_base}/.git"):
                continue
            if name.startswith(".DS_Store"):
                continue
            yield osp.join(root, name)


repo = "bert-base-uncased"
if len(sys.argv) >= 2:
    repo = sys.argv[-1]
if repo[-1] == "/":
    repo = repo[:-1]
print(repo)

FORMAT_NAME = lambda s: s.replace("-", "_").replace("/", "-")

for fpath in enumerate_hf_repo(folder_base=repo):
    # folder = fpath.split("/")[0]
    # rel_path = "/".join(fpath.split("/")[1:])
    folder = repo
    rel_path = fpath.replace(repo, "")[1:]
    print("DEBUG:", fpath, folder, rel_path)
    cmd = f"cd {folder}; git log --format=format:%H {rel_path}"
    stdout, stderr = run_command(cmd)
    print(folder, rel_path, "git id: ", stdout)

    sha1 = stdout.strip().split()[0]

    torrent_name = FORMAT_NAME(rel_path)
    repo_name = FORMAT_NAME(repo)
    torrent_path = osp.join("torrent", rel_path) + ".torrent"
    os.makedirs(osp.dirname(torrent_path), exist_ok=True)
    cmd = f"python py3createtorrent.py -t best5 {osp.join(folder, rel_path)} \
            --name '{repo_name}-{sha1}-{torrent_name}' \
            --webseed https://huggingface.co/{repo}/resolve/{sha1}/{rel_path} \
            --webseed https://hf-mirror.com/{repo}/resolve/{sha1}/{rel_path} \
            --output {torrent_path} --force"
    stdout, stderr = run_command(cmd)
    print(stdout, stderr)
    print(cmd)
    print("--" * 50)

    # exit(0)
