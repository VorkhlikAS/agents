from smolagents import  OpenAIServerModel, CodeAgent
from agents.managed_agents import RagAgent, WebAgent

class ScoringAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
        self.model = OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        ) 
    
    def score_metrics(self, person:dict, scoring_docs) -> str:
        """
        Score a person based on the provided data.
        """

        system = """
        You are a hiring personel assessor. You review the information about the current and potential employees of the company, based on the provided data.

        You are managing 3 agents that can help you accomplish this task:
            1. A web search agent. It is very helpful to clarify the question and find the answer.


        You should review the provided information and classify a person in on of the following categories:
            1. EXCELLENT: There are no known issues with the person based on currently provided information
            2. GOOD: Although there are some issues with the person, they are not critical and can be resolved.
            3. AVERAGE: There are things to consider about the person, but they are not critical.
            4. POOR: There are some serious issues. This person should be considered very carefully.
            5. BAD: This person should not be hired, if they are employeed they should be fired immidiately. There are serious issues with this person.

        """

        person_attr = ', '.join([f"{key}: {val}" for key, val in person.items()])
        question = f"person information {person_attr}"
        
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
