from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
import torch
from typing import Optional

# 检查是否支持 MPS
device = "mps" if torch.backends.mps.is_available() else "cpu"

MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"

# 优先从本地加载，如无则下载
def load_tokenizer(model_name: str) -> AutoTokenizer:
    try:
        return AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    except Exception:
        return AutoTokenizer.from_pretrained(model_name)

def load_model(model_name: str, device_map: Optional[str], dtype):
    try:
        return AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            dtype=dtype,
            local_files_only=True,
        )
    except Exception:
        return AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            dtype=dtype,
        )

# 初始化 tokenizer（本地优先）
tokenizer = load_tokenizer(MODEL_NAME)

model = load_model(
    MODEL_NAME,
    device_map=device,
    dtype=torch.float16,
)

generator = pipeline(
    "text-generation", 
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)


# 构建提示文本
prompt = "The weather is nice today, so I decided to"

# 生成回复
response = generator(prompt)
print(response[0]['generated_text'])
