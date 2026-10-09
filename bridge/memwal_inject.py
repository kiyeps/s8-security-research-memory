#!/usr/bin/env python3
"""pre_llm_call hook: inject durable Walrus Memory context at session start.

Why this shape:

  * `extra.is_first_turn` is true only on the first model call of a session,
    so the injection lands once, at the top of the conversation. Injecting on
    every turn would rewrite the prompt prefix and destroy prompt caching,
    which the Hermes core treats as sacred. One injection per session is
    both the cheapest and the cache-safe option.
  * A per-session marker file is a second guard in case `is_first_turn` is
    ever absent or wrong.
  * Failures emit nothing. A memory miss must never break a turn.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import memwal_common as mc  # noqa: E402

DEFAULT_QUERY = "bug bounty research target finding decision next step"


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    try:
        extra = payload.get("extra") or {}
        session_id = payload.get("session_id") or ""
        first_turn = bool(extra.get("is_first_turn"))

        if not first_turn:
            return 0
        if mc.already_injected(session_id):
            mc.log("inject", {"session_id": session_id, "action": "skip_marker"})
            return 0

        query = (extra.get("user_message") or "").strip() or DEFAULT_QUERY
        result = mc.recall(query, timeout=25)
        hits = mc._hits(result)

        if not hits:
            mc.mark_injected(session_id, {"hits": 0})
            mc.log("inject", {"session_id": session_id, "action": "no_hits",
                              "query": query[:120]})
            return 0

        context = mc.build_context(hits, query)
        mc.mark_injected(session_id, {"hits": len(hits), "chars": len(context)})
        mc.log("inject", {"session_id": session_id, "action": "injected",
                          "hits": len(hits), "chars": len(context),
                          "query": query[:120]})
        print(json.dumps({"context": context}))
    except Exception as exc:  # never break a turn
        mc.log("inject", {"session_id": locals().get("session_id", ""),
                          "action": "error", "error": str(exc)[:300]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
