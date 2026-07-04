FROM python:3.9-slim

WORKDIR /app

# This prevents Python from writing .pyc files and force stdout/stderr to be unbuffered
# Unbuffered output is critical for Docker logs to stream out in real-time
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "run.py", \
     "--input", "data.csv", \
     "--config", "config.yaml", \
     "--output", "metrics.json", \
     "--log-file", "run.log"]