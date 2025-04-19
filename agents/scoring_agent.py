from smolagents import  OpenAIServerModel, CodeAgent
from agents.managed_agents import RagAgent, WebAgent

class ScoringAgent:
    def __init__(self, model_id: str, api_base: str, api_key: str):
        self.model = OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key=api_key
        ) 
    
    def score_person(self, characterization:str, total_debt: str, violations_shops: dict, violations_investigations:dict, urls_payments:list, scoring_docs) -> str:
        """
        Score a person based on the provided data.
        """

        system = """
        You are a hiring personel assessor for a telecom company. 
        You review the information about the current and potential employees of the company, based on the provided data.

        Here is a description of each field of information you might get:
            * characterization: A short description of the person.
            * total_debt: This is the total debt the employee has in the company. This could be due to vacation cancellations, sick leaves or other reasons.
            Nonetheless, this is a red flag if a person has a high debt.
            * violations_shops: Violations in shops. These are documented via camera recordings. Some of the violations might be critical, but some of them might not be.
            * violations_investigations: You should carefully consider all investigations. Some of the violations might be critical, but some of them might not be. 
            You should check the details of each investigation.
            * urls_payments: The urls of the payments the person has made with the monthly spendings in rubles (Average salary is 80000). 
            You should check them to see if there are risks of gambling or others.

        You are managing 3 agents that can help you accomplish this task:
            1. A web search agent. Not all web pages contain malicious content, but some of them do. Don't be rash with your decisions, consider the results carefully.
            2. A retriever agent to search related documents. If you haven't found the answer in the web search, you can use this agent to find related documents.


        You should review the provided information and classify a person in on of the following categories:
            1. EXCELLENT: There are no known issues with the person based on currently provided information
            2. GOOD: Although there are some issues with the person, they are not critical and can be resolved.
            3. AVERAGE: There are things to consider about the person, but they are not critical.
            4. POOR: There are some serious issues. This person should be considered very carefully.
            5. BAD: This person should not be hired, if they are employeed they should be fired immidiately. There are serious issues with this person.

        Provide an answer with a category and your reasoning in the following format:
        Category: <category>, Reasoning: <reasoning> 

        Here is a person you should review:\n
        """
        person_attr = f"characterization: {characterization}, total_debt: {total_debt}\n"
        person_attr = person_attr + ', '.join([f"{key}: {val}" for key, val in violations_shops.items()]) + "\n"
        person_attr = person_attr + ', '.join([f"{key}: {val}" for key, val in violations_investigations.items()]) + "\n"
        person_attr = person_attr + ', '.join([f"{key}: {val}" for key, val in urls_payments.items()]) + "\n"
        question = system + person_attr

        self.agent = CodeAgent(
            model=self.model, 
            managed_agents =[
                RagAgent(
                    docs=scoring_docs,
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
                response = response
                break
            except Exception as e:
                fail_counter += 1

        return response
