#FROM python:3.12-slim

#WORKDIR /app

#COPY requirements.txt .

#RUN pip install -r requirements.txt

#COPY simulators/ecomm-site-1/apps ./apps
#COPY shared ./shared

#CMD ["uvicorn","apps.main:app","--host","0.0.0.0","--port","8001"]

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY simulators/ecomm-site-1/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY simulators/ecomm-site-1/apps ./apps
COPY shared ./shared

CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8001"]
