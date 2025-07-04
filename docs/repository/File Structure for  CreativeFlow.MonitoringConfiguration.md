# Specification

# 1. Files

- **Path:** prometheus/prometheus.yml  
**Description:** Main Prometheus server configuration. Defines global settings, scrape intervals, rule file paths, service discovery configurations, and Alertmanager targets. Orchestrates how Prometheus discovers and scrapes metrics from various exporters and services.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** prometheus  
**Type:** Configuration  
**Relative Path:** prometheus/prometheus.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** global  
**Type:** Object  
**Attributes:** required  
    - **Name:** rule_files  
**Type:** Array  
**Attributes:** required  
    - **Name:** scrape_configs  
**Type:** Array  
**Attributes:** optional|deprecated_in_favor_of_scrape_config_files  
    - **Name:** scrape_config_files  
**Type:** Array  
**Attributes:** optional  
    - **Name:** alerting  
**Type:** Object  
**Attributes:** required  
    
**Implemented Features:**
    
    - Prometheus Core Configuration
    - Service Discovery Setup
    - Alertmanager Integration
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** Central configuration for the Prometheus monitoring server, defining its operational parameters and data sources.  
**Logic Description:** Specifies global scrape interval, evaluation interval. Lists paths to rule files (recording and alerting). Includes or references scrape configurations for all monitored targets. Configures Alertmanager endpoints for alert forwarding.  
**Documentation:**
    
    - **Summary:** This file is the master configuration for Prometheus, dictating how it collects metrics, evaluates rules, and interacts with Alertmanager. It references other YAML files for specific rules and scrape job definitions.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/rules/recording_rules.yml  
**Description:** Defines Prometheus recording rules to pre-compute frequently needed or computationally expensive queries, storing the results as new time series. Helps optimize dashboard loading and alerting performance.  
**Template:** PromQL Rule File (YAML)  
**Dependency Level:** 0  
**Name:** recording_rules  
**Type:** RuleFile  
**Relative Path:** prometheus/rules/recording_rules.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** groups  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Metrics Pre-computation
    - Query Performance Optimization
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To define recording rules that create new time series by aggregating or transforming existing metrics.  
**Logic Description:** Contains groups of recording rules. Each rule has an 'expr' (PromQL expression) and a 'record' (name of the new metric). Examples include aggregating request counts per minute, calculating error rates, or summing resource usage across instances.  
**Documentation:**
    
    - **Summary:** This file specifies PromQL expressions that Prometheus will evaluate periodically to create new, aggregated time series. These pre-calculated metrics improve query performance for dashboards and alerts.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/rules/application_alerts.yml  
**Description:** Defines Prometheus alerting rules for core application services (e.g., web frontend, API gateway, Odoo backend, n8n workflows, custom backend services). Covers aspects like error rates, latency, saturation, and availability.  
**Template:** PromQL Rule File (YAML)  
**Dependency Level:** 0  
**Name:** application_alerts  
**Type:** RuleFile  
**Relative Path:** prometheus/rules/application_alerts.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** groups  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Application Performance Alerting
    - Application Availability Alerting
    - Application Error Rate Alerting
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - QA-003.1
    
**Purpose:** To define alert conditions based on metrics from application components to notify operations teams of issues.  
**Logic Description:** Contains groups of alerting rules. Each rule specifies a PromQL expression ('expr') that, if true for a certain duration ('for'), triggers an alert. Includes labels (e.g., severity) and annotations (e.g., summary, description, runbook_url). Examples: API P99 latency > 500ms, HTTP 5xx error rate > 5%, Odoo job queue length > 100.  
**Documentation:**
    
    - **Summary:** This file defines alerting rules for monitoring the health and performance of various application services. Alerts are triggered based on predefined thresholds for metrics like latency, error rates, and resource usage specific to applications.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** prometheus/rules/infrastructure_alerts.yml  
