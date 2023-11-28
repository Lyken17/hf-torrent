## HF-Torrent

This repo contains experimental torrent-style download for model weights in huggingface.

The core implementation is `main_hub.py`, which downloads file from huggingface and convert them to seedable torrents.

## How to use

* Create 

    ```python generate_popular_torrents.py -r efederici/retnet-120m```

    This script will start (1) download model files from huggingface (2) iterate the folder (3) generate torrents for each file and then put under `hf-torrent-store/{repo}`.

* Download (WIP)

    ```python download.py -r microsoft/resnet-50```


* Seeding (WIP)


