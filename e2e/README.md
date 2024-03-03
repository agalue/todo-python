# TODO Application end-to-end Test

The provided Docker compose will deploy the following applications:

- Grafana Mimir (to store metrics sent by OTEL Collector)
- Grafana Loki (to store logs sent by OTEL Collector)
- Grafana Tempo (to store traces sent by OTEL Collector)
- OpenTelemetry Collector (receiving data from the API and export it to the Grafana LGTM Stack)
- Prometheus collecting metrics from all the applications
- Grafana with data sources to explore all the collected data
- PostgreSQL (as the backend for the TODO API)
- TODO API (compiled from source), available at http://localhost:8080/todos
- TODO Vue UI (compiled from source), available at http://localhost:8081/

```bash
docker compose up -d
```