# Specification

# 1. Telemetry And Metrics Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-18
  - **Technology Stack:**
    
    - Python (FastAPI/Flask)
    - Node.js (n8n, Notification Service)
    - Odoo 18+
    - RabbitMQ
    - PostgreSQL 16+
    - Redis
    - MinIO
    - React 19+
    - TypeScript
    - Flutter 3.19+
    - Dart
    - Kubernetes (K3s/RKE2/K8s)
    - Docker
    - Nginx
    - Cloudflare
    - Ansible
    - OpenAI API
    - Stability AI API
    - Stripe SDK
    - PayPal SDK
    - HashiCorp Vault
    - Prometheus
    - Grafana
    - ELK Stack/Grafana Loki
    - OpenTelemetry
    - Yjs
    
  - **Monitoring Components:**
    
    - Prometheus
    - Grafana
    - Prometheus Alertmanager / Grafana Alerting
    - ELK Stack / Grafana Loki
    - OpenTelemetry (Jaeger/Zipkin)
    - Sentry / Rollbar (for error tracking)
    - Google Analytics 4 (GA4)
    - Mixpanel / Amplitude
    - Firebase Analytics
    
  - **Requirements:**
    
    - System for AI creative generation with user management, subscription billing, real-time collaboration, external API access, mobile applications, and comprehensive MLOps capabilities. Focus on performance, scalability, reliability, security, and regulatory compliance. Monitoring and observability are critical for operational stability and meeting NFRs/KPIs.
    
  - **Environment:** production
  
- **Standard System Metrics Selection:**
  
  - **Hardware Utilization Metrics:**
    
    - **Name:** system_cpu_utilization_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Overall CPU utilization of host servers.  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** >80%
    - **Critical:** >90% for 5m
    
**Justification:** MON-010, CPIO-003, REQ-SSPE-020: Essential for capacity planning and performance troubleshooting.  
    - **Name:** system_memory_utilization_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Overall memory utilization of host servers.  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** >85%
    - **Critical:** >95% for 5m
    
**Justification:** MON-010, CPIO-003, REQ-SSPE-020: Tracks memory pressure, vital for stability.  
    - **Name:** system_disk_io_rate_bytes_per_sec  
**Type:** gauge  
**Unit:** bytes/sec  
**Description:** Disk I/O throughput for critical storage volumes.  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** Approaching device limits
    - **Critical:** Sustained max device limits
    
**Justification:** MON-010, CPIO-003: Identifies disk bottlenecks affecting DB and object storage.  
    - **Name:** system_disk_space_used_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Disk space utilization for critical volumes (logs, DB, MinIO).  
**Collection:**
    
    - **Interval:** 5m
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** >80%
    - **Critical:** >90%
    
**Justification:** MON-010, CPIO-003, REQ-SSPE-020: Prevents service outages due to full disks.  
    - **Name:** system_network_throughput_bytes_per_sec  
**Type:** gauge  
**Unit:** bytes/sec  
**Description:** Network traffic volume on server interfaces.  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** Approaching link capacity
    - **Critical:** Sustained link saturation
    
**Justification:** MON-010, CPIO-003: Monitors network bandwidth usage, identifies saturation.  
    - **Name:** gpu_utilization_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Utilization of GPU cores in the AI processing cluster.  
**Collection:**
    
    - **Interval:** 10s
    - **Method:** Prometheus DCGM exporter (MON-002)
    
**Thresholds:**
    
    - **Warning:** Avg >85% for 10m (potential scaling need)
    - **Critical:** Avg >95% for 5m (saturation)
    
**Justification:** MON-010, CPIO-008, REQ-SSPE-018, REQ-SSPE-012: Core for AI workload performance and capacity.  
    - **Name:** gpu_memory_used_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** GPU memory utilization in the AI processing cluster.  
**Collection:**
    
    - **Interval:** 10s
    - **Method:** Prometheus DCGM exporter (MON-002)
    
**Thresholds:**
    
    - **Warning:** >80%
    - **Critical:** >90%
    
**Justification:** MON-010, CPIO-008, REQ-SSPE-018, REQ-SSPE-012: Tracks GPU memory, vital for model capacity.  
    - **Name:** gpu_temperature_celsius  
**Type:** gauge  
**Unit:** celsius  
**Description:** GPU temperature in the AI processing cluster.  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** Prometheus DCGM exporter (MON-002)
    
**Thresholds:**
    
    - **Warning:** >80C
    - **Critical:** >85C
    
**Justification:** MON-010, CPIO-008, REQ-SSPE-018: GPU health monitoring.  
    
  - **Runtime Metrics:**
    
    - **Name:** app_gc_collection_duration_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Garbage collection pause times for managed runtimes.  
**Technology:** Python (if applicable), Node.js, Odoo (JMX)  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** Prometheus JMX exporter / language-specific agent
    
**Criticality:** medium  
**Justification:** MON-002 (JMX for Odoo): General application health and performance.  
    - **Name:** app_thread_pool_active_threads_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active threads in application thread pools.  
**Technology:** Python, Node.js, Odoo  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus language-specific agent / JMX
    
**Criticality:** medium  
**Justification:** MON-002: Application responsiveness and resource usage.  
    - **Name:** db_connection_pool_active_connections_count  
