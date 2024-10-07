import requests

# endpoint URL
url = "http://<IP>:631/printers/<PRINTER_NAME>"


headers = {
    'Host': '<IP>:631',
    'Cookie': 'org.cups.sid=da25cdc2314163cfff206ad59ddf3ee8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://<IP>:631/printers/<PRINTER_NAME>',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://<IP>:631',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Te': 'trailers',
    'Connection': 'keep-alive',
}

# payload (form data) for the print-test-page operation
data = {
    'org.cups.sid': 'da25cdc2314163cfff206ad59ddf3ee8',
    'OP': 'print-test-page'
}


response = requests.post(url, headers=headers, data=data, verify=False)  # verify=False to ignore SSL warnings if needed

debugging
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Check the response
if response.status_code == 200:
    print("Test page successfully sent to the printer.")
else:
    print("Failed to send test page.")
