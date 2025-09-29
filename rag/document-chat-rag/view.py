"""
View类 - 处理Streamlit UI组件和用户界面
负责展示界面元素和用户交互
"""

import base64
import streamlit as st
from typing import List, Dict, Any, Optional, Generator
from document_converter import DocumentConverter


class DocumentChatView:
    """KFlow RAG视图类，处理所有UI相关的操作"""
    
    def __init__(self):
        self.setup_page_config()
        self.document_converter = DocumentConverter()
    
    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="KFlow RAG",
            page_icon="📚",
            layout="wide"
        )
        
        # 添加自定义CSS样式
        st.markdown("""
        <style>
        /* 修改进度条颜色为绿色 */
        .stProgress > div > div > div > div {
            background-color: #28a745 !important;
        }
        
        """, unsafe_allow_html=True)
    
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
    
    def display_document_preview(self, uploaded_file, max_pages: int = 5):
        """
        显示文档预览（统一使用PDF预览方式）
        
        Args:
            uploaded_file: 上传的文件对象
            max_pages: 最大显示页数
        """
        with st.sidebar:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # 显示文档信息
            st.markdown("### 文档信息")
            st.info(f"📄 文件名: {uploaded_file.name}")
            st.info(f"📊 文件大小: {uploaded_file.size / 1024:.1f} KB")
            st.info(f"📝 文件类型: {file_extension.upper()}")
            
            # 页数配置
            st.markdown("### 预览设置")
            max_pages = st.slider("显示页数", min_value=1, max_value=10, value=max_pages, 
                                help="设置预览文档的最大页数")
            
            try:
                # 将文件指针重置到开头
                uploaded_file.seek(0)
                
                if file_extension == 'pdf':
                    # PDF文件直接显示
                    base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
                else:
                    # 其他文件类型转换为PDF
                    st.info("正在转换文档为PDF预览...")
                    
                    if file_extension in ['docx', 'doc']:
                        # Word文档转换
                        pdf_content = self.document_converter.convert_docx_to_pdf(
                            uploaded_file.read(), max_pages
                        )
                    else:
                        # 其他文档类型转换
                        uploaded_file.seek(0)
                        content = uploaded_file.read().decode('utf-8')
                        pdf_content = self.document_converter.convert_to_pdf(
                            content, f'.{file_extension}', max_pages
                        )
                    
                    if pdf_content is None:
                        st.error("文档转换失败，无法预览")
                        return
                    
                    base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
                
                # 显示PDF预览
                st.markdown("### 文档预览")
                pdf_display = f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0&view=FitH" 
                        width="100%" 
                        height="500" 
                        type="application/pdf"
                        style="border: 1px solid #ddd; border-radius: 5px;">
                </iframe>
                """
                
                st.markdown(pdf_display, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"预览失败: {e}")
                # 降级到文本预览
                try:
                    uploaded_file.seek(0)
                    content = uploaded_file.read().decode('utf-8')
                    preview = content[:1000] + "..." if len(content) > 1000 else content
                    st.markdown("### 文本预览")
                    st.text_area("文档内容预览", preview, height=200, disabled=True, label_visibility="collapsed")
                except Exception as e2:
                    st.warning(f"无法预览文件内容: {e2}")
    
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
    
    def show_progress_bar(self, progress: int, message: str):
        """
        显示单个动态进度条
        
        Args:
            progress: 进度百分比 (0-100)
            message: 进度消息
        """
        # 创建进度条容器
        progress_container = st.container()
        
        with progress_container:
            # 显示动态百分比
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold; color: #28a745;'>{progress}%</div>", unsafe_allow_html=True)
            
            # 显示绿色进度条
            progress_bar = st.progress(progress / 100)
            
            # 当进度达到100%时显示完成信息
            if progress == 100:
                st.success("✅ 文档加载完成")
    
    def create_progress_container(self):
        """创建进度显示容器"""
        return st.container()
    
    def display_sidebar_progress(self, progress: int, message: str):
        """
        在侧边栏顶部显示单个动态进度条
        
        Args:
            progress: 进度百分比 (0-100)
            message: 进度消息
        """
        with st.sidebar:
            # 使用session state来存储进度占位符
            if 'progress_placeholder' not in st.session_state:
                st.session_state.progress_placeholder = st.empty()
            
            # 在占位符中显示进度条
            with st.session_state.progress_placeholder.container():
                self.show_progress_bar(progress, message)
    
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