**Type:** gauge  
**Unit:** count  
**Description:** Active connections in database connection pools.  
**Technology:** PostgreSQL (via PgBouncer exporter or app-level)  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus exporter
    
**Criticality:** high  
**Justification:** REQ-DA-013, REQ-SSPE-008: Monitors database connection usage and potential bottlenecks.  
    
  - **Request Response Metrics:**
    
    - **Name:** http_server_request_latency_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Latency of HTTP requests to servers/services.  
**Dimensions:**
    
    - service_name
    - http_method
    - http_path
    - http_status_code
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Prometheus client libraries / OpenTelemetry
    
**Justification:** REQ-SSPE-003 (API latency), REQ-WCI-002 (UI responsiveness depends on this), MON-006 (API req/resp logging).  
    - **Name:** http_server_request_count_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of HTTP requests received by servers/services.  
**Dimensions:**
    
    - service_name
    - http_method
    - http_path
    - http_status_code
    
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Prometheus client libraries / OpenTelemetry
    
**Justification:** NFR-002 (throughput), REQ-SSPE-005, MON-006 (API req/resp logging).  
    
  - **Availability Metrics:**
    
    - **Name:** service_uptime_seconds_total  
**Type:** counter  
**Unit:** seconds  
**Description:** Total time a service has been reported as up by health checks.  
**Calculation:** Sum of seconds service is healthy. Uptime % = (service_uptime_seconds_total / total_observation_seconds_total) * 100  
**Sla Target:** 99.9%  
**Justification:** SREDRP-001, CPIO-018, NFR-003, REQ-2-011: Core availability requirement.  
    - **Name:** component_health_status_binary  
**Type:** gauge  
**Unit:** boolean (0/1)  
**Description:** Health status of individual components/services (1=up, 0=down).  
**Calculation:** Derived from health checks or synthetic monitoring probes.  
**Sla Target:** N/A  
**Justification:** SREDRP-006 (auto-failover depends on health status), NFR-003.  
    
  - **Scalability Metrics:**
    
    - **Name:** kubernetes_pod_replicas_desired_count  
**Type:** gauge  
**Unit:** count  
**Description:** Desired number of replicas for a Kubernetes deployment.  
**Capacity Threshold:** Defined by HPA config  
**Auto Scaling Trigger:** True  
**Justification:** CPIO-008, REQ-SSPE-007, REQ-SSPE-011: Tracks auto-scaling activity.  
    - **Name:** kubernetes_pod_replicas_current_count  
**Type:** gauge  
**Unit:** count  
**Description:** Current number of running replicas for a Kubernetes deployment.  
**Capacity Threshold:** Defined by HPA config  
**Auto Scaling Trigger:** True  
**Justification:** CPIO-008, REQ-SSPE-007, REQ-SSPE-011: Tracks current scale.  
    - **Name:** rabbitmq_queue_messages_ready_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of messages ready for consumption in RabbitMQ queues.  
**Capacity Threshold:** Varies per queue (e.g., >1000 as warning)  
**Auto Scaling Trigger:** True  
**Justification:** REQ-SSPE-009, REQ-SSPE-019, CPIO-007, MON-010: Indicates processing backlogs and trigger for AI worker scaling.  
    - **Name:** rabbitmq_queue_consumers_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active consumers for RabbitMQ queues.  
**Capacity Threshold:** Varies per queue  
**Auto Scaling Trigger:** False  
**Justification:** CPIO-007: Verifies consumers are active.  
    
  
- **Application Specific Metrics Design:**
  
  - **Transaction Metrics:**
    
    - **Name:** ai_generation_latency_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** End-to-end latency for AI creative generation requests.  
**Business_Context:** Core product feature performance.  
**Dimensions:**
    
    - generation_type (sample/high_res)
    - user_tier
    - ai_model_provider
    - ai_model_name
    
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application-level timing
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      - p90
      - p95
      - p99
      
    - **Window:** 1m, 5m, 1h
    
**Justification:** REQ-SSPE-001, REQ-SSPE-002, NFR-001: Core performance NFRs.  
    - **Name:** user_registration_duration_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Time taken for a user to complete the registration process.  
**Business_Context:** User onboarding efficiency.  
**Dimensions:**
    
    - registration_method (email/social)
    
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application-level timing
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      - p95
      
    - **Window:** 1h, 1d
    
**Justification:** KPI-001 (Registration success implies performance), KPI-002 (TTFV related).  
    - **Name:** payment_processing_duration_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Time taken for payment processing via gateways.  
**Business_Context:** Billing system performance.  
**Dimensions:**
    
    - payment_gateway (stripe/paypal)
    - transaction_type (subscription/one_time)
    
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application-level timing
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      - p95
      
    - **Window:** 1h, 1d
    
**Justification:** REQ-6-014: Smooth payment experience.  
    
  - **Cache Performance Metrics:**
    
    - **Name:** redis_cache_hit_ratio_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Cache hit ratio for Redis.  
**Cache Type:** Redis (session, user_profile, templates)  
**Hit Ratio Target:** >80%  
**Justification:** REQ-DA-003, CPIO-006: Measures effectiveness of caching strategy.  
    - **Name:** redis_commands_latency_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Latency for Redis commands.  
