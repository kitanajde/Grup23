# main.py
import logging

from config import LOG_PATH
import db
from auth import register_user, login_user
from whitelist import WHITELIST
import tron_fx
import identity_disc


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

LOG = logging.getLogger("flynn")


def show_menu():
    print("1) Register")
    print("2) Login")
    print("3) Exit\n")


def register_flow():
    print("\n--- Register ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    role = input("Role (admin/user): ").strip()

    if role not in ["admin", "user"]:
        print("Invalid role.")
        return

    if register_user(username, password, role):
        print("User registered successfully.")
        LOG.info(f"user registered: {username} as {role}")
    else:
        print("User already exists.")


def login_flow():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user, msg = login_user(username, password)
    print(msg)

    if not user:
        LOG.warning(f"failed login for user: {username}")
        return

    LOG.info(f"user authenticated: {username}")
    command_loop(user)


def command_loop(user):
    username = user["username"]
    role = user["role"]

    print("\n--- Secure Command Console ---")
    print("Type 'help' for command list. 'exit' to logout.\n")

    while True:
        raw = input(f"{role}@{username}> ").strip()

        if raw == "":
            continue

        if raw.lower() == "exit":
            print("Logged out.")
            LOG.info(f"user logged out: {username}")
            break

        if raw.lower() == "help":
            print("Available commands:")
            for cmd, entry in WHITELIST.items():
                r = entry["role"]
                print(f"- {cmd}  ({r})")
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        entry = WHITELIST.get(cmd)
        if not entry:
            print("Command not allowed.")
            LOG.warning(f"blocked command '{cmd}' by {username}")
            continue

        required_role = entry["role"]
        if required_role != "any" and role != required_role:
            print("Insufficient permissions.")
            LOG.warning(f"permission denied for '{cmd}' by {username}")
            continue

        try:
            entry["fn"](user, arg)
            LOG.info(f"cmd {cmd} executed by {username}")
            from db import log_command
            log_command(username, raw)
            identity_disc.record_command(username)
        except Exception as e:
            print("Error:", e)
            LOG.error(f"cmd {cmd} failed for {username}: {e}")


def main():
    db.init_db()
    print(tron_fx.LOGO)
    tron_fx.boot_animation()

    while True:
        show_menu()
        choice = input("> ").strip()
        if choice == "1":
            register_flow()
        elif choice == "2":
            login_flow()
        elif choice == "3":
            print("Goodbye, program.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