**Description:** Defines Prometheus alerting rules for underlying infrastructure components such as servers (CPU, memory, disk), databases (PostgreSQL, Redis), message queues (RabbitMQ), Kubernetes cluster, and network devices.  
**Template:** PromQL Rule File (YAML)  
**Dependency Level:** 0  
**Name:** infrastructure_alerts  
**Type:** RuleFile  
**Relative Path:** prometheus/rules/infrastructure_alerts.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** groups  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Server Health Alerting
    - Database Performance Alerting
    - Message Queue Alerting
    - Kubernetes Cluster Alerting
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - QA-003.1
    
**Purpose:** To define alert conditions based on metrics from infrastructure components to ensure their stability and performance.  
**Logic Description:** Contains groups of alerting rules for infrastructure. Examples: Node CPU utilization > 90% for 5m, Disk space < 10% free, PostgreSQL replication lag > 5m, RabbitMQ unacknowledged messages > 1000, Redis memory usage > 80%, K8s node not ready.  
**Documentation:**
    
    - **Summary:** This file configures alerts for infrastructure-level issues, covering servers, databases, message brokers, and the Kubernetes cluster. Alerts help detect resource exhaustion, connectivity problems, or component failures.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** prometheus/rules/ai_model_alerts.yml  
**Description:** Defines specific Prometheus alerting rules for custom AI models deployed on the platform, focusing on their performance, error rates, and resource consumption as per INT-007. Includes alerts for model drift if corresponding metrics are available.  
**Template:** PromQL Rule File (YAML)  
**Dependency Level:** 0  
**Name:** ai_model_alerts  
**Type:** RuleFile  
**Relative Path:** prometheus/rules/ai_model_alerts.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** groups  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Custom AI Model Performance Alerting
    - Custom AI Model Error Rate Alerting
    - Custom AI Model Resource Alerting
    - Potential Model Drift Alerting
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - QA-003.1
    - INT-007
    
**Purpose:** To monitor the operational health and performance of custom AI models served by the platform.  
**Logic Description:** Contains alerting rules specific to custom AI models. Examples: Inference P99 latency > Xms for model Y, Error rate > Z% for model Y, GPU memory utilization per model pod > W%, Significant change in output distribution for model Y (drift detection).  
**Documentation:**
    
    - **Summary:** This file focuses on alerts for custom AI models, tracking their specific performance metrics, error rates, resource usage on the GPU cluster, and potentially signs of model drift to ensure their reliability and quality.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** prometheus/rules/business_process_alerts.yml  
**Description:** Defines Prometheus alerting rules based on key business process metrics and KPIs, such as user registration success rate, payment completion rate, AI generation pipeline success rate, and credit consumption anomalies.  
**Template:** PromQL Rule File (YAML)  
**Dependency Level:** 0  
**Name:** business_process_alerts  
**Type:** RuleFile  
**Relative Path:** prometheus/rules/business_process_alerts.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** groups  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Business KPI Alerting
    - User Journey Funnel Alerting
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - QA-003.1
    
**Purpose:** To monitor the health of critical business workflows and user-facing processes.  
**Logic Description:** Contains alerting rules tied to business outcomes. Examples: Registration success rate < 95% over 1h, Payment failure rate > 10% over 1h, AI generation success rate < 98% (KPI-004), Unusual spike in credit consumption.  
**Documentation:**
    
    - **Summary:** This file defines alerts based on high-level business metrics and Key Performance Indicators (KPIs) to quickly identify issues impacting core business functions or user experience funnels.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** prometheus/scrape_configs/node_exporter_targets.yml  
**Description:** Prometheus scrape configuration for node_exporter instances running on all servers, collecting system-level hardware and OS metrics (CPU, memory, disk, network).  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** node_exporter_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/node_exporter_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** static_configs  
**Type:** Array  
**Attributes:** optional  
    - **Name:** file_sd_configs  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Server OS Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To define how Prometheus discovers and scrapes metrics from node_exporters across the server fleet.  
