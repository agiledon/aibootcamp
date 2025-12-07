import torch
from torch.utils.data import Dataset, DataLoader
import tiktoken
from pathlib import Path

class GPTDataset(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        # 对传入的文本进行分词
        token_ids = tokenizer.encode(txt) 

        # 遍历所有可能的输入和目标序列
        for i in range(0, len(token_ids) - max_length, stride): 
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1:i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]
    

def create_dataloader(txt, batch_size = 4, max_length = 256,
                         stride = 256, shuffle = True, drop_last = True, num_workers = 0):
    tokenizer = tiktoken.get_encoding("gpt2")
    dataset = GPTDataset(txt, tokenizer, max_length, stride) 
    return DataLoader(dataset, 
                      batch_size = batch_size, 
                      shuffle = shuffle, 
                      drop_last = drop_last, 
                      num_workers = num_workers)


base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "the-verdict.txt"
with open(str(data_path), "r", encoding="utf-8") as f:
    raw_text = f.read()
data_loader = create_dataloader(raw_text, batch_size = 8, max_length = 4, stride = 4, shuffle=False)
data_iter = iter(data_loader)
inputs, targetx = next(data_iter)
print("Inputs:\n", inputs)
print("Targets:\n", targetx)