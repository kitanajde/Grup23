# tron_fx.py
import time
import random

NEON_BLUE = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


LOGO = f"""{NEON_BLUE}{BOLD}
== TRON:// SECURE GRID CONSOLE ==
   Flynn Secure Command Interface
{RESET}"""


def boot_animation():
    print(f"{NEON_BLUE}Initializing Secure Grid...{RESET}")
    time.sleep(0.3)
    print("[█         ] 10%")
    time.sleep(0.3)
    print("[███       ] 30%")
    time.sleep(0.3)
    print("[██████    ] 60%")
    time.sleep(0.3)
    print("[██████████] 100%")
    time.sleep(0.2)
    print(f"{NEON_BLUE}ACCESS CHANNEL OPENED{RESET}")
    time.sleep(0.3)
    print()


def end_of_line():
    print(f"{NEON_BLUE}END OF LINE.{RESET}")


def mcp_reaction(threat_score: int, suspicious_found: bool) -> str:
    # Basit mood sistemi
    if threat_score >= 10:
        return "MCP: User behavior critical. Surveillance level increased."
    if suspicious_found and threat_score >= 5:
        return "MCP: User behavior irregularity detected. Continue monitoring."
    if suspicious_found:
        return "MCP: Anomaly in user input. Pattern logged."
    # Şüpheli yoksa arada bir tatlı şey söylesin
    if random.random() < 0.2:
        return "MCP: Grid remains stable. Proceed, program."
    return ""
