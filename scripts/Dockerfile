FROM python:3.12-slim

WORKDIR /app

COPY scripts/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts ./scripts
COPY shared ./shared

CMD ["sh"]