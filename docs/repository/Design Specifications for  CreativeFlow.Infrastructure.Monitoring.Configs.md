# Software Design Specification (SDS) for CreativeFlow.Infrastructure.Monitoring.Configs

## 1. Introduction

### 1.1 Purpose
This document provides a detailed technical specification for the `CreativeFlow.Infrastructure.Monitoring.Configs` repository. This repository implements the "Observability as Code" strategy for the CreativeFlow AI platform. It contains all the necessary configuration files to set up, manage, and maintain the comprehensive monitoring, logging, and alerting stack as defined in SRS sections `QA-003`, `DEP-005`, and `MON-001` through `MON-013`.

The configurations herein will be version-controlled and deployed via the CI/CD pipeline, ensuring a consistent, repeatable, and auditable observability infrastructure across all environments (Development, Staging, Production, DR).

### 1.2 Scope
The scope of this repository is strictly limited to the configuration files for the following tools:
-   **Metrics & Alerting:** Prometheus, Alertmanager
-   **Visualization:** Grafana
-   **Logging & Analysis:** ELK Stack (Elasticsearch, Logstash, Kibana, Filebeat) or Grafana Loki Stack
-   **Distributed Tracing & Telemetry:** OpenTelemetry Collector

This document specifies the structure, content, and logic of these configuration files. It does not cover the deployment or management of the tools' server infrastructure, which is handled by the IaC repository (`CreativeFlow.Infrastructure.Ansible`).

## 2. System Overview & Design Principles

The monitoring configuration adheres to the following core principles:

-   **Observability as Code:** All configurations (scrape jobs, rules, dashboards, log pipelines) are defined in version-controlled text files (YAML, JSON), enabling GitOps workflows.
-   **Dynamic Configuration:** Service discovery is prioritized to automatically detect and monitor new service instances without manual configuration changes, supporting a scalable microservices architecture.
-   **Modularity & Reusability:** Configurations are broken down into logical files by service or function (e.g., separate rule files for platform vs. application) to improve maintainability.
-   **Standardization:** A standardized, structured JSON format for logs is enforced across the entire platform to enable efficient parsing, searching, and analysis.
-   **Traceability:** All logs, metrics, and traces will be correlated using a unique `trace_id` propagated across service calls, enabling end-to-end request visibility.

## 3. Prometheus Configuration (`prometheus/`)

### 3.1 Master Configuration (`prometheus.yml`)
This is the main entry point for the Prometheus server.

-   **`global`:**
    -   `scrape_interval`: `15s` (default)
    -   `evaluation_interval`: `15s`
-   **`rule_files`:**
    -   Includes all `*.rules.yml` files from the `rules/` directory.
    -   Example: `- /etc/prometheus/rules/*.rules.yml`
-   **`scrape_configs`:**
    -   A list of jobs, one for each major service category.
    -   Each job will use the `file_sd_configs` mechanism to read targets from the `targets/file_sd/` directory. This is critical for dynamic target management (`MON-002`).
    -   **Relabeling (`relabel_configs`)** will be used to add environment labels and other metadata from the service discovery files to the scraped metrics.

yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "/etc/prometheus/rules/*.rules.yml"

scrape_configs:
  - job_name: 'application-services'
    file_sd_configs:
      - files: ['/etc/prometheus/targets/file_sd/application-services.json']
    relabel_configs:
      # Add standard labels from SD file
      - source_labels: [__meta_file_sd_service_name]
        target_label: service
      - source_labels: [__meta_file_sd_environment]
        target_label: env

  - job_name: 'infrastructure-services'
    file_sd_configs:
      - files: ['/etc/prometheus/targets/file_sd/infrastructure-services.json']
    # ... similar relabel_configs

  - job_name: 'ai-cluster-nodes'
    file_sd_configs:
      - files: ['/etc/prometheus/targets/file_sd/ai-cluster.json']
    # ... similar relabel_configs


### 3.2 Service Discovery Targets (`prometheus/targets/file_sd/`)
These JSON files provide Prometheus with dynamic lists of endpoints to scrape. They will be managed and updated by Ansible or a service registration system.

-   **`application-services.json`, `infrastructure-services.json`, `ai-cluster.json`:**
    -   **Schema:** A JSON array of objects.
    -   **Object Structure:**
        -   `targets`: An array of strings, where each string is a `host:port` of a target to scrape.
        -   `labels`: A key-value map of labels to attach to all metrics from these targets (e.g., `service: "user-management-api"`, `env: "production"`).

json
// prometheus/targets/file_sd/application-services.json - Example
[
  {
    "targets": ["10.0.1.10:8000", "10.0.1.11:8000"],
    "labels": {
      "service": "api-gateway",
      "env": "production"
    }
  },
  {
    "targets": ["10.0.2.5:9100"],
    "labels": {
      "service": "odoo-backend",
      "env": "production"
    }
  }
]


### 3.3 Alerting & Recording Rules (`prometheus/rules/`)
These files contain the core logic for monitoring and alerting, fulfilling requirements `MON-011`, `MON-012`, and `MON-013`.