**Cache Type:** Redis  
**Hit Ratio Target:** N/A  
**Justification:** CPIO-006: Monitors Redis performance.  
    
  - **External Dependency Metrics:**
    
    - **Name:** external_service_call_latency_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Latency of calls to external third-party services.  
**Dependency:** AI (OpenAI/StabilityAI), Payment (Stripe/PayPal), SocialMediaAPIs  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Response Time:** Varies by provider, internal SLOs set
    - **Availability:** Varies by provider
    
**Justification:** AISIML-004, AISIML-005, SMPIO-008, REQ-6-014: Tracks performance of critical external dependencies.  
    - **Name:** external_service_call_error_count_total  
**Type:** counter  
**Unit:** count  
**Description:** Number of errors when calling external third-party services.  
**Dependency:** AI, Payment, SocialMediaAPIs  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Response Time:** N/A
    - **Availability:** Varies by provider
    
**Justification:** AISIML-004, AISIML-005, SMPIO-008, REQ-6-016: Tracks reliability of critical external dependencies.  
    
  - **Error Metrics:**
    
    - **Name:** application_error_count_total  
**Type:** counter  
**Unit:** count  
**Description:** Total count of application errors.  
**Error Types:**
    
    - 5xx_http_errors
    - uncaught_exceptions
    - specific_business_logic_errors
    
**Dimensions:**
    
    - service_name
    - error_code
    - error_severity
    
**Alert Threshold:** >X errors/min or >Y% error rate  
**Justification:** MON-006, MON-008, MON-011, REQ-007.1: Overall application stability.  
    - **Name:** ai_generation_error_count_total  
**Type:** counter  
**Unit:** count  
**Description:** Number of failed AI generation attempts.  
**Error Types:**
    
    - n8n_workflow_failure
    - ai_model_api_error
    - content_safety_violation
    - credit_deduction_failure
    
**Dimensions:**
    
    - failure_reason
    - user_tier
    - model_provider
    
**Alert Threshold:** >X% failure rate (KPI-004, REQ-SSPE-019, MON-013)  
**Justification:** REQ-007.1, REQ-SSPE-019, KPI-004: Tracks reliability of core AI feature.  
    - **Name:** mobile_app_crash_count_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of mobile application crashes.  
**Error Types:**
    
    - native_crash
    - dart_exception
    
**Dimensions:**
    
    - os_version
    - app_version
    - device_model
    
**Alert Threshold:** Crash-free user rate < 99.5% (KPI-004, REQ-8-007)  
**Justification:** REQ-8-007, REQ-SSPE-004, MON-009: Mobile app stability.  
    
  - **Throughput And Latency Metrics:**
    
    - **Name:** n8n_workflow_duration_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Execution time for n8n workflows.  
**Percentiles:**
    
    - p50
    - p90
    - p99
    
**Buckets:**
    
    - 1000
    - 5000
    - 15000
    - 30000
    - 60000
    - 120000
    
**Sla Targets:**
    
    - **P90:** part of REQ-SSPE-001/002 targets
    - **P99:** part of REQ-SSPE-001/002 targets
    
**Justification:** REQ-SSPE-019, REQ-3-001 to REQ-3-015: Performance of AI generation backend.  
    - **Name:** collaboration_sync_latency_ms  
**Type:** histogram  
**Unit:** ms  
**Description:** Latency for real-time collaboration updates (CRDT sync).  
**Percentiles:**
    
    - p90
    - p95
    
**Buckets:**
    
    - 50
    - 100
    - 200
    - 500
    - 1000
    - 2000
    
**Sla Targets:**
    
    - **P95:** <2000ms (REQ-5-001)
    
**Justification:** REQ-5-001: Real-time collaboration responsiveness.  
    
  
- **Business Kpi Identification:**
  
  - **Critical Business Metrics:**
    
    - **Name:** ai_generation_success_rate_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Percentage of AI generation attempts that complete successfully.  
**Business Owner:** Product Team  
**Calculation:** (Successful AI Generations / Total AI Generation Attempts) * 100  
**Reporting Frequency:** real-time, daily, weekly  
**Target:** >98%  
**Justification:** KPI-004, REQ-SSPE-019: Core product effectiveness.  
    - **Name:** user_activation_rate_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Percentage of new registered users who complete a key activation event (e.g., first successful creative generation) within X days.  
**Business Owner:** Product/Marketing Team  
**Calculation:** (Activated Users / New Registered Users) * 100 over period  
**Reporting Frequency:** daily, weekly  
**Target:** Target TBD (e.g., >60%)  
**Justification:** KPI-002: Measures onboarding effectiveness.  
    - **Name:** customer_churn_rate_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Percentage of paying subscribers who cancel their subscription in a given period.  
**Business Owner:** Product/Sales Team  
**Calculation:** (Cancelled Subscribers in Period / Subscribers at Start of Period) * 100  
**Reporting Frequency:** monthly  
**Target:** < X% (Target TBD)  
**Justification:** KPI-005: Measures customer retention.  
    - **Name:** time_to_first_value_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Time taken for a new user to achieve their first key value moment (e.g., generating their first creative).  
**Business Owner:** Product Team  
**Calculation:** Time difference between registration and first key action.  
**Reporting Frequency:** daily, weekly  
**Target:** Median < X minutes (Target TBD)  
**Justification:** KPI-002: Onboarding efficiency and product stickiness.  
    
  - **User Engagement Metrics:**
    
    - **Name:** daily_active_users_dau_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of unique users engaging with the platform daily.  
