FROM python:3.11-slim
EXPOSE 8080
WORKDIR /code
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["opentelemetry-instrument", "--traces_exporter", "otlp", "--metrics_exporter", "otlp", "--logs_exporter", "otlp", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]