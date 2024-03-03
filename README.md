# TODO Application with FastAPI and OpenTelemetry

A Simple TODO ReST API implemented with FastAPI and sqlModel backed by PostgreSQL in an async mode that sends telemetry metrics, logs, and traces to an OpenTelemetry Collector, which in turn will forward observability data to Grafana's LGTM stack.

The LGTM Stack and the OTEL Collector are monitored via Prometheus to gather performance metrics.
