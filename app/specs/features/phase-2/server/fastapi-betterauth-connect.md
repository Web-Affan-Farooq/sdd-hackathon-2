# FastAPI + BetterAuth JWT Integration Specification

## Core Authentication Flow

**JWT Token Issuance:**
- BetterAuth frontend issues JWT tokens upon user login/signup
- Tokens contain user claims: `user_id`, `email`, `exp` (expiry)
- Shared secret (`BETTER_AUTH_SECRET`) used for signing/verification
- Token lifespan: 7 days (configurable via environment)

**Header Requirements:**
- All backend requests must include: `Authorization: Bearer <token>`
- Missing/invalid tokens return `401 Unauthorized`
- Expired tokens trigger frontend redirect to login

**Backend Verification Process:**
1. Extract token from Authorization header
2. Verify signature using shared secret
3. Decode payload to extract `user_id`
4. Validate token hasn't expired
5. Compare URL `user_id` with token `user_id` for ownership verification
6. Reject requests with mismatched user IDs

**Security Isolation:**
- All database queries filtered by authenticated `user_id`
- No cross-user data exposure
- Token validation before any data access
- Stateless authentication (no session storage)

**Environment Configuration:**
- `BETTER_AUTH_SECRET`: Must match between frontend/backend
- `NEXT_PUBLIC_API_URL`: Backend base URL for frontend requests
- No hardcoded secrets in source code

**Error Handling:**
- 401: Invalid/missing/expired token
- 403: Valid token but unauthorized resource access
- Automatic token refresh not implemented (Phase II)
- Clear error messages for debugging
