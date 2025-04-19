from smolagents import ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool, VisitWebpageTool, CodeAgent
from agents.tools.rag import RetrieverTool
from agents.tools.last_month import LastMonthTool
from agents.tools.min_max_avg import MinMaxAvgTool  


class ManagedAgent:
    def __init__(self, model: OpenAIServerModel):
        self.model = model


class RagAgent(ManagedAgent):
    def __init__(self, model: OpenAIServerModel, docs):
        """
        Initialize the RAG Agent with a model and documents.
        """
        super().__init__(model=model)
        metrics_rag_tool = RetrieverTool(docs=docs)
        self.agent = ToolCallingAgent(
            model=self.model,
            tools=[
                metrics_rag_tool
            ],
            name="rag_agent",
            description="An agent that retrieves info from documents. Give it a query as an argument"
        )


class WebAgent(ManagedAgent):
    def __init__(self, model: OpenAIServerModel):
        """
        Initialize the Web Agent with a model.
        """
        super().__init__(model=model)
        web_search_tool = DuckDuckGoSearchTool()
        visit_web_page_tool = VisitWebpageTool()
        self.agent = ToolCallingAgent(
            model=self.model,
            tools=[
                web_search_tool,
                visit_web_page_tool
            ],
            name="web_agent",
            description="An agent that searches web pages. Give it a query as an argument"
        )

class StatisticsAgent(ManagedAgent):
    def __init__(self, model: OpenAIServerModel, last_month_values: list, min_values: list, avg_values: list, max_values: list):
        """
        Initialize the Statistics Agent with a model.
        """
        super().__init__(model=model)
        last_month_tool = LastMonthTool(last_month_values)
        min_max_avg_tool = MinMaxAvgTool(
            min_values=min_values,
            avg_values=avg_values,
            max_values=max_values
        )
        self.agent = ToolCallingAgent(
            model=self.model,
            tools=[
                last_month_tool,
                min_max_avg_tool
            ],
            name="statistics_agent",
            description="An agent that compares the current metrics with the last month metrics. Give it a query as an argument"
        )
