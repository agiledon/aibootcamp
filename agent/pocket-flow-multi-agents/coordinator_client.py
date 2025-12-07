# coordinator_client.py
import aiohttp
import json
import asyncio
from typing import Dict, List

class MultiAgentCoordinator:
    def __init__(self):
        self.agent_endpoints = {
            "researcher": "http://localhost:8001/api/a2a",
            "architect": "http://localhost:8002/api/a2a", 
            "writer": "http://localhost:8003/api/a2a"
        }
    
    async def send_task_to_agent(self, agent_name: str, task_description: str, context: Dict = None):
        """向指定智能体发送任务"""
        endpoint = self.agent_endpoints[agent_name]
        
        request_data = {
            "jsonrpc": "2.0",
            "id": f"task_{agent_name}_{id(self)}",
            "method": "tasks/send",
            "params": {
                "input": {
                    "parts": [{
                        "type": "text",
                        "text": task_description
                    }]
                }
            }
        }
        
        # 添加上下文信息
        if context:
            request_data["params"]["context"] = context
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    endpoint,
                    json=request_data,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    result = await response.json()
                    return self._extract_artifact_text(result)
                    
            except Exception as e:
                print(f"与智能体 {agent_name} 通信失败: {e}")
                return None
    
    def _extract_artifact_text(self, response):
        """从A2A响应中提取文本内容"""
        if "result" in response:
            artifacts = response["result"].get("artifacts", [])
            if artifacts and "parts" in artifacts[0]:
                for part in artifacts[0]["parts"]:
                    if part.get("type") == "text":
                        return part["text"]
        return None
    
    async def collaborative_report_writing(self, topic: str):
        """协调多个智能体协作撰写报告"""
        print(f"🎯 开始协作撰写报告：「{topic}」")
        print("-" * 50)
        
        # 1. 研究员智能体进行资料搜集
        print("1. 派遣研究员智能体搜集资料...")
        research_result = await self.send_task_to_agent(
            "researcher", 
            f"请深入研究以下主题：{topic}"
        )
        
        if not research_result:
            print("❌ 研究员智能体任务失败")
            return None
            
        print("✅ 研究完成")
        print(f"研究摘要: {research_result[:100]}...")
        print()
        
        # 2. 架构师智能体设计方案
        print("2. 派遣架构师智能体设计架构...")
        design_result = await self.send_task_to_agent(
            "architect",
            f"基于以下研究设计技术架构：{research_result}",
            {"research_data": research_result}
        )
        
        if not design_result:
            print("❌ 架构师智能体任务失败")
            return None
            
        print("✅ 架构设计完成")
        print(f"设计要点: {design_result[:100]}...")
        print()
        
        # 3. 撰稿人智能体撰写报告
        print("3. 派遣撰稿人智能体撰写报告...")
        final_report = await self.send_task_to_agent(
            "writer",
            f"请基于以下内容撰写完整技术报告：研究：{research_result}，设计：{design_result}",
            {
                "research_data": research_result,
                "design_data": design_result,
                "topic": topic
            }
        )
        
        if not final_report:
            print("❌ 撰稿人智能体任务失败")
            return None
            
        print("✅ 报告撰写完成")
        print("-" * 50)
        return final_report

# 使用示例
async def main():
    coordinator = MultiAgentCoordinator()
    
    # 协作撰写关于A2A框架的报告
    topic = "A2A框架在分布式多智能体系统中的应用"
    report = await coordinator.collaborative_report_writing(topic)
    
    if report:
        print("📄 最终报告:")
        print("=" * 60)
        print(report)
        print("=" * 60)
        print("🎉 多智能体协作任务完成！")
    else:
        print("❌ 协作任务失败")

if __name__ == "__main__":
    # 运行前请确保先启动三个智能体服务
    asyncio.run(main())