def mcp_welcome(user: dict):
    if user["role"] == "admin":
        print("MCP: Welcome, creator.")
    else:
        print(f"MCP: Access channel opened for user '{user['username']}'.")
    print("END OF LINE.")

def mcp_threat_warning():
    print("MCP: User behavior irregularity detected.")
    print("END OF LINE.")
