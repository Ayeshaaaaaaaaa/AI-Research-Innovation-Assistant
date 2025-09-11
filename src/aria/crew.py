# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
# from typing import List
# # If you want to run a snippet of code before or after the crew starts,
# # you can use the @before_kickoff and @after_kickoff decorators
# # https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# @CrewBase
# class Aria():
#     """Aria crew"""

#     agents: List[BaseAgent]
#     tasks: List[Task]

#     # Learn more about YAML configuration files here:
#     # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
#     # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
#     # If you would like to add tools to your agents, you can learn more about it here:
#     # https://docs.crewai.com/concepts/agents#agent-tools
#     @agent
#     def researcher(self) -> Agent:
#         return Agent(
#             config=self.agents_config['researcher'], # type: ignore[index]
#             verbose=True
#         )

#     @agent
#     def reporting_analyst(self) -> Agent:
#         return Agent(
#             config=self.agents_config['reporting_analyst'], # type: ignore[index]
#             verbose=True
#         )

#     # To learn more about structured task outputs,
#     # task dependencies, and task callbacks, check out the documentation:
#     # https://docs.crewai.com/concepts/tasks#overview-of-a-task
#     @task
#     def research_task(self) -> Task:
#         return Task(
#             config=self.tasks_config['research_task'], # type: ignore[index]
#         )

#     @task
#     def reporting_task(self) -> Task:
#         return Task(
#             config=self.tasks_config['reporting_task'], # type: ignore[index]
#             output_file='report.md'
#         )

#     @crew
#     def crew(self) -> Crew:
#         """Creates the Aria crew"""
#         # To learn how to add knowledge sources to your crew, check out the documentation:
#         # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

#         return Crew(
#             agents=self.agents, # Automatically created by the @agent decorator
#             tasks=self.tasks, # Automatically created by the @task decorator
#             process=Process.sequential,
#             verbose=True,
#             # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
#         )



from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from crewai_tools import CodeInterpreterTool

from tools.scholar_tool import SearchScholar
from tools.summarizer import SummarizerTool
from tools.fact_check_tool import FactCheckerTool
from tools.writer_tools import WriterTool
from tools.review_tools import ReviewerTool
from dotenv import load_dotenv
import os
from crewai import LLM
load_dotenv()

@CrewBase
class Aria():
    """
    ARIA Crew - orchestrates the multi-agent research pipeline.
    Agents and tasks are loaded from YAML (agents.yaml / tasks.yaml) via CrewBase.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # -------------------------
    # Agents
    # -------------------------
    

    @agent
    def researcher(self) -> Agent:
        """Researcher: uses scholar search + (optionally) summarizer tool to fetch raw findings."""
        return Agent(
            config=self.agents_config['researcher'],  # must match key in agents.yaml
            
            # tools=[SearchScholar()],                 # attach the search tool
            tools=[CodeInterpreterTool()],
            verbose=True,
        )

    @agent
    def fact_checker(self) -> Agent:
        """FactChecker: validates researcher's claims using external sources / news."""
        return Agent(
            config=self.agents_config['fact_checker'],
            
            # tools=[FactCheckerTool()],
            tools=[CodeInterpreterTool()],
            verbose=True,
        )

    @agent
    def summarizer(self) -> Agent:
        """Summarizer: condenses verified findings into structured notes."""
        return Agent(
            config=self.agents_config['summarizer'],
            
            # tools=[SummarizerTool()],
            tools=[CodeInterpreterTool()],
            verbose=True,
        )

    @agent
    def writer(self) -> Agent:
        """Writer: expands summaries into a full markdown report."""
        return Agent(
            config=self.agents_config['writer'],
            
            # tools=[WriterTool()],
            tools=[CodeInterpreterTool()],
            verbose=True,
        )

    @agent
    def reviewer(self) -> Agent:
        """Reviewer: performs grammar / clarity / style checks and final polishing."""
        return Agent(
            config=self.agents_config['reviewer'],
            
            # tools=[ReviewerTool()],
            tools=[CodeInterpreterTool()],
            verbose=True,
        )

    # -------------------------
    # Tasks (order matters for sequential process)
    # -------------------------
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # defined in tasks.yaml
        )

    @task
    def fact_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_check_task'],
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_task'],
        )

    @task
    def write_report_task(self) -> Task:
        # Save the report produced by the writer to disk
        return Task(
            config=self.tasks_config['write_report_task'],
            output_file='report.md'
        )

    @task
    def review_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_report_task'],
            # optionally specify an output_file if you want a final reviewed file
            output_file='report_reviewed.md'
        )

    # -------------------------
    # Crew builder
    # -------------------------
    @crew
    def crew(self) -> Crew:
        """
        Build the Crew. For a strict pipeline (research -> check -> summarize -> write -> review)
        use sequential. If you want a manager-driven workflow, switch to Process.hierarchical.
        """
        print("⚡ Crew is being created...")
        return Crew(
            agents=self.agents,   # created by @agent decorators
            tasks=self.tasks,     # created by @task decorators (order matches definitions above)
            process=Process.sequential,
            verbose=True,
        )
