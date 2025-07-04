# Specification

# 1. Files

- **Path:** prometheus/prometheus.yml  
**Description:** Main Prometheus configuration file. Defines global settings, scrape intervals, and includes rule files and service discovery targets. This file orchestrates the entire metrics collection strategy.  
**Template:** YAML Configuration Template  
**Dependency Level:** 1  
**Name:** prometheus.yml  
**Type:** Configuration  
**Relative Path:** prometheus/prometheus.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Metrics Collection
    - Service Discovery Configuration
    
**Requirement Ids:**
    
    - MON-001
    - MON-002
    - DEP-005
    - QA-003
    
**Purpose:** To configure the Prometheus server, defining what to scrape (targets) and how to evaluate data (rules).  
**Logic Description:** Contains global configuration blocks (global, scraping_config). Specifies paths to rule_files for alerting and recording rules. Defines scrape_configs for various services (node_exporter, application APIs, databases, message queues, AI cluster) using file_sd_configs pointing to the targets directory. This setup allows targets to be updated dynamically without restarting Prometheus.  
**Documentation:**
    
    - **Summary:** This file is the master configuration for the Prometheus monitoring system. It bootstraps the collection of all time-series metrics from across the CreativeFlow AI platform.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/targets/file_sd/application-services.json  
**Description:** File-based service discovery configuration for core application microservices, including the API Gateway, user management, creative management, etc. This file is managed automatically by a configuration management tool or service registration system.  
**Template:** JSON Configuration  
**Dependency Level:** 0  
**Name:** application-services.json  
**Type:** Configuration  
**Relative Path:** prometheus/targets/file_sd/application-services.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Microservice Metrics Scraping
    
**Requirement Ids:**
    
    - MON-002
    - DEP-005
    
**Purpose:** To provide Prometheus with a dynamic list of application service endpoints to scrape for metrics.  
**Logic Description:** A JSON array of objects. Each object represents a scrape target group and contains a 'targets' array with host:port strings of the application instances, and a 'labels' object for attaching metadata like service name, environment, and version.  
**Documentation:**
    
    - **Summary:** Defines the network endpoints for Prometheus to scrape metrics from application services. This allows for dynamic addition or removal of service instances.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/targets/file_sd/infrastructure-services.json  
**Description:** File-based service discovery for core infrastructure components like PostgreSQL (via postgres_exporter), RabbitMQ (via rabbitmq_exporter), Redis (via redis_exporter), and MinIO.  
**Template:** JSON Configuration  
**Dependency Level:** 0  
**Name:** infrastructure-services.json  
**Type:** Configuration  
**Relative Path:** prometheus/targets/file_sd/infrastructure-services.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Infrastructure Metrics Scraping
    
**Requirement Ids:**
    
    - MON-002
    - DEP-005
    
**Purpose:** To provide Prometheus with a dynamic list of infrastructure service endpoints to scrape for metrics.  
**Logic Description:** A JSON array of objects, similar to application-services.json, but for stateful services and middleware. Each entry defines targets and labels for a specific infrastructure component's exporter.  
**Documentation:**
    
    - **Summary:** Defines the network endpoints for Prometheus to scrape metrics from databases, message queues, and other infrastructure services.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/targets/file_sd/ai-cluster.json  
**Description:** File-based service discovery for the AI processing cluster. Includes targets for Kubernetes node metrics (via node_exporter) and GPU metrics (via DCGM exporter).  
**Template:** JSON Configuration  
**Dependency Level:** 0  
**Name:** ai-cluster.json  
**Type:** Configuration  
**Relative Path:** prometheus/targets/file_sd/ai-cluster.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - ServiceDiscovery
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - GPU Metrics Scraping
    - Kubernetes Node Metrics
    
**Requirement Ids:**
    
    - MON-002
    - DEP-005
    - INT-007
    - MON-010
    
**Purpose:** To enable Prometheus to monitor the health and performance of the GPU-enabled Kubernetes cluster.  
**Logic Description:** A JSON array defining target endpoints for node_exporter on each K8s worker and the service endpoint for the DCGM exporter, allowing collection of detailed GPU utilization, memory, and temperature metrics.  
**Documentation:**
    
    - **Summary:** Provides Prometheus with the necessary endpoints to collect vital performance metrics from the AI processing cluster's hardware and GPU resources.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/rules/platform.rules.yml  
**Description:** Prometheus rule file defining alerting rules for core platform services and infrastructure, such as high CPU/memory usage, low disk space, and service availability (e.g., TargetDown).  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** platform.rules.yml  
**Type:** Configuration  
**Relative Path:** prometheus/rules/platform.rules.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Infrastructure Alerting
    - Resource Saturation Alerts
    
