# Phase 1 Blueprint — VPS Recon

Status: **Not started.** Blocked on the user providing SSH access (public
key exchange, never a root password — see "Access" below and
`BLUEPRINT.md`'s locked decisions).

## Goal

Establish safe, key-based access to the user's Hostinger VPS and get a
factual picture of what's already running on it, before any later phase
(2, 6, 9) installs or changes anything there.

## Scope (from `docs/ORIGINAL_BLUEPRINT.md`, Phase 1)

1. SSH into the Hostinger VPS.
2. Check OS version and available resources (RAM/disk/CPU).
3. Check whether Docker is installed; install it if missing.
4. Enumerate existing containers/services and what ports they occupy
   (original brief flags port 80/443 specifically — likely something is
   already serving there).
5. Verify DNS: confirm what `kaylas.cloud` currently resolves to, and
   whether it already points at this VPS.

Out of scope for Phase 1 (belong to later phases): installing ChromaDB
(Phase 2), n8n (Phase 8), the in-browser terminal/file manager (Phase 9),
or deploying the site itself to the VPS (the site is deployed on Vercel
per `BLUEPRINT.md` — the VPS is for backend services, not hosting the
frontend).

## Access (locked decision — do not deviate)

- **SSH key-based only.** Never request, paste, or store a root password
  in chat or in any file in this repo.
- Exchange method: the user generates a keypair (or reuses an existing
  one), adds the **public** key to the VPS's `~/.ssh/authorized_keys`
  (via Hostinger's control panel or an existing session), and shares only
  the public key / connection details (host, port, username) needed to
  connect.
- If the user pastes a password anyway, stop and ask them to rotate it
  and switch to key auth instead of proceeding.

## Information needed from the user before starting

- VPS hostname or IP.
- SSH port (if not 22) and username (if not root).
- Confirmation that a public key has been added to `authorized_keys`, or
  a key for us to add via a Hostinger panel/browser terminal the user
  drives themselves.

## Recon steps (execution order once access exists)

1. `ssh <user>@<host>` connectivity check — confirm key auth works, no
   password prompt.
2. `cat /etc/os-release`, `uname -a` — OS/kernel version.
3. `nproc`, `free -h`, `df -h` — CPU/RAM/disk headroom.
4. `docker --version` / `which docker` — Docker present?
   - If missing: install via the official Docker install script, then
     `docker --version` to confirm.
5. `docker ps -a` — existing containers, images, restart policies.
6. `ss -tlnp` (or `netstat -tlnp`) — listening ports, cross-reference
   with `docker ps` to see what's bound to 80/443 and whether it's
   Docker-managed or a bare install (nginx/apache directly on the host).
7. DNS check (run locally, not on the VPS): `dig kaylas.cloud +short`
   and `dig www.kaylas.cloud +short` — compare against the VPS's public
   IP to see if DNS already points here or is still on a registrar
   parking page / elsewhere.
8. Record findings in a "VPS state" section appended to this file (not
   BLUEPRINT.md's summary table, to keep that table high-level) with
   raw command output trimmed to the relevant lines.

## Deliverable

Once run, this file gets a `## Findings (as of <date>)` section appended
with: OS, Docker status, running containers + ports, DNS resolution
result, and any conflicts that later phases need to plan around (e.g.
"port 80/443 already serve X — Phase 9's control tower needs a different
port or a reverse-proxy path"). `BLUEPRINT.md`'s phase table gets updated
from "Not started" to "Done" (or "Partial" with what's left) in the same
commit as the findings.

## Open question

VPS IP/hostname, SSH port, and username are still needed from the user —
this phase cannot start until those are provided (see `BLUEPRINT.md`'s
"Open questions" section).
