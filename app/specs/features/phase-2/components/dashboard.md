# User Dashboard for Task Management

## Layout
**Sidebar (left):**
- User profile (avatar, name)
- Navigation: Inbox, Today, Upcoming, Filters
- Tags/Categories list
- Stats: Total tasks, completed, pending

**Main Content (center):**
- Task list with cards
- Add task quick input (top)
- Filter/Sort controls
- Bulk actions checkbox

**Detail Panel (right - optional):**
- Task detail view when selected
- Edit form inline
- Due date picker, priority selector

## Task Card Component
**Fields displayed:**
- Checkbox (complete/incomplete)
- Title (bold if high priority)
- Tags (color-coded chips)
- Due date (with overdue warning)
- Priority indicator (dot/icon)
- Actions menu (edit, delete, duplicate)

**Interactive features:**
- Click to expand details
- Drag-and-drop reordering (stretch)
- Keyboard shortcuts (j/k navigation)

## Task Creation Modal
**Fields:**
- Title (required)
- Description (textarea, markdown support)
- Due date (date picker + time)
- Priority dropdown
- Tags input (with suggestions)
- Recurrence toggle + options
- Reminder toggle + offset

**Quick add:**
- Floating button (mobile)
- Keyboard shortcut (Ctrl/Cmd + N)
- Natural language parsing (Phase III)

## State Management
- Zustand store for task state
- Optimistic updates for CRUD
- Real-time sync via polling (Phase V: WebSockets)

## Responsive Behavior
- Mobile: Single column, bottom nav
- Tablet: Sidebar collapses
- Desktop: Three-panel layout