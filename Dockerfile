FROM python:3.12.7

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pdf

RUN apt update && \
    apt install -y htop libgl1-mesa-glx libglib2.0-0


COPY requirements.txt . 

RUN pip install -r requirements.txt



COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
