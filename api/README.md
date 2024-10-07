# TODO Application API

A simple TODO ReST API implemented with FastAPI and sqlModel (based on SQLAlchemy) in asynchronous mode for testing purposes.

It has OpenTelemetry auto-instrumentation enabled.

Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U -r requirements.txt
```

Run PostgreSQL via Docker:

```bash
docker run -d --rm --name postgres \
  -e POSTGRES_DB=todo \
  -e POSTGRES_USER=postgres
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine
```

Run API without OpenTelemetry for development:

```bash
uvicorn main:app --reload
```

To run the API with OpenTelemetry enabled, deploy the OTEL Collector as follows:

```bash
docker run -d --rm --name otelcol \
  -p 4317:4317 \
  otel/opentelemetry-collector-contrib:latest
```

Then,

```bash
export OTEL_SERVICE_NAME=api
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_PYTHON_LOG_CORRELATION=true

opentelemetry-instrument uvicorn main:app
```
