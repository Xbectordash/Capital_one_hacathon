from pydantic import BaseModel,Field
from typing import List, Dict

class QueryUnderstandingSchema(BaseModel):
    intents: List[str] = Field(default_factory=list)
    entities: Dict[str, str] = Field(default_factory=dict)
    confidence_score: float = 0.0
