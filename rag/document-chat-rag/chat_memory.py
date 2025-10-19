"""
对话记忆管理模块
负责管理对话历史、token计数和自动摘要功能
"""

import logging
import tiktoken
from typing import List, Dict, Any, Optional
from llama_index.llms.deepseek import DeepSeek

logger = logging.getLogger(__name__)


class ChatMemoryManager:
    """
    对话记忆管理器
    
    功能：
    1. 管理对话历史
    2. 计算对话历史的 token 数量
    3. 当对话历史超过上限时自动进行摘要
    """
    
    def __init__(
        self, 
        llm: Optional[DeepSeek] = None,
        max_tokens: int = 8000,  # DeepSeek 支持 64K，我们设置为 8K 作为对话历史上限
        summary_ratio: float = 0.8,  # 当达到 80% 时触发摘要
        encoding_name: str = "cl100k_base"  # GPT-4 使用的编码，适用于大多数模型
    ):
        """
        初始化对话记忆管理器
        
        Args:
            llm: 语言模型实例，用于生成摘要
            max_tokens: 对话历史的最大 token 数量
            summary_ratio: 触发摘要的比例阈值
            encoding_name: tiktoken 编码名称
        """
        self.llm = llm
        self.max_tokens = max_tokens
        self.summary_ratio = summary_ratio
        self.messages: List[Dict[str, str]] = []
        self.summary: Optional[str] = None  # 存储对话摘要
        
        # 初始化 tiktoken 编码器
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
            logger.info(f"✅ 初始化 tiktoken 编码器: {encoding_name}")
        except Exception as e:
            logger.warning(f"⚠️ 无法加载 tiktoken 编码器 {encoding_name}，使用默认编码器: {e}")
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        logger.info(f"✅ ChatMemoryManager 初始化完成 - 最大 tokens: {max_tokens}, 摘要阈值: {summary_ratio * 100}%")
    
    def count_tokens(self, text: str) -> int:
        """
        计算文本的 token 数量
        
        Args:
            text: 待计算的文本
            
        Returns:
            token 数量
        """
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            logger.warning(f"⚠️ Token 计数失败，使用字符数估算: {e}")
            # 粗略估算：1 token ≈ 4 个字符
            return len(text) // 4
    
    def get_total_tokens(self) -> int:
        """
        获取当前对话历史的总 token 数量
        
        Returns:
            总 token 数量
        """
        total = 0
        
        # 如果有摘要，计算摘要的 tokens
        if self.summary:
            total += self.count_tokens(self.summary)
        
        # 计算所有消息的 tokens
        for message in self.messages:
            # role 和 content 都需要计算
            total += self.count_tokens(message["role"])
            total += self.count_tokens(message["content"])
            # 添加一些开销（格式化字符等）
            total += 4
        
        return total
    
    def should_summarize(self) -> bool:
        """
        判断是否应该进行摘要
        
        Returns:
            是否需要摘要
        """
        current_tokens = self.get_total_tokens()
        threshold = self.max_tokens * self.summary_ratio
        
        should = current_tokens >= threshold
        
        if should:
            logger.info(f"📊 对话历史达到摘要阈值 - 当前 tokens: {current_tokens}, 阈值: {threshold}")
        
        return should
    
    def add_message(self, role: str, content: str):
        """
        添加消息到对话历史
        
        Args:
            role: 消息角色 (user/assistant)
            content: 消息内容
        """
        self.messages.append({"role": role, "content": content})
        logger.info(f"💬 添加消息 - 角色: {role}, 内容长度: {len(content)} 字符, 当前总 tokens: {self.get_total_tokens()}")
        
        # 检查是否需要摘要
        if self.should_summarize():
            self._auto_summarize()
    
    def _auto_summarize(self):
        """
        自动对对话历史进行摘要
        
        该方法会：
        1. 将较早的对话进行摘要
        2. 保留最近的几轮对话
        3. 更新摘要和消息列表
        """
        if not self.llm:
            logger.warning("⚠️ 未配置 LLM，无法进行自动摘要")
            return
        
        if len(self.messages) < 4:  # 至少需要 2 轮对话才进行摘要
            logger.info("💬 对话轮次不足，跳过摘要")
            return
        
        try:
            logger.info("🔄 开始自动摘要对话历史...")
            
            # 保留最近的 4 条消息（2 轮对话）
            recent_messages = self.messages[-4:]
            messages_to_summarize = self.messages[:-4]
            
            if not messages_to_summarize:
                logger.info("💬 没有需要摘要的消息")
                return
            
            # 构建摘要提示
            conversation_text = ""
            for msg in messages_to_summarize:
                role_name = "用户" if msg["role"] == "user" else "助手"
                conversation_text += f"{role_name}: {msg['content']}\n\n"
            
            summary_prompt = f"""请对以下对话历史进行简洁的摘要，保留关键信息和上下文：

对话历史：
{conversation_text}

之前的摘要：
{self.summary if self.summary else "无"}

请提供一个简洁的综合摘要（不超过 200 字）："""
            
            # 生成摘要
            response = self.llm.complete(summary_prompt)
            new_summary = str(response).strip()
            
            # 更新摘要和消息列表
            self.summary = new_summary
            self.messages = recent_messages
            
            # 计算摘要后的 token 数量
            new_total = self.get_total_tokens()
            
            logger.info(f"✅ 对话摘要完成")
            logger.info(f"📊 摘要长度: {len(new_summary)} 字符")
            logger.info(f"📊 保留消息数: {len(self.messages)}")
            logger.info(f"📊 摘要后总 tokens: {new_total}")
            logger.info(f"📝 摘要内容: {new_summary[:100]}...")
            
        except Exception as e:
            logger.error(f"❌ 自动摘要失败: {e}")
            import traceback
            logger.error(f"❌ 错误堆栈: {traceback.format_exc()}")
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取当前对话历史
        
        Returns:
            消息列表
        """
        return self.messages.copy()
    
    def get_summary(self) -> Optional[str]:
        """
        获取对话摘要
        
        Returns:
            对话摘要或 None
        """
        return self.summary
    
    def get_context_for_query(self, max_history_turns: int = 3) -> str:
        """
        获取用于查询的上下文
        
        包含摘要（如果有）和最近的对话历史
        
        Args:
            max_history_turns: 最大历史轮次数
            
        Returns:
            格式化的上下文字符串
        """
        context_parts = []
        
        # 添加摘要（如果有）
        if self.summary:
            context_parts.append(f"对话摘要：\n{self.summary}\n")
        
        # 添加最近的对话历史
        if self.messages:
            # 获取最近的 N 轮对话（每轮包含用户和助手的消息）
            recent_messages = self.messages[-(max_history_turns * 2):]
            
            if recent_messages:
                context_parts.append("最近的对话：")
                for msg in recent_messages:
                    role_name = "用户" if msg["role"] == "user" else "助手"
                    context_parts.append(f"{role_name}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        """清空对话历史和摘要"""
        self.messages.clear()
        self.summary = None
        logger.info("🗑️ 对话历史已清空")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        
        Returns:
            统计信息字典
        """
        total_tokens = self.get_total_tokens()
        usage_percentage = (total_tokens / self.max_tokens) * 100 if self.max_tokens > 0 else 0
        
        return {
            "total_tokens": total_tokens,
            "max_tokens": self.max_tokens,
            "usage_percentage": usage_percentage,
            "message_count": len(self.messages),
            "has_summary": self.summary is not None,
            "summary_length": len(self.summary) if self.summary else 0,
            "summary": self.summary  # 添加摘要内容
        }

