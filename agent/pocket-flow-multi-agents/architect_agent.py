# architect_agent.py
from pocketflow import Node, Flow
from common.server import A2AServer
from common.types import AgentCard, AgentSkill
from task_manager import PocketFlowTaskManager

class DesignNode(Node):
    def prep(self, shared):
        research_data = shared.get("research_data", "")
        design_requirements = shared.get("requirements", "设计可靠的系统架构")
        return {"research": research_data, "reqs": design_requirements}

    def exec(self, inputs):
        research = inputs["research"]
        reqs = inputs["reqs"]
        
        design_spec = f"""
        基于研究内容的技术架构设计：
        研究输入：{research[:100]}...
        设计要求：{reqs}
        
        架构方案：
        1. 采用微服务架构，每个智能体独立部署
        2. 使用A2A协议进行服务间通信
        3. 引入服务发现机制实现智能体动态注册
        4. 添加负载均衡和故障转移机制
        """
        return {"specification": design_spec}

    def post(self, shared, prep_res, exec_res):
        shared["design_spec"] = exec_res["specification"]
        return "success"

class ArchitectTaskManager(PocketFlowTaskManager):
    async def on_send_task(self, request):
        # 从请求中提取架构设计需求
        requirements = self._extract_query(request)
        research_data = self._extract_context(request)  # 假设可以获取研究数据
        
        shared_data = {
            "requirements": requirements,
            "research_data": research_data
        }
        
        design_node = DesignNode()
        flow = Flow(start=design_node)
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
            id="design_spec_001",
            parts=[TextPart(text=shared_data["design_spec"])]
        )
        
        return self._create_success_response(
            task_id=request.params.id,
            artifacts=[response_artifact]
        )

def start_architect_agent():
    skills = [
        AgentSkill(
            id="design",
            name="架构设计",
            description="基于需求和研究数据设计技术架构",
            inputModes=["text"],
            outputModes=["text"]
        )
    ]
    
    agent_card = AgentCard(
        name="系统架构师智能体",
        version="1.0",
        description="负责技术架构和系统设计",
        skills=skills
    )
    
    task_manager = ArchitectTaskManager()
    
    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
        host="0.0.0.0",
        port=8002  # 架构师智能体运行在8002端口
    )
    
    print("🏗️ 架构师智能体已启动，服务端口：8002")
    server.start()

if __name__ == "__main__":
    start_architect_agent()