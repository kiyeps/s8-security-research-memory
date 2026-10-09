# Model and Runtime Information

## Runtimes

| Runtime | Role | Interface |
|---|---|---|
| Hermes Agent | Primary runtime and chatbot. | Telegram (`@Celiynbot`) |
| OpenClaw | Second runtime, used for the cross-runtime demonstration. | Telegram (`@choviybot`) |

Host: Linux (Ubuntu under WSL2), x86_64. Python 3 and Node.js on `PATH`.

## Model

- The assistant's resident model during the demonstration:
  `deepseek-v4.1-flash` family, served through an OpenAI-compatible endpoint.
- The bridge itself is model-agnostic. Any runtime that can call the memory
  tools works; nothing in this repository depends on a specific model vendor.

## Walrus Memory components

| Component | Reference |
|---|---|
| `@mysten-incubation/memwal-mcp` | 0.0.14 (MCP server used by Hermes) |
| `@mysten-incubation/oc-memwal` | 0.0.7 (OpenClaw plugin) |
| Network | Sui mainnet |
| Relayer | `https://relayer.memory.walrus.xyz` |

## Runtime notes that matter for this bridge

- Shell hooks register once per process at runtime startup. A restart is
  required for hook configuration changes to take effect.
- The gateway drops pending messages at a fresh start; this is runtime
  behavior, not bridge behavior, and is noted here only so a reader does not
  mistake it for a memory-layer problem.
- Hook timeouts are deliberately short. A slow memory layer degrades to "no
  injected context" rather than a stalled turn.
