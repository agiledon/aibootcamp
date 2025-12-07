# researcher_agent.py
from pocketflow import Node, Flow
from common.server import A2AServer
from common.types import AgentCard, AgentSkill, AgentCapabilities
from task_manager import PocketFlowTaskManager
import asyncio

# 1. 定义研究员智能体的核心逻辑节点
class ResearchNode(Node):
    def prep(self, shared):
        # 从A2A请求中获取研究主题
        research_topic = shared.get("topic", "通用研究")
        return {"topic": research_topic}

    def exec(self, inputs):
        topic = inputs["topic"]
        # 模拟实际研究过程，这里可以替换为真实的网络搜索、数据库查询等
        research_findings = f"""
        关于「{topic}」的研究摘要：
        1. A2A协议基于JSON-RPC 2.0，提供了智能体间通信的标准。
        2. 核心组件包括A2AServer、TaskManager和AgentCard。
        3. 该协议支持异步任务管理和分布式部署。
        """
        return {"findings": research_findings}

    def post(self, shared, prep_res, exec_res):
        shared["research_result"] = exec_res["findings"]
        return "success"

# 2. 自定义TaskManager
class ResearchTaskManager(PocketFlowTaskManager):
    async def on_send_task(self, request):
        # 提取研究主题
        topic = self._extract_query(request)
        
        # 准备共享数据并执行工作流
        shared_data = {"topic": topic}
        research_node = ResearchNode()
        flow = Flow(start=research_node)
        flow.run(shared_data)
        
        # 构建A2A响应
        from pydantic import BaseModel
        class TextPart(BaseModel):
            type: str = "text"
            text: str

        class Artifact(BaseModel):
            id: str
            parts: list

        response_artifact = Artifact(
            id="research_result_001",
            parts=[TextPart(text=shared_data["research_result"])]
        )
        
        return self._create_success_response(
            task_id=request.params.id,
            artifacts=[response_artifact]
        )

# 3. 定义智能体能力
def create_researcher_card():
    skills = [
        AgentSkill(
            id="research",
            name="技术研究",
            description="对给定技术主题进行深入研究并整理资料",
            inputModes=["text"],
            outputModes=["text"]
        )
    ]
    
    return AgentCard(
        name="技术研究员智能体",
        description="专注于技术领域的资料搜集和研究分析",
        url="http://localhost:8001",
        version="1.0",
        capabilities=AgentCapabilities(
            streaming=False,
            pushNotifications=False,
            stateTransitionHistory=False,
        ),
        skills=skills,
    )

# 4. 启动研究员智能体服务
def start_researcher_agent():
    agent_card = create_researcher_card()
    task_manager = ResearchTaskManager()
    
    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
        host="0.0.0.0",
        port=8001  # 研究员智能体运行在8001端口
    )
    
    print("🔬 研究员智能体已启动，服务端口：8001")
    server.start()

if __name__ == "__main__":
    start_researcher_agent()