#### 3.3.1 `platform.rules.yml`
Focuses on infrastructure health.

-   **Host Metrics:**
    -   `HostHighCpuLoad`: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100) > 90` for 5 minutes.
    -   `HostOutOfMemory`: `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10` for 5 minutes.
    -   `HostDiskWillFillIn4Hours`: `predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4 * 3600) < 0` for 10 minutes.
-   **Service Availability:**
    -   `TargetDown`: `up == 0` for 1 minute.
-   **Annotations:** Must include a summary, description, and a link to a runbook.

#### 3.3.2 `application.rules.yml`
Focuses on application performance and business KPIs.

-   **API Performance:**
    -   `HighApiErrorRate`: `sum(rate(http_requests_total{status=~"5.."}[5m])) by (job, service) / sum(rate(http_requests_total[5m])) by (job, service) * 100 > 5` for 2 minutes.
    -   `HighApiLatency`: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job, service)) > 0.5` for 5 minutes. (Targets NFR-001/KPI-004)
-   **Business Metrics:**
    -   `LowRegistrationSuccessRate`: `sum(rate(registration_success_total[10m])) / (sum(rate(registration_success_total[10m])) + sum(rate(registration_failure_total[10m]))) < 0.95` for 10 minutes (if both metrics are non-zero). (Targets KPI-001)

#### 3.3.3 `ai-pipeline.rules.yml`
Specific alerts for the AI workflow, crucial for `MON-013`.

-   **Queueing:**
    -   `RabbitMQQueueHigh`: `rabbitmq_queue_messages_ready > 1000` for 5 minutes.
-   **Workflow Performance:**
    -   `N8NWorkflowSlow`: `histogram_quantile(0.90, sum(rate(n8n_workflow_execution_time_seconds_bucket[10m])) by (le, workflow_name)) > 30` for sample generation workflows.
    -   `AIGenerationErrorRateHigh`: `sum(rate(ai_generation_requests_total{status="failed"}[10m])) by (model_name) / sum(rate(ai_generation_requests_total[10m])) by (model_name) > 2` for 5 minutes. (Targets KPI-004)
-   **GPU Health:**
    -   `GpuHighTemperature`: `dcgm_gpu_temp_celsius > 85` for 3 minutes.
    -   `GpuHighUtilization`: `avg by (instance, gpu) (dcgm_gpu_utilization[5m]) > 95` for 10 minutes.

## 4. Alertmanager Configuration (`alertmanager/alertmanager.yml`)
This file orchestrates alert notifications, implementing the escalation matrix from `QA-003.1` and `MON-012`.

-   **`global`:** Defines default settings, like SMTP server or Slack API URL (though secrets should be in env vars).
-   **`route`:** The core routing tree.
    -   `group_by`: `['alertname', 'service', 'env']` to group related alerts.
    -   `group_wait`: `30s`
    -   `group_interval`: `5m`
    -   `repeat_interval`: `4h`
    -   `receiver`: `'default-slack-receiver'` (a low-priority default).
    -   `routes`: A list of sub-routes to match specific alerts.
-   **`receivers`:** Defines the notification channels.
-   **`inhibit_rules`:** Defines rules to suppress alerts (e.g., suppress all alerts for a host if the `HostDown` alert is firing).

yaml
# alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'service', 'env']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack-notifications'

  # Sub-routes for escalation
  routes:
    - receiver: 'pagerduty-sre-oncall'
      matchers:
        - severity="critical"
      continue: true # Allow it to also go to Slack

    - receiver: 'slack-backend-alerts'
      matchers:
        - severity="warning"
        - team="backend"

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: '{{ template "slack.default.apiurl" . }}' # Use template for secret
        channel: '#general-alerts'
        text: '{{ template "slack.default.text" . }}'

  - name: 'pagerduty-sre-oncall'
    pagerduty_configs:
      - routing_key: '{{ .CommonLabels.pd_routing_key | default "YOUR_DEFAULT_ROUTING_KEY" }}'
        # Templates for rich notifications


## 5. Grafana Provisioning (`grafana/`)
Dashboards and data sources managed as code (`MON-003`).

### 5.1 Data Sources (`grafana/provisioning/datasources/datasources.yml`)
Configures connections to Prometheus and the logging backend.

yaml
# grafana/provisioning/datasources/datasources.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090 # Internal service name
    access: proxy
    isDefault: true
  - name: Loki
    type: loki
    url: http://loki:3100
    access: proxy
  # OR
  - name: Elasticsearch
    type: elasticsearch
    url: http://elasticsearch:9200
    access: proxy
    jsonData:
      timeField: "@timestamp"


### 5.2 Dashboards (`grafana/provisioning/dashboards/json/`)
The JSON models for key dashboards. These are complex files, so the spec will define the key panels and queries.

