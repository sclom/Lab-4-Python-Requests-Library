#!/usr/bin/env python3
"""
Lab 4 Dev Container Health Check

Checks:
- DNS resolution (key sites + target APIs)
- Basic internet reachability (HEAD)
- Required Python packages (requests)

Outputs:
- /workspace/logs/devcontainer_health.log (machine-graded markers)
- /workspace/logs/DEVCONTAINER_STATUS.txt (student-friendly banner)
Exit codes:
- --deep => nonzero on failure (blocks container creation)
- default => always zero (non-blocking)
"""
from __future__ import annotations
import socket, sys, importlib.util
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

LOG_DIR = Path("/workspace/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "devcontainer_health.log"
BANNER_PATH = LOG_DIR / "DEVCONTAINER_STATUS.txt"

# Minimal set for this lab
REQUIRED_PKGS = ["requests"]

DNS_HOSTS = [
    "github.com",
    "pypi.org",
    "icanhazdadjoke.com",
    "deckofcardsapi.com"
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def log(line: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")

def banner(lines) -> None:
    with BANNER_PATH.open("w", encoding="utf-8") as f:
        for l in lines:
            f.write(l.rstrip() + "\n")

def check_dns() -> bool:
    ok = True
    for host in DNS_HOSTS:
        try:
            ip = socket.gethostbyname(host)
            log(f"LAB4_DNS_OK host={host} ip={ip}")
        except Exception as e:
            ok = False
            log(f"LAB4_DNS_FAIL host={host} err={type(e).__name__}:{e}")
    return ok

def check_internet() -> bool:
    # Use the Dad Jokes API host as the probe to be context-appropriate
    try:
        req = urllib.request.Request("https://icanhazdadjoke.com", method="HEAD")
        with urllib.request.urlopen(req, timeout=6) as resp:
            log(f"LAB4_NET_OK status={resp.status}")
            return 200 <= resp.status < 400
    except Exception as e:
        log(f"LAB4_NET_FAIL err={type(e).__name__}:{e}")
        return False

def check_packages() -> bool:
    ok = True
    for pkg in REQUIRED_PKGS:
        if importlib.util.find_spec(pkg):
            log(f"LAB4_PKG_OK name={pkg}")
        else:
            ok = False
            log(f"LAB4_PKG_FAIL name={pkg}")
    return ok

def main(deep: bool = False) -> None:
    log(f"LAB4_HEALTH_START ts={now_iso()} deep={deep}")
    dns_ok = check_dns()
    net_ok = check_internet()
    pkg_ok = check_packages()
    overall = dns_ok and net_ok and pkg_ok
    log(f"LAB4_HEALTH_SUMMARY dns={dns_ok} net={net_ok} pkg={pkg_ok} overall={overall}")
    log(f"LAB4_HEALTH_END ts={now_iso()}")

    # Student-facing banner
    lines = [
        "================= DEVCONTAINER HEALTH (Lab 4) =================",
        f"Time (UTC): {now_iso()}",
        f"DNS resolution: {'PASS' if dns_ok else 'FAIL'}",
        f"Internet reachability: {'PASS' if net_ok else 'FAIL'}",
        "Required Python packages:",
    ]
    for pkg in REQUIRED_PKGS:
        present = "OK" if importlib.util.find_spec(pkg) else "MISSING"
        lines.append(f"  - {pkg}: {present}")
    lines.append("Overall status: " + ("READY ✅" if overall else "NOT READY ❌"))
    lines.append("Details: logs/devcontainer_health.log")
    lines.append("===============================================================")
    banner(lines)

    # Exit code strategy
    sys.exit(0 if (overall or not deep) else 1)

if __name__ == "__main__":
    main(deep="--deep" in sys.argv)
