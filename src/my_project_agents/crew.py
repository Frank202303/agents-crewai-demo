from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from my_project_agents.tools.custom_tool import SentimentAnalysisTool
from crewai import LLM
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
from dotenv import load_dotenv
load_dotenv()

# https://docs.crewai.com/en/concepts/llms#google-gemini-api

llm = LLM(
    model="gemini-2.5-flash",
    temperature=0.3
    # api_key=os.getenv("GEMINI_API_KEY")
)
api_key=os.getenv("GOOGLE_API_KEY")
# print(f" 我的key: {api_key}")
# Frank: 那 LLM 到底在哪控制？
# 👉 答案是：
# ✔ 全局统一控制（最重要）
# 在：
# 👉 .env + provider setup

# 你现在用的是“新版自动注入模式”: @CrewBase   旧版本需要：agent_config = './agents.yaml'

@CrewBase
class MyProjectAgents():
    """MyProjectAgents crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    # 定义 Agent 1
    @agent
    def sales_rep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sales_rep_agent'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    # 定义 Agent 2：lead_sales_rep_agent
    @agent
    def lead_sales_rep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_sales_rep_agent'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    # 开始分配 任务
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def lead_profiling_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_profiling_task'], # type: ignore[index]
            # 03: 使用什么工具
            tools= [DirectoryReadTool(directory='./knowledge'), FileReadTool(), SerperDevTool()]  # SerperDevTool 是检索 工具（框架内置）
        )

    @task
    def personalized_outreach_task(self) -> Task:
        return Task(
            # 01：已经在task文件上指定agent了
            #:02：要做什么事情
            config=self.tasks_config['personalized_outreach_task'], # type: ignore[index]
            # 03: 使用什么工具
            tools= [SentimentAnalysisTool(), SerperDevTool()],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyProjectAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
