import subprocess
import sys
import requests

def get_session_id(ip, printer_name):
    # Run the curl command to get the Set-Cookie header with org.cups.sid
    curl_command = f"curl -v -c cookies.txt http://{ip}:631/printers/{printer_name} 2>&1 | grep 'Set-Cookie'"
    
    # Execute the curl command in the shell and capture the output
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    
    # Parse the output to extract the session ID
    if result.returncode == 0:
        output = result.stdout
        sid = None
        for line in output.splitlines():
            if 'Set-Cookie:' in line and 'org.cups.sid=' in line:
                # Extract the org.cups.sid value from the line
                sid = line.split('org.cups.sid=')[1].split(';')[0]
                break
        if sid:
            return sid
        else:
            print("Failed to extract org.cups.sid from the response.")
            sys.exit(1)
    else:
        print("Curl command failed to execute.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python send_request.py <IP> <PRINTER_NAME>")
        sys.exit(1)

    ip = sys.argv[1]
    printer_name = sys.argv[2]

    # Get the session ID dynamically
    sid = get_session_id(ip, printer_name)

    # Define the endpoint URL
    url = f"http://{ip}:631/printers/{printer_name}"

    # Define the headers with the dynamic session ID
    headers = {
        'Host': f'{ip}:631',
        'Cookie': f'org.cups.sid={sid}',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'https://{ip}:631/printers/{printer_name}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'https://{ip}:631',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'keep-alive',
    }

    # Define the payload (form data) for the print-test-page operation
    data = {
        'org.cups.sid': sid,
        'OP': 'print-test-page'
    }

    # Send the POST request to the endpoint
    response = requests.post(url, headers=headers, data=data, verify=False)

    # Print out the response for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Check the response
    if response.status_code == 200:
        print("Test page successfully sent to the printer.")
    else:
        print("Failed to send test page.")
