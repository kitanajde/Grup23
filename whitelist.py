# whitelist.py
import time

from validation import sanitize_arg
import db
import dangerscan
import identity_disc
import tron_fx


def cmd_echo(user, arg):
    arg = sanitize_arg(arg or "")
    print(f"[ECHO] {arg}")

    # Tehlikeli cümle analizi
    result = dangerscan.analyze_text(arg)
    flagged = result["flagged_sentences"]
    threat_delta = result["threat_delta"]

    if flagged:
        print("\nSuspicious sentences detected:")
        for s in flagged:
            print(f"  !!! {s}")
        identity_disc.add_threat(user["username"], threat_delta)
        msg = tron_fx.mcp_reaction(
            threat_score=_get_threat_score(user["username"]),
            suspicious_found=True
        )
        if msg:
            print(msg)
    else:
        msg = tron_fx.mcp_reaction(
            threat_score=_get_threat_score(user["username"]),
            suspicious_found=False
        )
        if msg:
            print(msg)


def cmd_scan_text(user, arg):
    text = arg or ""
    print("Scanning text for threats...\n")
    result = dangerscan.analyze_text(text)
    flagged = result["flagged_sentences"]
    threat_delta = result["threat_delta"]

    if not flagged:
        print("No suspicious sentences found.")
    else:
        print("Suspicious sentences:")
        for s in flagged:
            print(f"  !!! {s}")

        identity_disc.add_threat(user["username"], threat_delta)
        msg = tron_fx.mcp_reaction(
            threat_score=_get_threat_score(user["username"]),
            suspicious_found=True
        )
        if msg:
            print(msg)

    tron_fx.end_of_line()


def cmd_time(user, arg):
    print("Current time:", time.ctime())


def cmd_admin_stats(user, arg):
    logs = db.get_recent_commands(limit=10)
    print("Last 10 commands:")
    for entry in logs:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry["created_at"]))
        print(f"[{ts}] {entry['username']}: {entry['cmd']}")
    tron_fx.end_of_line()


def cmd_list_users(user, arg):
    users = db.list_users()
    print("Registered users:")
    for u in users:
        print(f"- {u['username']} ({u['role']})")
    tron_fx.end_of_line()


def cmd_recent_commands(user, arg):
    try:
        limit = int(arg) if arg else 10
    except ValueError:
        limit = 10

    logs = db.get_recent_commands(limit=limit)
    print(f"Last {len(logs)} commands:")
    for entry in logs:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry["created_at"]))
        print(f"[{ts}] {entry['username']}: {entry['cmd']}")
    tron_fx.end_of_line()


def cmd_identity_disc(user, arg):
    disc = identity_disc.get_disc(user["username"])
    if not disc:
        print("No identity disc data.")
        tron_fx.end_of_line()
        return

    print(f"Identity Disc for USER: {disc['username']}")
    print("--------------------------------")
    print(f"Role: {disc['role']}")
    print(f"Security Level: {disc['security_level']}")
    print(f"Commands Executed: {disc['commands_executed']}")
    print(f"Threat Score: {disc['threat_score']}")
    print(f"Login Count: {disc['login_count']}")
    print(f"Last Access: {disc['last_access']}")
    print("--------------------------------")
    tron_fx.end_of_line()


def cmd_grid_scan(user, arg):
    print("Scanning system sectors...")
    time.sleep(0.3)
    print("Sector 1: OK")
    time.sleep(0.2)
    print("Sector 2: OK")
    time.sleep(0.2)
    print("Sector 3: anomaly detected")
    time.sleep(0.2)
    print("Sector 4: OK")
    print("GRID STATUS: STABLE")
    tron_fx.end_of_line()


def cmd_lightwall(user, arg):
    print("Deploying defensive lightwall...")
    time.sleep(0.3)
    print("[|||||||||||||||||] Protection active.")
    tron_fx.end_of_line()


def cmd_sector_map(user, arg):
    print("Mapping grid...")
    time.sleep(0.3)
    print("[Sector 1] Programs: stable")
    print("[Sector 2] I/O Streams: active")
    print("[Sector 3] Security Node: anomaly")
    print("[Sector 4] Power Circuits: stable")
    print("GRID MAPPING COMPLETE.")
    tron_fx.end_of_line()


def _get_threat_score(username: str) -> int:
    disc = identity_disc.get_disc(username)
    if not disc:
        return 0
    return disc["threat_score"]


WHITELIST = {
    # Herkes
    "echo":        {"fn": cmd_echo,         "role": "any"},
    "time":        {"fn": cmd_time,         "role": "any"},
    "scan-text":   {"fn": cmd_scan_text,    "role": "any"},
    "identity-disc": {"fn": cmd_identity_disc, "role": "any"},

    # TRON/GRID efekt komutları (herkes kullanabilir, ama istersen admin yapabilirsin)
    "grid-scan":   {"fn": cmd_grid_scan,    "role": "any"},
    "lightwall":   {"fn": cmd_lightwall,    "role": "any"},
    "sector-map":  {"fn": cmd_sector_map,   "role": "any"},

    # Admin komutları
    "admin-stats":     {"fn": cmd_admin_stats,     "role": "admin"},
    "list-users":      {"fn": cmd_list_users,      "role": "admin"},
    "recent-commands": {"fn": cmd_recent_commands, "role": "admin"},
}
