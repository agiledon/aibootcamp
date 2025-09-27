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
                "选择文档文件", 
                type=["pdf", "docx", "doc", "md", "markdown", "csv", "txt"],
                help="支持PDF、Word、Markdown、CSV、TXT文件进行文档问答"
            )
            
            if uploaded_file:
                st.write("正在处理文档...")
                
        return uploaded_file
    
    def display_document_preview(self, uploaded_file):
        """
        显示文档预览（支持PDF和其他文档类型）
        
        Args:
            uploaded_file: 上传的文件对象
        """
        with st.sidebar:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
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
            else:
                # 对于非PDF文件，显示文件信息
                st.markdown("### 文档信息")
                st.info(f"📄 文件名: {uploaded_file.name}")
                st.info(f"📊 文件大小: {uploaded_file.size / 1024:.1f} KB")
                st.info(f"📝 文件类型: {file_extension.upper()}")
                
                # 对于文本文件，显示部分内容预览
                if file_extension in ['txt', 'md', 'markdown', 'csv']:
                    try:
                        uploaded_file.seek(0)
                        content = uploaded_file.read().decode('utf-8')
                        
                        if file_extension in ['md', 'markdown']:
                            # 对于 markdown 文件，显示渲染后的预览
                            st.markdown("### 内容预览")
                            preview = content[:1000] + "..." if len(content) > 1000 else content
                            st.markdown(preview)
                        else:
                            # 对于其他文本文件，显示纯文本预览
                            preview = content[:500] + "..." if len(content) > 500 else content
                            st.markdown("### 内容预览")
                            st.text_area("文档内容预览", preview, height=200, disabled=True, label_visibility="collapsed")
                    except Exception as e:
                        st.warning(f"无法预览文件内容: {e}")
    
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
    
    def show_document_stats(self, doc_count: int, total_chars: int):
        """显示文档统计信息"""
        st.info(f"📊 文档统计: 加载了 {doc_count} 个片段，总字符数 {total_chars}")
    
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
