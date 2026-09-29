from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class AgeResponse(BaseModel):
    num: int = 10
    age: Decimal = Field(json_schema_extra={"type": "number"})

@app.get("/demo-age", response_model=AgeResponse)
def get_age() -> AgeResponse:
    return AgeResponse(num = 50, age=Decimal("20.5"))