
from smolagents import CodeAgent, OpenAIServerModel, tool, ToolCallingAgent

@tool
def get_context() -> str:
    """
    Get context.
    """
    return f"You should score the employee based on the records from the Security Department, his debt, his spendings"

@tool
def get_person() -> str:
    """
    Get person.
    """
    return f"Calm and reasonable, no debt, gambler"



# Configure the model to connect to LM Studio's API
model = OpenAIServerModel(
    model_id="mistral-small-latest",  # Replace with your loaded model's name
    api_base="https://api.mistral.ai/v1",  # LM Studio's API endpoint
    api_key="MHf2OOExuaY2ZklA0tUiUhIJ0xiKzsNz"  # Dummy API key; LM Studio doesn't require authentication
)

# Initialize the agent with the configured model and no additional tools
agent = ToolCallingAgent(tools=[get_context, get_person], model=model )

# Define the question to be processed
question = """Score the following person based on these metrics
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

# Run the agent with the question
response = agent.run(question)

# Output the response
print("""
=======================================
=======================================
=======================================
=======================================
=======================================
=======================================
=======================================
=============ENDENDEND=================
=======================================
=======================================
=======================================
=======================================
=======================================
=======================================
=======================================
""")
print(response)
