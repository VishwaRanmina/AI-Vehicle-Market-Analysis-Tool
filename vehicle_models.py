
from pydantic import BaseModel
from pydantic.v1 import Field


class CarAnalysis(BaseModel):
    key_insights : str = Field(description="Key insights about the car deals")
    summary : str = Field(description="2-3 sentence summary")
    best_average_price : str = Field(description="Best average price to buy")