## HF-Torrent

This repository contains an experimental torrent-style download for model weights in Hugging Face.

The core implementation is `main_hub.py`, which downloads files from Hugging Face and converts them into seedable torrents.

## How to use

`pip install hf-torrent`

Before launching downloads, make sure you have [aria2c](https://aria2.github.io/) installed and 

<details>
<summary>  run the following command in a separate terminal </summary>

```bash
aria2c --enable-rpc --rpc-listen-all \
    --max-upload-limit=4M \
    --optimize-concurrent-downloads=true \
    --bt-detach-seed-only=true \
    --seed-ratio=10.0  
```
</details>


Then you can start using HF-Torrent with the following command:

```bash
hf-torrent <your target repo>
```

[![asciicast](https://asciinema.org/a/4ppEU7HDGzUqwReSIosXOkCs9.svg)](https://asciinema.org/a/4ppEU7HDGzUqwReSIosXOkCs9)


Or if you have your preferred torrent clients, you can pull the torrent file only

```bash
hf-torrent --get-torrent <your target repo>
```


## How to contribute

### Installation

To install, run the following command:

`pip install -r requirements.txt`


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