**Segmentation:**
    
    - user_tier
    - platform (web/mobile)
    
**Cohort Analysis:** True  
**Justification:** NFR-002, REQ-SSPE-006: Measures platform adoption and engagement.  
    - **Name:** monthly_active_users_mau_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of unique users engaging with the platform monthly.  
**Segmentation:**
    
    - user_tier
    - platform (web/mobile)
    
**Cohort Analysis:** True  
**Justification:** NFR-002, REQ-SSPE-006: Measures platform adoption and engagement.  
    
  - **Conversion Metrics:**
    
    - **Name:** registration_funnel_completion_rate_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Percentage of users who start and successfully complete the registration process.  
**Funnel Stage:** Registration  
**Conversion Target:** >90%  
**Justification:** KPI-001: User acquisition effectiveness.  
    - **Name:** free_to_paid_conversion_rate_percent  
**Type:** gauge  
**Unit:** percent  
**Description:** Percentage of free tier users who upgrade to a paid subscription.  
**Funnel Stage:** Subscription Upgrade  
**Conversion Target:** Target TBD (e.g., >5%)  
**Justification:** KPI-003: Monetization effectiveness.  
    
  - **Operational Efficiency Kpis:**
    
    - **Name:** ai_generation_pipeline_throughput_requests_per_minute  
**Type:** gauge  
**Unit:** requests/minute  
**Description:** Number of AI generation requests processed per minute.  
**Calculation:** Count of completed generation requests / time window in minutes.  
**Benchmark Target:** 1000 (NFR-002, REQ-SSPE-005)  
**Justification:** REQ-SSPE-019, NFR-002: System capacity and efficiency.  
    
  - **Revenue And Cost Metrics:**
    
    - **Name:** monthly_recurring_revenue_mrr_amount  
**Type:** gauge  
**Unit:** currency (e.g., USD)  
**Description:** Total monthly recurring revenue from subscriptions.  
**Frequency:** daily (calculated), monthly (reported)  
**Accuracy:** Matches Odoo financial records  
**Justification:** REQ-11-004 (implies tracking this): Core business financial health.  
    
  - **Customer Satisfaction Indicators:**
    
    
  
- **Collection Interval Optimization:**
  
  - **Sampling Frequencies:**
    
    - **Metric Category:** System Hardware (CPU, Basic Mem/Disk/Net)  
**Interval:** 15s  
**Justification:** Balance between responsiveness to issues and load.  
**Resource Impact:** low  
    - **Metric Category:** GPU Metrics (Util, Mem, Temp)  
**Interval:** 10s  
**Justification:** GPUs are critical and expensive; closer monitoring needed for AI workloads.  
**Resource Impact:** low  
    - **Metric Category:** Application Runtime (GC, Threads)  
**Interval:** 30s  
**Justification:** Sufficient for general health, less volatile than direct request metrics.  
**Resource Impact:** low  
    - **Metric Category:** API/Service Request Latency/Counters (Aggregated)  
**Interval:** Prometheus scrape: 15-30s (metrics are event-driven, scrape is collection)  
**Justification:** Real-time insights into service performance.  
**Resource Impact:** medium  
    - **Metric Category:** RabbitMQ Queue Depths  
**Interval:** 10s  
**Justification:** Critical for AI pipeline throughput and auto-scaling triggers.  
**Resource Impact:** low  
    - **Metric Category:** Business KPIs (aggregated from events/DB)  
**Interval:** 1m-1h (calculation frequency for gauges)  
**Justification:** Business trends, not typically needing sub-second resolution.  
**Resource Impact:** low (if efficiently calculated)  
    
  - **High Frequency Metrics:**
    
    - **Name:** gpu_utilization_percent  
**Interval:** 10s  
**Criticality:** high  
**Cost Justification:** Optimizing expensive GPU resources, timely scaling.  
    - **Name:** rabbitmq_queue_messages_ready_count (for AI gen queues)  
**Interval:** 10s  
**Criticality:** high  
**Cost Justification:** Driving AI worker auto-scaling, preventing processing delays.  
    - **Name:** http_server_request_latency_ms (P95/P99 for critical APIs)  
**Interval:** Events pushed, aggregated by Prometheus every 15s  
**Criticality:** high  
**Cost Justification:** Meeting NFRs for API responsiveness (REQ-SSPE-003).  
    
  - **Cardinality Considerations:**
    
    - **Metric Name:** http_server_request_latency_ms  
**Estimated Cardinality:** High if 'http_path' is not well-managed.  
**Dimension Strategy:** Use templated paths (e.g., /users/{user_id} -> /users/:id), avoid dynamic path segments as distinct label values.  
**Mitigation Approach:** Path normalization in instrumentation or Prometheus relabeling rules.  
    - **Metric Name:** ai_generation_latency_ms  
**Estimated Cardinality:** Medium (generation_type, user_tier, model_provider, model_name).  
**Dimension Strategy:** Ensure model_name doesn't create excessive unique values; perhaps group less common models.  
**Mitigation Approach:** Careful selection of reported model names.  
    
  - **Aggregation Periods:**
    
    - **Metric Type:** Performance Latencies (API, AI Gen)  
