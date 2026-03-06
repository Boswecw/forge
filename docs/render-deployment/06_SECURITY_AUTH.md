# Forge Ecosystem - Security & Authentication

**Document Version:** 1.0.0
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Authentication

### JWT Token Flow

1. **Login**: `POST /api/v1/auth/login` → Returns JWT token
2. **Authorization**: Include `Authorization: Bearer <token>` in all requests
3. **Validation**: Services verify JWT signature and expiration
4. **Refresh**: `POST /api/v1/auth/refresh` → Get new token before expiration

### Token Structure

```json
{
  "sub": "user_id",
  "username": "user@example.com",
  "exp": 1707222400,
  "iat": 1707136000,
  "roles": ["user", "admin"]
}
```

**Expiration**: 24 hours default
**Algorithm**: HS256 (symmetric key signing)

---

## Authorization

### Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| **user** | Read/write own resources |
| **admin** | Read/write all resources, manage users |
| **operator** | Read all, write operational data |
| **service** | Service-to-service communication |

### Ring-Based Authorization (ForgeAgents)

| Ring | Access Level |
|------|--------------|
| **Ring 0** | Owner - full control |
| **Ring 1** | Operator - execute, read |
| **Ring 2** | Read-only - view only |

---

## Encryption

### At Rest
- **Algorithm**: AES-256-GCM
- **Key Management**: Environment variables (SECRETS_ENCRYPTION_KEY)
- **Encrypted Fields**: LLM API keys, user passwords (bcrypt)

### In Transit
- **Protocol**: TLS 1.3
- **Certificate**: Let's Encrypt (automatic via Render)
- **Ciphers**: Modern only (no TLS 1.0/1.1)

---

## Audit Logging

### Immutable Event Log

Every security-relevant action is logged with:
- **Event Type**: LOGIN, CREATE, UPDATE, DELETE, etc.
- **User ID**: Who performed the action
- **Resource**: What was affected
- **Signature**: HMAC-SHA256 for tamper detection
- **Timestamp**: When it occurred (immutable)

### Retention

- **Audit logs**: 90 days minimum
- **Security events**: 365 days
- **Compliance logs**: Per regulatory requirements

---

## Anomaly Detection

### Detector Types

1. **Impossible Travel**: Login from two distant locations within short time
2. **Brute Force**: Multiple failed login attempts
3. **Data Exfiltration**: Large data exports
4. **Suspicious Patterns**: Unusual API usage
5. **After-Hours Access**: Access outside normal hours
6. **Bulk Mutations**: Mass updates/deletes

### Response

Anomalies trigger:
- Real-time alerts to operators
- Automatic rate limiting
- Optional account suspension (configurable)

---

## Compliance

### Frameworks Supported

- **GDPR**: Right to erasure, data portability, breach notification
- **CCPA**: Consumer data rights, opt-out mechanisms
- **HIPAA**: Encryption, audit logs, access controls
- **SOC2 Type II**: Security, availability, confidentiality
- **PCI-DSS**: Payment card data security (if applicable)

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
