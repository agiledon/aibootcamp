#!/usr/bin/env python3
"""
测试 Ollama 嵌入模型是否正常工作
验证端口 58094 和标准端口 11434
"""

import requests
import json
import sys
from typing import Optional, Dict, Any


def test_ollama_endpoint(base_url: str, port: int) -> Dict[str, Any]:
    """
    测试 Ollama 端点是否可用
    
    Args:
        base_url: 基础 URL (如 "http://127.0.0.1")
        port: 端口号
        
    Returns:
        测试结果字典
    """
    url = f"{base_url}:{port}"
    result = {
        "url": url,
        "port": port,
        "available": False,
        "models": [],
        "embedding_test": None,
        "error": None
    }
    
    # 1. 测试基础连接 - 检查 /api/tags
    try:
        print(f"\n{'='*60}")
        print(f"测试端点: {url}")
        print(f"{'='*60}")
        
        tags_url = f"{url}/api/tags"
        print(f"1. 检查服务状态: GET {tags_url}")
        response = requests.get(tags_url, timeout=5)
        
        if response.status_code == 200:
            result["available"] = True
            data = response.json()
            models = data.get("models", [])
            result["models"] = [model.get("name", "") for model in models]
            print(f"   ✅ 服务可用")
            print(f"   📦 已安装模型: {', '.join(result['models']) if result['models'] else '无'}")
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"   ❌ 服务不可用: HTTP {response.status_code}")
            return result
            
    except requests.exceptions.ConnectionError:
        result["error"] = "连接被拒绝 - 服务可能未运行"
        print(f"   ❌ 连接失败: 服务可能未运行在端口 {port}")
        return result
    except requests.exceptions.Timeout:
        result["error"] = "连接超时"
        print(f"   ❌ 连接超时")
        return result
    except Exception as e:
        result["error"] = str(e)
        print(f"   ❌ 错误: {e}")
        return result
    
    # 2. 测试嵌入模型 - 检查是否有 nomic-embed-text
    if "nomic-embed-text" not in " ".join(result["models"]):
        result["error"] = "未找到 nomic-embed-text 模型"
        print(f"   ⚠️  未找到 nomic-embed-text 模型")
        print(f"   💡 请运行: ollama pull nomic-embed-text")
        return result
    
    # 3. 测试嵌入 API - /api/embeddings (注意是复数)
    try:
        embed_url = f"{url}/api/embeddings"
        print(f"\n2. 测试嵌入 API: POST {embed_url}")
        
        # 查找正确的模型名称
        model_name = None
        for model in result["models"]:
            if "nomic-embed-text" in model:
                model_name = model
                break
        
        if not model_name:
            result["error"] = "无法确定模型名称"
            print(f"   ❌ 无法确定模型名称")
            return result
        
        print(f"   使用模型: {model_name}")
        print(f"   测试文本: 'Hello, this is a test'")
        
        payload = {
            "model": model_name,
            "prompt": "Hello, this is a test"
        }
        
        response = requests.post(embed_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            embedding = data.get("embedding", [])
            if embedding:
                result["embedding_test"] = {
                    "success": True,
                    "dimension": len(embedding),
                    "sample_values": embedding[:5]  # 前5个值作为示例
                }
                print(f"   ✅ 嵌入生成成功")
                print(f"   📊 嵌入维度: {len(embedding)}")
                print(f"   📝 示例值: {embedding[:5]}")
            else:
                result["embedding_test"] = {
                    "success": False,
                    "error": "响应中没有嵌入向量"
                }
                print(f"   ⚠️  响应中没有嵌入向量")
        else:
            result["embedding_test"] = {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
            print(f"   ❌ 嵌入生成失败: HTTP {response.status_code}")
            print(f"   📄 响应: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        result["embedding_test"] = {
            "success": False,
            "error": "请求超时"
        }
        print(f"   ❌ 请求超时")
    except Exception as e:
        result["embedding_test"] = {
            "success": False,
            "error": str(e)
        }
        print(f"   ❌ 错误: {e}")
    
    return result


def test_llamaindex_embedding():
    """
    测试通过 LlamaIndex 的 OllamaEmbedding 类调用
    """
    print(f"\n{'='*60}")
    print("测试 LlamaIndex OllamaEmbedding 集成")
    print(f"{'='*60}")
    
    try:
        from llama_index.embeddings.ollama import OllamaEmbedding
        from llama_index.core import Settings
        
        print("1. 初始化 OllamaEmbedding...")
        embed_model = OllamaEmbedding(
            model_name="nomic-embed-text:latest",
            request_timeout=60,
            keep_alive="5m"
        )
        print("   ✅ 初始化成功")
        
        print("\n2. 测试生成嵌入向量...")
        test_text = "Hello, this is a test for embedding generation"
        print(f"   测试文本: '{test_text}'")
        
        embedding = embed_model.get_text_embedding(test_text)
        
        print(f"   ✅ 嵌入生成成功")
        print(f"   📊 嵌入维度: {len(embedding)}")
        print(f"   📝 前5个值: {embedding[:5]}")
        
        # 测试批量生成
        print("\n3. 测试批量生成嵌入向量...")
        test_texts = [
            "First document",
            "Second document",
            "Third document"
        ]
        embeddings = embed_model.get_text_embedding_batch(test_texts)
        print(f"   ✅ 批量生成成功: {len(embeddings)} 个嵌入向量")
        print(f"   📊 每个维度: {[len(e) for e in embeddings]}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        print(f"   📄 详细错误:\n{traceback.format_exc()}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("Ollama 嵌入模型验证工具")
    print("="*60)
    
    # 测试标准端口
    print("\n【测试标准 Ollama 端口 11434】")
    result_11434 = test_ollama_endpoint("http://127.0.0.1", 11434)
    
    # 测试用户提到的端口
    print("\n【测试端口 58094】")
    result_58094 = test_ollama_endpoint("http://127.0.0.1", 58094)
    
    # 测试 LlamaIndex 集成
    print("\n【测试 LlamaIndex 集成】")
    llamaindex_ok = test_llamaindex_embedding()
    
    # 总结
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    
    print(f"\n端口 11434 (标准):")
    if result_11434["available"]:
        print(f"  ✅ 服务可用")
        if result_11434["embedding_test"] and result_11434["embedding_test"].get("success"):
            print(f"  ✅ 嵌入模型工作正常")
        else:
            print(f"  ❌ 嵌入模型测试失败")
    else:
        print(f"  ❌ 服务不可用: {result_11434.get('error', '未知错误')}")
    
    print(f"\n端口 58094:")
    if result_58094["available"]:
        print(f"  ✅ 服务可用")
        if result_58094["embedding_test"] and result_58094["embedding_test"].get("success"):
            print(f"  ✅ 嵌入模型工作正常")
        else:
            print(f"  ❌ 嵌入模型测试失败")
    else:
        print(f"  ❌ 服务不可用: {result_58094.get('error', '未知错误')}")
        print(f"  💡 这可能是 Ollama 的内部代理端口，通常不需要直接访问")
    
    print(f"\nLlamaIndex 集成:")
    if llamaindex_ok:
        print(f"  ✅ 集成测试通过")
    else:
        print(f"  ❌ 集成测试失败")
    
    # 建议
    print(f"\n{'='*60}")
    print("建议")
    print(f"{'='*60}")
    
    if not result_11434["available"]:
        print("1. 启动 Ollama 服务:")
        print("   ollama serve")
        print("   或")
        print("   python start_ollama.py")
    
    if result_11434["available"] and "nomic-embed-text" not in " ".join(result_11434["models"]):
        print("2. 安装嵌入模型:")
        print("   ollama pull nomic-embed-text")
    
    if result_11434["available"] and result_11434["embedding_test"] and not result_11434["embedding_test"].get("success"):
        print("3. 检查 Ollama 日志以获取更多错误信息")
    
    if not llamaindex_ok and result_11434["available"]:
        print("4. 检查 LlamaIndex 配置和依赖是否正确安装")


if __name__ == "__main__":
    main()

