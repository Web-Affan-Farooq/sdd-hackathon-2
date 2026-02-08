# Authentication Forms

## Login Form
**Fields:**
- Email (required, valid email format)
- Password (required, min 8 chars)
- Remember me checkbox (optional)

**Validation:**
- Zod schema in `/lib/schemas/auth.ts`
- Real-time feedback
- Submit only when valid

**API Integration:**
- POST to Better Auth `/api/auth/signin/email`
- Store JWT token in httpOnly cookie
- Redirect to `/dashboard`

## Signup Form
**Fields:**
- Name (required, 2-50 chars)
- Email (required, unique)
- Password (required, min 8 chars, strength indicator)
- Confirm Password (must match)

**Validation:**
- Password strength: lowercase, uppercase, number, special char
- Email uniqueness check on blur
- Zod schema with refine() for confirm password

**API Integration:**
- POST to Better Auth `/api/auth/signup/email`
- Auto-login after successful signup
- Redirect to `/dashboard`

## Form Components
/components/auth/
├── LoginForm.tsx
├── SignupForm.tsx
├── AuthFormWrapper.tsx (shared layout)
└── PasswordInput.tsx (with show/hide toggle)

## Error Handling
- Display API errors below form
- Clear errors on field change
- Network error fallback message

## Security
- CSRF tokens (Better Auth handles)
- Rate limiting on backend
- Password hashing (Better Auth)