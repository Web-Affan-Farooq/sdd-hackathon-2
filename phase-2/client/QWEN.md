# Frontend Guidelines – Phase II

## MCP servers (mandatory):
context 7

## Stack
- **Framework**: Next.js 16 (App Router)
- **Styling**: Tailwind CSS
- **API Client**: Custom `fetch` wrapper in `lib/api.ts`
- **Authentication**: Better Auth with JWT tokens
- **Forms**: React Hook Form + Zod validation

## Project Structure (`/frontend`)
```
app/
├── (auth)/          # Auth-related pages (login, signup)
├── (dashboard)/     # Main app pages
├── api/             # Next.js API routes (if needed)
├── layout.tsx       # Root layout
└── page.tsx         # Home page
components/
├── ui/              # Reusable UI primitives
├── tasks/           # Task-specific components
└── auth/            # Auth components
lib/
├── api.ts           # Centralized API client
├── auth.ts          Auth utilities (JWT handling)
└── utils.ts         # Helpers
```

## Authentication Flow
1. User logs in via Better Auth → receives JWT token
2. Store token securely (httpOnly cookie recommended)
3. Include token in all API requests:
   ```typescript
   Authorization: Bearer <token>
   ```
4. All API calls must pass `user_id` from token in URL

## API Integration
- Use `lib/api.ts` for all backend calls (FastAPI at `http://localhost:8000`)
- All endpoints follow: `/api/{user_id}/tasks` and variations
- Handle 401 errors (token expired) → redirect to login

## Task Features (UI Implementation)
- **Basic CRUD**: Add, view, edit, delete, toggle complete
- **Organization**: Priority badges, tag chips
- **Search/Filter**: Client-side filtering + backend search API
- **Sorting**: Dropdown for due date/priority/title
- **Advanced**: Date pickers for due dates, recurrence options

## Development Rules
1. **Server Components default**: Fetch initial data server-side
2. **'use client' only for interactivity**: Forms, toggles, real-time updates
3. **Mobile-first**: Responsive Tailwind classes
4. **Type-safe**: Full TypeScript, no `any`
5. **Accessibility**: Semantic HTML, ARIA labels, keyboard nav

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Auth endpoint

## Deployment
- Build for Vercel: `npm run build`
- Ensure CORS allows your backend domain
- Submit Vercel URL for Phase II submission
```