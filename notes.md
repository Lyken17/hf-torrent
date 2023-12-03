## HF folder structure
The new cache file layout looks like this:
- The cache directory contains one subfolder per repo_id (namespaced by repo type)
- inside each repo folder:
    - refs is a list of the latest known revision => commit_hash pairs
    - blobs contains the actual file blobs (identified by their git-sha or sha256, depending on
        whether they're LFS files or not)
    - snapshots contains one subfolder per commit, each "commit" contains the subset of the files
        that have been resolved at that particular commit. Each filename is a symlink to the blob
        at that particular commit.

## Git commit hash of specific file
Find the commit history of specific file

```
git log --format=format:%H <file>
```

Create tensor 
```
python py3createtorrent.py -t best5 bert-base-uncased/model.safetensors --webseed https://huggingface.co/bert-base-uncased/resolve/main/model.safetensors
```