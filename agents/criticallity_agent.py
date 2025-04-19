from smolagents import ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool, CodeAgent
import logging
from typing import Dict
from agents.tools.last_month import LastMonthTool
from agents.tools.min_max_avg import MinMaxAvgTool
from agents.tools.rag import RetrieverTool
from agents.managed_agents import RagAgent, WebAgent, StatisticsAgent

class CriticallityAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
        self.model = OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        ) 
    
    def score_metrics(self, metrics, last_month_values: list, min_values: list, avg_values: list, max_values: list, metrics_docs) -> str:
        """
        Score a metrics based on the provided metrics.
        """

        system = """
            You are a security assessment agent that provides a mark based on the metrics.
            Your task is to mark the results of the current vulnerability assessment of the company based on the following metrics:
                1. SLA: The ratio of tasks that were completed on time to the total number of tasks.
                2. Visibility: The ratio of hosts that are visible to the security team to the total number of hosts.
                3. Average duration: The average time it takes to complete a task in days.
                4. Density by company: Average number of critical vulnerabilities per unique FQDNs.
                5. Density by ownerblock: Average number of critical vulnerabilities per unique FQDNs, grouped by ownerblock.
                6. Density by application: Average number of critical vulnerabilities per unique FQDNs, grouped by application.
            
            Your final answer should be a number, ranging from 0 to 10. Where 0-3 is good, 4-6 is medium, and 7-10 is bad.

            You are managing 2 agents that can help you accomplish this task:
                1. A web search agent
                2. A retriever agent to search related documents

            You can use the following tools to score the metrics:
                2. MinMaxAvgTool to look up what were the min, max, and average values for these parameters currently in the company
                3. last_month_tool to look up what were the values for these parameters last month

            Use final_answer_tool to provide a single number as a final answer.\n
        """

        question = system + f"SLA: {metrics.sla}, VISIBILITY: {metrics.visibility}, AVG_DURATION: {metrics.avg_duration}, DENSITY_BY_COMPANY: {metrics.density_by_company}, DENSITY_BY_OWNERBLOCK: {metrics.density_by_ownerblock}, DENSITY_BY_APPLICATION: {metrics.density_by_application}"

        self.agent = CodeAgent(
            model=self.model, 
            managed_agents =[
                RagAgent(
                    docs=metrics_docs,
                    model=self.model
                ).agent,
                WebAgent(
                    model=self.model
                ).agent,
                StatisticsAgent(
                    last_month_values=last_month_values,
                    min_values=min_values,
                    avg_values=avg_values,
                    max_values=max_values,
                    model=self.model
                ).agent
            ],
            tools=[
                # last_month_tool,
                # min_max_avg_tool,
            ],

        )

        fail_counter = 0
        while True:
            try:
                if fail_counter > 5:
                    break
                response = self.agent.run(question)
                response = int(response)
                break
            except Exception as e:
                fail_counter += 1

        return int(response)
