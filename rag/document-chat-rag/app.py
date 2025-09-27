# 运行命令：uv run streamlit run app.py

"""
主应用文件 - 使用MVP模式重构的文档聊天RAG应用
"""

from controller import DocumentChatController

def main():
    """主函数，启动应用"""
    # 创建控制器并运行应用
    controller = DocumentChatController()
    controller.run()

if __name__ == "__main__":
    main()