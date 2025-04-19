from smolagents import ToolCallingAgent, OpenAIServerModel, tool, DuckDuckGoSearchTool
import logging
# from smolagents.prompts import TOOL_CALLING_SYSTEM_PROMPT

class ScoringAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
        """
        Initialize the ScoringAgent with the model configuration.
        """
        self.model = OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        )

        self.search_tool = DuckDuckGoSearchTool()

        self.agent = ToolCallingAgent(model=self.model, tools=[self.get_context, self.search_tool])
        

    @staticmethod
    @tool
    def get_context() -> str:
        """
        Get context for scoring.
        """
        return (
            """Score the following person based on these metrics
            Metrics: Records from security: Violent or not?, What is his debt?, What he spends his money on?

            Your final answer should be a number, ranging from 0 to 10. 

            Example question 1:
            Violent, no debt, no gambling
            Example answer 1:
            4

            Example question 2:
            Calm, 300 rub. debt, gambler
            Example answer 2:
            2

            Example question 3:
            Reasonable, Charizmatic, 100 rub. debt. debt, no gambling
            Example answer 3:
            8
            """
        )
    
    def score_person(self, metrics) -> str:
        """
        Score a person based on the provided metrics.
        """
        question = f"Score the following person based on these metrics\n{metrics.attitute}, {metrics.gambling}, {metrics.debt}"
        
        fail_counter = 0
        while True:
            try:
                if fail_counter > 3:
                    break
                response = self.agent.run(question)
                response = int(response)
                break
            except Exception as e:
                fail_counter += 1
                raise Exception("Failed to get a valid response after multiple attempts.")

        return response
