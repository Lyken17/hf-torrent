## HF-Torrent

This repository contains an experimental torrent-style download for model weights in Hugging Face.

The core implementation is `main_hub.py`, which downloads files from Hugging Face and converts them into seedable torrents.

## Installation

To install, run the following command:

`pip install -r requirements.txt`

## How to use

Before using HF-Torrent, make sure you have [aria2c](https://aria2.github.io/) installed. Then, in a separate terminal, run the following command:

```bash
aria2c --enable-rpc --rpc-listen-all \
    --max-upload-limit=4M \
    --optimize-concurrent-downloads=true \
    --bt-detach-seed-only=true \
    --seed-ratio=10.0  \
    --daemon # remove this if you want to observe the logs.

```

Next, install the `aria2p[tui]` package by running:

```bash
pip install "aria2p[tui]"

```

Once installed, you can start using HF-Torrent with the following command:

```bash
python download.py <your target repo>

```

## How to contribute

### Seeding

It is easy to contribute to seeding! First, change `--seed-ratio=0` (from 10 to 0) when launching the `aria2c` RPC. Setting `0` means the daemon will seed infinitely.
Next, change the upload bandwidth limit to a value that suits you, for example: `--max-upload-limit=20M` (4M by default).

After making these changes, launching seeding is as simple as downloading models. You can start seeding by running the following script and help distribute your favorite models!

```bash
python download.py <your target repo>

```

### Create

To create a popular torrent, run the following command:

`python generate_popular_torrents.py -r efederici/retnet-120m`

This script will (1) download model files from Hugging Face, (2) iterate through the folder, (3) generate torrents for each file, and then put them under `hf-torrent-store/{repo}`.

We are looking for a wanted model list. Please open an issue if you have any favorite models to share.