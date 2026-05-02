# Heart Attack Risk Prediction

Проект предсказывает риск сердечного приступа по данным пациента.

Приложение реализовано на **FastAPI**: принимает путь к CSV-файлу, выполняет предсказание и возвращает результат в JSON.

---

## Структура проекта

```text
heart_attacks/
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── src/
│   ├── data_processor.py
│   └── predictor.py
│
├── models/
│   └── final_model.joblib
│
├── data/
│   ├── raw/
│   │   ├── heart_train.csv
│   │   └── heart_test.csv
│   └── predictions/
│       └── submission.csv
│
├── notebooks/
│   └── research.ipynb
│
├── scripts/
│   ├── test_api.py
│   └── test.py
│
├── requirements.txt
└── README.md
```

---

## Установка

Проект рекомендуется запускать через conda-окружение `ds`.

```bash
conda create -n ds python=3.12
conda activate ds
pip install -r requirements.txt
```

Минимальный `requirements.txt`:

```text
pandas
numpy
scipy
scikit-learn==1.8.0
fastapi
uvicorn
pydantic
joblib
requests
matplotlib
seaborn
jupyterlab
notebook
ipykernel
```

Важно: модель `models/final_model.joblib` сохранена в окружении со `scikit-learn==1.8.0`.

Проверить версию:

```bash
python -c "import sklearn; print(sklearn.__version__)"
```

---

## Модель

Перед запуском API в проекте должен быть файл:

```text
models/final_model.joblib
```

Если модель сохраняется из ноутбука в папке `notebooks/`, используйте путь:

```python
final_model = FinalModel(
    best_model,
    model_path="../models/final_model.joblib"
)

final_model.fit(X, y)
final_model.save()
```

Если версия `scikit-learn` была изменена, модель нужно заново обучить и сохранить в том же окружении.

---

## Запуск API

Из корня проекта:

```bash
conda activate ds
python -m uvicorn app.main:app --reload
```

После запуска API доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger-документация:

```text
http://127.0.0.1:8000/docs
```

---

## Запрос к API

В Swagger откройте:

```text
POST /predict
```

Пример тела запроса:

```json
{
  "file_path": "data/raw/heart_test.csv"
}
```

Пример ответа:

```json
{
  "status": "success",
  "rows_count": 966,
  "predictions": [
    {
      "id": 7746,
      "prediction": 0
    },
    {
      "id": 4202,
      "prediction": 1
    }
  ]
}
```

Где:

- `id` — идентификатор пациента;
- `prediction`:
  - `0` — низкий риск;
  - `1` — высокий риск.

---

## Проверка API через скрипт

Файл:

```text
scripts/test_api.py
```

Запуск:

```bash
conda activate ds
python scripts/test_api.py
```

Пример содержимого:

```python
import requests


url = "http://127.0.0.1:8000/predict"

payload = {
    "file_path": "data/raw/heart_test.csv"
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print(response.json())
```

---

## Файл предсказаний

Итоговый файл должен лежать здесь:

```text
data/predictions/submission.csv
```

Формат файла:

```csv
,id,prediction
0,7746,0
1,4202,1
2,6632,0
```

Файл нужно сохранять с индексом:

```python
submission.to_csv("data/predictions/submission.csv", index=True)
```

Это важно, потому что проверочный скрипт читает файл через:

```python
pd.read_csv(args.student, index_col=0)
```

После чтения должны остаться две колонки:

```text
id
prediction
```

---

## Проверка качества модели

Проверочный скрипт:

```text
scripts/test.py
```

Запуск:

```bash
conda activate ds
python scripts/test.py --student data/predictions/submission.csv --correct correct_answers.csv
```

Скрипт проверяет:

- наличие колонок `id` и `prediction`;
- совпадение количества строк;
- выводит `classification_report`.

Основная метрика для сравнения моделей — `macro avg f1-score`.

Если файла `correct_answers.csv` нет, локально можно проверить только формат `submission.csv`.

---

## Основные классы

`DataProcessor` — подготовка данных: переименование колонок, обработка `gender`, удаление технических колонок.

`HeartAttackPredictor` — загрузка модели, чтение CSV, предобработка, предсказание и возврат результата.

---

## Краткий порядок запуска

```bash
conda activate ds
cd "../heart_attacks"
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Далее откройте:

```text
http://127.0.0.1:8000/docs
```

и выполните запрос к методу:

```text
POST /predict
```

с телом:

```json
{
  "file_path": "data/raw/heart_test.csv"
}
```

---

## Частые ошибки

### `Method Not Allowed`

Ошибка появляется, если открыть `/predict` в браузере обычным GET-запросом.

Для предсказания используйте Swagger:

```text
http://127.0.0.1:8000/docs
```

или отправляйте POST-запрос.

### `No module named uvicorn`

Установите зависимости:

```bash
pip install -r requirements.txt
```

или отдельно:

```bash
pip install uvicorn fastapi
```

### `Can't get attribute ... sklearn`

Версия `scikit-learn` в окружении не совпадает с версией, в которой сохранена модель.

Для проекта нужна версия:

```text
1.8.0
```

### `CSV-файл не найден`

Проверьте путь в запросе:

```json
{
  "file_path": "data/raw/heart_test.csv"
}
```

Путь указывается относительно корня проекта.

---

## Автор

Sergey Kiselev  
sandyclawz@gmail.com

Проект выполнен в рамках учебного проекта по машинному обучению на Яндекс.Практикум.