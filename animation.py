import time
import os
import sys

NEON_BLUE = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

GRID_FRAMES = [
    """
        \\\\|||||||| GRID INITIALIZING ||||||||////
    """,
    """
        \\\\////|||| LOADING SECURITY LAYERS ||||\\\\////
    """,
    """
        ||||==== MCP ACCESS CHANNEL OPENING ====||||
    """,
    """
        <<<<---- ESTABLISHING CONNECTION ---->>>>
    """,
    """
        >>>>==== ACCESS LINK ONLINE ====<<<<
    """,
]

LOGO = f"""
{NEON_BLUE}{BOLD}
    ███████╗██╗  ██╗██╗   ██╗██╗     ██╗   ██╗███╗   ██╗
    ██╔════╝██║ ██╔╝██║   ██║██║     ██║   ██║████╗  ██║
    █████╗  █████╔╝ ██║   ██║██║     ██║   ██║██╔██╗ ██║
    ██╔══╝  ██╔═██╗ ██║   ██║██║     ██║   ██║██║╚██╗██║
    ███████╗██║  ██╗╚██████╔╝███████╗╚██████╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
{RESET}
"""

def tron_intro():
    os.system("cls" if os.name == "nt" else "clear")
    print(NEON_BLUE + "BOOTING FLYNN SECURE CONSOLE..." + RESET)
    time.sleep(1)

    for frame in GRID_FRAMES:
        os.system("cls" if os.name == "nt" else "clear")
        print(NEON_BLUE + frame + RESET)
        time.sleep(0.5)

    os.system("cls" if os.name == "nt" else "clear")
    for i in range(3):
        print(LOGO)
        time.sleep(0.3)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.15)

    print(LOGO)
    print(NEON_BLUE + ">>> CONNECTION STABLE" + RESET)
    time.sleep(1)