**Logic Description:** Specifies a job_name (e.g., 'node_exporter'). Uses static_configs for fixed IPs or file_sd_configs/consul_sd_configs/ec2_sd_configs etc. for dynamic discovery of node_exporter targets. Defines scrape interval and metrics path.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to collect system-level metrics (CPU, memory, disk, network) from all servers via node_exporter.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/application_service_targets.yml  
**Description:** Prometheus scrape configuration for custom application services (web, API, Odoo, n8n, etc.) that expose Prometheus metrics endpoints.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** application_service_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/application_service_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** optional  
    - **Name:** static_configs  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Application-Specific Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To configure Prometheus to scrape custom metrics exposed by various backend and application services.  
**Logic Description:** Defines job_names for different application types (e.g., 'creativeflow-api', 'odoo-backend', 'n8n-workflows'). Uses Kubernetes service discovery (kubernetes_sd_configs) for services running in K8s, or other discovery methods. Specifies metrics_path (e.g., '/metrics') and relabel_configs for proper labeling.  
**Documentation:**
    
    - **Summary:** This file configures Prometheus to collect application-level metrics from various services like the API backend, Odoo, and n8n, typically exposed on a /metrics endpoint.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/database_targets.yml  
**Description:** Prometheus scrape configuration for database exporters (e.g., postgres_exporter, redis_exporter).  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** database_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/database_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** static_configs  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - PostgreSQL Metrics Scraping
    - Redis Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To collect performance and health metrics from PostgreSQL and Redis databases.  
**Logic Description:** Defines separate jobs for 'postgres_exporter' and 'redis_exporter'. Specifies connection details (usually via static_configs or environment variables for exporters) and target exporter endpoints.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to scrape metrics from database exporters like postgres_exporter and redis_exporter, providing insights into database health and performance.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/message_queue_targets.yml  
**Description:** Prometheus scrape configuration for RabbitMQ exporter.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** message_queue_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/message_queue_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** static_configs  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - RabbitMQ Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To collect metrics about RabbitMQ cluster, queues, and message rates.  
**Logic Description:** Defines a job for 'rabbitmq_exporter'. Specifies the exporter's target endpoint and connection details for RabbitMQ management API.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to collect metrics from the RabbitMQ exporter, monitoring queue lengths, message rates, and broker health.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/kubernetes_targets.yml  
**Description:** Prometheus scrape configuration for Kubernetes components (kubelet, cAdvisor, kube-state-metrics, API server).  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** kubernetes_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/kubernetes_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** required  
    - **Name:** relabel_configs  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Kubernetes Cluster Metrics Scraping
    - Pod/Container Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To collect detailed metrics about the Kubernetes cluster, nodes, pods, and containers.  
**Logic Description:** Defines jobs for scraping Kubernetes API server, kubelet (cAdvisor), and kube-state-metrics. Uses 'kubernetes_sd_configs' for service discovery within the cluster. Includes relabel_configs to properly label metrics.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to collect comprehensive metrics from the Kubernetes cluster itself, including node status, pod resource usage, and control plane health.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/gpu_targets.yml  
**Description:** Prometheus scrape configuration for NVIDIA DCGM exporter to collect GPU metrics (utilization, memory, temperature).  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** gpu_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/gpu_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** optional  
    - **Name:** static_configs  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - GPU Metrics Scraping (DCGM)
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To collect detailed performance and health metrics from NVIDIA GPUs used in the AI processing cluster.  
**Logic Description:** Defines a job for 'dcgm_exporter'. Uses Kubernetes service discovery if DCGM exporter runs as a DaemonSet, or static configs. Specifies the exporter's metrics endpoint.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to collect GPU-specific metrics (utilization, memory, temperature, power) via the NVIDIA DCGM exporter, essential for monitoring the AI processing cluster.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** prometheus/scrape_configs/custom_ai_model_targets.yml  
**Description:** Prometheus scrape configuration for custom AI models that expose their own Prometheus metrics endpoints. Relevant for INT-007.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** custom_ai_model_targets  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/custom_ai_model_targets.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** required  
    - **Name:** relabel_configs  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Custom AI Model Metrics Scraping
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To collect specific performance and operational metrics from deployed custom AI models.  
**Logic Description:** Defines jobs for scraping metrics from custom AI models, likely discovered via Kubernetes service discovery based on labels/annotations. Includes relabeling to add model_name, model_version labels.  
**Documentation:**
    
    - **Summary:** Configuration for Prometheus to scrape metrics exposed by custom AI models. This allows fine-grained monitoring of individual model performance and behavior, crucial for MLOps and INT-007.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Prometheus.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Metrics
    
