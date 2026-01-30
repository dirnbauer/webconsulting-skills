---
name: vercel-react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
version: 1.0.0
license: MIT
triggers:
  - react
  - next.js
  - nextjs
  - performance
  - optimization
  - bundle size
  - waterfalls
  - data fetching
  - suspense
  - server components
metadata:
  author: vercel
---

# Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Contains 57 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-auth-actions` - Authenticate server actions like API routes
- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-dedup-props` - Avoid duplicate serialization in RSC props
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners
- `client-passive-event-listeners` - Use passive listeners for scroll
- `client-localstorage-schema` - Version and minimize localStorage data

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-memo-with-default-value` - Hoist default non-primitive props
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-derived-state-no-effect` - Derive state during render, not effects
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-simple-expression-in-memo` - Avoid memo for simple primitives
- `rerender-move-effect-to-event` - Put interaction logic in event handlers
- `rerender-transitions` - Use startTransition for non-urgent updates
- `rerender-use-ref-transient-values` - Use refs for transient frequent values

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-hydration-suppress-warning` - Suppress expected mismatches
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals
- `rendering-usetransition-loading` - Prefer useTransition for loading state

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-init-once` - Initialize app once per app load
- `advanced-use-latest` - useLatest for stable callback refs

---

## Detailed Rules

### Eliminating Waterfalls (CRITICAL)

#### async-defer-await
Move `await` into branches where the value is actually needed.

```tsx
// ❌ BAD: Awaiting early blocks everything
async function getData() {
  const data = await fetchData();
  if (condition) {
    return data;
  }
  return null;
}

// ✅ GOOD: Defer await until needed
async function getData() {
  const dataPromise = fetchData();
  if (condition) {
    return await dataPromise;
  }
  return null;
}
```

#### async-parallel
Use `Promise.all()` for independent operations.

```tsx
// ❌ BAD: Sequential fetches
const user = await fetchUser(id);
const posts = await fetchPosts(id);
const comments = await fetchComments(id);

// ✅ GOOD: Parallel fetches
const [user, posts, comments] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
  fetchComments(id),
]);
```

#### async-suspense-boundaries
Use Suspense boundaries to stream content progressively.

```tsx
// ✅ GOOD: Suspense enables streaming
export default function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  );
}
```

### Bundle Size Optimization (CRITICAL)

#### bundle-barrel-imports
Import directly from source files, not barrel files (index.ts).

```tsx
// ❌ BAD: Barrel import pulls in entire library
import { Button } from '@/components';

// ✅ GOOD: Direct import
import { Button } from '@/components/Button';
```

#### bundle-dynamic-imports
Use `next/dynamic` for heavy components.

```tsx
// ❌ BAD: Always loads heavy component
import HeavyChart from './HeavyChart';

// ✅ GOOD: Dynamic import
import dynamic from 'next/dynamic';
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
});
```

#### bundle-defer-third-party
Load analytics and logging after hydration.

```tsx
// ✅ GOOD: Defer analytics loading
useEffect(() => {
  import('./analytics').then((module) => module.init());
}, []);
```

### Server-Side Performance (HIGH)

#### server-cache-react
Use `React.cache()` for per-request deduplication.

```tsx
// ✅ GOOD: Cached per-request
import { cache } from 'react';

const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});
```

#### server-parallel-fetching
Restructure components to parallelize server fetches.

```tsx
// ❌ BAD: Parent awaits before child renders
async function Page() {
  const user = await getUser();
  return <Profile user={user} />;
}

// ✅ GOOD: Start fetch in parent, await in child
async function Page() {
  const userPromise = getUser();
  return <Profile userPromise={userPromise} />;
}

async function Profile({ userPromise }) {
  const user = await userPromise;
  return <div>{user.name}</div>;
}
```

### Re-render Optimization (MEDIUM)

#### rerender-memo
Extract expensive calculations into memoized components.

```tsx
// ✅ GOOD: Expensive component memoized
const ExpensiveList = memo(function ExpensiveList({ items }) {
  return items.map((item) => <ExpensiveItem key={item.id} item={item} />);
});
```

#### rerender-functional-setstate
Use functional setState for stable callbacks.

```tsx
// ❌ BAD: Callback changes on every render
const increment = () => setCount(count + 1);

// ✅ GOOD: Stable callback
const increment = useCallback(() => setCount((c) => c + 1), []);
```

#### rerender-transitions
Use `startTransition` for non-urgent updates.

```tsx
// ✅ GOOD: Non-urgent update doesn't block input
const [isPending, startTransition] = useTransition();

function handleChange(value) {
  setInputValue(value); // Urgent
  startTransition(() => {
    setSearchResults(filterData(value)); // Non-urgent
  });
}
```

---

## Credits & Attribution

This skill is adapted from **[Vercel Engineering](https://vercel.com)**.

Original repository: https://github.com/vercel-labs/agent-skills

**Copyright (c) Vercel, Inc.** - MIT License  
Adapted by webconsulting.at for this skill collection
