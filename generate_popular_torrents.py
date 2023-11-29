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
        for repo in [
            "bert-base-uncased",
            "gpt2",
            "microsoft/resnet-50",
            "facebook/opt-125m",
            "facebook/opt-350m",
            "NousResearch/Llama-2-13b-chat-hf",
            "NousResearch/Llama-2-13b-hf",
            "NousResearch/Llama-2-7b-chat-hf",
            "NousResearch/Llama-2-7b-hf",
            "stabilityai/stable-diffusion-xl-base-1.0",
            "stabilityai/stable-diffusion-xl-1.0-tensorrt",
            "stabilityai/stable-diffusion-xl-refiner-1.0",
        ]:
            main(repo=repo)
