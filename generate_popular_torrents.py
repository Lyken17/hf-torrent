import argparse
import json, yaml
from main_hub import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="HF-Torrent creator",
    )
    parser.add_argument("-r", "--repo", default=None, type=str, help="Repo name")
    args = parser.parse_args()

    if args.repo is not None:
        if args.repo.endswith(".yaml"):
            with open(args.repo, "r") as f:
                yaml_info = yaml.load(f, Loader=yaml.FullLoader)
                repos = yaml_info["repos"]
            for repo in repos:
                main(repo=repo)
        else:
            main(repo=args.repo)
    else:
        with open("configs/popular-models.yaml", "r") as f:
            yaml_info = yaml.load(f, Loader=yaml.FullLoader)
            repos = yaml_info["repos"]
        with open("configs/popular-repos-crawled.yaml", "r") as f:
            yaml_info = yaml.load(f, Loader=yaml.FullLoader)
            for repo in yaml_info["repos"]:
                repos.append(repo)

        with open("configs/skipped-repos.yaml", "r") as f:
            yaml_info = yaml.load(f, Loader=yaml.FullLoader)

        repos = sorted(list(set(repos)))
        
        for repo in repos:
            if repo in yaml_info["repo"]:
                continue
            print(repo)
            main(repo=repo, delete_existing=True)
