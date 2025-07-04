sequenceDiagram
    actor "User Load (System Input)" as actoruserload
    participant "RabbitMQ" as compmessagequeuerabbitmq
    participant "Prometheus" as svcprometheusmonitoring
    participant "Kubernetes Cluster" as compk8scluster
    participant "AI Worker Pod(s)" as repoaiworkerpod
    actor "Cloud Provider API / Infra Provisioner" as actorcloudproviderapi

    actoruserload-compmessagequeuerabbitmq: 1. User activity generates 'AIGenerationJobRequested' messages
    activate compmessagequeuerabbitmq
    note over compmessagequeuerabbitmq: Queue depth for AI jobs increases due to incoming user requests.

    svcprometheusmonitoring-compmessagequeuerabbitmq: 2. ScrapeMetrics() [rabbitmqqueuemessagesready]
    activate svcprometheusmonitoring
    compmessagequeuerabbitmq--svcprometheusmonitoring: MetricValue(queueDepth)

    compk8scluster-svcprometheusmonitoring: 3. QueryMetric(metricName='rabbitmqqueuemessagesready', ...)
    activate compk8scluster
    note over compk8scluster: HPA (Horizontal Pod Autoscaler) polls Prometheus (or Custom Metrics API fed by Prometheus) for the scaling metric.
    svcprometheusmonitoring--compk8scluster: MetricValue(currentQueueDepth)
    deactivate svcprometheusmonitoring

    loop 4. currentQueueDepth  targetThreshold
        compk8scluster-compk8scluster: 4.1. HPA: CalculateNewReplicas()
        compk8scluster--compk8scluster: newReplicaCount
        compk8scluster-compk8scluster: 4.2. HPA: UpdateDeployment(aiWorkerDeployment, desiredReplicas=newReplicaCount)
        note over compk8scluster: HPA updates the .spec.replicas field of the AI Worker Deployment object via Kubernetes API Server.
        compk8scluster--compk8scluster: ack
    end

    compk8scluster-compk8scluster: 5. DeploymentController: Observe new desiredReplicas
    compk8scluster-compk8scluster: 6. DeploymentController: CreateNewPodObject(s)
    note over compk8scluster: Deployment Controller creates new Pod specifications based on the Deployment template.
    compk8scluster--compk8scluster: podObject(s) Created
    compk8scluster-compk8scluster: 7. Scheduler: WatchForUnassignedPods()
    compk8scluster-compk8scluster: 8. Scheduler: FilterNodesForPod(newPod, gpuRequirement)
    compk8scluster--compk8scluster: suitableNode / noSuitableNode

    alt 9. suitableNode found
        compk8scluster-compk8scluster: 9.1. Scheduler: BindPodToNode(podName, nodeName)
        compk8scluster--compk8scluster: ack
        compk8scluster-compk8scluster: 9.2. Kubelet (on Node): ObservePodAssignment(podName)
        compk8scluster-compk8scluster: 9.3. Kubelet: PullContainerImage(imageName)
        compk8scluster--compk8scluster: imagePulled
        compk8scluster-repoaiworkerpod: 9.4. Kubelet: StartContainer() - AIWorkerPod created
        activate repoaiworkerpod
        repoaiworkerpod--compk8scluster: podRunning
    else 10. noSuitableNode (insufficient GPU resources)
        compk8scluster-compk8scluster: 10.1. Scheduler: Pod remains Unschedulable
        compk8scluster-compk8scluster: 10.2. ClusterAutoscaler: DetectUnschedulablePods(reason='InsufficientGPU')
        compk8scluster-compk8scluster: 10.3. ClusterAutoscaler: EvaluateNodePoolScalingOptions(gpuNodePool)
        compk8scluster--compk8scluster: canScaleUpGpuPool
        compk8scluster-actorcloudproviderapi: 10.4. ClusterAutoscaler: RequestNewNode(gpuNodePool, count)
        activate actorcloudproviderapi
        actorcloudproviderapi--compk8scluster: nodeProvisioningStarted
        actorcloudproviderapi-compk8scluster: 10.5. New GPU Node Joins Cluster
        note over compk8scluster: New node registers with Kubernetes API server and becomes schedulable.
        deactivate actorcloudproviderapi
        compk8scluster-compk8scluster: 10.6. Scheduler: Re-evaluate Pod (now finds new node)
        note right of compk8scluster: Flow proceeds similar to Alternative 9 (Schedule Pod on Available Node).
    end

    note over repoaiworkerpod: This interaction occurs for each newly started AI Worker Pod.
    repoaiworkerpod-compmessagequeuerabbitmq: 11. Connect() & SubscribeToQueue(aijobqueue)
    compmessagequeuerabbitmq--repoaiworkerpod: ack/subscriptionConfirmed

    loop 12. while jobs available and pod active
        repoaiworkerpod-compmessagequeuerabbitmq: ConsumeJob()
        compmessagequeuerabbitmq--repoaiworkerpod: jobData
        repoaiworkerpod-repoaiworkerpod: 12.1. ProcessJob(jobData)
        repoaiworkerpod--repoaiworkerpod: processingComplete
        repoaiworkerpod-compmessagequeuerabbitmq: 12.2. AcknowledgeJob(jobId)
        note over compmessagequeuerabbitmq: Job is removed from queue; queue depth decreases.
    end

    svcprometheusmonitoring-compmessagequeuerabbitmq: 13. ScrapeMetrics() [updated rabbitmqqueuemessagesready]
    activate svcprometheusmonitoring
    compmessagequeuerabbitmq--svcprometheusmonitoring: MetricValue(newQueueDepth)

    compk8scluster-svcprometheusmonitoring: 14. QueryMetric(metricName='rabbitmqqueuemessagesready', ...)
    note over compk8scluster: HPA continues to monitor the metric.
    svcprometheusmonitoring--compk8scluster: MetricValue(newQueueDepth)
    deactivate svcprometheusmonitoring

    compk8scluster-compk8scluster: 15. HPA: EvaluateMetric(newQueueDepth, targetThreshold)
    note over compk8scluster: If newQueueDepth is below target for a period, HPA might scale down (not detailed here).

    deactivate compk8scluster
    deactivate repoaiworkerpod
    deactivate compmessagequeuerabbitmq
    
    note over actoruserload,actorcloudproviderapi: This diagram illustrates the scale-up scenario. Scale-down logic by HPA would be similar but triggered by low queue depth/utilization.
    note over actoruserload,actorcloudproviderapi: Error handling for provisioning failures (Pod/Node) or AI worker crashes are handled by Kubernetes self-healing mechanisms and specific alerting, not detailed in this scaling sequence.
    note over actoruserload,actorcloudproviderapi: Alternative scaling metric could be average GPU utilization across worker pods (from DCGM via Prometheus). HPA would then scale up if average GPU util is high AND there are pending jobs (high queue depth), or scale down if util is low.