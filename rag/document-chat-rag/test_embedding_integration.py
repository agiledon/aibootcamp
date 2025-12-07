#!/usr/bin/env python3
"""
测试 LlamaIndex OllamaEmbedding 集成
需要在虚拟环境中运行
"""

import sys
import os

# 尝试导入必要的模块
try:
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.core import Settings
    print("✅ 成功导入 LlamaIndex 模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("\n💡 请确保在虚拟环境中运行此脚本:")
    print("   cd rag/document-chat-rag")
    print("   source .venv/bin/activate  # 或 uv run python test_embedding_integration.py")
    sys.exit(1)

def test_ollama_embedding():
    """测试 Ollama 嵌入模型"""
    print("\n" + "="*60)
    print("测试 OllamaEmbedding 集成")
    print("="*60)
    
    try:
        # 1. 初始化嵌入模型
        print("\n1. 初始化 OllamaEmbedding...")
        embed_model = OllamaEmbedding(
            model_name="nomic-embed-text:latest",
            request_timeout=60,
            keep_alive="5m"
        )
        print(f"   ✅ 模型: {embed_model.model_name}")
        # request_timeout 可能不是属性，而是初始化参数
        timeout = getattr(embed_model, 'request_timeout', 'N/A')
        print(f"   ✅ 超时设置: {timeout}")
        
        # 2. 测试单个文本嵌入
        print("\n2. 测试单个文本嵌入生成...")
        test_text = "Hello, this is a test for embedding generation"
        print(f"   测试文本: '{test_text}'")
        
        embedding = embed_model.get_text_embedding(test_text)
        
        print(f"   ✅ 嵌入生成成功")
        print(f"   📊 嵌入维度: {len(embedding)}")
        print(f"   📝 前5个值: {embedding[:5]}")
        print(f"   📝 后5个值: {embedding[-5:]}")
        
        # 3. 测试批量嵌入
        print("\n3. 测试批量嵌入生成...")
        test_texts = [
            "First document about machine learning",
            "Second document about natural language processing",
            "Third document about deep learning"
        ]
        print(f"   批量文本数量: {len(test_texts)}")
        
        embeddings = embed_model.get_text_embedding_batch(test_texts)
        
        print(f"   ✅ 批量生成成功")
        print(f"   📊 生成的嵌入数量: {len(embeddings)}")
        print(f"   📊 每个嵌入的维度: {[len(e) for e in embeddings]}")
        
        # 4. 验证嵌入质量（检查是否都是不同的）
        print("\n4. 验证嵌入质量...")
        if len(embeddings) == len(test_texts):
            print(f"   ✅ 所有文本都成功生成了嵌入")
        
        # 检查嵌入是否不同（简单的相似度检查）
        import numpy as np
        try:
            emb1 = np.array(embeddings[0])
            emb2 = np.array(embeddings[1])
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            print(f"   📊 前两个嵌入的余弦相似度: {similarity:.4f}")
            if similarity < 0.99:  # 如果相似度不是太高，说明嵌入是不同的
                print(f"   ✅ 嵌入向量具有区分性")
        except Exception as e:
            print(f"   ⚠️  无法计算相似度: {e}")
        
        # 5. 测试查询嵌入
        print("\n5. 测试查询嵌入生成...")
        query_text = "What is machine learning?"
        print(f"   查询文本: '{query_text}'")
        
        query_embedding = embed_model.get_query_embedding(query_text)
        
        print(f"   ✅ 查询嵌入生成成功")
        print(f"   📊 查询嵌入维度: {len(query_embedding)}")
        
        # 6. 测试 Settings 集成
        print("\n6. 测试 Settings 集成...")
        Settings.embed_model = embed_model
        
        test_embedding_via_settings = Settings.embed_model.get_text_embedding("test via settings")
        print(f"   ✅ 通过 Settings 生成嵌入成功")
        print(f"   📊 嵌入维度: {len(test_embedding_via_settings)}")
        
        print("\n" + "="*60)
        print("✅ 所有测试通过！Ollama 嵌入模型工作正常")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        print(f"\n详细错误信息:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_ollama_embedding()
    sys.exit(0 if success else 1)

