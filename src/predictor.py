from pathlib import Path

import joblib
import pandas as pd

from src.data_processor import DataProcessor


class HeartAttackPredictor:
    def __init__(self, model_path: str = "models/final_model.joblib"):
        self.model_path = Path(model_path)
        self.processor = DataProcessor()
        self.model = None

    def load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Файл модели не найден: {self.model_path}")

        self.model = joblib.load(self.model_path)

    def predict_from_csv(self, csv_path: str) -> pd.DataFrame:
        if self.model is None:
            self.load_model()

        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV-файл не найден: {csv_path}")

        df = pd.read_csv(csv_path)

        X, ids = self.processor.prepare_test(df)

        predictions = self.model.predict(X).astype(int)

        result = pd.DataFrame({
            "id": ids,
            "prediction": predictions
        })

        return result