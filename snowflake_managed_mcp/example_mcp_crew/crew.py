from crewai import Crew, Process
from .tools.mcp_tool import call_mcp_analyst
from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()


llm = LLM(
    api_key=os.getenv("APP__OPENAI_KEY"),
    model="openai/gpt-5-nano",
    stop=["END"],
    seed=42
)

def load_yaml(file_path):
    import yaml
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_crew():
    agents_config = load_yaml("example_mcp_crew/config/agents.yaml")
    tasks_config = load_yaml("example_mcp_crew/config/tasks.yaml")

    from crewai import Agent, Task

    analyst_agent = Agent(
        role=agents_config["analyst"]["role"],
        goal=agents_config["analyst"]["goal"],
        backstory=agents_config["analyst"]["backstory"],
        tools=[call_mcp_analyst],
        llm=llm,
        verbose=True,
    )

    data_task = Task(
        description=tasks_config["data_analysis_task"]["description"],
        expected_output=tasks_config["data_analysis_task"]["expected_output"],
        agent=analyst_agent
    )

    crew = Crew(
        agents=[analyst_agent],
        tasks=[data_task],
        process=Process.sequential,
        tracing=True
    )

    return crew