**Periods:**
    
    - 1m
    - 5m
    - 1h
    - 1d
    
**Retention Strategy:** Raw for short term, aggregated for long term.  
    - **Metric Type:** Error Rates  
**Periods:**
    
    - 1m
    - 5m
    - 1h
    
**Retention Strategy:** Aggregated for alerting and trends.  
    - **Metric Type:** Resource Utilization (CPU, Mem, GPU)  
**Periods:**
    
    - 1m
    - 10m
    - 1h
    
**Retention Strategy:** Aggregated for capacity planning and trend analysis.  
    
  - **Collection Methods:**
    
    - **Method:** Prometheus Pull  
**Applicable Metrics:**
    
    - system_*
    - gpu_*
    - app_runtime_*
    - db_*
    - rabbitmq_*
    - redis_*
    
**Implementation:** Standard Prometheus exporters (node, postgres, dcgm, etc. - MON-002).  
**Performance:** Low to medium overhead, configurable scrape intervals.  
    - **Method:** Application Instrumentation Push (to Prometheus client library / OpenTelemetry Collector)  
**Applicable Metrics:**
    
    - http_server_*
    - ai_generation_latency_ms
    - n8n_workflow_duration_ms
    - application_error_count_total
    
**Implementation:** Language-specific Prometheus client libraries or OpenTelemetry SDKs.  
**Performance:** Low overhead per request, aggregation at client/collector.  
    - **Method:** RUM Push (Client-side to Analytics Platform)  
**Applicable Metrics:**
    
    - web_lcp_ms
    - mobile_app_launch_time_ms
    - javascript_error_total
    - mobile_app_crash_count_total
    
**Implementation:** GA4, Mixpanel/Amplitude, Firebase SDKs in frontend/mobile apps.  
**Performance:** Minimal impact on client performance if SDKs are optimized.  
    
  
- **Aggregation Method Selection:**
  
  - **Statistical Aggregations:**
    
    - **Metric Name:** http_server_request_count_total  
**Aggregation Functions:**
    
    - sum
    - rate
    
**Windows:**
    
    - 1m
    - 5m
    - 1h
    
**Justification:** Track request volume and rate of change.  
    - **Metric Name:** system_cpu_utilization_percent  
**Aggregation Functions:**
    
    - avg
    - max
    
**Windows:**
    
    - 1m
    - 10m
    - 1h
    
**Justification:** Understand typical and peak CPU load.  
    
  - **Histogram Requirements:**
    
    - **Metric Name:** http_server_request_latency_ms  
**Buckets:**
    
    - 50
    - 100
    - 200
    - 500
    - 1000
    - 2500
    - 5000
    - 10000
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Accuracy:** Sufficient for SLO monitoring (REQ-SSPE-003).  
**Justification:** Detailed latency distribution for API performance analysis.  
    - **Metric Name:** ai_generation_latency_ms (sample)  
**Buckets:**
    
    - 1000
    - 5000
    - 10000
    - 15000
    - 20000
    - 25000
    - 30000
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Accuracy:** Sufficient for SLO monitoring (REQ-SSPE-001).  
**Justification:** Track sample generation performance against NFR.  
    - **Metric Name:** ai_generation_latency_ms (high_res)  
**Buckets:**
    
    - 15000
    - 30000
    - 60000
    - 90000
    - 120000
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Accuracy:** Sufficient for SLO monitoring (REQ-SSPE-002).  
**Justification:** Track high-resolution generation performance against NFR.  
    
  - **Percentile Calculations:**
    
    - **Metric Name:** http_server_request_latency_ms  
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Algorithm:** Prometheus histogram_quantile  
**Accuracy:** Good estimate based on histogram buckets.  
**Justification:** Required for NFRs (REQ-SSPE-003, REQ-WCI-002).  
    - **Metric Name:** ai_generation_latency_ms  
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Algorithm:** Prometheus histogram_quantile  
**Accuracy:** Good estimate based on histogram buckets.  
**Justification:** Required for NFRs (REQ-SSPE-001, REQ-SSPE-002).  
    
  - **Metric Types:**
    
    - **Name:** http_server_request_count_total  
**Implementation:** counter  
**Reasoning:** Monotonically increasing count of requests.  
**Resets Handling:** Handled by `rate()` and `increase()` functions in PromQL.  
    - **Name:** system_cpu_utilization_percent  
**Implementation:** gauge  
**Reasoning:** Represents a current value that can go up or down.  
**Resets Handling:** N/A  
    - **Name:** http_server_request_latency_ms  
**Implementation:** histogram  
**Reasoning:** To observe distribution and calculate percentiles for latencies.  
**Resets Handling:** N/A  
    
  - **Dimensional Aggregation:**
    
    - **Metric Name:** http_server_request_count_total  
**Dimensions:**
    
    - service_name
    - http_status_code_class (2xx, 4xx, 5xx)
    
**Aggregation Strategy:** Sum by service and status code class.  
**Cardinality Impact:** Low to medium.  
**Justification:** Overall service health and error rates per service.  
    
  - **Derived Metrics:**
    
    - **Name:** api_error_rate_percent  
