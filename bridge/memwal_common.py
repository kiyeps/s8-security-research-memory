"""Shared helpers for the Hermes to Walrus Memory bridge.

Design rule for every function here: never raise into the agent. The bridge
is an enhancement, so a failure must degrade to "no memory context injected"
rather than breaking a turn. Callers treat any exception as a miss.

Paths are environment-overridable; the defaults match a standard install.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from typing import Any, Dict, List, Optional

BRIDGE_DIR = os.environ.get("MEMWAL_BRIDGE_DIR") or os.path.expanduser(
    "~/.hermes/memwal-bridge"
)
NODE = os.environ.get("MEMWAL_NODE") or "node"
MCP_CLIENT = os.path.join(BRIDGE_DIR, "mcp_client.mjs")
MCP_BIN = os.environ.get("MEMWAL_MCP_BIN") or os.path.expanduser(
    "~/.memwal/runtime/0.0.14/node_modules/"
    "@mysten-incubation/memwal-mcp/dist/bin/memwal-mcp.js"
)
NAMESPACE = os.environ.get("MEMWAL_NAMESPACE", "hermes/default")

STATE = os.path.join(BRIDGE_DIR, "state")
PENDING = os.path.join(STATE, "pending.jsonl")
SYNCED = os.path.join(STATE, "synced.jsonl")
SESSIONS = os.path.join(STATE, "sessions")
LOGS = os.path.join(BRIDGE_DIR, "logs")

RECALL_LIMIT = 6
CONTEXT_MAX_CHARS = 1800


def _ensure_dirs() -> None:
    for d in (STATE, SESSIONS, LOGS):
        os.makedirs(d, exist_ok=True)


def log(name: str, record: Dict[str, Any]) -> None:
    """Append one JSON line to a bridge log. Best effort."""
    try:
        _ensure_dirs()
        record = dict(record)
        record.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        with open(os.path.join(LOGS, f"{name}.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _invoke(cmd: str, arg: str, limit: Optional[int], timeout: int) -> Dict[str, Any]:
    """Drive the MCP server through the client script. Returns {} on failure.

    MEMWAL_BRIDGE_DRY_RUN=1 short-circuits any write so plumbing can be tested
    without adding blobs to Mainnet.
    """
    if os.environ.get("MEMWAL_BRIDGE_DRY_RUN") == "1" and cmd in ("remember", "bulk"):
        return {"_dry_run": True, "_cmd": cmd}
    argv = [NODE, MCP_CLIENT, MCP_BIN, cmd, NAMESPACE, arg]
    if limit is not None:
        argv.append(str(limit))
    proc = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=BRIDGE_DIR,
    )
    if not proc.stdout.strip():
        return {"_error": "empty stdout", "_stderr": proc.stderr[-300:]}
    return json.loads(proc.stdout)


def recall(query: str, timeout: int = 25) -> Dict[str, Any]:
    return _invoke("recall", query, RECALL_LIMIT, timeout)


def remember(text: str, timeout: int = 90) -> Dict[str, Any]:
    return _invoke("remember", text, None, timeout)


def _hits(payload: Dict[str, Any]) -> List[str]:
    """Pull the memory strings out of an MCP recall result."""
    text = payload.get("text") or ""
    if not text or "No matching memories" in text:
        return []
    return [text]


def build_context(hits: List[str], query: str) -> str:
    body = "\n".join(hits)[:CONTEXT_MAX_CHARS]
    return (
        "[Walrus Memory] Durable research memory recalled from Walrus Mainnet "
        f"(namespace {NAMESPACE}).\n"
        "These records are the source of truth for earlier research context; the "
        "local MEMORY.md is a cache and fallback only.\n"
        f"Query: {query[:160]}\n\n{body}"
    )


def session_marker(session_id: str) -> str:
    safe = "".join(c for c in (session_id or "unknown") if c.isalnum() or c in "_-")
    return os.path.join(SESSIONS, f"{safe or 'unknown'}.json")


def already_injected(session_id: str) -> bool:
    path = session_marker(session_id)
    if not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return bool(data.get("injected"))
    except Exception:
        return False


def mark_injected(session_id: str, detail: Dict[str, Any]) -> None:
    try:
        _ensure_dirs()
        with open(session_marker(session_id), "w", encoding="utf-8") as fh:
            json.dump({"injected": True, "at": time.time(), **detail}, fh)
    except Exception:
        pass
