from smolagents import  OpenAIServerModel, CodeAgent
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

            You are managing 3 agents that can help you accomplish this task:
                1. A web search agent. It is very helpful to clarify the question and find the answer.
                2. A retriever agent to search related documents
                3. A statistics agent to compare current values with the historical ones from the company. This however does not help you grade the metrics, but it can help you understand the context of the metrics.

            You should use web search to clarify the metrics before useing statistics agent to compare the current values with the historical ones. 
            If you feel like you still lack clarity about the metrics, you can use the retriever agent to search related documents.

            Your final answer should be a number, ranging from 0 to 10. Where 0-3 is good, 4-6 is medium, and 7-10 is bad.\n
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
            tools=[],
            max_steps=15
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
