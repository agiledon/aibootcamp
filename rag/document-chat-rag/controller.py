"""
Controller类 - 处理用户请求，协调View和Model之间的交互
负责业务逻辑的协调和用户交互的处理
"""

import gc
from typing import Optional, Any
from model import DocumentChatModel
from view import DocumentChatView


class DocumentChatController:
    """文档聊天控制器类，协调Model和View之间的交互"""
    
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
            
            # 成功提示已经在进度条中显示，不需要额外的成功消息
            self.view.display_document_preview(uploaded_file, max_pages=5)
            return True
        else:
            # 显示错误信息
            self.view.display_sidebar_progress(0, f"处理失败: {message}")
            self.view.show_error_message(message)
            self.view.stop_app()
            return False
    
    def handle_chat_input(self, user_input: str) -> bool:
        """
        处理用户聊天输入
        
        Args:
            user_input: 用户输入的消息
            
        Returns:
            bool: 处理是否成功
        """
        if not user_input or not user_input.strip():
            return False
        
        if self.current_query_engine is None:
            self.view.show_warning_message("请先上传文档")
            return False
        
        # 添加用户消息到历史
        self.model.add_message("user", user_input)
        self.view.display_user_message(user_input)
        
        # 显示助手回复
        response_generator = self.model.query_document(self.current_query_engine, user_input)
        
        if response_generator is None:
            self.view.show_error_message("查询失败，请重试")
            return False
        
        # 显示流式响应
        full_response = self.view.display_assistant_response(response_generator)
        
        # 添加助手回复到历史
        self.model.add_message("assistant", full_response)
        
        # 同步状态到session state
        import streamlit as st
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
        
        # 渲染侧边栏并处理文件上传
        uploaded_file = self.view.render_sidebar()
        
        # 只有在文件真正发生变化时才处理文件上传
        if uploaded_file:
            # 检查是否是新的文件
            if (not hasattr(st.session_state, 'current_file_name') or 
                st.session_state.current_file_name != uploaded_file.name):
                self.handle_file_upload(uploaded_file)
            else:
                # 文件相同，直接显示预览
                self.view.display_document_preview(uploaded_file, max_pages=5)
        
        # 处理聊天输入
        user_input = self.view.render_chat_input()
        
        if user_input:
            self.handle_chat_input(user_input)
            st.rerun()
