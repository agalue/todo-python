# TODO Application end-to-end Test

The provided Docker compose will deploy the following applications:

- Grafana Mimir (to store metrics sent by OTEL Collector), exposed on port 9009.
- Grafana Loki (to store logs sent by OTEL Collector), exposed on port 3100.
- Grafana Tempo (to store traces sent by OTEL Collector), exposed on port 3200.
- OpenTelemetry Collector (receiving data from the API and export it to the Grafana LGTM Stack), exposed on ports 4317 (gRPC), and 4318 (http).
- Prometheus collecting metrics from all the applications, exposed on port 9090.
- Grafana with data sources to explore all the collected data, exposed on port 3000.
- PostgreSQL (as the backend for the TODO API), exposed on port 5432.
- TODO API (compiled from source), exposed on port 8080 (with a Swagger UI available at http://localhost:8080/docs/).
- TODO Vue UI (compiled from source), exposed on port 8081 (e.x. http://localhost:8081/).

To start the environment, do the following (assuming you're running Linux or you have either [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [OrbStack](https://orbstack.dev/) installed):

```bash
docker compose pull
docker compose build
docker compose up -d
```

Grafana contains data sources for Prometheus, Mimir, Loki and Tempo.

To bring it down:

```bash
docker compose down -v
```

## Visualize Data

Using the Explore view in Grafana, you can choose the proper data source and start exploring the collected OTEL data. Use Mimir for metrics, Loki for logs and Tempo for traces. To look into performance metrics from the running applications, use the Prometheus data source.
