import argparse
from main_hub import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="HF-Torrent creator",
    )
    parser.add_argument("-r-", "--repo", default=None)
    args = parser.parse_args()
    
    if args.repo is not None:
        main(repo=args.repo)
    else:
        import json
        with open("popular_repos.json", "r") as f:
            repos = json.load(f)
        with open("popular_repos_crawled.json", "r") as f:
            repos += json.load(f)
        repos = list(set(repos))
        for repo in repos:
            main(repo=repo)