-   **`system-overview.json`:**
    -   **Panels:** Stat panels for KPIs (Active Users, API Error Rate %, AI Success Rate %). Time series graphs for API latency (P95, P99), AI generation throughput, DB query performance.
    -   **Queries:** `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`, `histogram_quantile(...)`.
-   **`ai-pipeline-deep-dive.json`:**
    -   **Variables:** Dropdowns to filter by `workflow_name` and `model_name`.
    -   **Panels:** Time series for RabbitMQ queue depth (`rabbitmq_queue_messages_ready`). Time series for n8n execution latency (`n8n_workflow_execution_time_seconds_bucket`). Heatmap for GPU utilization (`dcgm_gpu_utilization`). Table of recent AI generation errors.
-   **`logs-overview.json`:**
    -   **Data Source:** Loki or Elasticsearch.
    -   **Variables:** Dropdowns for `service`, `env`, `level`.
    -   **Panels:** "Logs" panel for interactive querying. Pie chart of `count by (level)`. Time series of log volume (`rate(log_messages_total[1m])`).

## 6. Logging Pipeline Configuration

### 6.1 Option A: ELK Stack (`elk/`)
The specification for using Elasticsearch, Logstash, and Kibana.

-   **`elk/filebeat/filebeat.yml`:**
    -   Uses autodiscover for container logs on Docker/Kubernetes.
    -   `filebeat.autodiscover.providers`: type `docker`.
    -   `hints.enabled: true` to use container labels for metadata.
    -   `output.logstash`: hosts `["logstash:5044"]`.
-   **`elk/logstash/pipeline/logstash.conf`:**
    -   `input { beats { port => 5044 } }`
    -   `filter { if [container][name] { ... } json { source => "message" } grok { match => { "message" => "%{COMBINEDAPACHELOG}" } } ... }`
    -   `output { elasticsearch { hosts => ["http://elasticsearch:9200"] index => "creativeflow-logs-%{+YYYY.MM.dd}" } }`
-   **`elk/elasticsearch/index-templates/creativeflow-logs-template.json`:**
    -   `index_patterns`: `["creativeflow-logs-*"]`.
    -   `template.settings.index.lifecycle.name`: `"creativeflow-ilm-policy"`.
    -   `template.mappings.properties`: Defines fields like `@timestamp` (date), `trace_id` (keyword), `http.status_code` (integer), `message` (text). This enforces the Standardized Log Schema.
    -   An associated ILM policy will define phases: `hot` (7 days), `warm` (30 days), `cold` (90 days), `delete` (365 days), as per `MON-007`.

## 7. Distributed Tracing Configuration (`opentelemetry/`)
Specification for the OpenTelemetry Collector (`MON-008`).

-   **`opentelemetry/otel-collector-config.yml`:**
    -   **`receivers.otlp`:** Configured to receive traces over gRPC and HTTP.
    -   **`processors.batch`:** Batches telemetry to reduce export calls.
    -   **`exporters`:**
        -   `jaeger`: endpoint `jaeger-collector:14250`.
        -   `prometheus`: endpoint `0.0.0.0:8889` (for metrics derived from spans, e.g., RED metrics).
        -   `loki`: endpoint `loki:3100/loki/api/v1/push` (to correlate traces with logs).
    -   **`service.pipelines.traces`:** `receivers: [otlp] -> processors: [batch] -> exporters: [jaeger, loki]`.
    -   **`service.pipelines.metrics`:** `receivers: [otlp] -> processors: [batch] -> exporters: [prometheus]`.

## 8. Data Models & Schemas

### 8.1 Standardized Log Schema
All logs shipped to the central logging system MUST conform to the following structured JSON schema (`MON-005`).

json
{
  "@timestamp": "2025-06-18T12:51:09.123Z",
  "log.level": "INFO", // e.g., INFO, WARN, ERROR, DEBUG
  "service.name": "user-management-api",
  "service.version": "1.2.3",
  "host.name": "prod-app-server-01",
  "trace.id": "a1b2c3d4e5f67890", // Correlation ID
  "span.id": "f9e8d7c6b5a43210",
  "message": "User login successful",
  "details": {
    "user.id": "uuid-of-the-user",
    "http.request.method": "POST",
    "http.request.path": "/api/v1/auth/login",
    "http.response.status_code": 200,
    "duration_ms": 55,
    "error.stack_trace": null // Populated on ERROR level
  }
}


## 9. Security Considerations

-   **Secrets Management:** All sensitive information in configuration files (e.g., Alertmanager `api_url`, Grafana `secureJsonData`, Logstash passwords) MUST NOT be hardcoded. They must be referenced as environment variables, which are injected securely at deploy time by the CI/CD pipeline from a secrets manager like HashiCorp Vault.
-   **Network Access:** Network policies must restrict access to monitoring components. For example, Prometheus should only be accessible from Grafana and Alertmanager. The logging system's ingestion port should only be accessible from authorized log shippers.

This SDS provides a comprehensive blueprint for creating the configuration files that will drive the CreativeFlow AI platform's entire observability stack, ensuring traceability back to all functional and non-functional requirements.