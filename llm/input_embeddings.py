import torch
from pathlib import Path

from dataloader import create_dataloader

vocab_size = 50257
output_dim = 256

# 实例化一个嵌入层
token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

#打印嵌入层的底层权重矩阵
print("The weight of token embedding layer:\n", token_embedding_layer.weight)

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "the-verdict.txt"
with open(str(data_path), "r", encoding="utf-8") as f:
    raw_text = f.read()

max_length = 4
dataloader = create_dataloader(raw_text, batch_size = 8, max_length = max_length, stride = max_length, shuffle=False)
data_iter = iter(dataloader)
inputs, targets = next(data_iter)

print("Inputs:\n", inputs)
print("Inputs shape:\n", inputs.shape)

token_embeddings = token_embedding_layer(inputs)
print("Token embeddings:\n", token_embeddings)
print("Token embeddings shape:\n", token_embeddings.shape)

context_length = max_length
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
pos_embeddings = pos_embedding_layer(torch.arange(context_length))
print("Positional embeddings:\n", pos_embeddings)
print("Positional embeddings shape:\n", pos_embeddings.shape)

input_embeddings = token_embeddings + pos_embeddings
print("Input embeddings:\n", input_embeddings)
print("Input embeddings shape:\n", input_embeddings.shape)