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

    import json, yaml
    if response.status_code == 200:
        with open("popular-repos-crawled.yaml", "r") as f:
            repos = yaml.load(f, Loader=yaml.FullLoader)["repos"]
        models = response.json()
        for model in models:
            print(model["id"])
            repos.append(model["id"])
        repos = sorted(list(set(repos)))
        with open("popular-repos-crawled.yaml", "w") as f:
            yaml.dump({"repos": repos}, f, default_flow_style=False)
    else:
        print(f"Failed to retrieve models. Status code: {response.status_code}")
