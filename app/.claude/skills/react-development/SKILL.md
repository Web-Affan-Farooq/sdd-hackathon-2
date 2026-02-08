---
name: "react-typescript-development"
description: "Write production-ready React code with TypeScript focusing on type safety, modern patterns, and maintainability. Use when user asks to build React components, hooks, or applications."
version: "1.0.0"
---

# React + TypeScript Development Skill

## When to Use This Skill

- User asks to "build a React component" or "create a React app"
- User needs help with React patterns, hooks, or TypeScript types

## Core Principles

1. **Type Safety First**: Never use `any` unless absolutely necessary
2. **Modern React**: Use functional components, hooks, and latest patterns
3. **Clean Code**: Write readable, maintainable code with proper separation
4. **Production Ready**: Handle loading, error, and edge cases

## Procedure

### 1. Component Structure
- Create functional components with explicit return types
- Use `React.FC<Props>` or explicit return type `: JSX.Element`
- Always forward refs for interactive elements
- Include proper `displayName` for debugging

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', onClick, children }) => {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### 2. TypeScript Patterns
- Define interfaces for props at the top
- Use generics for reusable components
- Create custom types for complex data structures
- Use union types for variant props
- Always export types/interfaces

```typescript
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

export function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <div className="list">
      {items.map((item, index) => (
        <div key={index} className="list-item">
          {renderItem(item)}
        </div>
      ))}
    </div>
  );
}
```

### 3. Custom Hooks
- Prefix with `use` (e.g., `useLocalStorage`)
- Return typed values in array/tuple
- Include proper dependency arrays
- Handle cleanup in useEffect

```typescript
interface UseLocalStorage<T> {
  value: T;
  setValue: (value: T) => void;
}

export function useLocalStorage<T>(key: string, initialValue: T): UseLocalStorage<T> {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T) => {
    setStoredValue(value);
    localStorage.setItem(key, JSON.stringify(value));
  }, [key]);

  return { value: storedValue, setValue };
}
```

### 4. State Management
- Use useState for local component state
- Use useReducer for complex state logic
- Use context for app-wide state (when needed)
- Keep state as close to where it's used as possible

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

type AuthAction = 
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_ERROR'; payload: string };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { user: action.payload, isLoading: false, error: null };
    case 'LOGIN_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    default:
      return state;
  }
};
```

## Output Format

Always provide:
1. **Complete Code**: Ready-to-use component/hook with imports
2. **Type Definitions**: All interfaces/types used
3. **Usage Example**: How to use the component
4. **Key Points**: Important implementation notes

## Quality Criteria

- **No `any` types** - Use proper typing
- **Proper error handling** - Loading states, error boundaries
- **Accessible** - Semantic HTML, ARIA labels when needed
- **Performance** - Memoization when beneficial, cleanup effects
- **Clean imports** - Group external, internal, type imports

## Example

**Input**: "Create a modal component in React with TypeScript"

**Output**:

```typescript
import React, { useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ 
  isOpen, 
  onClose, 
  title, 
  children 
}) => {
  // Close on ESC key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button onClick={onClose} aria-label="Close modal">×</button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
};
/*
 <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Example">
   <p>Modal content here</p>
 </Modal>
*/
```
**Key Points**:
- Uses useEffect for ESC key support with cleanup
- Prevents event bubbling with stopPropagation
- Accessible with aria-label on close button
- Proper typing for all props

This skill focuses purely on the technical implementation of React + TypeScript without getting into UI design decisions. It provides clear patterns and examples for writing quality React code with proper TypeScript support.