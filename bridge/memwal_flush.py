#!/usr/bin/env python3
"""Drain the mirror queue. Runs on a schedule; silent when there is nothing to do.

Empty stdout keeps the cron job silent, which is the wanted behaviour for a
watchdog. It only speaks when it actually moved work, or when it failed.
"""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import memwal_common as mc  # noqa: E402


def read_pending():
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


def write_pending(records):
    tmp = mc.PENDING + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, mc.PENDING)


def main() -> int:
    pending = read_pending()
    if not pending:
        return 0
    if os.environ.get("MEMWAL_BRIDGE_DRY_RUN") == "1":
        mc.log("flush", {"action": "dry_run", "pending": len(pending)})
        return 0

    survivors, moved, failed = [], 0, 0
    for rec in pending:
        try:
            result = mc.remember(rec.get("text", ""), timeout=90)
            if result.get("error") or "_error" in result:
                survivors.append(rec)
                failed += 1
            else:
                moved += 1
                with open(mc.SYNCED, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps({**rec, "synced_at": time.time(),
                                         "via": "flush"}, ensure_ascii=False) + "\n")
        except Exception:
            survivors.append(rec)
            failed += 1

    write_pending(survivors)
    mc.log("flush", {"moved": moved, "failed": failed, "remaining": len(survivors)})

    if moved or failed:
        print(f"walrus memory mirror: moved={moved} failed={failed} "
              f"remaining={len(survivors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
