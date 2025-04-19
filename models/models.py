from pydantic import BaseModel
from typing import List, Dict

class PersonParams(BaseModel):
    attitute: str
    gambling: str
    debt: str

class MetricsParams(BaseModel):
    sla: str
    visibility: str
    avg_duration: str
    density_by_company: str
    density_by_ownerblock: str
    density_by_application: str
    last_month_values: Dict[str, str]  # Dictionary to store key-value pairs for last month's values
    min: Dict[str, str]  # Dictionary for minimum values
    max: Dict[str, str]  # Dictionary for maximum values
    avg: Dict[str, str]  # Dictionary for average values