**Requirement Ids:**
    
    - MON-011
    - MON-012
    - QA-003.1
    - DEP-005
    
**Purpose:** To define the alerting logic for the underlying health and performance of the platform's infrastructure.  
**Logic Description:** Contains a 'groups' array, each with a name and a set of 'rules'. Each rule defines an 'alert' name, an 'expr' (PromQL query), a 'for' duration, 'labels' (including severity), and 'annotations' (summary and description for the alert notification). Examples include alerts for high CPU, low disk space, and services being down.  
**Documentation:**
    
    - **Summary:** This file configures alerts for fundamental infrastructure health, ensuring operations teams are notified of potential issues with servers, disks, or core services.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/rules/application.rules.yml  
**Description:** Prometheus rule file for application-specific alerts, such as high API error rates (HTTP 5xx), high API latency (violating NFRs), and business process failures (e.g., low registration success rate).  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** application.rules.yml  
**Type:** Configuration  
**Relative Path:** prometheus/rules/application.rules.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - APM Alerting
    - Business Process Alerting
    
**Requirement Ids:**
    
    - MON-011
    - MON-012
    - QA-003.1
    - MON-010
    
**Purpose:** To define alerting logic based on application-level metrics to detect issues impacting user experience and business functions.  
**Logic Description:** Contains PromQL queries that calculate error rates, latency percentiles (using histogram_quantile), and success rates for key business transactions. Rules are defined with severities (e.g., warning, critical) and detailed annotations to help with troubleshooting.  
**Documentation:**
    
    - **Summary:** Configures alerts that monitor the health of the application itself, focusing on error rates, performance against SLOs, and the success of key user journeys.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** prometheus/rules/ai-pipeline.rules.yml  
**Description:** Prometheus rule file specifically for the AI creative generation pipeline. Includes alerts for high generation error rates, long queue depths in RabbitMQ, slow n8n workflow execution times, and poor performance of custom AI models.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** ai-pipeline.rules.yml  
**Type:** Configuration  
**Relative Path:** prometheus/rules/ai-pipeline.rules.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Pipeline Monitoring Alerts
    - Custom Model Performance Alerts
    
**Requirement Ids:**
    
    - MON-011
    - MON-013
    - INT-007
    - QA-003.1
    
**Purpose:** To monitor the health and performance of the most critical and resource-intensive part of the platform: the AI generation pipeline.  
**Logic Description:** Defines alerts based on metrics from n8n, RabbitMQ, and custom AI model exporters. Rules monitor job queue length, processing latency per pipeline stage, GPU utilization saturation, and AI model-specific error counters. This is crucial for fulfilling MON-013.  
**Documentation:**
    
    - **Summary:** This file contains the alerting logic to ensure the AI creative generation workflow is performing efficiently and reliably, notifying teams of bottlenecks or failures.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** alertmanager/alertmanager.yml  
**Description:** Main Alertmanager configuration. Defines alert routing trees based on labels (e.g., severity, service), specifies receiver integrations (PagerDuty, Slack, email), and configures silencing and inhibition rules.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** alertmanager.yml  
**Type:** Configuration  
**Relative Path:** alertmanager/alertmanager.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alert Routing and Escalation
    - Notification Channel Integration
    
**Requirement Ids:**
    
    - MON-012
    - QA-003.1
    - DEP-005
    
**Purpose:** To manage and route alerts generated by Prometheus to the correct teams through the appropriate channels.  
**Logic Description:** Contains a 'route' block with a main receiver and sub-routes that match alerts based on labels. Each route directs alerts to a 'receiver'. The 'receivers' block defines the configuration for each notification channel, such as Slack channel webhooks, PagerDuty integration keys, or email server settings. Implements the escalation matrix defined in QA-003.1.  
**Documentation:**
    
    - **Summary:** This file is the brain of the alerting system, determining who gets notified, how, and when, for any given issue detected by Prometheus.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** grafana/provisioning/dashboards/dashboard-provider.yml  
**Description:** Grafana provisioning file that tells Grafana where to find dashboard JSON models on the filesystem, enabling dashboards to be managed as code.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** dashboard-provider.yml  
**Type:** Configuration  
**Relative Path:** grafana/provisioning/dashboards/dashboard-provider.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Dashboard Provisioning
    
**Requirement Ids:**
    
    - MON-003
    - DEP-005
    
