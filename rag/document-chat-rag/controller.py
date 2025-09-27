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
    
    def _init_session_state(self):
        """初始化Streamlit session state"""
        import streamlit as st
        
        if "id" not in st.session_state:
            st.session_state.id = self.model.get_session_id()
            st.session_state.file_cache = {}
            st.session_state.messages = []
    
    def handle_file_upload(self, uploaded_file) -> bool:
        """
        处理文件上传
        
        Args:
            uploaded_file: 上传的文件对象
            
        Returns:
            bool: 处理是否成功
        """
        if uploaded_file is None:
            return False
        
        # 显示处理状态
        self.view.show_processing_status("正在处理文档...")
        
        # 处理PDF文件
        success, message, query_engine = self.model.process_pdf_file(uploaded_file)
        
        if success:
            self.current_query_engine = query_engine
            self.view.show_success_message("文档处理完成！")
            self.view.display_pdf_preview(uploaded_file)
            return True
        else:
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
            self.view.show_warning_message("请先上传PDF文档")
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
        
        return True
    
    def handle_clear_chat(self):
        """处理清空聊天"""
        self.model.clear_messages()
        import streamlit as st
        st.session_state.messages = []
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
        
        if uploaded_file:
            self.handle_file_upload(uploaded_file)
        
        # 处理聊天输入
        user_input = self.view.render_chat_input()
        
        if user_input:
            self.handle_chat_input(user_input)
            st.rerun()
        
        # 同步session state
        st.session_state.messages = self.model.get_messages()
