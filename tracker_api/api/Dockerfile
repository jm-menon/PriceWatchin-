FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY tracker_api/api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY tracker_api/api/ .
COPY scripts/bootstrap_database.py .
COPY infra/postgres/init.sql ./init.sql
COPY shared ./shared

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]
