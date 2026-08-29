FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    ninja-build \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY workers/scraper/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY workers/scraper ./scraper
COPY shared ./shared

CMD ["python", "scraper/main.py"]
###################################
#FROM python:3.12-slim

#ENV PYTHONUNBUFFERED=1

#WORKDIR /app

#RUN apt-get update && apt-get install -y \
 #   git \
  #  cmake \
   # ninja-build \
    #build-essential \
    #&& rm -rf /var/lib/apt/lists/*

#COPY workers/scraper/requirements.txt ./requirements.txt

#RUN pip install --no-cache-dir -r requirements.txt

#COPY workers/scraper ./scraper
#COPY shared ./shared

#CMD ["python", "-m", "scraper.main"]