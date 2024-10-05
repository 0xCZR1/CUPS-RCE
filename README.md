# CUPS RCE PoC (Remote Command Execution via Foomatic-rip Injection)

##Used IppSec's explanation, MalwareCube's one and EvilSocket's one, alongside with the docus and CVEs.

## Overview

This proof of concept (PoC) demonstrates a remote code execution (RCE) vulnerability in **CUPS** (Common Unix Printing System) by exploiting **Foomatic-rip** injection via IPP (Internet Printing Protocol). The script sets up a malicious IPP printer, which allows for arbitrary command execution on the target system.

### CVEs Addressed

- **CVE-2024-47076**: Improper validation of IPP attributes in libcupsfilters.
- **CVE-2024-47175**: Injection of malicious data into PPD files via libppd.
- **CVE-2024-47177**: Command injection via Foomatic-rip.

---

## How It Works

1. The script spins up a malicious **IPP server** that listens for print jobs.
2. It sends a specially crafted UDP packet to announce the "malicious printer" to the target.
3. When the target queries the printer, it receives a response with a command injection payload.
4. The payload is executed when the target sends a print job to the malicious printer.

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
```
### Example:
`python3 poc.py 192.168.1.10 192.168.1.20 "mkdir /tmp/pwned"`
This will start an IPP server on your local machine, send a malicious UDP packet to the target machine, and attempt to execute the command on the target via Foomatic-rip.

### Code Breakdown:

- IPPServerManager: Manages the IPP server lifecycle, starting and stopping the server in a separate thread.

- PrinterPwned: A subclass of StatelessPrinter, designed to inject a malicious command into the FoomaticRIPCommandLine attribute.

- send_browsed_packet: Sends a UDP packet announcing the "malicious" printer to the target.

- run: Starts the IPP server and keeps it running until interrupted.