- **Path:** alertmanager/alertmanager.yml  
**Description:** Main Alertmanager configuration. Defines routing rules for alerts from Prometheus, specifies receivers (email, Slack, PagerDuty, etc.), inhibition rules to prevent alert storms, and references alert notification templates.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** alertmanager  
**Type:** Configuration  
**Relative Path:** alertmanager/alertmanager.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** global  
**Type:** Object  
**Attributes:** optional  
    - **Name:** route  
**Type:** Object  
**Attributes:** required  
    - **Name:** receivers  
**Type:** Array  
**Attributes:** required  
    - **Name:** inhibit_rules  
**Type:** Array  
**Attributes:** optional  
    - **Name:** templates  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Alert Routing
    - Notification Configuration
    - Alert Inhibition
    - Alert Templating
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003.1
    
**Purpose:** Central configuration for Alertmanager, determining how alerts are processed, grouped, and routed to appropriate notification channels.  
**Logic Description:** Defines global settings like SMTP server, Slack API URL. Specifies a main route and sub-routes based on alert labels (e.g., severity, service). Configures receivers for email, Slack, PagerDuty with their specific settings. Defines inhibition rules to silence alerts based on others. Lists paths to custom notification templates.  
**Documentation:**
    
    - **Summary:** This file configures Alertmanager to handle alerts fired by Prometheus. It defines where and how notifications are sent based on alert severity and other labels, and includes rules to prevent alert flooding.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Alertmanager  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** alertmanager/templates/default_notification.tmpl  
**Description:** Default Go template for formatting alert notifications sent by Alertmanager (e.g., for email or Slack). Can be customized to include more context or specific formatting.  
**Template:** Go Template  
**Dependency Level:** 0  
**Name:** default_notification  
**Type:** TemplateFile  
**Relative Path:** alertmanager/templates/default_notification.tmpl  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Implemented Features:**
    
    - Customizable Alert Notification Formatting
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003.1
    
**Purpose:** To define the structure and content of alert notifications.  
**Logic Description:** Uses Go templating language to iterate over alerts and their labels/annotations, formatting them into a human-readable message. Includes common fields like alert name, summary, description, severity, start time, and potentially links to Grafana dashboards or runbooks.  
**Documentation:**
    
    - **Summary:** A Go template file used by Alertmanager to format the content of alert notifications. This allows for customization of how alerts appear in email, Slack, or other receivers.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Alertmanager.Templates  
**Metadata:**
    
    - **Category:** Alerting
    
- **Path:** grafana/provisioning/datasources/prometheus_ds.yml  
**Description:** Grafana datasource provisioning file for Prometheus. Allows Grafana to connect to and query the Prometheus server.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** prometheus_ds  
**Type:** DatasourceDefinition  
**Relative Path:** grafana/provisioning/datasources/prometheus_ds.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** apiVersion  
**Type:** Integer  
**Attributes:** required  
    - **Name:** datasources  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Grafana Prometheus Datasource Configuration
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To automatically configure the Prometheus datasource in Grafana upon startup.  
**Logic Description:** Defines a datasource with a name (e.g., 'Prometheus-Main'), type ('prometheus'), URL of the Prometheus server, access mode (server/browser), and other relevant settings like scrape interval overrides if needed.  
**Documentation:**
    
    - **Summary:** This YAML file is used by Grafana's provisioning system to automatically set up the Prometheus data source, enabling dashboards to query metrics from Prometheus.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Datasources  
**Metadata:**
    
    - **Category:** Visualization
    
