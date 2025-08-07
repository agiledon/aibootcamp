from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class DddExpertCrew():
  """遵循DDD方法和过程开展领域建模的DDD Expert Crew"""

  agents: List[BaseAgent]
  tasks: List[Task]

  @agent
  def domain_expert(self) -> Agent:
    return Agent(
      config=self.agents_config['domain_expert'], # type: ignore[index]
      verbose=True
    #   tools=[SerperDevTool()]
    )

  @agent
  def developer(self) -> Agent:
    return Agent(
      config=self.agents_config['developer'], # type: ignore[index]
      verbose=True
    #   tools=[SerperDevTool()]
    )

  @agent
  def tester(self) -> Agent:
    return Agent(
      config=self.agents_config['tester'], # type: ignore[index]
      verbose=True
    #   tools=[SerperDevTool()]
    )
  
  @task
  def domain_modeling_task(self) -> Task:
    return Task(
      config=self.tasks_config['domain_modeling_task'], # type: ignore[index]
      output_file='output/domain_model.md'
    )

  @task
  def code_generation_task(self) -> Task:
    return Task(
      config=self.tasks_config['code_generation_task'], # type: ignore[index]  
      output_file='output/domain_model.java'
    )

  @task
  def unit_test_task(self) -> Task:
    return Task(
      config=self.tasks_config['unit_test_task'], # type: ignore[index]
      output_file='output/domain_model_test.java'
    )
  
  @crew
  def crew(self) -> Crew:
    """Creates the DddExpertCrew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )