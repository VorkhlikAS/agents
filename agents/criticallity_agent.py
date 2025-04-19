from smolagents import ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool, tool, Tool
import logging
from typing import Dict
from agents.tools.last_month import LastMonthTool
from agents.tools.min_max_avg import MinMaxAvgTool

class CriticallityAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
        """
        Initialize the CriticallityAgent with the model configuration.
        """
        self.model = OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        ) 

    @tool
    def get_context() -> str:
        """
        Get context for scoring.
        """
        return (
            "You are a security assessment agent that provides a mark based on the metrics."
            "Your task is to mark the results of the current vulnerability "
            "assessment of the company based on the following metrics:\n\n"
            "1. SLA: The ratio of tasks that were completed on time to the total number of tasks.\n"
            "2. Visibility: The ratio of hosts that are visible to the security team to the total number of hosts.\n"
            "3. Average duration: The average time it takes to complete a task in days.\n"
            "4. Density by company: Average number of critical vulnerabilities per unique FQDNs.\n"
            "5. Density by ownerblock: Average number of critical vulnerabilities per unique FQDNs, grouped by ownerblock.\n"
            "6. Density by application: Average number of critical vulnerabilities per unique FQDNs, grouped by application.\n\n"
            "Your final answer should be a number, ranging from 0 to 10. Where 0-3 is good, 4-6 is medium, and 7-10 is bad. "
            "You can use web search to look up the normal values for these parameters"
            "You can use min_max_avg_tool to look up what were the min, max, and average values for these parameters currently in the company\n"
            "You can use last_month_tool to look up what were the values for these parameters last month\n"
            "Provide a SINGLE number from 0 to 10 as an answer!"
        )
    
    def score_metrics(self, metrics, last_month_values: list, min_values: list, avg_values: list, max_values: list) -> str:
        """
        Score a metrics based on the provided metrics.
        """
        question = f"SLA: {metrics.sla}, VISIBILITY: {metrics.visibility}, AVG_DURATION: {metrics.avg_duration}, DENSITY_BY_COMPANY: {metrics.density_by_company}, DENSITY_BY_OWNERBLOCK: {metrics.density_by_ownerblock}, DENSITY_BY_APPLICATION: {metrics.density_by_application}"
        
        search_tool = DuckDuckGoSearchTool()
        min_max_avg_tool = MinMaxAvgTool(min_values, avg_values, max_values)
        last_month_tool = LastMonthTool(last_month_values)

        self.agent = ToolCallingAgent(model=self.model, tools=[
            search_tool,
            self.get_context, 
            last_month_tool,
            min_max_avg_tool,
        ])

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
