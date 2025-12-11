# Data Model: User Authentication System

**Feature**: 002-authentication | **Date**: 2025-12-10

## User Entity

### User Schema
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String/ObjectId | Required, Unique | Primary identifier for the user |
| email | String | Required, Unique, Valid email format | User's email address for login |
| password | String | Required, Min 8 chars, Hashed | Securely hashed password |
| displayName | String | Optional | User's display name |
| createdAt | Date | Required | Account creation timestamp |
| updatedAt | Date | Required | Last update timestamp |
| lastLoginAt | Date | Optional | Last successful login timestamp |
| isActive | Boolean | Default: true | Account status flag |
| emailVerified | Boolean | Default: false | Email verification status |

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- Stored as bcrypt hash with salt rounds = 12

## Session/Token Entity

### JWT Token Structure
| Claim | Type | Description |
|-------|------|-------------|
| sub | String | User ID (subject) |
| email | String | User's email |
| iat | Number | Issued at timestamp |
| exp | Number | Expiration timestamp (30 min) |

## Database Collections/Tables

### MongoDB Collections:
```
users: {
  _id: ObjectId,
  email: String,
  password: String,
  displayName: String,
  createdAt: Date,
  updatedAt: Date,
  lastLoginAt: Date,
  isActive: Boolean,
  emailVerified: Boolean
}
```

### PostgreSQL Tables:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  displayName VARCHAR(255),
  createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  lastLoginAt TIMESTAMP WITH TIME ZONE,
  isActive BOOLEAN DEFAULT TRUE,
  emailVerified BOOLEAN DEFAULT FALSE
);
```

## Relationships

### User to Learning Progress (Future Extension)
- One user to many learning progress records
- User ID as foreign key in progress tracking table

## Validation Rules

### Email Validation
- Must follow standard email format (regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/)
- Must be unique across all users
- Maximum length: 255 characters

### Password Validation
- Minimum length: 8 characters
- Must contain at least one uppercase letter
- Must contain at least one lowercase letter
- Must contain at least one number
- Maximum length: 128 characters (for bcrypt compatibility)

### Display Name Validation
- Optional field
- Maximum length: 100 characters
- Can contain letters, numbers, spaces, hyphens, and underscores

## Indexes

### Database Indexes
- Email field: Unique index for fast lookups and uniqueness enforcement
- CreatedAt field: Index for sorting and querying by creation date
- IsActive field: Index for filtering active users