FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY workers/scraper/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY workers/scraper ./scraper
COPY shared ./shared

CMD ["python", "scraper/main.py"]