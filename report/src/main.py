#! python3
import sys
from io import BytesIO
from urllib3 import HTTPResponse
from http.client import parse_headers

rawresponse = sys.stdin.read().encode("utf8")
redirects = []

while True:
    header, body = rawresponse.split(b"\r\n\r\n", 1)
    if body[:4] == b"HTTP":
        redirects.append(header)
        rawresponse = body
    else:
        break

f = BytesIO(header)
# read one line for HTTP/2 STATUSCODE MESSAGE
requestline = f.readline().split(b" ")
protocol, status = requestline[:2]
headers = parse_headers(f)

resp = HTTPResponse(body, headers=headers)
resp.status = int(status)

if ('text/html' in resp.headers['Content-Type']):
    print("body")
    print(body.decode())
