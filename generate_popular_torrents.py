import argparse
from main_hub import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="HF-Torrent creator",
    )
    parser.add_argument("-r", "--repo", default=None)
    args = parser.parse_args()

    if args.repo is not None:
        main(repo=args.repo)
    else:
        import json, yaml

        with open("popular-models.yaml", "r") as f:
            yaml_info = yaml.load(f, Loader=yaml.FullLoader)
            repos = yaml_info["repos"]
        with open("popular-repos-crawled.yaml", "r") as f:
            yaml_info = yaml.load(f, Loader=yaml.FullLoader)
            for repo in yaml_info["repos"]:
                if repo in yaml_info["_skipped"]:
                    continue
                repos.append(repo)

        repos = list(set(repos))
        for repo in repos:
            print(repo)
            main(repo=repo, delete_existing=True)
