import os
from transformers import AutoTokenizer
from datasets import load_dataset, load_from_disk

# 设置本地缓存目录
CACHE_DIR = "./cache"
MODEL_CACHE_DIR = os.path.join(CACHE_DIR, "models")
DATASET_CACHE_DIR = os.path.join(CACHE_DIR, "datasets")

# 创建缓存目录
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(DATASET_CACHE_DIR, exist_ok=True)

def load_tokenizer_with_cache(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    """加载分词器，优先从本地缓存加载"""
    model_path = os.path.join(MODEL_CACHE_DIR, model_name.replace("/", "--"))
    
    if os.path.exists(model_path):
        print(f"从本地缓存加载模型: {model_path}")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
    else:
        print(f"从HuggingFace下载模型: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=MODEL_CACHE_DIR
        )
        # 保存到本地缓存
        tokenizer.save_pretrained(model_path)
        print(f"模型已保存到本地缓存: {model_path}")
    
    return tokenizer

def load_dataset_with_cache(dataset_name="HuggingFaceH4/ultrachat_200k", split="test_sft"):
    """加载数据集，优先从本地缓存加载"""
    dataset_path = os.path.join(DATASET_CACHE_DIR, dataset_name.replace("/", "--"))
    
    if os.path.exists(dataset_path):
        print(f"从本地缓存加载数据集: {dataset_path}")
        dataset = load_from_disk(dataset_path)
    else:
        print(f"从HuggingFace下载数据集: {dataset_name}")
        dataset = load_dataset(
            dataset_name, 
            split=split,
            cache_dir=DATASET_CACHE_DIR
        )
        # 保存到本地缓存
        dataset.save_to_disk(dataset_path)
        print(f"数据集已保存到本地缓存: {dataset_path}")
    
    return dataset

def format_prompt(example, tokenizer):
    """利用TinyLlama使用的<|user|>模板格式化提示词"""
    # 格式化回答
    chat = example["messages"]
    prompt = tokenizer.apply_chat_template(chat, tokenize=False)
    return {"text": prompt}

# 加载分词器
template_tokenizer = load_tokenizer_with_cache()

# 加载数据并利用TinyLlama使用的模板进行格式化
dataset = load_dataset_with_cache()
dataset = (
    dataset
    .shuffle(seed=42)
    .select(range(3_000))
)
dataset = dataset.map(lambda x: format_prompt(x, template_tokenizer))

# 格式化后的提示词示例
print("格式化后的提示词示例:")
print(dataset["text"][2576])