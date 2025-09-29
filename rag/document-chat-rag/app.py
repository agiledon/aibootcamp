# 运行命令：uv run streamlit run app.py

"""
主应用文件 - KFlow RAG智能文档问答系统
"""

from controller import DocumentChatController

def main():
    """主函数，启动应用"""
    # 创建控制器并运行应用
    controller = DocumentChatController()
    controller.run()

if __name__ == "__main__":
    main()