#!/usr/bin/env python3
"""
启动Ollama服务的脚本
用于启动Ollama服务以支持嵌入模型功能
"""

import subprocess
import time
import sys
import requests

def check_ollama_service():
    """检查Ollama服务是否运行"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama_service():
    """启动Ollama服务"""
    try:
        print("正在检查Ollama服务状态...")
        
        if check_ollama_service():
            print("✅ Ollama服务已经在运行")
            return True
        
        print("正在启动Ollama服务...")
        
        # 启动Ollama服务
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("Ollama服务启动中，请等待...")
        print("服务地址: http://localhost:11434")
        print("按 Ctrl+C 停止服务")
        
        # 等待服务启动
        for i in range(30):  # 等待最多30秒
            time.sleep(1)
            if check_ollama_service():
                print("✅ Ollama服务启动成功！")
                
                # 检查是否有nomic-embed-text模型
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=5)
                    if response.status_code == 200:
                        models = response.json().get("models", [])
                        model_names = [model["name"] for model in models]
                        
                        if "nomic-embed-text:latest" in model_names:
                            print("✅ nomic-embed-text模型已安装")
                        else:
                            print("⚠️  nomic-embed-text模型未安装")
                            print("请运行: ollama pull nomic-embed-text")
                except Exception as e:
                    print(f"⚠️  检查模型时出错: {e}")
                
                return True
            print(f"等待服务启动... ({i+1}/30)")
        
        print("⚠️  Ollama服务启动超时")
        return False
        
    except FileNotFoundError:
        print("❌ 错误: 未找到Ollama命令")
        print("请确保已安装Ollama并添加到PATH环境变量")
        print("安装方法: https://ollama.ai/download")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n正在停止Ollama服务...")
        process.terminate()
        print("Ollama服务已停止")
    except Exception as e:
        print(f"❌ 启动Ollama服务失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Ollama服务启动器")
    print("=" * 50)
    
    if start_ollama_service():
        print("\n📝 下一步:")
        print("   1. 确保nomic-embed-text模型已安装: ollama pull nomic-embed-text")
        print("   2. 运行应用: uv run streamlit run app.py")
        print("   3. 上传文档进行测试")
    else:
        print("\n❌ Ollama服务启动失败")
        print("请检查Ollama安装和配置")

if __name__ == "__main__":
    main()
