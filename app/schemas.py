from pydantic import BaseModel


class PredictionRequest(BaseModel):
    file_path: str


class PredictionResponse(BaseModel):
    status: str
    rows_count: int
    predictions: list[dict]