- **Path:** grafana/provisioning/datasources/loki_ds.yml  
**Description:** Grafana datasource provisioning file for Loki. Enables Grafana to connect to Loki for log querying and visualization.  
**Template:** YAML Configuration  
**Dependency Level:** 0  
**Name:** loki_ds  
**Type:** DatasourceDefinition  
**Relative Path:** grafana/provisioning/datasources/loki_ds.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** apiVersion  
**Type:** Integer  
**Attributes:** required  
    - **Name:** datasources  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Grafana Loki Datasource Configuration
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To automatically configure the Loki datasource in Grafana upon startup for log visualization.  
**Logic Description:** Defines a datasource with a name (e.g., 'Loki-Main'), type ('loki'), URL of the Loki server, and potentially derived fields or other settings.  
**Documentation:**
    
    - **Summary:** This YAML file configures Grafana to connect to a Loki instance, allowing users to query and visualize logs alongside metrics within Grafana dashboards.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Datasources  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** grafana/provisioning/dashboards/dashboard_provider.yml  
**Description:** Grafana dashboard provisioning configuration. Tells Grafana where to find dashboard JSON files to load them automatically.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** dashboard_provider  
**Type:** Configuration  
**Relative Path:** grafana/provisioning/dashboards/dashboard_provider.yml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** apiVersion  
**Type:** Integer  
**Attributes:** required  
    - **Name:** providers  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Grafana Dashboard Provisioning
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To configure Grafana to automatically load and update dashboards defined as JSON files from a specified directory.  
**Logic Description:** Defines one or more dashboard providers. Each provider specifies a name, type ('file'), options (path to dashboard JSON files, e.g., '/etc/grafana/provisioning/dashboards' or a path within the Grafana container), and settings like 'allowUiUpdates: false' to ensure dashboards are managed as code.  
**Documentation:**
    
    - **Summary:** This file instructs Grafana's provisioning system on how to discover and load dashboard definitions from JSON files stored in the `grafana/dashboards/` directory.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** Visualization
    
- **Path:** grafana/dashboards/system_overview_dashboard.json  
**Description:** Grafana dashboard JSON definition for a high-level system overview. Displays key health metrics for major components and overall platform status.  
**Template:** JSON Dashboard  
**Dependency Level:** 0  
**Name:** system_overview_dashboard  
**Type:** DashboardDefinition  
**Relative Path:** grafana/dashboards/system_overview_dashboard.json  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** title  
**Type:** String  
**Attributes:** required  
    - **Name:** panels  
**Type:** Array  
**Attributes:** required  
    - **Name:** templating  
**Type:** Object  
**Attributes:** optional  
    - **Name:** time  
**Type:** Object  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Overall System Health Visualization
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To provide a consolidated view of the platform's health and key performance indicators.  
**Logic Description:** JSON structure defining Grafana dashboard elements. Includes panels for displaying CPU/memory/disk usage for critical server groups, API error rates, AI generation throughput, database connection counts, message queue depths, etc. Uses variables for filtering by environment or service.  
**Documentation:**
    
    - **Summary:** A Grafana dashboard definition providing a high-level overview of the entire CreativeFlow AI platform's health, combining key metrics from various components into a single view.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** Visualization
    
- **Path:** grafana/dashboards/custom_ai_model_monitoring.json  
**Description:** Grafana dashboard JSON definition for monitoring custom AI models (INT-007). Displays performance (latency, throughput), error rates, and resource usage (GPU, CPU, memory) specific to deployed custom models. Can be a template dashboard parameterized by model ID/name.  
**Template:** JSON Dashboard  
**Dependency Level:** 0  
**Name:** custom_ai_model_monitoring  
**Type:** DashboardDefinition  
**Relative Path:** grafana/dashboards/custom_ai_model_monitoring.json  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** title  
**Type:** String  
**Attributes:** required  
    - **Name:** panels  
**Type:** Array  
**Attributes:** required  
    - **Name:** templating  
**Type:** Object  
**Attributes:** required  
    
