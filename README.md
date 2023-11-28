## HF-Torrent

This repo contains experimental torrent-style download for model weights in huggingface.

The core implementation is `main_hub.py`, which downloads file from huggingface and convert them to seedable torrents.

## Installation

`pip install -r requirements.txt`

## How to use

First, make sure you have `aria2c` installed. Then, in a separate terminal

```bash
aria2c --enable-rpc --rpc-listen-all \
    --max-upload-limit=4M \
    --optimize-concurrent-downloads=true \
    --bt-detach-seed-only=true \
    --seed-ratio=10.0  \
    --daemon # remove this if you want observe the logs.
```

Next `pip install "aria2p[tui]"`. Then you are here to go.

```bash
python download.py <your target repo>
```


## How to contribute

* Seeding

    It is pretty much easy to join to contribe to seeding! First change `--seed-ratio=0` (from 10 to 0) when launching aria2c rpc, `0` means the daemon will seed infinitely. 
    Then change upload bandwidth limit to a value good to you `--max-upload-limit=20M` (4M by default.)

    Next, just as simple as download models. You can launch seeding via following scripts and help distributing your favorite models!

    ```bash
    python download.py <your target repo>
    ```

* Create 

    ```python generate_popular_torrents.py -r efederici/retnet-120m```

    This script will start (1) download model files from huggingface (2) iterate the folder (3) generate torrents for each file and then put under `hf-torrent-store/{repo}`.

    We are seeking for a wanted model list. Please file up an issue if you have favorite models to be shared.


