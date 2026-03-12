<<<<<<< bolt/optimize-dashboard-renders-4239373034026468842
## 2025-03-11 - Stabilizing Callback Props for Framer-Motion Lists
**Learning:** In React, passing state variables like a controlled input's value (e.g., `topic`) directly as props or as dependencies to a `useCallback` that is passed down to a mapped list of components (especially heavy components with `framer-motion` animations) will cause the entire list to re-render on every keystroke. Even if the list item component is wrapped in `React.memo()`, a changing callback reference invalidates the memoization.
**Action:** Use `useRef` and `useEffect` to keep track of the latest state variable value. Access `topicRef.current` inside the `useCallback` instead of depending on the state variable itself. This stabilizes the callback's reference, preserving `React.memo()` on list items and preventing massive re-renders during text input.
=======
## 2024-05-14 - Optimize Backend Stats Endpoint FAILED
**Learning:** You cannot use `asyncio.gather` to execute multiple `session.exec()` queries concurrently on the same `AsyncSession`. Attempting to do so will result in an `IllegalStateChangeError` or `InvalidRequestError` because the underlying connection cannot multiplex the queries.
**Action:** Do not use `asyncio.gather` for concurrent database queries on a single SQLAlchemy `AsyncSession`. Find another optimization.
>>>>>>> main