**Implemented Features:**
    
    - Custom AI Model Performance Visualization
    - Custom AI Model Resource Monitoring
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To provide detailed operational insights into the performance and health of individual custom AI models.  
**Logic Description:** JSON structure defining Grafana dashboard panels. Includes panels for inference latency, request throughput, error rates, GPU utilization, GPU memory usage, CPU/memory usage per model instance or deployment. Uses template variables to select specific model IDs or versions for focused analysis.  
**Documentation:**
    
    - **Summary:** A Grafana dashboard definition specifically for monitoring the performance and resource consumption of custom AI models deployed on the platform, fulfilling INT-007.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** Visualization
    
- **Path:** loki/loki-config.yaml  
**Description:** Configuration file for the Loki server. Defines storage backend (e.g., MinIO, local filesystem), retention policies for logs, query limits, and server operational parameters.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** loki-config  
**Type:** Configuration  
**Relative Path:** loki/loki-config.yaml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** auth_enabled  
**Type:** Boolean  
**Attributes:** required  
    - **Name:** server  
**Type:** Object  
**Attributes:** required  
    - **Name:** ingester  
**Type:** Object  
**Attributes:** required  
    - **Name:** storage_config  
**Type:** Object  
**Attributes:** required  
    - **Name:** schema_config  
**Type:** Object  
**Attributes:** required  
    - **Name:** limits_config  
**Type:** Object  
**Attributes:** optional  
    - **Name:** table_manager  
**Type:** Object  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Centralized Log Storage Configuration
    - Log Retention Policy Management
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To configure the Loki log aggregation system, including its storage backend, indexing, and data retention strategies.  
**Logic Description:** Specifies Loki server settings (HTTP listen port, gRPC port). Configures ingester parameters (chunk handling). Defines 'storage_config' for object storage (e.g., MinIO S3 endpoint, bucket name, credentials) or filesystem. Sets 'schema_config' for index periods. Configures 'compactor' and 'table_manager' for retention policies (e.g., delete logs older than X days).  
**Documentation:**
    
    - **Summary:** This file contains the configuration for the Loki log aggregation server, defining how logs are stored, indexed, and retained. It specifies the backend storage (e.g., MinIO) and retention periods.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Loki  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** promtail/promtail-config.yaml  
**Description:** Configuration file for Promtail, the log shipping agent for Loki. Defines how Promtail discovers log sources (e.g., Kubernetes pods, local files), scrapes logs, applies labels, and sends them to the Loki server.  
**Template:** YAML Configuration  
**Dependency Level:** 1  
**Name:** promtail-config  
**Type:** Configuration  
**Relative Path:** promtail/promtail-config.yaml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** server  
**Type:** Object  
**Attributes:** required  
    - **Name:** clients  
**Type:** Array  
**Attributes:** required  
    - **Name:** positions  
**Type:** Object  
**Attributes:** required  
    - **Name:** scrape_configs  
**Type:** Array  
**Attributes:** required  
    
**Implemented Features:**
    
    - Log Shipping Configuration
    - Log Source Discovery
    - Log Labeling and Parsing (basic)
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    
**Purpose:** To configure Promtail agents to collect logs from various sources and forward them to Loki.  
**Logic Description:** Specifies Promtail server settings (HTTP port). Defines 'clients' array with Loki server URL(s). Configures 'positions' file path for tracking read offsets. Contains 'scrape_configs' defining jobs to discover and tail log files or container logs. Includes 'pipeline_stages' for basic log parsing and relabeling to add metadata like 'job', 'namespace', 'pod', 'container', 'service', 'level'. Promtail aims for standardized JSON format for logs where possible by applications or through its pipeline stages.  
**Documentation:**
    
    - **Summary:** This file configures Promtail, the log collection agent for Loki. It specifies which log files or container logs to monitor, how to label them, and where to send them (the Loki instance).
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Promtail  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** promtail/scrape_configs/kubernetes_logs.yaml  
**Description:** Promtail scrape configuration snippet for collecting logs from Kubernetes pods. To be included or referenced by the main promtail-config.yaml.  
**Template:** YAML Configuration Snippet  
**Dependency Level:** 0  
**Name:** kubernetes_logs  
**Type:** Configuration  
**Relative Path:** promtail/scrape_configs/kubernetes_logs.yaml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** required  
    - **Name:** relabel_configs  
