#!/usr/bin/env python3
"""
Milvus功能测试脚本
用于验证Milvus连接和基本功能
"""

import sys
import os

def test_milvus_connection():
    """测试Milvus连接"""
    print("🔍 测试Milvus连接...")
    
    try:
        from milvus_repository import MilvusRepository
        repo = MilvusRepository()
        info = repo.get_collection_info()
        
        print(f"✅ 连接成功!")
        print(f"   集合名称: {info['collection_name']}")
        print(f"   存储类型: {info['storage_type']}")
        print(f"   状态: {info['status']}")
        
        if info['status'] == 'connected':
            print("🎉 Milvus服务器运行正常，可以开始使用!")
            return True
        else:
            print("⚠️  Milvus服务器不可用，将使用内存存储模式")
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_application_integration():
    """测试应用集成"""
    print("\n🔍 测试应用集成...")
    
    try:
        from controller import DocumentChatController
        controller = DocumentChatController()
        info = controller.model.get_milvus_info()
        
        print(f"✅ 应用集成成功!")
        print(f"   集合名称: {info['collection_name']}")
        print(f"   存储类型: {info['storage_type']}")
        print(f"   状态: {info['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 应用集成失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Milvus功能测试")
    print("=" * 50)
    
    # 测试Milvus连接
    milvus_ok = test_milvus_connection()
    
    # 测试应用集成
    app_ok = test_application_integration()
    
    print("\n" + "=" * 50)
    print("📊 测试结果")
    print("=" * 50)
    
    if milvus_ok and app_ok:
        print("🎉 所有测试通过! 可以开始使用应用了")
        print("\n📝 下一步:")
        print("   1. 运行应用: uv run streamlit run app.py")
        print("   2. 上传文档进行测试")
        print("   3. 进行RAG问答")
    else:
        print("⚠️  部分测试失败，请检查配置")
        if not milvus_ok:
            print("   - Milvus连接问题，请检查Docker服务")
        if not app_ok:
            print("   - 应用集成问题，请检查依赖安装")
    
    print("\n💡 健康检查命令:")
    print("   curl http://localhost:9091/healthz")
    print("   docker-compose ps")

if __name__ == "__main__":
    main()
