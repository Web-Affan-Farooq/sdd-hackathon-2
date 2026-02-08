# User Isolation & Authentication Middleware Specification

## Authentication Middleware

**Token Processing Flow:**
1. Intercept all `/api/*` requests
2. Extract `Authorization: Bearer <token>` header
3. Validate JWT signature using shared secret
4. Decode payload to obtain `user_id`, `email`, expiry
5. Inject authenticated user data into request context
6. Reject requests with invalid/expired tokens (401)

## User Isolation Enforcement

**Resource Ownership Verification:**
- Compare URL `{user_id}` parameter with JWT `user_id` claim
- Mismatch results in 403 Forbidden response
- All database queries automatically filter by authenticated `user_id`

**Data Access Patterns:**
- SQL queries include `WHERE user_id = :current_user_id`
- No direct access to raw database models
- ORM-level filtering via SQLModel relationships
- Audit logging of all user operations

**Security Layers:**
1. Route-level authentication middleware
2. Database query filtering
3. Response data sanitization
4. Cross-user access prevention at API boundary