**Type:** Array  
**Attributes:** optional  
    - **Name:** pipeline_stages  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Kubernetes Pod Log Collection
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To configure Promtail to discover and collect logs from all relevant Kubernetes pods.  
**Logic Description:** Defines a job for Kubernetes logs. Uses 'kubernetes_sd_configs' to discover pods. Includes 'relabel_configs' to extract useful labels from pod metadata (e.g., namespace, pod_name, container_name, app_label). May include 'pipeline_stages' for parsing JSON logs or applying further transformations specific to Kubernetes logs.  
**Documentation:**
    
    - **Summary:** A specific Promtail scrape configuration for collecting logs from containers running within the Kubernetes cluster. This ensures logs from microservices and AI models are captured.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Promtail.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** promtail/scrape_configs/ai_model_specific_logs.yaml  
**Description:** Promtail scrape configuration snippet for custom AI model container logs, potentially with specific parsing rules. Relevant for INT-007.  
**Template:** YAML Configuration Snippet  
**Dependency Level:** 0  
**Name:** ai_model_specific_logs  
**Type:** Configuration  
**Relative Path:** promtail/scrape_configs/ai_model_specific_logs.yaml  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** job_name  
**Type:** String  
**Attributes:** required  
    - **Name:** kubernetes_sd_configs  
**Type:** Array  
**Attributes:** required  
    - **Name:** relabel_configs  
**Type:** Array  
**Attributes:** optional  
    - **Name:** pipeline_stages  
**Type:** Array  
**Attributes:** optional  
    
**Implemented Features:**
    
    - Custom AI Model Log Collection
    - AI Model Log Parsing
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To specifically configure log collection and parsing for custom AI models running in Kubernetes.  
**Logic Description:** Defines a job targeting AI model pods (e.g., selected via specific labels). Includes relabeling to add model_name, model_version. Pipeline stages might include regex or JSON parsing tailored to the log output format of the custom AI models.  
**Documentation:**
    
    - **Summary:** A Promtail scrape configuration focused on collecting and potentially parsing logs generated by custom AI models. This is important for debugging and monitoring model behavior as per INT-007.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Promtail.ScrapeConfigs  
**Metadata:**
    
    - **Category:** Logging
    
- **Path:** grafana/dashboards/logs_ai_model_dashboard.json  
**Description:** Grafana dashboard JSON definition for visualizing logs from custom AI models (INT-007), sourced from Loki. Allows filtering by model, version, and keyword search.  
**Template:** JSON Dashboard  
**Dependency Level:** 0  
**Name:** logs_ai_model_dashboard  
**Type:** DashboardDefinition  
**Relative Path:** grafana/dashboards/logs_ai_model_dashboard.json  
**Repository Id:** REPO-MONITORING-CONFIG-001  
**Pattern Ids:**
    
    - ConfigurationFile
    
**Members:**
    
    - **Name:** title  
**Type:** String  
**Attributes:** required  
    - **Name:** panels  
**Type:** Array  
**Attributes:** required  
    - **Name:** templating  
**Type:** Object  
**Attributes:** optional  
    
**Implemented Features:**
    
    - AI Model Log Visualization
    - Log Filtering and Search for AI Models
    
**Requirement Ids:**
    
    - DEP-005
    - QA-003
    - INT-007
    
**Purpose:** To provide a dedicated view for analyzing logs generated by custom AI models for troubleshooting and performance analysis.  
**Logic Description:** JSON structure defining Grafana dashboard. Includes panels for displaying log streams from AI models (using LogQL queries against Loki), log counts by severity, and visualizations of error patterns. Uses template variables for model_name, model_version, and log_level.  
**Documentation:**
    
    - **Summary:** A Grafana dashboard to specifically view and analyze logs from custom AI models, aiding in debugging, performance analysis, and fulfilling monitoring requirements of INT-007.
    
**Namespace:** CreativeFlow.Infrastructure.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** Logging
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

