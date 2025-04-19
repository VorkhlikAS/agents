from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import dotenv
import os
from agents.scoring_agent import ScoringAgent
from agents.criticallity_agent import CriticallityAgent
from models.models import PersonParams, MetricsParams

# Load environment variables from .env file
dotenv.load_dotenv(override=True)
# Set the OpenAI API key
api_key = os.getenv("API_KEY")
api_base = os.getenv("API_BASE")
model_id = os.getenv("MODEL_ID")

app = FastAPI()

scoring_agent = ScoringAgent(
    model_id=model_id,  
    api_base=api_base,  
    api_key=api_key 
)

ccriticallity_agent = CriticallityAgent(
    model_id=model_id,  
    api_base=api_base,  
    api_key=api_key 
)

def score_person(params: PersonParams) -> str:
    result = scoring_agent.score_person(params)
    return result

def score_metrics(params: MetricsParams) -> str:
    result = ccriticallity_agent.score_metrics(params, params.last_month_values, params.min, params.avg, params.max)
    return result

@app.post("/score_person")
def run_person_endpoint(data: PersonParams):
    try:
        result = score_person(data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/score_metrics")
def run_metrics_endpoint(data: MetricsParams):
    try:
        result = score_metrics(data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

