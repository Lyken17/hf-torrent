from main_hub import main

for repo in [
    "bert-base-uncased",
    "gpt2",
    "facebook/opt-350m",
    "NousResearch/Llama-2-13b-chat-hf",
    "NousResearch/Llama-2-13-hf",
    "NousResearch/Llama-2-7b-chat-hf",
    "NousResearch/Llama-2-7b-hf",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/stable-diffusion-xl-1.0-tensorrt",
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    
]:
    main(repo=repo)