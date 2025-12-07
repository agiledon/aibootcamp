# writer_agent.py
from pocketflow import Node, Flow
from common.server import A2AServer
from common.types import AgentCard, AgentSkill
from task_manager import PocketFlowTaskManager

class WritingNode(Node):
    def prep(self, shared):
        research = shared.get("research_data", "")
        design = shared.get("design_data", "")
        topic = shared.get("topic", "技术报告")
        
        return {
            "topic": topic,
            "research": research,
            "design": design
        }

    def exec(self, inputs):
        topic = inputs["topic"]
        research = inputs["research"]
        design = inputs["design"]
        
        report = f"""
        《{topic}》技术报告
        
        一、研究摘要
        {research}
        
        二、架构设计
        {design}
        
        三、总结与展望
        本报告详细分析了相关技术，并提出了可行的架构方案。
        A2A框架为分布式智能体协作提供了良好的基础。
        """
        return {"report": report}

    def post(self, shared, prep_res, exec_res):
        shared["final_report"] = exec_res["report"]
        return "success"

class WriterTaskManager(PocketFlowTaskManager):
    async def on_send_task(self, request):
        topic = self._extract_query(request)
        # 在实际场景中，这里会从请求中提取研究数据和设计数据
        research_data = "从研究员智能体获取的数据"
        design_data = "从架构师智能体获取的数据"
        
        shared_data = {
            "topic": topic,
            "research_data": research_data,
            "design_data": design_data
        }
        
        writing_node = WritingNode()
        flow = Flow(start=writing_node)
        flow.run(shared_data)
        
        from pydantic import BaseModel
        class TextPart(BaseModel):
            type: str = "text"
            text: str

        class Artifact(BaseModel):
            id: str
            parts: list

        response_artifact = Artifact(
            id="final_report_001",
            parts=[TextPart(text=shared_data["final_report"])]
        )
        
        return self._create_success_response(
            task_id=request.params.id,
            artifacts=[response_artifact]
        )

def start_writer_agent():
    skills = [
        AgentSkill(
            id="write",
            name="报告撰写",
            description="整合研究和设计内容，撰写完整技术报告",
            inputModes=["text"],
            outputModes=["text"]
        )
    ]
    
    agent_card = AgentCard(
        name="技术撰稿人智能体",
        version="1.0",
        description="负责技术文档和报告撰写",
        skills=skills
    )
    
    task_manager = WriterTaskManager()
    
    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
        host="0.0.0.0",
        port=8003  # 撰稿人智能体运行在8003端口
    )
    
    print("✍️ 撰稿人智能体已启动，服务端口：8003")
    server.start()

if __name__ == "__main__":
    start_writer_agent()