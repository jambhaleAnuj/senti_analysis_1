"""In-memory ephemeral cache for analysis payloads.

Provides a very small utility to store analysis data keyed by a short UUID.
This avoids pushing large JSON blobs through query strings.
Not suitable for production (single-process, no eviction policy beyond TTL).
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, Optional

DEFAULT_TTL_SECONDS = 15 * 60  # 15 minutes

_store: Dict[str, tuple[float, Dict[str, Any]]] = {}


def put(payload: Dict[str, Any], ttl: int = DEFAULT_TTL_SECONDS) -> str:
    key = uuid.uuid4().hex[:12]
    expires = time.time() + ttl
    _store[key] = (expires, payload)
    return key


def get(key: str) -> Optional[Dict[str, Any]]:
    entry = _store.get(key)
    if not entry:
        return None
    expires, data = entry
    if time.time() > expires:
        _store.pop(key, None)
        return None
    return data


def purge_expired() -> None:
    now = time.time()
    to_delete = [k for k, (exp, _) in _store.items() if exp < now]
    for k in to_delete:
        _store.pop(k, None)
