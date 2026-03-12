## 2024-05-14 - Optimize Backend Stats Endpoint FAILED
**Learning:** You cannot use `asyncio.gather` to execute multiple `session.exec()` queries concurrently on the same `AsyncSession`. Attempting to do so will result in an `IllegalStateChangeError` or `InvalidRequestError` because the underlying connection cannot multiplex the queries.
**Action:** Do not use `asyncio.gather` for concurrent database queries on a single SQLAlchemy `AsyncSession`. Find another optimization.
