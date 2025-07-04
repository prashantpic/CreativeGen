sequenceDiagram
    actor "WebApp (PWA)" as repo-webapp-pwa
    participant "API Gateway" as comp-apigateway-nginx
    participant "Odoo Backend" as svc-odoo-backend
    participant "Stripe" as ext-payment-stripe
    participant "PostgreSQL DB" as repo-db-postgresql
    participant "RabbitMQ" as comp-messagequeue-rabbitmq
    participant "Notification Service" as svc-notification-service

    repo-webapp-pwa-comp-apigateway-nginx: 1. RequestSubscriptionUpgrade(plan='Pro')
    activate comp-apigateway-nginx
    comp-apigateway-nginx-svc-odoo-backend: 2. ForwardRequestSubscriptionUpgrade(userId, plan='Pro')
    activate svc-odoo-backend
    svc-odoo-backend-ext-payment-stripe: 2.1. CreateCheckoutSession(plan='Pro', userId, successUrl, cancelUrl)
    activate ext-payment-stripe
    ext-payment-stripe--svc-odoo-backend: 2.2. CheckoutSession{id, url, clientSecret}
    deactivate ext-payment-stripe
    svc-odoo-backend--comp-apigateway-nginx: 3. UpgradeInitiationResponse{checkoutSessionId/clientSecret}
    deactivate svc-odoo-backend
    comp-apigateway-nginx--repo-webapp-pwa: 4. UpgradeInitiationResponse{checkoutSessionId/clientSecret}
    deactivate comp-apigateway-nginx

    note over ext-payment-stripe: User completes payment process directly with Stripe UI (redirect or embedded elements). This diagram shows the system interactions around that user action.
    loop User Payment Interaction
        repo-webapp-pwa-repo-webapp-pwa: 5. User redirected to Stripe Checkout / Interacts with Stripe Elements
    end

    ext-payment-stripe-svc-odoo-backend: 6. Webhook: paymentintent.succeeded (or checkout.session.completed)
    activate svc-odoo-backend
    note right of svc-odoo-backend: Odoo Backend verifies webhook signature for security. Details of Odoo's internal model updates (e.g., Sales Order, Invoice status) are abstracted.
    svc-odoo-backend-svc-odoo-backend: 6.1. Verify Stripe Webhook Signature & Event Data
    svc-odoo-backend-svc-odoo-backend: 6.2. Update Odoo Internal Subscription Records (e.g., Sales Order, Invoice)
    svc-odoo-backend-repo-db-postgresql: 6.3. UPDATE users SET subscriptiontier='Pro', ...
    activate repo-db-postgresql
    repo-db-postgresql--svc-odoo-backend: 6.4. DB Update Ack
    deactivate repo-db-postgresql
    svc-odoo-backend-repo-db-postgresql: 6.5. UPDATE subscriptions SET status='active', plan_id='Pro', ...
    activate repo-db-postgresql
    repo-db-postgresql--svc-odoo-backend: 6.6. DB Update Ack
    deactivate repo-db-postgresql
    note over comp-messagequeue-rabbitmq: The SubscriptionTierChanged event may also be consumed by other services like an Auth Service (for permission/role cache updates), but Auth Service is not a direct participant in this specific diagram as per participantRepositoryIds for SD-CF-004. Odoo updated the user's tier in the shared DB which Auth service can read.
    svc-odoo-backend-comp-messagequeue-rabbitmq: 6.7. Publish Event: SubscriptionTierChanged{userId, newTier='Pro'}
    activate comp-messagequeue-rabbitmq
    svc-odoo-backend--ext-payment-stripe: 7. 200 OK (Webhook Acknowledgement)
    deactivate svc-odoo-backend

    comp-messagequeue-rabbitmq-svc-notification-service: 8. Deliver Event: SubscriptionTierChanged
    deactivate comp-messagequeue-rabbitmq
    activate svc-notification-service
    svc-notification-service-svc-notification-service: 8.1. Process SubscriptionTierChanged Event
    svc-notification-service-repo-webapp-pwa: 8.2. WebSocket: NotifySubscriptionUpdate(newTier='Pro')
    activate repo-webapp-pwa
    deactivate svc-notification-service

    repo-webapp-pwa-repo-webapp-pwa: 9. Update UI to reflect 'Pro' subscription
    deactivate repo-webapp-pwa
