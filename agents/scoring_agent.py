from smolagents import ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool, tool, Tool, VisitWebpageTool
import logging
from typing import Dict
from agents.tools.last_month import LastMonthTool
from agents.tools.min_max_avg import MinMaxAvgTool
from agents.tools.rag import RetrieverTool

class ScoringAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
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
        return """
            You 
        """
    
    def score_metrics(self, metrics, last_month_values: list, min_values: list, avg_values: list, max_values: list, metrics_docs) -> str:
        """
        Score a metrics based on the provided metrics.
        """
        question = f"SLA: {metrics.sla}, VISIBILITY: {metrics.visibility}, AVG_DURATION: {metrics.avg_duration}, DENSITY_BY_COMPANY: {metrics.density_by_company}, DENSITY_BY_OWNERBLOCK: {metrics.density_by_ownerblock}, DENSITY_BY_APPLICATION: {metrics.density_by_application}"
        
        search_tool = DuckDuckGoSearchTool()
        min_max_avg_tool = MinMaxAvgTool(min_values, avg_values, max_values)
        last_month_tool = LastMonthTool(last_month_values)
        metrics_rag_tool = RetrieverTool(docs=metrics_docs)

        self.agent = ToolCallingAgent(model=self.model, tools=[
            # search_tool,
            self.get_context, 
            # last_month_tool,
            # min_max_avg_tool,
            metrics_rag_tool
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
