from pydantic import BaseModel
from typing import List, Dict

class PersonParams(BaseModel):
    characterization: str
    total_debt: str
    violations_shops: Dict[str, str]
    violations_investigations: Dict[str, str]
    urls_payments: Dict[str, str]


class MetricsParams(BaseModel):
    sla: str
    visibility: str
    avg_duration: str
    density_by_company: str
    density_by_ownerblock: str
    density_by_application: str
    last_month_values: Dict[str, str]
    min: Dict[str, str] 
    max: Dict[str, str] 
    avg: Dict[str, str]