**Calculation:** sum(rate(http_server_request_count_total{http_status_code=~"5.."}[5m])) by (service_name) / sum(rate(http_server_request_count_total[5m])) by (service_name) * 100  
**Source Metrics:**
    
    - http_server_request_count_total
    
**Update Frequency:** Prometheus scrape interval (e.g., 15s)  
**Justification:** MON-011: Alerting on API error rates.  
    - **Name:** ai_generation_success_rate_percent_derived  
**Calculation:** (sum(rate(ai_generation_request_total{status="success"}[1h])) / sum(rate(ai_generation_request_total[1h]))) * 100  
**Source Metrics:**
    
    - ai_generation_request_total (with status label)
    
**Update Frequency:** Prometheus scrape interval  
**Justification:** KPI-004, REQ-SSPE-019: Tracking core business KPI.  
    
  
- **Storage Requirements Planning:**
  
  - **Retention Periods:**
    
    - **Metric Type:** Prometheus Metrics (High Resolution)  
**Retention Period:** 30-90 days  
**Justification:** DEP-005 (general reference to metrics). Operational troubleshooting and short-term trend analysis.  
**Compliance Requirement:** N/A  
    - **Metric Type:** Prometheus Metrics (Aggregated/Downsampled)  
**Retention Period:** 1-2 years  
**Justification:** Long-term capacity planning and trend analysis.  
**Compliance Requirement:** N/A  
    - **Metric Type:** Application Logs (Operational/Debug)  
**Retention Period:** 14 days (hot), 30 days (warm/cold)  
**Justification:** MON-007: Troubleshooting recent issues.  
**Compliance Requirement:** N/A  
    - **Metric Type:** Application Logs (Info/Audit)  
**Retention Period:** 90 days (hot), 1 year (warm/cold)  
**Justification:** MON-007: Audit and compliance needs.  
**Compliance Requirement:** Varies (e.g., financial transaction related logs per REQ-6-020)  
    - **Metric Type:** Security Audit Logs  
**Retention Period:** 12+ months (active), longer in archive  
**Justification:** MON-007, SEC-006: Compliance and security investigation.  
**Compliance Requirement:** Typically 12 months or more based on regulations.  
    
  - **Data Resolution:**
    
    - **Time Range:** Last 24 hours  
**Resolution:** Raw (e.g., 10s-60s)  
**Query Performance:** High, for dashboards and alerting.  
**Storage Optimization:** N/A  
    - **Time Range:** Last 30 days  
**Resolution:** 1-5 minutes (downsampled)  
**Query Performance:** Medium, for trend analysis.  
**Storage Optimization:** Downsampling reduces storage.  
    - **Time Range:** >30 days  
**Resolution:** 1 hour (downsampled)  
**Query Performance:** Low, for long-term capacity planning.  
**Storage Optimization:** Significant storage reduction.  
    
  - **Downsampling Strategies:**
    
    - **Source Resolution:** 15s  
**Target Resolution:** 1m  
**Aggregation Method:** avg, sum, max, min, count (as appropriate for metric type)  
**Trigger Condition:** Automated Prometheus recording rules.  
    - **Source Resolution:** 1m  
**Target Resolution:** 1h  
**Aggregation Method:** avg, sum, max, min, count  
**Trigger Condition:** Automated Prometheus recording rules.  
    
  - **Storage Performance:**
    
    - **Write Latency:** <100ms for Prometheus TSDB appends
    - **Query Latency:** <1s for typical Grafana dashboard panels, <10s for complex ad-hoc queries
    - **Throughput Requirements:** Sustain NFR-002 request rates for metrics generation.
    - **Scalability Needs:** Scale with user growth (1M users - REQ-SSPE-006) and data volume.
    
  - **Query Optimization:**
    
    - **Query Pattern:** Time-series queries by service/instance over specific time ranges.  
**Optimization Strategy:** Prometheus TSDB optimized for time-series. Grafana query optimization.  
**Indexing Requirements:**
    
    - Prometheus uses its own indexing.
    
    - **Query Pattern:** Log search by correlation ID, user ID, error message.  
**Optimization Strategy:** ELK/Loki indexing on key fields.  
**Indexing Requirements:**
    
    - correlation_id
    - user_id
    - service_name
    - timestamp
    - log_level
    
    
  - **Cost Optimization:**
    
    - **Strategy:** Metric Cardinality Management  
**Implementation:** Avoid high-cardinality labels, use relabeling rules in Prometheus.  
**Expected Savings:** Reduced Prometheus storage and query load.  
**Tradeoffs:** Potential loss of very granular query dimensions.  
    - **Strategy:** Log Tiered Storage & Retention  
**Implementation:** Configure ELK/Loki index lifecycle management to move older logs to cheaper storage or delete.  
**Expected Savings:** Reduced log storage costs.  
**Tradeoffs:** Slower query performance for older, cold-stored logs.  
    
  
- **Project Specific Metrics Config:**
  
  - **Standard Metrics:**
    
    - **Name:** node_cpu_seconds_total  
**Type:** counter  
**Unit:** seconds  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** node_exporter
    
**Thresholds:**
    
    - **Warning:** rate > 0.8 per core
    - **Critical:** rate > 0.9 per core
    
**Dimensions:**
    
    - instance
    - mode (user, system, idle, etc.)
    
    - **Name:** process_resident_memory_bytes  
