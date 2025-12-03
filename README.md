# Flynn's Secure Grid Console — TRON-Inspired Security CLI

Flynn's Secure Grid Console is a security-focused, TRON-inspired command interface designed to simulate the digital GRID environment using safe modern practices.  
It combines authentication, RBAC, command whitelisting, input sanitization, threat detection, identity disc system, MCP-style reactions, TRON-style animations, and system sector simulation.

This repo contains the full implementation of a mid-sized secure console project completed over **two sprints** by a **three-member team**.

---

#  Project Overview

Flynn’s Secure Grid Console is a command-line security framework with:
- PBKDF2 password hashing  
- SQLite-based identity & audit logging  
- Threat-word detection  
- TRON-style boot animation  
- Identity Disc system (per-user metadata & stats)  
- GRID scan, sector map, and lightwall security emulation  
- MCP-style behavior engine  
- Role-based command permissions  
- Command history tracking  

You can think of it as a **modern security console that feels like something inside the TRON universe**.

---

#  TRON-Inspired Features

###  1. Secure Grid Boot Animation  
Displayed when the system starts:
Initializing Secure Grid...
[█ ] 10%
[███ ] 30%
[██████ ] 60%
[██████████] 100%
ACCESS CHANNEL OPENED


###  2. Identity Disc System  
Every user has a digital “Identity Disc” like in TRON:


Identity Disc for USER: sam
Role: admin
Security Level: 4
Commands Executed: 123
Threat Score: 2
Last Access: 2025-11-29 19:22:18

END OF LINE.


###  3. GRID Scan


grid-scan
Scanning system sectors...
Sector 1: OK
Sector 2: OK
Sector 3: anomaly detected
Sector 4: OK
GRID STATUS: STABLE
END OF LINE.


###  4. Lightwall Security Deployment  
Inspired by light cycles:


lightwall
Deploying defensive lightwall...
[|||||||||||||||||||||] Protection active.


###  5. MCP Behavior Engine  
Console reacts to user activity, threat words, and suspicious actions:
- “User behavior irregularity detected.”  
- “Cease functions immediately.”  
- Admin login → “Welcome, creator.”  
- Too many failed logins → “Access denied, program.”  

### 6. Threat Word Detection  
User messages containing dangerous phrases are automatically flagged.

---

#  System Architecture



flynn_console/
│
├── main.py # CLI flow, animations, MCP logic
├── auth.py # Register, login, lockout
├── db.py # SQLite models & audit logging
├── utils.py # PBKDF2 hashing + salt
├── validation.py # Input sanitization + threat scanning
├── identity_disc.py # TRON Identity Disc system
├── grid.py # Grid scan, sector map, lightwall
├── whitelist.py # Command whitelist + RBAC rules
├── config.py # Paths, DB location, constants
│
├── data/flynn.db # SQLite database
└── logs/system.log # Event logging


---

#  Sprint Summary (Two Sprints, Three People)

##  Sprint 1 (07.11.2025 → 17.11.2025)
###  Sprint Goal  
Authentication base, CLI skeleton, architecture planning, initial validation.

###  Betül – Lead & Security Developer  
- Designed the full system architecture.  
- Created the base CLI workflow and menu controller.  
- Planned the RBAC hierarchy (admin/user).  

### Metehan – Backend & Auth Developer  
- Implemented register/login functions.  
- Integrated PBKDF2 hashing with salt generation.  
- Added password verification flow.  

###  İlayda – Validation & Security QA  
- Implemented basic input validation rules using regex.  
- Performed early hashing + salt correctness tests.  

---

##  Sprint 2 (18.11.2025 → 28.11.2025)
###  Sprint Goal  
Whitelist engine, RBAC enforcement, logging, lockout, sanitization completion.

###  Betül – Lead & Security Developer  
- Implemented full RBAC logic from Sprint 1’s plan.  
- Integrated logging system for authentication + command usage.  
- Added admin-only commands into whitelist.  

###  Metehan – Backend & Core Logic Developer  
- Built whitelist command engine.  
- Wrote command execution pipeline with argument parsing.  
- Ensured shell-safe execution (no system calls).  

###  İlayda – Validation & Security Testing  
- Completed sanitization system.  
- Implemented brute-force lockout mechanism (5 fails → 5 minutes).  
- Tested command injection, argument manipulation, and hash consistency.  

---

# Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/flynn-secure-grid-console.git
cd flynn-secure-grid-console

2. Install Python Dependencies
pip install -r requirements.txt

3. Run the Console
python main.py

Example Usage
Login
Username: sam
Password: ********
Login successful.
Welcome, creator.

Running a Command
sam@admin> grid-scan
Scanning system sectors...
Sector 3: anomaly detected
GRID STATUS: STABLE
END OF LINE.

Identity Disc
sam@admin> disc

🧪 Threat Detection Example

Input:

delete all system files


Output:

⚠ THREAT WORD DETECTED: delete
⚠ THREAT WORD DETECTED: system
Threat Score increased.

 Future Work

Web dashboard for Grid monitoring

TRON Lightcycle-style visualization of command activity

AI-enhanced MCP behavior patterns

Network-based program-to-program communication

 License

MIT License or your preferred license.

---  

If you'd like, I can also generate:  
 `requirements.txt`  
 A full “identity_disc.py”, “grid.py”, and MCP behavior engine  
 GitHub badges (build passing, python version, license)  
 A demo GIF for your repository  

Just say **"generate all modules"** or **"add more TRON flavor"**.
