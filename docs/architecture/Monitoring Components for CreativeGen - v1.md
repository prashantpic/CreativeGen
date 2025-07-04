# Specification

# 1. Monitoring Components

## 1.1. Centralized Metrics Collection & Visualization
Prometheus for collecting time-series metrics from all system components, services, infrastructure, databases, message queues, and GPU resources. Grafana for dashboards visualizing key metrics, trends, and operational health. (DEP-005, QA-003, MON-001, MON-003, REQ-SSPE-018)

### 1.1.3. Type
MetricsPlatform

### 1.1.5. Provider
Prometheus, Grafana

### 1.1.6. Features

- Time-series metrics collection from diverse exporters (node, postgres, rabbitmq, nginx, redis, Odoo/JMX, n8n, DCGM for GPUs) (MON-002)
- Role-based visualization dashboards for KPIs, system health, application performance, business processes, and resource utilization (CPU, memory, disk, network, GPU) (MON-003, MON-010)
- Monitoring of custom AI models (performance, resource consumption) (INT-007, AISIML-011)
- Tracking of infrastructure health and business process performance (MON-010)
- Storage for metrics data with defined retention (DEP-005)

### 1.1.7. Configuration

- **Prometheus Scrape Interval:** 15s-60s (configurable per job)
- **Grafana Data Sources:** Prometheus, potentially others like ELK/Loki for log correlation
- **Monitored Components:** Web/API servers, Odoo, n8n, AI cluster, PostgreSQL, Redis, RabbitMQ, MinIO, Kubernetes, OS, Network
- **Key Dashboards:** Overall System Health, Service-Specific Performance, AI Generation Pipeline, Resource Utilization (CPU, GPU, Memory, Network, Disk), Business KPIs (Registration, Payments, Credits)

## 1.2. Centralized Logging Platform
ELK Stack (Elasticsearch, Logstash, Kibana) for centralized log aggregation, storage, indexing, and analysis from all applications, infrastructure, OS, and security systems. (DEP-005, QA-003, MON-004)

### 1.2.3. Type
LogAggregation

### 1.2.5. Provider
ELK Stack (Elasticsearch, Logstash, Kibana)

### 1.2.6. Features

- Log collection from all applications (frontend, backend, Odoo, n8n, AI services, mobile) and infrastructure components (MON-004)
- Log shipping via Filebeat or Fluentd/Fluent Bit (MON-005)
- Standardized structured JSON log format (MON-005)
- Inclusion of unique correlation IDs (trace IDs) for distributed tracing (MON-005)
- Configurable log levels (DEBUG, INFO, WARN, ERROR, CRITICAL) per environment (MON-005)
- Logging of critical events: API requests/responses, auth attempts, errors, business transactions, AI model invocations, state changes, security events (MON-006)
- Secure storage and search/analysis capabilities via Kibana (MON-004)
- Configurable log retention policies with tiered storage (MON-007)

### 1.2.7. Configuration

- **Log Shipper:** Filebeat/Fluentd/Fluent Bit
- **Log Format:** Structured JSON with Correlation ID
- **Default Log Level Production:** INFO
- **Security Audit Log Retention:** Minimum 12 months active
- **Operational Log Retention:** 14 days hot, 30-90 days warm, 1 year cold/archive (tiered)

## 1.3. Distributed Tracing System
OpenTelemetry for generating and collecting traces across microservices, with Jaeger/Zipkin for distributed trace storage, visualization, and latency analysis. (QA-003, MON-008)

### 1.3.3. Type
DistributedTracing

### 1.3.5. Provider
OpenTelemetry, Jaeger (or Zipkin)

### 1.3.6. Features

- Trace generation and collection from all relevant services (backend, Odoo, n8n, AI services)
- Span and trace correlation using propagated context (correlation IDs from MON-005)
- Request path visualization across services
- Latency analysis for individual service calls and end-to-end transactions
- Service dependency mapping based on trace data
- Configurable sampling strategy

### 1.3.7. Configuration

- **Trace Collector Endpoint:** Jaeger/Zipkin Collector URL
- **Default Sampling Rate:** e.g., 0.1 (10%) for production, 1.0 (100%) for development/staging
- **Instrumented Services:** All backend microservices, n8n custom nodes if applicable, Odoo custom modules

