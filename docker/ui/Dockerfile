FROM python:3.12-slim

WORKDIR /app

COPY requirements-ui.txt .
RUN pip install --no-cache-dir -r requirements-ui.txt

COPY src/ ./src/

WORKDIR /app/src

CMD ["python", "-m", "marketresearch.main"]
