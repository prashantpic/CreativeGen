sequenceDiagram
    actor "WebApp (PWA)" as repowebapppwa
    participant "API Gateway" as compapigatewaynginx
    participant "Odoo Backend" as svcodoobackend
    participant "PostgreSQL DB" as repodbpostgresql
    participant "RabbitMQ" as compmessagequeuerabbitmq
    participant "n8n Workflow Engine" as svcn8nworkflowengine
    participant "OpenAI Service" as extaiopenai
    participant "K8s AI Cluster" as compk8scluster
    participant "MinIO Storage" as repostorageminio
    participant "Notification Service" as svcnotificationservice

    note over repowebapppwa: User is authenticated prior to this flow.

    repowebapppwa--compapigatewaynginx: 1. Submit Creative Request (prompt, params)
    activate compapigatewaynginx

    compapigatewaynginx--svcodoobackend: 2. Forward Creative Request
    activate svcodoobackend
    svcodoobackend--svcodoobackend: 2.1. Validate Request & Check Credits (REQ-016)
    svcodoobackend--repodbpostgresql: 2.2. Record Generation Request (status: pendingsamples)
    activate repodbpostgresql
    repodbpostgresql--svcodoobackend: generationRequestId
    deactivate repodbpostgresql
    svcodoobackend--compmessagequeuerabbitmq: 2.3. Publish Event: AIGenerationJobRequested
    activate compmessagequeuerabbitmq
    deactivate compmessagequeuerabbitmq
    svcodoobackend--compapigatewaynginx: 3. HTTP 202 Accepted (Request Queued)
    deactivate svcodoobackend

    compapigatewaynginx--repowebapppwa: 3. HTTP 202 Accepted (Request Queued)
    deactivate compapigatewaynginx

    activate repowebapppwa
    repowebapppwa--repowebapppwa: 3.1. [UI shows 'Generating samples...']
    deactivate repowebapppwa

    compmessagequeuerabbitmq--svcn8nworkflowengine: 4. Consume Event: AIGenerationJobRequested
    activate svcn8nworkflowengine
    svcn8nworkflowengine--svcn8nworkflowengine: 4.1. Pre-process data, select AI model
    alt [AI Model Choice]
        svcn8nworkflowengine--extaiopenai: 4.2.1. [case OpenAI] Call OpenAI API for samples
        activate extaiopenai
        extaiopenai--svcn8nworkflowengine: Sample Image Data/URLs
        deactivate extaiopenai
    else [case K8s Custom Model]
        svcn8nworkflowengine--compk8scluster: 4.2.2. [case K8s Custom Model] Submit AI Job for samples
        activate compk8scluster
        compk8scluster--svcn8nworkflowengine: Sample Image Data/Paths
        deactivate compk8scluster
    end
    loop [For Each Sample]
        svcn8nworkflowengine--repostorageminio: 4.3. Store Sample Image
        activate repostorageminio
        repostorageminio--svcn8nworkflowengine: Stored Path/URL
        deactivate repostorageminio
    end
    note right of svcodoobackend: Odoo deducts credits for sample generation (REQ-016) as part of step 4.4 processing.
    svcn8nworkflowengine--svcodoobackend: 4.4. Update Generation Request (samples metadata, deduct credits)
    activate svcodoobackend
    svcodoobackend--repodbpostgresql: 4.4.1. UPDATE generations (status, sampleassets, creditscostsample)
    activate repodbpostgresql
    repodbpostgresql--svcodoobackend: Ack
    deactivate repodbpostgresql
    svcodoobackend--svcn8nworkflowengine: Ack
    deactivate svcodoobackend
    svcn8nworkflowengine--compmessagequeuerabbitmq: 4.5. Publish Event: AIGenerationSamplesReady
    activate compmessagequeuerabbitmq
    deactivate compmessagequeuerabbitmq
    deactivate svcn8nworkflowengine

    compmessagequeuerabbitmq--svcnotificationservice: 5. Consume Event: AIGenerationSamplesReady
    activate svcnotificationservice

    svcnotificationservice--repowebapppwa: 6. WebSocket: samplesready (sample URLs/data)
    deactivate svcnotificationservice

    activate repowebapppwa
    repowebapppwa--repowebapppwa: 6.1. [UI displays samples to user]
    deactivate repowebapppwa

    repowebapppwa--compapigatewaynginx: 7. User Selects Sample (generationRequestId, selectedSampleId)
    activate compapigatewaynginx

    compapigatewaynginx--svcodoobackend: 8. Forward Sample Selection
    activate svcodoobackend
    svcodoobackend--repodbpostgresql: 8.1. Update Generation Request (status: processingfinal, selectedsampleid)
    activate repodbpostgresql
    repodbpostgresql--svcodoobackend: Ack
    deactivate repodbpostgresql
    svcodoobackend--compmessagequeuerabbitmq: 8.2. Publish Event: AIGenerationFinalJobRequested
    activate compmessagequeuerabbitmq
    deactivate compmessagequeuerabbitmq
    svcodoobackend--compapigatewaynginx: 9. HTTP 202 Accepted (Final Generation Queued)
    deactivate svcodoobackend

    compapigatewaynginx--repowebapppwa: 9. HTTP 202 Accepted (Final Generation Queued)
    deactivate compapigatewaynginx

    activate repowebapppwa
    repowebapppwa--repowebapppwa: 9.1. [UI shows 'Generating final asset...']
    deactivate repowebapppwa

    compmessagequeuerabbitmq--svcn8nworkflowengine: 10. Consume Event: AIGenerationFinalJobRequested
    activate svcn8nworkflowengine
    svcn8nworkflowengine--svcn8nworkflowengine: 10.1. Prepare for high-res generation
    alt [AI Model Choice]
        svcn8nworkflowengine--extaiopenai: 10.2.1. [case OpenAI] Call OpenAI API for final asset
        activate extaiopenai
        extaiopenai--svcn8nworkflowengine: High-Res Image Data
        deactivate extaiopenai
    else [case K8s Custom Model]
        svcn8nworkflowengine--compk8scluster: 10.2.2. [case K8s Custom Model] Submit AI Job for final asset
        activate compk8scluster
        compk8scluster--svcn8nworkflowengine: High-Res Image Data/Path
        deactivate compk8scluster
    end
    svcn8nworkflowengine--repostorageminio: 10.3. Store Final Asset Image
    activate repostorageminio
    repostorageminio--svcn8nworkflowengine: Stored Path/URL
    deactivate repostorageminio
    note right of svcodoobackend: Odoo deducts credits for final generation (REQ-016) as part of step 10.4 processing.
    svcn8nworkflowengine--svcodoobackend: 10.4. Update Generation Request (final asset metadata, deduct credits)
    activate svcodoobackend
    svcodoobackend--repodbpostgresql: 10.4.1. UPDATE generations (status: completed, finalassetpath, creditscostfinal)
    activate repodbpostgresql
    repodbpostgresql--svcodoobackend: Ack
    deactivate repodbpostgresql
    svcodoobackend--svcn8nworkflowengine: Ack
    deactivate svcodoobackend
    svcn8nworkflowengine--compmessagequeuerabbitmq: 10.5. Publish Event: AIGenerationFinalAssetReady
    activate compmessagequeuerabbitmq
    deactivate compmessagequeuerabbitmq
    deactivate svcn8nworkflowengine

    compmessagequeuerabbitmq--svcnotificationservice: 11. Consume Event: AIGenerationFinalAssetReady
    activate svcnotificationservice

    svcnotificationservice--repowebapppwa: 12. WebSocket: finalassetready (finalAssetUrl)
    deactivate svcnotificationservice

    activate repowebapppwa
    repowebapppwa--repowebapppwa: 12.1. [UI displays final asset to user]
    deactivate repowebapppwa

    note over repowebapppwa, svcnotification_service: Error handling (e.g., AI model failure, insufficient credits) leads to alternative paths not fully detailed here but would involve error responses or notifications.
