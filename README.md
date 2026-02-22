RSS/Atom Feeds →│ Async Watcher│───stores──▶ In-memory store (or Redis later)
                └──────┬───────┘
                       │
                 Flask/FastAPI
                       │
        ┌──────────────┴──────────────┐
        GET /incidents
        POST /feeds