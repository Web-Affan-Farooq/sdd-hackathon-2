# Best Practices for Scalable Next.js Applications

This document defines a **production-grade design pattern** for building scalable, maintainable, and reusable Next.js applications using a **modular architecture combined with native Next.js private routing**.

The goal is to provide a **clear, enforceable structure** that works equally well for small teams, large teams, and long-lived codebases.

---

## 1. Frontend Requirements

All frontend source code **must live inside the `/src` directory** and follow a **modular, feature-first architecture**.

### Mandatory Technologies

* **Next.js (App Router)**
* **TypeScript** (required)
* **React**
* **Tailwind CSS** (mandatory for styling)
* **Zustand** (global state management)
* **better-auth** (authentication)
* **Zod** (schema validation)
* **react-hook-form** (form handling)
* **Axios** (HTTP client)
* **pnpm** (package manager — npm/yarn not allowed)
* **Docker** (application must be dockerized)

---

## 2. Winning Design Pattern for Next.js

### **Modular Architecture + Native Next.js Private Routes**

> This design pattern is the default low-level design constitution for scalable Next.js applications.

### Why this works

* Encourages **locality of logic**
* Minimizes cross-feature coupling
* Scales naturally as features grow
* Aligns with how Next.js App Router is designed

---

## 3. Constraints

* This architecture is **only applicable to Next.js applications**
* The project **must use TypeScript**
* App Router (`/app`) must be used

---

## 4. Core Rules

### 4.1 File Sharing Rule (Most Important)

If a file is shared between **two or more routes at the same level**, it **must be moved to their nearest common parent directory**.

#### Example

If `/login` and `/signup` share the same Zod validation:

```text
(app)
└── (auth)
    ├── login
    ├── signup
    └── _validations
```

Both routes must import the shared validation from `(auth)/_validations`.

#### Folder vs File Rule

* If **multiple shared files exist**, create a directory:

  ```
  _validations/
  ```
* If **only one shared file exists**, avoid folder overkill:

  ```
  _validations.ts
  ```

---

## 5. Secondary Files Placement Rules

Any file that supports a route (but is not a route itself) **must follow `_`-prefixed conventions**.

### Approved `_` Directories and Files

| Purpose           | Folder          | File (if single)    |
| ----------------- | --------------- | ------------------- |
| Zod validations   | `_validations/` | `_validations.ts`   |
| Components        | `_components/`  | `ComponentName.tsx` |
| Types             | `_types/`       | `_types.ts`         |
| Utilities         | `_utils/`       | `_utils.ts`         |
| API / Axios logic | `_api/`         | `_api.ts`           |

This rule:

* prevents accidental routing
* makes intent explicit
* improves navigability

---

## 6. File Naming Conventions

### File Names

* **Components** → PascalCase

  ```text
  LoginInput.tsx
  ```

* **Hooks** → kebab-case

  ```text
  use-mobile.ts
  ```

* **Utilities** → camelCase

  ```text
  webhookPayment.ts
  ```

* **Types** → kebab-case

  ```text
  api-response.ts
  ```

* **Zod Schemas** → kebab-case

  ```text
  login-schema.ts
  ```

### Code Identifiers (Exports)

* Functions, hooks, utilities, schemas → **camelCase**
* Components → **PascalCase**

---

## 7. Reusability First Principle

Reusability is the **primary design goal**.

* Prefer shared logic at the **closest common parent**
* Avoid premature global abstractions
* Never duplicate schemas or utilities across routes

---

## 8. Utility Design Rule (Functional vs OOP)

If a utility contains **three or more tightly coupled functions** that:

* call each other
* depend on execution order
* share implicit state

❌ **Do NOT keep them as independent functions**

### ❌ Anti-pattern

```ts
function updateAccountActivity() {}
function attachToken() {}
function verifyIfUserExists() {}

function auth() {
  const email = verifyIfUserExists()
  if (email) {
    attachToken()
    updateAccountActivity()
  } else {
    return { message: "User not found", status: 404 }
  }
}
```

### ✅ Correct Approach (OOP Encapsulation)

```ts
class Auth {
  constructor() {
    const email = this.verifyIfUserExists()

    if (email) {
      this.attachToken()
      this.updateAccountActivity()
    } else {
      return { message: "User not found", status: 404 }
    }
  }

  verifyIfUserExists() {}
  attachToken() {}
  updateAccountActivity() {}
}
```

### Rule of Thumb

* **Pure transformations** → functions
* **State + behavior** → class

---

## 9. Component Rules

* All components **must be functional components**
* Components must be named in **PascalCase**
* **Default exports are forbidden**, except:

  * `page.tsx`
  * `layout.tsx`

All other components **must use named exports**.

---

## 10. Barrel Export Rule (`index.ts`)

Inside a **route-specific private module**:

* If the number of files is **≤ 5**, create an `index.ts`
* Export those files from `index.ts` to simplify imports

```ts
export { LoginForm } from "./LoginForm"
export { LoginInput } from "./LoginInput"
```

### Important Constraint

* Barrel exports are **allowed only within the same route boundary**
* Never barrel-export across unrelated features

---

## Final Note

This guide is intentionally **strict**.

It exists to:

* reduce ambiguity
* enforce consistency
* scale teams and codebases
* make architecture explainable to humans and machines

If followed correctly, this pattern produces:

* clean diffs
* predictable structure
* refactor-friendly code
* senior-level project organization


