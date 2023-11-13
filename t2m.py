import sys
import bencodepy
import hashlib
import base64


def make_magnet_from_torrent(file):
    metadata = bencodepy.decode_from_file(file)
    # from pprint import pprint
    # for key in [b'announce', b'announce-list', b'created by', b'info']:
    # pprint(metadata[key])
    # print(metadata.keys())
    subj = metadata[b"info"]
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    sha1hash = hashlib.sha1(hashcontents).hexdigest()
    b32hash = base64.b32encode(digest).decode()
    # print(metadata[b'info'][b'name'].decode())
    # print(b'announce' not in metadata)
    
    chosen_hash = sha1hash
    if b"announce" not in metadata:
        magnet = (
            "magnet:?"
            + "xt=urn:btih:"
            + chosen_hash
            + "&dn="
            + metadata[b"info"][b"name"].decode()
        )
    else:
        magnet = (
            "magnet:?"
            + "xt=urn:btih:"
            + chosen_hash
            + "&dn="
            + metadata[b"info"][b"name"].decode()
            + "&tr="
            + metadata[b"announce"].decode()
        )
        # + '&xl=' + str(metadata[b'info'][b'length'])
    if b"url-list" in metadata:
        if not isinstance(metadata[b"url-list"], (tuple, list)):
            url_lists = metadata[b"url-list"].decode()
            url_lists = [
                url_lists,
            ]
        else:
            url_lists = [url.decode() for url in metadata[b"url-list"]]
        for url_list in url_lists:
            # webseeds
            addtion_xl = f"&ws={url_list}"
            # print(addtion_xl)
            magnet += addtion_xl
    return magnet


if __name__ == "__main__":
    import sys

    # magnet = make_magnet_from_torrent(sys.argv[1])
    import glob
    import os, os.path as osp

    # print('Number of arguments:', len(sys.argv), 'arguments.'
    # print('Argument List:', str(sys.argv))
    fpath = osp.join(sys.argv[1].strip())

    if osp.isfile(fpath) and fpath.endswith(".torrent"):
        magnet = make_magnet_from_torrent(fpath)
        print(magnet)
        exit(0)
    if osp.isdir(fpath):
        for root, dirs, files in os.walk(fpath, topdown=False):
            for name in files:
                fpath = osp.join(root, name)
                # print(fpath)
                if not fpath.endswith(".torrent"):
                    continue
                magnet = make_magnet_from_torrent(fpath)
                print(magnet)
