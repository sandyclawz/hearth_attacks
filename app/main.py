from fastapi import FastAPI, HTTPException

from app.schemas import PredictionRequest, PredictionResponse
from src.predictor import HeartAttackPredictor


app = FastAPI(
    title="Heart Attack Risk Prediction API",
    description="API для предсказания риска сердечного приступа по CSV-файлу",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Heart Attack Risk Prediction API is running"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        predictor = HeartAttackPredictor(
            model_path="models/final_model.joblib"
        )

        result = predictor.predict_from_csv(request.file_path)

        return {
            "status": "success",
            "rows_count": len(result),
            "predictions": result.to_dict(orient="records")
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при выполнении предсказания: {error}"
        )