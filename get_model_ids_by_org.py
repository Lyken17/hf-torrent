import requests
import os

organization_name = "facebook"
api_token = os.environ["HF_API_TOKEN"]

for org in [
    "facebook",
    "Intel",
    "microsoft",
    "stabilityai",
    "runwayml",
    "deepseek-ai",
    "Qwen",
    "fnlp",
    "THUDM",
    "openchat",
    "openai",
    "mistralai",
    "latent-consistency",
]:
    response = requests.get(
        "https://huggingface.co/api/models",
        params={
            "author": org,
            "sort": "likes",
            "direction": "-1",
            "limit": "10",
            "full": "True",
            "config": "True",
        },
        headers={"Authorization": f"Bearer {api_token}"},
    )

    import json
    if response.status_code == 200:
        with open("popular_repos_crawled.json", "r") as f:
            repos = json.load(f)
        models = response.json()
        for model in models:
            print(model["id"])
            repos.append(model["id"])
        repos = list(set(repos))
        with open("popular_repos_crawled.json", "w") as f:
            json.dump(repos, f, indent=2)
    else:
        print(f"Failed to retrieve models. Status code: {response.status_code}")
