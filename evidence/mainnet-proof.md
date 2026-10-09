# Mainnet Proof

Walrus Memory writes for this project land on Sui mainnet and are addressed
by blob id. This page records the safe, public parts of that evidence.

## Recorded write 1: live Telegram-triggered write

- Date: 2026-10-09.
- Path: a live Telegram message to the assistant triggered a memory write
  through the runtime's memory tool.
- Job id: `212de1b5-f4d7-4c9b-ac9d-1ff070e60df5` (returned by the relayer).
- Blob id: `Htzm9C3BsvyGjyralT8ya_YEdwffE_S_0x-pldjs4zM`.

## Recorded write 2: mirrored local memory update

- Date: 2026-10-09.
- Path: a local memory update, mirrored by the bridge's write-side hook.
- Job id: `dbf1a0d3-6e03-4b57-82c0-c1e28efc34cf`.
- Blob id: `g6DFIAiyKUUuHonIUniv69qoNaCgibppTe2SoMfGWjM`.

## Public retrieval check

Anyone can check that a blob id resolves, through the public aggregator:

```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  'https://aggregator.walrus-mainnet.walrus.space/v1/blobs/Htzm9C3BsvyGjyralT8ya_YEdwffE_S_0x-pldjs4zM'
# expected: 200
```

Re-checked 2026-10-09: HTTP 200. Note: some HTTP clients receive a
bot-signature rejection from the CDN in front of the aggregator; `curl`
works. See `../docs/limitations.md`, item 7.

## Cross-runtime marker blobs

The cross-runtime demonstration produced its own marker records:

| Direction | Marker | Blob id |
|---|---|---|
| Hermes wrote, OpenClaw read | XR-LIVE-20261009-A | `XYR0_uRCwCxkRkBNPq59OaRScii9nPgO5LVeZramQfg` |
| OpenClaw wrote, Hermes read | XR-LIVE-20261009-B | `tFAtE8GPE5MlHUcS-Omaot2jiHHGXAhduirAlj2E6O8` |

Both blobs re-checked 2026-10-09: HTTP 200.

## What a blob id proves, and what it does not

- It proves a write was accepted and stored: the id resolves to stored bytes
  on mainnet.
- The stored bytes are the client-side encrypted record. This repository does
  not publish decrypted record content.
- A blob id is not a credential. Publishing it does not grant access to the
  account or to unencrypted content.
