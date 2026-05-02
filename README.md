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

Создайте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Минимальный `requirements.txt`:

```text
pandas
numpy
scikit-learn==1.6.1
fastapi
uvicorn
pydantic
joblib
requests
```

Важно: версия `scikit-learn` должна совпадать с версией, в которой была сохранена модель `final_model.joblib`.

---

## Модель

Перед запуском API в проекте должен быть файл:

```text
models/final_model.joblib
```

Если модель сохраняется из ноутбука, расположенного в папке `notebooks/`, используйте путь:

```python
final_model = FinalModel(
    best_model,
    model_path="../models/final_model.joblib"
)

final_model.fit(X, y)
final_model.save()
```

---

## Запуск API

Из корня проекта:

```bash
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

В Swagger откройте метод:

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

Формат:

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

---

## Проверка качества модели

Проверочный скрипт:

```text
scripts/test.py
```

Запуск:

```bash
python scripts/test.py --student data/predictions/submission.csv --correct correct_answers.csv
```

Скрипт проверяет:

- наличие колонок `id` и `prediction`;
- совпадение количества строк;
- выводит `classification_report`.

Основная метрика для сравнения моделей — `macro avg f1-score`.

---

## Частые ошибки

### `No module named uvicorn`

Установите `uvicorn`:

```bash
pip install uvicorn fastapi
```

Запускать лучше так:

```bash
python -m uvicorn app.main:app --reload
```

### `Can't get attribute ... sklearn`

Версии `scikit-learn` в ноутбуке и в окружении API не совпадают.

Проверьте версию в Jupyter:

```python
import sklearn
print(sklearn.__version__)
```

Проверьте версию в терминале:

```bash
python -c "import sklearn; print(sklearn.__version__)"
```

Установите нужную версию:

```bash
pip install scikit-learn==1.6.1 --force-reinstall
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

## Основные классы

`DataProcessor` — подготовка данных: переименование колонок, обработка `gender`, удаление технических колонок.

`HeartAttackPredictor` — загрузка модели, чтение CSV, предобработка, предсказание и возврат результата.

---

## Автор
Sergey Kiselev (sandyclawz@gmail.com).
Проект выполнен в рамках учебного проекта по машинному обучению на Яндекс.Практикум.