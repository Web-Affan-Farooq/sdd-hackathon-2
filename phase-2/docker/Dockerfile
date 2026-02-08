FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "backend.src.api.main:app"]