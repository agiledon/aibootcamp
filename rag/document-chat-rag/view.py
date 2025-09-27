"""
View类 - 处理Streamlit UI组件和用户界面
负责展示界面元素和用户交互
"""

import base64
import streamlit as st
from typing import List, Dict, Any, Optional, Generator


class DocumentChatView:
    """文档聊天视图类，处理所有UI相关的操作"""
    
    def __init__(self):
        self.setup_page_config()
    
    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="文档聊天RAG",
            page_icon="📚",
            layout="wide"
        )
    
    def render_sidebar(self) -> Optional[Any]:
        """
        渲染侧边栏，包含文件上传功能
        
        Returns:
            上传的文件对象或None
        """
        with st.sidebar:
            st.header("📁 添加文档")
            
            uploaded_file = st.file_uploader(
                "选择PDF文件", 
                type="pdf",
                help="上传PDF文件进行文档问答"
            )
            
            if uploaded_file:
                st.write("正在处理文档...")
                
        return uploaded_file
    
    def display_pdf_preview(self, uploaded_file):
        """
        显示PDF预览
        
        Args:
            uploaded_file: 上传的文件对象
        """
        with st.sidebar:
            st.markdown("### PDF预览")
            
            # 将文件指针重置到开头
            uploaded_file.seek(0)
            base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
            
            # 嵌入PDF的HTML
            pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" 
                    height="400" 
                    type="application/pdf"
                    style="border: 1px solid #ddd; border-radius: 5px;">
            </iframe>
            """
            
            st.markdown(pdf_display, unsafe_allow_html=True)
    
    def render_chat_header(self):
        """渲染聊天界面头部"""
        col1, col2 = st.columns([6, 1])
        
        with col1:
            st.header("🤖 和DeepSeek对话")
        
        with col2:
            if st.button("🗑️ 清空", help="清空聊天记录"):
                return True
        
        return False
    
    def display_chat_messages(self, messages: List[Dict[str, str]]):
        """
        显示聊天消息历史
        
        Args:
            messages: 消息列表
        """
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def render_chat_input(self) -> Optional[str]:
        """
        渲染聊天输入框
        
        Returns:
            用户输入的消息或None
        """
        return st.chat_input("请输入您的问题...")
    
    def display_user_message(self, message: str):
        """
        显示用户消息
        
        Args:
            message: 用户消息内容
        """
        with st.chat_message("user"):
            st.markdown(message)
    
    def display_assistant_response(self, response_generator: Generator[str, None, None]):
        """
        显示助手回复（流式）
        
        Args:
            response_generator: 响应生成器
            
        Returns:
            完整的响应内容
        """
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                # 移除光标
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"生成响应时发生错误: {e}")
                full_response = "抱歉，生成响应时发生错误。"
                message_placeholder.markdown(full_response)
            
            return full_response
    
    def show_success_message(self, message: str):
        """显示成功消息"""
        st.success(message)
    
    def show_error_message(self, message: str):
        """显示错误消息"""
        st.error(message)
    
    def show_info_message(self, message: str):
        """显示信息消息"""
        st.info(message)
    
    def show_warning_message(self, message: str):
        """显示警告消息"""
        st.warning(message)
    
    def show_processing_status(self, message: str):
        """显示处理状态"""
        st.write(message)
    
    def stop_app(self):
        """停止应用"""
        st.stop()
    
    def render_main_layout(self):
        """渲染主布局"""
        # 初始化聊天历史
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # 渲染聊天头部
        clear_chat = self.render_chat_header()
        
        # 显示聊天消息历史
        self.display_chat_messages(st.session_state.messages)
        
        return clear_chat
