import tiktoken
from pathlib import Path

tokenizer = tiktoken.get_encoding("gpt2")

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "the-verdict.txt"
with open(str(data_path), "r", encoding="utf-8") as f:
    raw_text = f.read()

enc_text = tokenizer.encode(raw_text)
enc_sample = enc_text[50:]

context_size = 4 # 上下文大小决定了输入中包含多少个token
x = enc_sample[:context_size] # x存储输入的词元
y = enc_sample[1:context_size + 1] # y存储由x的每个输入词元右移一个位置所得的目标词元

print(f"x: {x}")
print(f"y:     {y}")

for i in range(1, context_size + 1):
    context = enc_sample[:i]
    desired = enc_sample[i]

    print(f"{context} ----> {desired}")
    print(f"{tokenizer.decode(context)} ----> {tokenizer.decode([desired])}")