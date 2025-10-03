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
    
    def display_existing_documents(self, documents: List[Dict[str, Any]]):
        """
        显示已有文档列表
        
        Args:
            documents: 文档信息列表
        """
        if not documents:
            return
        
        with st.sidebar:
            st.markdown("---")
            st.header("📚 知识库文档")
            
            for i, doc in enumerate(documents):
                with st.expander(f"📄 {doc['file_name']}", expanded=False):
                    st.write(f"**文件类型:** {doc['file_type']}")
                    st.write(f"**文档片段数:** {doc['document_count']}")
                    
                    # 添加文件图标
                    file_icon = self._get_file_icon(doc['file_type'])
                    st.markdown(f"{file_icon} {doc['file_name']}")
                    
                    # 添加删除按钮
                    col1, col2 = st.columns([1, 1])
                    with col2:
                        if st.button("🗑️ 删除", key=f"delete_{i}", help="删除此文档"):
                            # 存储要删除的文档信息到session state
                            st.session_state.delete_document = {
                                'file_name': doc['file_name'],
                                'file_type': doc['file_type'],
                                'document_count': doc['document_count'],
                                'index': i
                            }
                            st.rerun()
    
    def show_delete_confirmation(self, document_info: Dict[str, Any]) -> bool:
        """
        显示删除确认对话框
        
        Args:
            document_info: 要删除的文档信息
            
        Returns:
            bool: 用户是否确认删除
        """
        with st.sidebar:
            st.markdown("---")
            st.warning("⚠️ 确认删除文档")
            
            file_icon = self._get_file_icon(document_info['file_type'])
            st.write(f"{file_icon} **{document_info['file_name']}**")
            st.write(f"**文件类型:** {document_info['file_type']}")
            st.write(f"**文档片段数:** {document_info['document_count']}")
            
            st.write("**此操作将永久删除该文档及其所有片段，无法恢复！**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ 取消", key="cancel_delete"):
                    # 清除删除状态
                    if 'delete_document' in st.session_state:
                        del st.session_state.delete_document
                    st.rerun()
            
            with col2:
                if st.button("✅ 确认删除", key="confirm_delete", type="primary"):
                    return True
        
        return False
    
    def _get_file_icon(self, file_type: str) -> str:
        """
        根据文件类型返回对应的图标
        
        Args:
            file_type: 文件类型
            
        Returns:
            图标字符串
        """
        icon_map = {
            "PDF": "📕",
            "DOCX": "📘", 
            "DOC": "📘",
            "MD": "📝",
            "MARKDOWN": "📝",
            "TXT": "📄",
            "CSV": "📊"
        }
        return icon_map.get(file_type.upper(), "📄")
    
    def render_sidebar(self, existing_documents: List[Dict[str, Any]] = None) -> Optional[Any]:
        """
        渲染侧边栏，包含文件上传功能和已有文档列表
        
        Args:
            existing_documents: 已有文档列表
            
        Returns:
            上传的文件对象或None
        """
        with st.sidebar:
            # 显示已有文档列表（在添加文档上方）
            if existing_documents:
                self.display_existing_documents(existing_documents)
                st.markdown("---")
            
            st.header("📁 添加文档")
            
            uploaded_file = st.file_uploader(
                "选择文档文件", 
                type=["pdf", "docx", "doc", "md", "markdown", "csv", "txt"],
                help="支持PDF、Word、Markdown、CSV、TXT文件进行文档问答"
            )
            
            if uploaded_file:
                # 不在这里显示进度，让控制器处理
                pass
                
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
    
    def render_search_scope_control(self, existing_documents: List[Dict[str, Any]] = None):
        """
        渲染检索范围控制组件
        
        Args:
            existing_documents: 已有文档列表
            
        Returns:
            tuple: (search_scope, selected_documents)
        """
        # 检索范围选择
        col1, col2 = st.columns([3, 7])
        
        with col1:
            search_scope = st.selectbox(
                "检索范围",
                options=["全知识库", "已选文档"],
                help="选择检索范围：全知识库或特定文档"
            )
        
        selected_documents = []
        
        if search_scope == "已选文档":
            with col2:
                if existing_documents and len(existing_documents) > 0:
                    # 创建文档选择选项
                    doc_options = [f"{doc['file_name']} ({doc['file_type']})" for doc in existing_documents]
                    
                    selected_indices = st.multiselect(
                        "选择文档",
                        options=list(range(len(existing_documents))),
                        format_func=lambda x: doc_options[x],
                        help="选择要检索的文档（可多选）",
                        placeholder="请选择文档..."
                    )
                    
                    # 根据选择的索引获取文档信息
                    selected_documents = [existing_documents[i] for i in selected_indices]
                    
                    if selected_documents:
                        st.success(f"已选择 {len(selected_documents)} 个文档")
                    else:
                        st.info("请选择要检索的文档")
                else:
                    st.warning("知识库中没有文档，请先上传文档")
        
        else:  # 全知识库
            with col2:
                if existing_documents and len(existing_documents) > 0:
                    st.success(f"将检索知识库中的所有 {len(existing_documents)} 个文档")
                else:
                    st.warning("知识库中没有文档，请先上传文档")
        
        return search_scope, selected_documents
    
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
                print("🔍 开始显示流式响应...")
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                # 移除光标
                message_placeholder.markdown(full_response)
                print(f"✅ 流式响应显示完成，总长度: {len(full_response)} 字符")
                
            except Exception as e:
                error_msg = f"生成响应时发生错误: {e}"
                print(f"❌ 流式响应显示错误: {e}")
                print(f"❌ 错误类型: {type(e).__name__}")
                import traceback
                print(f"❌ 详细错误堆栈:")
                print(traceback.format_exc())
                
                st.error(error_msg)
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
    
    def show_service_status(self, chroma_status: str, ollama_status: str):
        """
        显示服务状态信息
        
        Args:
            chroma_status: ChromaDB服务状态
            ollama_status: Ollama服务状态
        """
        with st.sidebar:
            st.markdown("---")
            st.header("🔧 服务状态")
            
            # ChromaDB状态
            if chroma_status == "available":
                st.success("✅ ChromaDB: 已连接")
            elif chroma_status == "unavailable":
                st.warning("⚠️ ChromaDB: 不可用")
            else:
                st.error("❌ ChromaDB: 连接失败")
            
            # Ollama状态
            if ollama_status == "available":
                st.success("✅ Ollama: 可用")
            elif ollama_status == "unavailable":
                st.warning("⚠️ Ollama: 不可用")
            else:
                st.error("❌ Ollama: 连接失败")
    
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
        # 显示动态百分比
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold; color: #28a745;'>{progress}%</div>", unsafe_allow_html=True)
        
        # 显示绿色进度条
        progress_bar = st.progress(progress / 100)
        
        # 显示进度消息
        if progress < 100:
            st.info(f"📄 {message}")
        else:
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
