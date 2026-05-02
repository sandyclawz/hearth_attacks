import pandas as pd


class DataProcessor:
    def __init__(self, target_col="heart_attack_risk_binary", id_col="id"):
        self.target_col = target_col
        self.id_col = id_col

    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
            .str.replace(r"[()]", "", regex=True)
            .str.replace("-", "_", regex=False)
        )

        return df

    def clean_gender(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        gender_map = {
            "Male": "male",
            "Female": "female",
            "1.0": "male",
            "0.0": "female",
            1.0: "male",
            0.0: "female",
            1: "male",
            0: "female",
        }

        if "gender" in df.columns:
            df["gender"] = df["gender"].replace(gender_map)

        return df

    def prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.clean_gender(df)
        df = df.drop(columns=["unnamed:_0", "unnamed_0"], errors="ignore")

        return df

    def prepare_test(self, df: pd.DataFrame):
        df = self.prepare_dataframe(df)

        if self.id_col not in df.columns:
            raise ValueError(f"В файле отсутствует обязательная колонка `{self.id_col}`")

        ids = df[self.id_col].copy()

        X = df.drop(
            columns=[self.id_col, self.target_col],
            errors="ignore"
        )

        return X, ids