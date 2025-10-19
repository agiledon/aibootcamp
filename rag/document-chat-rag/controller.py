"""
Controller类 - 处理用户请求，协调View和Model之间的交互
负责业务逻辑的协调和用户交互的处理
"""

import gc
import logging
import streamlit as st
from typing import Optional, Any, List
from model import DocumentChatModel
from view import DocumentChatView

# 配置日志
logger = logging.getLogger(__name__)


class DocumentChatController:
    """KFlow RAG控制器类，协调Model和View之间的交互"""
    
    def __init__(self):
        self.model = DocumentChatModel()
        self.view = DocumentChatView()
        self.current_query_engine = None
        
        # 初始化session state
        self._init_session_state()
        
        # 从session state恢复状态
        self._restore_state()
    
    def _init_session_state(self):
        """初始化Streamlit session state"""
        import streamlit as st
        
        if "id" not in st.session_state:
            st.session_state.id = self.model.get_session_id()
            st.session_state.file_cache = {}
            st.session_state.messages = []
            st.session_state.current_query_engine = None
            st.session_state.file_processed = False
            st.session_state.current_file_name = None
            st.session_state.need_refresh_documents = False
    
    def _restore_state(self):
        """从session state恢复状态"""
        import streamlit as st
        
        # 恢复查询引擎
        if hasattr(st.session_state, 'current_query_engine') and st.session_state.current_query_engine is not None:
            self.current_query_engine = st.session_state.current_query_engine
        
        # 恢复文件缓存到model
        if hasattr(st.session_state, 'file_cache'):
            self.model.file_cache = st.session_state.file_cache
        
        # 恢复消息历史到model
        if hasattr(st.session_state, 'messages'):
            self.model.messages = st.session_state.messages
    
    def handle_file_upload(self, uploaded_file) -> bool:
        """
        处理文件上传
        
        Args:
            uploaded_file: 上传的文件对象
            
        Returns:
            bool: 处理是否成功
        """
        import streamlit as st
        
        if uploaded_file is None:
            return False
        
        # 检查是否是同一个文件，避免重复处理
        if (hasattr(st.session_state, 'current_file_name') and 
            st.session_state.current_file_name == uploaded_file.name and
            hasattr(st.session_state, 'file_processed') and 
            st.session_state.file_processed):
            # 文件已经处理过，直接使用缓存的查询引擎
            self.current_query_engine = st.session_state.current_query_engine
            # 显示缓存文件的进度条
            self.view.display_sidebar_progress(100, "使用缓存文件")
            self.view.display_document_preview(uploaded_file, max_pages=5)
            return True
        
        def progress_callback(progress: int, message: str):
            """进度回调函数"""
            # 在侧边栏显示动态进度
            self.view.display_sidebar_progress(progress, message)
        
        # 处理文档文件
        success, message, query_engine = self.model.process_document_file(uploaded_file, progress_callback)
        
        if success:
            self.current_query_engine = query_engine
            
            # 保存状态到session state
            st.session_state.current_query_engine = query_engine
            st.session_state.file_cache = self.model.file_cache
            st.session_state.file_processed = True
            st.session_state.current_file_name = uploaded_file.name
            
            # 设置标志，表示需要刷新知识库文档列表
            st.session_state.need_refresh_documents = True
            
            # 清除主界面的进度显示
            if 'main_progress_placeholder' in st.session_state:
                st.session_state.main_progress_placeholder.empty()
            
            # 清除侧边栏的进度显示
            if 'progress_placeholder' in st.session_state:
                st.session_state.progress_placeholder.empty()
            
            # 成功提示已经在进度条中显示，不需要额外的成功消息
            self.view.display_document_preview(uploaded_file, max_pages=5)
            return True
        else:
            # 显示错误信息
            self.view.display_sidebar_progress(0, f"处理失败: {message}")
            self.view.show_error_message(message)
            self.view.stop_app()
    
    def _handle_document_deletion(self):
        """处理文档删除操作"""
        # 检查是否有待删除的文档
        if 'delete_document' in st.session_state:
            document_info = st.session_state.delete_document
            
            # 显示确认对话框
            if self.view.show_delete_confirmation(document_info):
                # 用户确认删除
                file_name = document_info['file_name']
                success, message = self.model.delete_document(file_name)
                
                if success:
                    # 删除成功，清除相关状态
                    if hasattr(st.session_state, 'current_file_name') and st.session_state.current_file_name == file_name:
                        # 如果删除的是当前文件，清除当前状态
                        if 'current_query_engine' in st.session_state:
                            del st.session_state.current_query_engine
                        if 'file_processed' in st.session_state:
                            st.session_state.file_processed = False
                        if 'current_file_name' in st.session_state:
                            del st.session_state.current_file_name
                    
                    # 清除删除状态
                    del st.session_state.delete_document
                    
                    # 显示成功消息
                    st.success(f"✅ {message}")
                    
                    # 设置刷新标志
                    st.session_state.need_refresh_documents = True
                    
                    # 重新运行以刷新界面
                    st.rerun()
                else:
                    # 删除失败，显示错误消息
                    st.error(f"❌ {message}")
                    
                    # 清除删除状态
                    del st.session_state.delete_document
            return False
    
    def handle_chat_input(self, user_input: str) -> bool:
        """
        处理用户聊天输入
        
        Args:
            user_input: 用户输入的消息
            
        Returns:
            bool: 处理是否成功
        """
        import streamlit as st
        
        if not user_input or not user_input.strip():
            return False
        
        # 添加用户消息到历史
        self.model.add_message("user", user_input)
        self.view.display_user_message(user_input)
        
        # 检查是否有可用的查询引擎
        query_engine = None
        
        # 获取查询引擎（全知识库检索）
        query_engine = self.model.get_query_engine()
        
        if query_engine is None:
            # 检查知识库状态
            existing_docs = self.model.get_existing_documents()
            if not existing_docs or len(existing_docs) == 0:
                error_message = "知识库中没有文档，请先上传文档"
            else:
                error_message = "无法连接到知识库，请检查ChromaDB服务状态和嵌入模型配置"
            
            self.view.show_warning_message(error_message)
            
            # 添加错误消息到聊天历史
            self.model.add_message("assistant", f"❌ {error_message}")
            st.session_state.messages = self.model.get_messages()
            return False
        
        # 显示助手回复
        try:
            logger.info(f"🔍 开始查询文档，用户输入: {user_input}")
            response_generator = self.model.query_document(query_engine, user_input)
            
            if response_generator is None:
                error_message = "查询失败，可能是文档处理或LLM服务问题，请重试"
                logger.error(f"❌ 查询失败: {error_message}")
                self.view.show_error_message(error_message)
                # 添加错误消息到聊天历史
                self.model.add_message("assistant", f"❌ {error_message}")
                st.session_state.messages = self.model.get_messages()
                return False
            
            logger.info("✅ 查询成功，开始显示响应")
            
        except Exception as e:
            error_message = f"查询过程中发生异常: {str(e)}"
            logger.error(f"❌ 查询过程中发生异常: {e}")
            logger.error(f"❌ 异常类型: {type(e).__name__}")
            import traceback
            logger.error(f"❌ 详细错误堆栈: {traceback.format_exc()}")
            
            self.view.show_error_message(error_message)
            # 添加错误消息到聊天历史
            self.model.add_message("assistant", f"❌ {error_message}")
            st.session_state.messages = self.model.get_messages()
            return False
        
        # 显示流式响应
        full_response = self.view.display_assistant_response(response_generator)
        
        # 添加助手回复到历史
        self.model.add_message("assistant", full_response)
        
        # 同步状态到session state
        st.session_state.messages = self.model.get_messages()
        
        return True
    
    def handle_clear_chat(self):
        """处理清空聊天"""
        self.model.clear_messages()
        import streamlit as st
        st.session_state.messages = []
        # 清空聊天历史但不重置文件处理状态
        gc.collect()
    
    def run(self):
        """运行应用主循环"""
        import streamlit as st
        
        # 渲染主布局
        clear_chat = self.view.render_main_layout()
        
        # 处理清空聊天
        if clear_chat:
            self.handle_clear_chat()
            st.rerun()
        
        # 检查是否需要刷新文档列表
        need_refresh = getattr(st.session_state, 'need_refresh_documents', False)
        
        # 获取已有文档列表
        existing_documents = self.model.get_existing_documents()
        
        # 检查服务状态
        chroma_status, ollama_status = self.model.check_services_status()
        
        # 如果刚刚上传了文件，显示成功消息并清除刷新标志
        if need_refresh:
            st.session_state.need_refresh_documents = False
            # 在侧边栏顶部显示成功消息
            with st.sidebar:
                st.success("✅ 文档已成功添加到知识库！")
        
        # 显示服务状态
        self.view.show_service_status(chroma_status, ollama_status)
        
        
        # 处理文档删除操作
        self._handle_document_deletion()
        
        # 渲染侧边栏并处理文件上传
        uploaded_file = self.view.render_sidebar(existing_documents)
        
        # 只有在文件真正发生变化时才处理文件上传
        if uploaded_file:
            # 检查是否是新的文件
            if (not hasattr(st.session_state, 'current_file_name') or 
                st.session_state.current_file_name != uploaded_file.name):
                self.handle_file_upload(uploaded_file)
                # 文件上传处理完成后，触发界面刷新以显示更新的文档列表
                st.rerun()
            else:
                # 文件相同，直接显示预览
                self.view.display_document_preview(uploaded_file, max_pages=5)
        
        # 处理聊天输入
        user_input = self.view.render_chat_input()
        
        if user_input:
            self.handle_chat_input(user_input)
            st.rerun()
