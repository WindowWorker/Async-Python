from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.index import *
import sys

print(sys.version_info)

httpd = ThreadingHTTPServer(('', 8000), handler)
httpd.timeout = 5
httpd.serve_forever()