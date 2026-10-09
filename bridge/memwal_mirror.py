#!/usr/bin/env python3
"""post_tool_call hook: mirror durable memory writes to Walrus Memory.

Fires for the `memory` tool only (matcher `^memory$` in config).

Order of operations matters: the record is spooled to a local queue file
with an fsync BEFORE the network call is attempted, so a crash or a relayer
outage leaves the write recoverable. The queue is drained by
memwal_flush.py. This is what makes Walrus the durable store and the local
file a cache: nothing is lost while the network is down, and nothing lives
only in RAM.
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import memwal_common as mc  # noqa: E402

MIRRORED_ACTIONS = ("add", "replace")


def _read_pending():
    if not os.path.exists(mc.PENDING):
        return []
    out = []
    with open(mc.PENDING, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    return out


def _write_pending(records):
    tmp = mc.PENDING + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, mc.PENDING)


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    session_id = ""
    try:
        if payload.get("tool_name") != "memory":
            return 0

        extra = payload.get("extra") or {}
        session_id = payload.get("session_id") or ""
        status = extra.get("status")
        if status != "ok":
            mc.log("mirror", {"session_id": session_id, "action": "skip_status",
                              "status": status})
            return 0

        tool_input = payload.get("tool_input") or {}
        action = tool_input.get("action")
        content = (tool_input.get("content") or "").strip()
        target = tool_input.get("target") or "memory"

        if action not in MIRRORED_ACTIONS or not content:
            mc.log("mirror", {"session_id": session_id, "action": "skip_action",
                              "tool_action": action})
            return 0

        mc._ensure_dirs()
        record = {
            "id": uuid.uuid4().hex,
            "queued_at": time.time(),
            "session_id": session_id,
            "tool_action": action,
            "target": target,
            "text": content,
        }
        pending = _read_pending()
        pending.append(record)
        _write_pending(pending)
        mc.log("mirror", {"session_id": session_id, "action": "spooled",
                          "id": record["id"], "chars": len(content)})

        result = mc.remember(content, timeout=90)
        if result.get("_dry_run"):
            mc.log("mirror", {"session_id": session_id, "action": "dry_run_queued",
                              "id": record["id"]})
            return 0
        text = json.dumps(result)[:400]
        ok = not result.get("error") and "_error" not in result
        if ok:
            remaining = [r for r in _read_pending() if r.get("id") != record["id"]]
            _write_pending(remaining)
            with open(mc.SYNCED, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({**record, "synced_at": time.time(),
                                     "result": text}, ensure_ascii=False) + "\n")
            mc.log("mirror", {"session_id": session_id, "action": "synced",
                              "id": record["id"], "result": text})
        else:
            mc.log("mirror", {"session_id": session_id, "action": "queued_retry",
                              "id": record["id"], "result": text})
    except Exception as exc:
        mc.log("mirror", {"session_id": session_id, "action": "error",
                          "error": str(exc)[:300]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
