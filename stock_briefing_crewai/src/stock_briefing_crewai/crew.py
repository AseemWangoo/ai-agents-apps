from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class StockBriefingCrewai():
    """StockBriefingCrewai crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def collector(self) -> Agent:
        return Agent(
            config=self.agents_config['collector'], # type: ignore[index]
            verbose=True
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def risk_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_checker'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def brief_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['brief_writer'], # type: ignore[index]
            verbose=True
        )        

    @task
    def collect_task(self) -> Task:
        return Task(
            config=self.tasks_config['collect_task'], # type: ignore[index]
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_task'], # type: ignore[index]
        )
        
    @task
    def risk_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_task'], # type: ignore[index]
        )
        
    @task
    def brief_task(self) -> Task:
        return Task(
            config=self.tasks_config['brief_task'], # type: ignore[index]
        )        
    
    @crew
    def crew(self) -> Crew:
        """Creates the StockBriefingCrewai crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