**Type:** gauge  
**Unit:** bytes  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** app_exporter / node_exporter
    
**Thresholds:**
    
    - **Warning:** >80% of allocated
    - **Critical:** >90% of allocated
    
**Dimensions:**
    
    - job
    - instance
    
    - **Name:** nginx_http_requests_total  
**Type:** counter  
**Unit:** count  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** nginx_vts_exporter or ingress_nginx_exporter
    
**Thresholds:**
    
    - **Warning:** error rate > 5%
    - **Critical:** error rate > 10%
    
**Dimensions:**
    
    - host
    - status_code_class
    
    - **Name:** postgresql_pg_stat_activity_count  
**Type:** gauge  
**Unit:** count  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** postgres_exporter
    
**Thresholds:**
    
    - **Warning:** >80% of max_connections
    - **Critical:** >90% of max_connections
    
**Dimensions:**
    
    - datname
    - state
    
    - **Name:** rabbitmq_queue_messages  
**Type:** gauge  
**Unit:** count  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** rabbitmq_exporter
    
**Thresholds:**
    
    - **Warning:** >1000 for critical queues
    - **Critical:** >5000 for critical queues
    
**Dimensions:**
    
    - queue
    - vhost
    
    - **Name:** dcgm_gpu_utilization  
**Type:** gauge  
**Unit:** percent  
**Collection:**
    
    - **Interval:** 10s
    - **Method:** dcgm_exporter
    
**Thresholds:**
    
    - **Warning:** avg > 85%
    - **Critical:** avg > 95%
    
**Dimensions:**
    
    - gpu_uuid
    - instance
    
    
  - **Custom Metrics:**
    
    - **Name:** creativeflow_ai_generation_duration_seconds  
**Description:** Duration of AI creative generation process by type and model.  
**Calculation:** End time - Start time of generation workflow.  
**Type:** histogram  
**Unit:** seconds  
**Business Context:** Core product feature performance.  
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application instrumentation (n8n, AI Orchestration Service)
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - p90 > 30s for samples (REQ-SSPE-001)
      - p90 > 120s for high_res (REQ-SSPE-002)
      
    
    - **Name:** creativeflow_user_credits_consumed_total  
**Description:** Total credits consumed by users for billable actions.  
**Calculation:** Sum of credits deducted per action.  
**Type:** counter  
**Unit:** credits  
**Business Context:** Monetization and resource usage.  
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application instrumentation (Subscription & Billing Service)
    
**Alerting:**
    
    - **Enabled:** False
    
    - **Name:** creativeflow_subscription_event_total  
**Description:** Count of subscription lifecycle events.  
**Calculation:** Counter incremented on each subscription event.  
**Type:** counter  
**Unit:** count  
**Business Context:** Subscription management tracking.  
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** Application instrumentation (Odoo Adapter / Subscription Service)
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - high rate of payment_failure events
      
    
    - **Name:** creativeflow_api_user_request_count_total  
**Description:** Number of requests made by API users.  
**Calculation:** Counter incremented per API call from an API key.  
**Type:** counter  
**Unit:** count  
**Business Context:** API platform usage and monetization.  
**Collection:**
    
    - **Interval:** N/A (event-based)
    - **Method:** API Gateway or API Developer Platform Service instrumentation
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - rate limit exceeded count > X
      
    
    
  - **Dashboard Metrics:**
    
    - **Dashboard:** System Health Overview  
**Metrics:**
    
    - system_cpu_utilization_percent (avg by role)
    - system_memory_utilization_percent (avg by role)
    - system_disk_space_used_percent (critical volumes)
    - api_gateway_request_latency_ms (p95 overall)
    - api_error_rate_percent (overall)
    - rabbitmq_queue_messages_ready_count (key queues)
    - postgresql_pg_stat_activity_count (active connections)
    - service_uptime_percentage (key services)
    
**Refresh Interval:** 30s  
**Audience:** DevOps, SRE  
    - **Dashboard:** AI Generation Pipeline Performance  
**Metrics:**
    
    - creativeflow_ai_generation_duration_seconds (p90 by type)
    - ai_generation_success_rate_percent_derived
    - ai_generation_error_count_total (by failure_reason)
    - rabbitmq_queue_messages_ready_count (ai_gen_queue)
    - n8n_workflow_duration_ms (p90)
    - dcgm_gpu_utilization (avg per node)
    - external_ai_service_call_latency_ms (by provider)
    
**Refresh Interval:** 1m  
**Audience:** AI/ML Team, Product Team, DevOps  
    - **Dashboard:** Business KPIs  
**Metrics:**
    
    - daily_active_users_dau_count
    - monthly_active_users_mau_count
    - registration_funnel_completion_rate_percent
    - free_to_paid_conversion_rate_percent
    - monthly_recurring_revenue_mrr_amount
    - ai_generation_success_rate_percent
    
**Refresh Interval:** 1h  
**Audience:** Product Management, Business Stakeholders  
    
  
- **Implementation Priority:**
  
  - **Component:** Core System Metrics (CPU, Mem, Disk, Network, Nginx, PostgreSQL, RabbitMQ, Redis)  
**Priority:** high  
**Dependencies:**
    
    - Prometheus setup
    - Standard exporters
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** AI Generation Pipeline Metrics (Latency, Throughput, Error Rates, GPU Util)  
**Priority:** high  
**Dependencies:**
    
    - Prometheus setup
    - DCGM exporter
    - n8n instrumentation
    - AI Orchestration Service instrumentation
    