**Purpose:** To configure Grafana to automatically discover and load dashboard definitions from this repository.  
**Logic Description:** A simple YAML file specifying the provider type ('file'), name, and the path to the directory containing the JSON dashboard files (e.g., /etc/grafana/provisioning/dashboards/json).  
**Documentation:**
    
    - **Summary:** This configuration enables GitOps for Grafana dashboards, where committing a new JSON dashboard file to the repository automatically makes it available in Grafana.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** grafana/provisioning/dashboards/json/system-overview.json  
**Description:** Grafana dashboard JSON model for a high-level overview of the entire platform's health. Displays key performance indicators (KPIs) and the status of major components.  
**Template:** JSON Configuration  
**Dependency Level:** 1  
**Name:** system-overview.json  
**Type:** Dashboard  
**Relative Path:** grafana/provisioning/dashboards/json/system-overview.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Platform Health Visualization
    
**Requirement Ids:**
    
    - MON-003
    - MON-010
    - QA-003
    
**Purpose:** To provide a single pane of glass for at-a-glance monitoring of overall system health for SREs and management.  
**Logic Description:** A complex JSON object defining Grafana panels. Panels will use PromQL queries to display overall API error rates, total active users, AI generation throughput, database connection status, and message queue depths. It will use stat panels, time series graphs, and gauges for effective visualization.  
**Documentation:**
    
    - **Summary:** This dashboard provides a high-level, real-time view of the CreativeFlow AI platform's operational status and key business metrics.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** grafana/provisioning/dashboards/json/ai-pipeline-deep-dive.json  
**Description:** Detailed Grafana dashboard for monitoring the AI creative generation pipeline. Visualizes metrics from n8n, RabbitMQ, and the GPU cluster.  
**Template:** JSON Configuration  
**Dependency Level:** 1  
**Name:** ai-pipeline-deep-dive.json  
**Type:** Dashboard  
**Relative Path:** grafana/provisioning/dashboards/json/ai-pipeline-deep-dive.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Workflow Performance Monitoring
    - GPU Utilization Monitoring
    
**Requirement Ids:**
    
    - MON-003
    - MON-010
    - QA-003
    - INT-007
    
**Purpose:** To enable deep-dive analysis and troubleshooting of the AI generation workflow.  
**Logic Description:** JSON model for a Grafana dashboard with panels showing: RabbitMQ queue messages (published, ready, unacked); n8n workflow execution latency percentiles; success vs. error rates for AI model calls; and detailed GPU metrics (utilization, memory usage, temperature) per GPU, sourced from the DCGM exporter. Uses variables to filter by specific workflows or models.  
**Documentation:**
    
    - **Summary:** This dashboard is essential for the DevOps and AI/ML teams to monitor the performance, throughput, and resource consumption of the creative generation pipeline.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** grafana/provisioning/dashboards/json/logs-overview.json  
**Description:** Grafana dashboard for visualizing log data from Loki or Elasticsearch. Provides an overview of log volume, error rates, and allows for quick filtering and searching.  
**Template:** JSON Configuration  
**Dependency Level:** 1  
**Name:** logs-overview.json  
**Type:** Dashboard  
**Relative Path:** grafana/provisioning/dashboards/json/logs-overview.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Log Visualization
    
**Requirement Ids:**
    
    - MON-003
    - MON-004
    - QA-003
    
**Purpose:** To provide a centralized view into the log data from across the entire platform.  
**Logic Description:** JSON model for a Grafana dashboard configured with a Loki or Elasticsearch data source. Includes panels for log rate, log levels distribution (pie chart), top error messages, and a main logs panel for interactive exploration using LogQL or Lucene queries. Variables allow filtering by service, environment, and log level.  
**Documentation:**
    
    - **Summary:** This dashboard serves as the primary interface for exploring and analyzing aggregated log data, crucial for troubleshooting and operational awareness.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** grafana/provisioning/datasources/datasources.yml  
**Description:** Grafana provisioning file for automatically configuring data sources, such as Prometheus and Loki/Elasticsearch.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** datasources.yml  
**Type:** Configuration  
**Relative Path:** grafana/provisioning/datasources/datasources.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Datasource Configuration
    
**Requirement Ids:**
    
    - MON-003
    - DEP-005
    
**Purpose:** To ensure Grafana is automatically connected to the primary metrics and logging backends without manual setup.  
**Logic Description:** A YAML file containing a list of 'datasources'. Each entry specifies a name, type (e.g., 'prometheus', 'loki', 'elasticsearch'), URL of the backend service, and other necessary connection parameters. Secrets like passwords or API keys should be handled via environment variables.  
**Documentation:**
    
    - **Summary:** Defines the connections between Grafana and its underlying data stores, enabling the creation of dashboards that query metrics and logs.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** elk/logstash/pipeline/logstash.conf  
