from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai import LLM

@CrewBase
class MarketResearchCrew():
    """MarketResearchCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            lllm=LLM(model="gemini-flash-lite-latest"),
            tools=[SerperDevTool()]
        )


    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            lllm=LLM(model="gemini-flash-lite-latest"),
            verbose=True
        )


    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],
            output_file="output/market_research_report.md"  # enforce output path
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.analyst()],
            tasks=[self.research_task(), self.analysis_task()],
            process=Process.sequential,
            verbose=True
        )
