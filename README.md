# OTEL Python Playground

This repository contains a simple TODO ReST API implemented with [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/) backed by [PostgreSQL](https://www.postgresql.org/) in an async mode that sends telemetry metrics, logs, and traces to an OpenTelemetry [Collector](https://opentelemetry.io/docs/collector/), which in turn will forward observability data to Grafana's LGTM stack ([Loki](https://grafana.com/oss/loki/) for logs, [Grafana](https://grafana.com/oss/grafana/) for visualization, [Tempo](https://grafana.com/oss/tempo/) for traces, and [Mimir](https://grafana.com/oss/mimir/) for metrics). It also offers a simple WebUI implemeneted with [VueJS](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/en/).

The LGTM Stack and the OTEL Collector are monitored via [Prometheus](https://prometheus.io/) to gather performance metrics.

* The [api](api) folder contains the ReST API.
* The [ui](ui) folder contains the frontend UI.
* The [e2e](e2e) folder contains a Docker Compose to deploy the whole environment with all the dependencies.
