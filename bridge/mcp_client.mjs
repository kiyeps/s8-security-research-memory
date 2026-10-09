#!/usr/bin/env node
/**
 * Hermes client path: drives the same MCP server that Hermes wires as mcp_servers.memwal.
 * usage: node mcp_client.mjs <bin> <recall|remember|analyze|bulk> <namespace> <arg> [limit]
 *
 * Prints the raw JSON-RPC result so blob ids / job ids / errors are visible for evidence.
 * Never prints credentials (the MCP server reads them from the client credential file itself).
 */
import { spawn } from 'node:child_process';
import { randomUUID } from 'node:crypto';

const [bin, cmd, ns, arg, limit] = process.argv.slice(2);
if (!bin || !cmd || !ns) {
  console.error('usage: mcp_client.mjs <bin> <recall|remember|analyze|bulk> <namespace> <arg> [limit]');
  process.exit(2);
}

const proc = spawn('node', [bin, '--namespace', ns, '--prod'], { stdio: ['pipe', 'pipe', 'pipe'] });
let buf = '';
const pending = new Map();
let stderr = '';
proc.stdout.on('data', (d) => {
  buf += d.toString();
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (!line) continue;
    let m;
    try { m = JSON.parse(line); } catch { continue; }
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  }
});
proc.stderr.on('data', (d) => { stderr += d.toString(); });

function rpc(method, params) {
  const id = randomUUID();
  return new Promise((res, rej) => {
    pending.set(id, res);
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); rej(new Error('timeout ' + method)); } }, 180000);
    proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}
const call = (name, args) => rpc('tools/call', { name, arguments: args });
const txt = (m) => (m.result?.content ?? []).map((c) => c.text ?? '').join(' ');

const out = { ts: new Date().toISOString(), client: 'hermes-mcp', cmd, namespace: ns };

try {
  if (cmd === 'recall') {
    const r = await call('memwal_recall', { query: arg, limit: Number(limit || 5), namespace: ns });
    out.query = arg;
    out.text = txt(r);
    out.raw = r.result ?? r;
  } else if (cmd === 'remember') {
    const r = await call('memwal_remember', { text: arg, namespace: ns });
    out.text = txt(r);
    out.raw = r.result ?? r;
  } else if (cmd === 'analyze') {
    const r = await call('memwal_analyze', { text: arg, namespace: ns });
    out.text = txt(r);
    out.raw = r.result ?? r;
  } else if (cmd === 'bulk') {
    const r = await call('memwal_remember_bulk', { facts: [arg], namespace: ns });
    out.text = txt(r);
    out.raw = r.result ?? r;
  } else {
    out.error = 'unknown cmd';
  }
} catch (e) {
  out.error = String(e.message || e);
}
if (stderr.trim()) out.stderr_tail = stderr.trim().split('\n').slice(-4).join(' | ');
console.log(JSON.stringify(out, null, 1));
try { proc.kill('SIGKILL'); } catch {}
process.exit(0);
