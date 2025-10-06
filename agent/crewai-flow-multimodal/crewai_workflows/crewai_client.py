"""
CrewAI客户端管理模块
负责CrewAI LLM的初始化和配置
"""

import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crewai import Agent, Task, Crew, LLM
import config

logger = logging.getLogger(__name__)


class CrewAIClient:
    """CrewAI客户端管理类"""
    
    def __init__(self):
        self.crewai_llm = None
        self._initialize_crewai_llm()
    
    def _initialize_crewai_llm(self):
        """初始化CrewAI LLM"""
        try:
            self.crewai_llm = LLM(
                model=f"deepseek/{config.LLM_MODEL}",  # LiteLLM需要提供商前缀
                base_url=config.LLM_API_BASE,
                api_key=config.DEEPSEEK_API_KEY,
                temperature=0.1,
                timeout=120
            )
            logger.info(f"✅ CrewAI LLM初始化成功: deepseek/{config.LLM_MODEL}")
        except Exception as e:
            logger.error(f"❌ CrewAI LLM初始化失败: {e}")
            logger.error("请检查DeepSeek API配置")
            exit(1)
    
    def get_crewai_llm(self):
        """获取CrewAI LLM实例"""
        return self.crewai_llm
    
    def create_agent(self, role: str, goal: str, backstory: str, tools=None, verbose=True, allow_delegation=False):
        """创建CrewAI Agent"""
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=verbose,
            allow_delegation=allow_delegation,
            llm=self.crewai_llm
        )
    
    def create_task(self, description: str, agent: Agent, expected_output: str):
        """创建CrewAI Task"""
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
    
    def create_crew(self, agents: list, tasks: list, verbose=True, memory=False):
        """创建CrewAI Crew"""
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=verbose,
            memory=memory
        )

