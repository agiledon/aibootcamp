import matplotlib.pyplot as plt
import torch
import tiktoken
from pathlib import Path
from gpt_model import GPTModel
from gpt_model import generate_text_simple
from gpt_model import generate
import sys
sys.path.append('..')
from dataloader import create_dataloader
from gpt_config import GPT_CONFIG_124M

def main():
    model = GPTModel(GPT_CONFIG_124M)
    model.load_state_dict(torch.load("model.pth", weights_only=True))

    start_context = "Hello, I am"
    tokenizer = tiktoken.get_encoding("gpt2")
    encoded = tokenizer.encode(start_context)
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)
    # out = generate_text_simple(
    #     model=model,
    #     idx=encoded_tensor,
    #     max_new_tokens=10,
    #     context_size=GPT_CONFIG_124M["context_length"]
    # )
    out = generate(
        model=model,
        idx=encoded_tensor,
        max_new_tokens=10,
        context_size=GPT_CONFIG_124M["context_length"],
        temperature=0.8,
        top_k=40,
    )
    decoded_text = tokenizer.decode(out.squeeze(0).tolist())

    print(f"\n\n{50*'='}\n{22*' '}OUT\n{50*'='}")
    print("\nOutput:", out)
    print("Output length:", len(out[0]))
    print("Output text:", decoded_text)

if __name__ == "__main__":
    main()