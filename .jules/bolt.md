## 2024-05-14 - Optimize Backend Stats Endpoint FAILED
**Learning:** You cannot use `asyncio.gather` to execute multiple `session.exec()` queries concurrently on the same `AsyncSession`. Attempting to do so will result in an `IllegalStateChangeError` or `InvalidRequestError` because the underlying connection cannot multiplex the queries.
**Action:** Do not use `asyncio.gather` for concurrent database queries on a single SQLAlchemy `AsyncSession`. Find another optimization.

## 2026-05-22 - Offload CPU-bound text splitting
**Learning:** Synchronous CPU-bound operations like `RecursiveCharacterTextSplitter.split_documents` block the FastAPI event loop, leading to high jitter and decreased responsiveness for concurrent requests.
**Action:** Always wrap CPU-bound operations or synchronous library calls with `asyncio.to_thread` in asynchronous endpoints to preserve event loop responsiveness.
