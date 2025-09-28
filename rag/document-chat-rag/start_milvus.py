#!/usr/bin/env python3
"""
启动Milvus服务器的脚本
用于启动本地Milvus服务器以支持向量数据库功能
"""

import subprocess
import time
import sys
import os

def start_milvus_server():
    """启动Milvus服务器"""
    try:
        print("正在启动Milvus服务器...")
        
        # 启动Milvus服务器
        process = subprocess.Popen(
            ["milvus", "run", "standalone"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("Milvus服务器启动中，请等待...")
        print("服务器地址: http://localhost:19530")
        print("按 Ctrl+C 停止服务器")
        
        # 等待服务器启动
        time.sleep(5)
        
        # 检查服务器是否正常运行
        try:
            import requests
            # 使用正确的健康检查端点
            response = requests.get("http://localhost:9091/healthz", timeout=5)
            if response.status_code == 200:
                print("✅ Milvus服务器启动成功！")
                print("健康检查端点: http://localhost:9091/healthz")
            else:
                print("⚠️  Milvus服务器可能未完全启动")
        except ImportError:
            print("⚠️  无法检查服务器状态（缺少requests库）")
            print("请手动检查: curl http://localhost:9091/healthz")
        except Exception as e:
            print(f"⚠️  服务器状态检查失败: {e}")
            print("请手动检查: curl http://localhost:9091/healthz")
        
        # 保持进程运行
        process.wait()
        
    except FileNotFoundError:
        print("❌ 错误: 未找到Milvus命令")
        print("请确保已安装Milvus并添加到PATH环境变量")
        print("安装方法: https://milvus.io/docs/install_standalone-docker.md")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n正在停止Milvus服务器...")
        process.terminate()
        print("Milvus服务器已停止")
    except Exception as e:
        print(f"❌ 启动Milvus服务器失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_milvus_server()
