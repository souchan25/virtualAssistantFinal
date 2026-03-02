
## 2024-05-18 - [Fixing N+1 Queries with Prefetch in Django]
**Learning:** Using `prefetch_related` is powerful, but doing further filtering on the prefetched attributes inside a loop (like `.filter(is_active=True)`) will ignore the prefetched cache and execute new database queries, causing an N+1 problem.
**Action:** Use `Prefetch` objects with `to_attr` to pre-filter and cache lists, or do the filtering in Python after prefetching (e.g. `[m for m in all_meds if m.is_active]`) to retain the O(1) query performance. Be careful to check the business logic, for example when calculating adherence we need to count logs from *all* medications, not just the active ones!
