sequenceDiagram
    actor "User (Browser)" as useractor
    participant "CreativeFlow WebApp" as repowebapppwa
    actor "Google OAuth Service" as extsocialgoogle
    participant "API Gateway" as compapigatewaynginx
    participant "Odoo Backend" as svcodooobackend
    participant "PostgreSQL DB" as repodbpostgresql

    useractor-repowebapppwa: 1. Clicks 'Sign in with Google'
    activate repowebapppwa

    repowebapppwa-useractor: 2. Initiate Redirect to Google OAuth 2.0 Authorization Endpoint (with clientid, redirecturi, scope, responsetype=code, state)
    note over useractor,extsocialgoogle: User's browser handles redirection between WebApp and Google.

    activate useractor
    useractor-extsocialgoogle: 2.1 GET /oauth2/v2/auth?clientid=...&redirecturi=... (Browser navigates to Google)
    activate extsocialgoogle
    extsocialgoogle--useractor: Google Authentication/Consent Page HTML

    useractor-extsocialgoogle: 3. Submits Credentials & Grants Permissions
    extsocialgoogle--useractor: Authorization Code; Prepares redirect to WebApp

    extsocialgoogle-useractor: 4. Initiate Redirect to WebApp Redirect URI (with authorizationcode, state)
    deactivate extsocialgoogle

    useractor-repowebapppwa: 4.1 GET /oauth/google/callback?code=...&state=... (Browser navigates to WebApp)
    deactivate useractor
    repowebapppwa-repowebapppwa: 4.1.1 Client-side: Extract authorizationcode from URL

    repowebapppwa-compapigatewaynginx: 5. POST /api/v1/auth/google/callback (Body: { authorizationCode })
    activate compapigatewaynginx

    compapigatewaynginx-svcodooobackend: 6. Forward POST /auth/google/callback (Body: { authorizationCode })
    activate svcodooobackend

    note right of svcodooobackend: Server-to-server call, not visible to user's browser.
    svcodooobackend-extsocialgoogle: 7. POST /token (Exchange Authorization Code: clientid, clientsecret, code, granttype, redirecturi)
    activate extsocialgoogle
    extsocialgoogle--svcodooobackend: 8. Return { accesstoken, idtoken, refreshtoken?, expiresin }
    deactivate extsocialgoogle

    svcodooobackend-svcodooobackend: 9. Validate ID Token (signature, audience, issuer, expiry)

    svcodooobackend-extsocialgoogle: 10. GET /oauth2/v3/userinfo (Header: Authorization: Bearer )
    activate extsocialgoogle
    extsocialgoogle--svcodooobackend: 11. Return User Profile { sub, email, emailverified, name, picture, ... }
    deactivate extsocialgoogle

    svcodooobackend-repodbpostgresql: 12. SELECT User WHERE socialproviderid =  OR (email =  AND emailverified = true)
    activate repodbpostgresql
    repodbpostgresql--svcodooobackend: 13. Return User Record (or null if not found)
    deactivate repodbpostgresql

    alt Condition: User record found
        svcodooobackend-repodbpostgresql: 14.1.1 UPDATE User (e.g., lastloginat, sync profile fields, ensure socialproviderid is linked)
        activate repodbpostgresql
        repodbpostgresql--svcodooobackend: 14.1.2 Return Update Success
        deactivate repodbpostgresql
    else Condition: User record not found
        svcodooobackend-repodbpostgresql: 14.2.1 INSERT New User (email, name, socialprovider='google', socialproviderid=, emailverified=)
        activate repodbpostgresql
        repodbpostgresql--svcodooobackend: 14.2.2 Return New User Record
        deactivate repodbpostgresql
        svcodooobackend-svcodooobackend: 14.2.3 IF new user AND email not verified by Google AND REQ-001 requires verification THEN Trigger Email Verification Flow (async event)
        note right of svcodooobackend: REQ-001: Email verification for new accounts. If Google emailverified is true, this might be skipped.
    end

    svcodooobackend-svcodooobackend: 15. Generate JWT for User

    svcodooobackend--compapigatewaynginx: 16. Return { jwttoken, userprofile }
    deactivate svcodooobackend

    compapigatewaynginx--repowebapppwa: 17. Return { jwttoken, userprofile }
    deactivate compapigatewaynginx

    repowebapppwa-repowebapppwa: 18. Store JWT, Update UI (User Logged In), Navigate to Dashboard
    deactivate repowebapppwa