**Description:** Main Logstash pipeline configuration file. Defines the input, filter, and output stages for processing logs received from Filebeat before they are stored in Elasticsearch. (Used if ELK stack is chosen over Loki).  
**Template:** Logstash Configuration  
**Dependency Level:** 1  
**Name:** logstash.conf  
**Type:** Configuration  
**Relative Path:** elk/logstash/pipeline/logstash.conf  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - ETL
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Log Processing Pipeline
    - Log Parsing and Enrichment
    
**Requirement Ids:**
    
    - MON-004
    - MON-005
    
**Purpose:** To parse, normalize, and enrich incoming log data into a structured format suitable for storage and analysis in Elasticsearch.  
**Logic Description:** Contains three main sections: 'input', 'filter', and 'output'. The 'input' section configures a 'beats' input to listen for Filebeat connections. The 'filter' section uses plugins like 'json' to parse structured logs, 'grok' for unstructured logs (e.g., Nginx access logs), 'mutate' to add/remove fields, and 'date' to parse timestamps. The 'output' section configures the connection to the Elasticsearch cluster.  
**Documentation:**
    
    - **Summary:** This file defines the central log processing logic, transforming raw logs from various sources into clean, structured, and searchable data.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** elk/filebeat/filebeat.yml  
**Description:** Filebeat configuration to be deployed on all servers. It specifies which log files to monitor and where to send the log data (e.g., to Logstash or directly to Elasticsearch).  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** filebeat.yml  
**Type:** Configuration  
**Relative Path:** elk/filebeat/filebeat.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Log Shipping
    - Log Source Discovery
    
**Requirement Ids:**
    
    - MON-005
    - DEP-005
    
**Purpose:** To act as a lightweight agent on servers to collect and forward log files to the central logging system.  
**Logic Description:** Contains 'filebeat.inputs' to define log file paths to tail (e.g., /var/log/*.log, application-specific log paths). It can use autodiscover features for container logs. The 'output' section specifies the Logstash or Elasticsearch hosts. It's configured to add metadata like host and service name to each log event.  
**Documentation:**
    
    - **Summary:** This configuration file instructs the Filebeat agent on each server what log data to collect and where to send it for processing and storage.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** elk/elasticsearch/index-templates/creativeflow-logs-template.json  
**Description:** Elasticsearch index template that defines the mappings, settings, and lifecycle policies for the application's log indices. Ensures logs are indexed efficiently and managed over time.  
**Template:** JSON Configuration  
**Dependency Level:** 1  
**Name:** creativeflow-logs-template.json  
**Type:** Configuration  
**Relative Path:** elk/elasticsearch/index-templates/creativeflow-logs-template.json  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Log Index Management
    - Log Data Retention
    
**Requirement Ids:**
    
    - MON-007
    - MON-004
    
**Purpose:** To pre-define the structure and behavior of log indices in Elasticsearch for optimal performance and management.  
**Logic Description:** A JSON object defining an 'index_patterns' to match incoming log indices (e.g., 'creativeflow-logs-*'). The 'template' section contains 'settings' (e.g., number of shards) and 'mappings', which define the data type for each field (e.g., 'timestamp' as date, 'message' as text, 'http.status_code' as integer). It also links to an Index Lifecycle Management (ILM) policy for log retention.  
**Documentation:**
    
    - **Summary:** This file automates the creation and configuration of log indices in Elasticsearch, ensuring consistency and enabling features like data retention.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** opentelemetry/otel-collector-config.yml  
**Description:** Configuration for the OpenTelemetry Collector. Defines the pipeline for receiving, processing, and exporting telemetry data (traces, metrics, logs). Acts as a central, vendor-agnostic telemetry gateway.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** otel-collector-config.yml  
**Type:** Configuration  
**Relative Path:** opentelemetry/otel-collector-config.yml  
**Repository Id:** REPO-MONITORING-CONFIGS-001  
**Pattern Ids:**
    
    - TelemetryGateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Distributed Tracing Collection
    - Unified Telemetry Pipeline
    
**Requirement Ids:**
    
    - MON-008
    - QA-003
    
**Purpose:** To provide a standardized way to collect and process observability data before sending it to various backend systems.  
**Logic Description:** Contains 'receivers' (e.g., otlp, jaeger), 'processors' (e.g., batch, memory_limiter, attributes), 'exporters' (e.g., prometheus, loki, jaeger), and a 'service' section that connects these components into pipelines for traces, metrics, and logs. This enables flexible routing and processing of all telemetry data.  
**Documentation:**
    
    - **Summary:** This file configures the OpenTelemetry Collector, which acts as a central hub for receiving telemetry, processing it, and exporting it to specialized backends like Prometheus, Loki, and Jaeger.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