## 1.4. Application Error Tracking
Sentry (or Rollbar) for real-time capture, aggregation, and dashboarding of application exceptions and errors from frontend (JavaScript), backend (Python/Odoo, n8n), and mobile (Flutter/Dart) applications. (QA-003, MON-008)

### 1.4.3. Type
ErrorTracking

### 1.4.5. Provider
Sentry (or Rollbar)

### 1.4.6. Features

- Automatic capture of unhandled exceptions and errors
- Manual error reporting capabilities
- Contextual information (stack traces, user session data, request data, release version)
- Error grouping and de-duplication
- Real-time notifications for new or critical errors
- Integration with issue tracking systems (e.g., GitLab Issues)
- Dashboards for error rates and trends

### 1.4.7. Configuration

- **Dsn_Frontend:** Sentry DSN for React App
- **Dsn_Backend_Python:** Sentry DSN for Python Services
- **Dsn_Mobile_Flutter:** Sentry DSN for Flutter App
- **Environment Tagging:** Development, Staging, Production
- **Release Tracking:** Integrated with CI/CD pipeline (DEP-003)

## 1.5. Real User Monitoring & Client-Side Analytics
GA4 for web marketing analytics and RUM. Mixpanel (or Amplitude) for detailed user behavior analytics (web & mobile). Firebase Analytics for mobile app performance and user behavior. (QA-003, REQ-SSPE-021, MON-009, REQ-11-001, REQ-11-002, REQ-11-005, REQ-8-009)

### 1.5.3. Type
RUM_Analytics

### 1.5.5. Provider
Google Analytics 4, Mixpanel, Firebase Analytics

### 1.5.6. Features

- Web traffic and marketing campaign tracking (GA4) (REQ-11-001)
- Detailed user behavior analysis, funnel tracking, cohort analysis (Mixpanel/Amplitude) (REQ-11-002)
- Custom event tracking for key features, user journeys, conversions (web & mobile) (REQ-11-003)
- Forwarding of key non-sensitive revenue-related events (REQ-11-004)
- Mobile app metrics: active users, session duration, screen views, crash reports, ANRs (Firebase Analytics) (REQ-11-005, REQ-8-009)
- Core Web Vitals (LCP, FID, CLS) monitoring (web) (REQ-SSPE-021, REQ-SSPE-022)
- Client-side JavaScript error tracking (web) (REQ-SSPE-021)

### 1.5.7. Configuration

- **Ga4_Measurement Id:** G-XXXXXXXXXX
- **Mixpanel_Project Token:** YOUR_MIXPANEL_TOKEN
- **Firebase_Config:** google-services.json / GoogleService-Info.plist
- **Custom Event Tracking Plan:** Defined as per REQ-11-003, covering user registration, creative generation, subscription events, feature usage.

## 1.6. Operational Alerting System
Prometheus Alertmanager or Grafana Alerting for threshold-based alerting on metrics collected by Prometheus. Integrated with notification channels and escalation procedures. (DEP-005, QA-003.1, MON-011, MON-012, MON-013, REQ-SSPE-020)

### 1.6.3. Type
Alerting

### 1.6.5. Provider
Prometheus Alertmanager (or Grafana Alerting)

### 1.6.6. Features

- Definition of SMART alerting thresholds for critical system metrics, KPIs, NFRs, error rates, resource saturation (MON-011, REQ-SSPE-020)
- Alerting for AI generation errors and custom AI model performance anomalies (MON-013)
- Configurable alert severities (P1-P4) (MON-012)
- Integration with notification channels (PagerDuty/Opsgenie, Slack/MS Teams, email) based on severity and on-call schedules (MON-012)
- Linking alerts to Standard Operating Procedures (SOPs) or runbooks (MON-012)
- Alert de-duplication and grouping
- Regular review and tuning of alert thresholds (MON-012)

### 1.6.7. Configuration

- **Alertmanager Config:** Routing rules, receiver configurations, inhibition rules
- **Grafana Alerting Config:** Alert rules defined within Grafana dashboards/panels
- **Escalation Policy Integration:** PagerDuty/Opsgenie service keys, Slack webhook URLs
- **Critical Alert Thresholds:** API error rate > 5%, GPU Temp > 85C, Disk Free < 10%, AI Gen Success < 98% (examples from MON-011, KPI-004, REQ-SSPE-019)



---