**Estimated Effort:** High  
**Risk Level:** medium  
  - **Component:** API Gateway & Core API Performance Metrics (Latency, Error Rates, Throughput)  
**Priority:** high  
**Dependencies:**
    
    - Prometheus setup
    - API Gateway instrumentation
    - Backend service instrumentation
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Subscription & Billing Metrics (Payment success/failure, Subscription events, Credit consumption)  
**Priority:** high  
**Dependencies:**
    
    - Prometheus setup
    - Odoo Adapter/Subscription Service instrumentation
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Business KPIs (DAU/MAU, Conversion Rates, AI Success Rate)  
**Priority:** medium  
**Dependencies:**
    
    - Application event tracking
    - Analytics platform integration (GA4/Mixpanel)
    - Metrics aggregation logic
    
**Estimated Effort:** High  
**Risk Level:** medium  
  - **Component:** Mobile App Performance Metrics (Launch Time, Crash Rate)  
**Priority:** medium  
**Dependencies:**
    
    - Firebase Analytics / RUM tool integration
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  
- **Risk Assessment:**
  
  - **Risk:** Metric Overload / High Cardinality leading to Prometheus performance issues.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Careful label selection, use of recording rules for aggregation, cardinality analysis during design.  
**Contingency Plan:** Scale Prometheus, optimize queries, drop high-cardinality metrics/labels.  
  - **Risk:** Inaccurate or Misleading Metrics due to instrumentation errors or misinterpretation.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Thorough testing of metric collection, clear documentation of metric definitions and calculations, regular review of dashboards.  
**Contingency Plan:** Correct instrumentation, re-calculate historical data if possible, update documentation.  
  - **Risk:** Alert Fatigue from poorly tuned thresholds or noisy alerts.  
**Impact:** medium  
**Probability:** high  
**Mitigation:** Implement SMART thresholds, use alert inhibition/grouping, regular review and tuning of alerts (MON-012).  
**Contingency Plan:** Temporarily silence noisy alerts, investigate root cause, adjust thresholds.  
  - **Risk:** Monitoring System Outage impacting visibility into platform health.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Monitor the monitoring system itself (e.g., Prometheus self-monitoring, Alertmanager HA), have redundant monitoring components where feasible.  
**Contingency Plan:** Follow DR plan for monitoring system, rely on basic system logs in interim.  
  
- **Recommendations:**
  
  - **Category:** Metric Granularity & Cardinality  
**Recommendation:** Proactively manage metric cardinality. Avoid using unbounded unique identifiers (e.g., raw user IDs, full URLs with query params) as direct Prometheus label values. Use aggregation and grouping for high-cardinality dimensions.  
**Justification:** High cardinality significantly impacts Prometheus performance (storage, query speed, memory usage). Essential for a system aiming for 1M users.  
**Priority:** high  
**Implementation Notes:** Use Prometheus recording rules to create aggregated metrics with lower cardinality. For paths, use templated versions as labels.  
  - **Category:** Dashboarding & Visualization  
**Recommendation:** Develop role-specific Grafana dashboards that focus on actionable insights rather than just displaying raw data. Start with high-level system health and drill down to service/component specific views.  
**Justification:** Actionable dashboards help teams quickly identify and diagnose issues, improving MTTR. Aligns with MON-003 requirement for role-based access.  
**Priority:** high  
**Implementation Notes:** Follow dashboard design best practices (e.g., RED method - Rate, Errors, Duration; USE method - Utilization, Saturation, Errors).  
  - **Category:** Alerting Strategy  
**Recommendation:** Focus alerts on symptom-based issues (e.g., user-facing errors, high latency impacting SLOs, service unavailability) rather than purely cause-based alerts (e.g., high CPU without impact). Link alerts to SOPs/runbooks (MON-012).  
**Justification:** Reduces alert noise, ensures alerts are actionable, and helps in quicker incident response. Aligns with MON-011 and QA-003.1.  
**Priority:** high  
**Implementation Notes:** Define clear SLOs for critical services and alert when these are at risk or breached.  
  - **Category:** Log Correlation  
**Recommendation:** Ensure consistent propagation and logging of Correlation IDs (Trace IDs) across all services and asynchronous operations (MON-005, MON-006). This is vital for effective distributed tracing and log analysis.  
**Justification:** Crucial for troubleshooting issues in a microservices architecture, especially complex flows like AI generation.  
**Priority:** high  
**Implementation Notes:** Use OpenTelemetry standards for trace propagation. Ensure n8n workflows and Odoo customizations also participate in tracing where possible.  
  - **Category:** Regular Review & Iteration  
**Recommendation:** Establish a process for regularly reviewing (e.g., quarterly) the effectiveness of collected metrics, dashboards, and alert thresholds. Prune unused or low-value metrics and refine alerts based on operational experience.  
**Justification:** Ensures the monitoring system remains relevant, efficient, and doesn't contribute to noise or performance degradation. Aligns with MON-012 for alert tuning.  
**Priority:** medium  
**Implementation Notes:** Involve representatives from DevOps, SRE, Product, and Development teams in these reviews.  
  


---

