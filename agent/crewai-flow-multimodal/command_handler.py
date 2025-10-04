"""
命令处理器
负责处理用户输入并创建相应的命令
"""

import logging
from typing import Optional

from command_pattern import Command, TextQueryCommand, AudioQueryCommand, SystemSetupCommand, ExitCommand

logger = logging.getLogger(__name__)


class CommandHandler:
    """命令处理器类"""
    
    def __init__(self, record_audio_func=None):
        self.record_audio_func = record_audio_func
        self.commands = {
            "1": self._handle_text_query,
            "2": self._handle_audio_query,
            "3": self._handle_exit
        }
    
    def _handle_text_query(self) -> Command:
        """处理文本查询输入"""
        query = input("\n💬 Enter your question: ").strip()
        if query:
            return TextQueryCommand(query)
        else:
            print("❌ Please enter a valid question.")
            return None
    
    def _handle_audio_query(self) -> Command:
        """处理音频查询输入"""
        if not self.record_audio_func:
            print("❌ Audio recording function not available.")
            return None
            
        duration = input("\n🎤 Recording duration in seconds (default 10): ").strip()
        duration = int(duration) if duration.isdigit() else 10
        
        audio_file = self.record_audio_func(duration)
        if audio_file:
            return AudioQueryCommand(audio_file)
        else:
            print("❌ Failed to record audio.")
            return None
    
    def _handle_exit(self) -> Command:
        """处理退出输入"""
        return ExitCommand()
    
    def get_command(self, choice: str) -> Optional[Command]:
        """根据用户选择获取相应的命令"""
        handler = self.commands.get(choice)
        if handler:
            return handler()
        else:
            print("❌ Invalid choice. Please enter 1-3.")
            return None
    
    def show_menu(self):
        """显示菜单选项"""
        print("\nWhat would you like to do?")
        print("1. 💬 Ask a question (text)")
        print("2. 🎤 Record and ask a question")
        print("3. 🚪 Exit")
    
    def execute_command(self, command: Command) -> str:
        """执行命令并返回结果"""
        if command is None:
            return ""
        
        result = command.execute()
        
        # 特殊处理退出命令
        if result == "EXIT":
            return "EXIT"
        
        return result
