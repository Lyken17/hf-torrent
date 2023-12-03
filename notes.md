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

Create tensor (single file)
```
python py3createtorrent.py -t best5 bert-base-uncased/model.safetensors --webseed https://huggingface.co/bert-base-uncased/resolve/main/model.safetensors
```

Create tensor (folder)
python py3createtorrent.py -t best5 \
    $HOME/.cache/huggingface/hub/models--bert-base-uncased/snapshots/1dbc166cf8765166998eff31ade2eb64c8a40076  \
    --output bert-base-uncased.torrent \
    --name 1dbc166cf8765166998eff31ade2eb64c8a40076 --webseed https://huggingface.co/bert-base-uncased/resolve/


https://hf-mirror.com/u/1dbc166cf8765166998eff31ade2eb64c8a40076/models/bert-base-uncased/d/README.md