from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.promises import *
import sys, threading
from api.excepts import *


async def sendResponse(request, status):
  return request.send_response(status)


async def endHeaders(request):
  return request.end_headers()


async def readResponseBody(res, length):
  try:
    bdy = bytearray(length + 16)
    res.readinto(bdy)
    return bdy
  except:
    try:
      return res.read()
    except:
      return b''


def killRequest(request):
  if 'kill' in request.kill:
    none()


def reboot():
  #httpd.shutdown()
  httpd.serve_forever()


async def atimeout(request, seconds):
  await asyncio.sleep(seconds)
  request.isTimedOut = true
  ct = 'text/html'
  code = 408
  writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/'
  if '.css' in request.path:
    ct = 'text/css'
    code = 200
    writeEnd = b''
  if '.js' in request.path:
    return killRequest(request)
    ct = 'text/javascript'
    code = 200
    writeEnd = b''
  request.send_response(code)
  request.send_header('Content-type', ct)
  await endHeaders(request)
  rtrn = await writeResponseBody(request, writeEnd)
  if 'planetpython' in request.headers['Host']:
    killRequest(request)
  await AQ(streamDetach, [request.wfile])
  if request.headers['Host'] in hostShortCircuit:
    killRequest(request)
  return rtrn


async def writeResponseBody(req, body):
  if hasattr(req, "localhost"):
    if req.localhost == 'async-python-reverse-proxy.weblet.repl.co':
      await (await promise(atimeout, [req, 1])).start()
  try:
    return req.wfile.write(body)
  except:
    return


async def readRequest(req, length):
  if length < 5:
    return b''
  return req.rfile.read(length)


async def connectClient(host):
  return http.client.HTTPSConnection(host)


async def connectRequest(connection, requestCommand, requestPath, requestBody,
                         requestHeaders):
  return connection.request(requestCommand,
                            requestPath,
                            body=requestBody,
                            headers=requestHeaders)


async def connectResponse(connection):
  return connection.getresponse()


async def connectClose(connection):
  connection.close()


async def streamDetach(stream):
  stream.detach()


async def readBody(req, host):
  reqBody = None
  requestBodyLength = req.headers['Content-Length']
  if (req.rfile.readable() and requestBodyLength):
    reqBody = await readRequest(req, int(requestBodyLength))
    if len(reqBody) < 5:
      reqBody = None
  return reqBody


def bustCache(path):
  hash = ''
  if '#' in path:
    hash = '#' + path.split('#')[1]
  char = '?'
  if '?' in path:
    char = '&'
  return path.split('#')[0] + char + 'bustcache=' + str(time.time()).replace(
    '.', '')


def stripHostParam(path):
  if '?hostname=' in path:
    if '&' in path:
      hostparts = path.split('?hostname=')
      params = hostparts[1].split('&')
      params[0] = ''
      params = '&'.join(params).split()
      params[0] = '?'
      path = hostparts[0] + ''.join(params)
    elif '#' in path:
      hostparts = path.split('?hostname=')
      hash = hostparts[1].split('#')
      hash[0] = ''
      path = hostparts[0] + '#'.join(hash)
  elif '&hostname=' in path:
    hostparts = path.split('&hostname=')
    if '&' in hostparts[1]:
      params = hostparts[1].split('&')
      params[0] = ''
      path = hostparts[0] + '&'.join(params)
    elif '#' in path:
      hostparts = path.split('&hostname=')
      hash = hostparts[1].split('#')
      hash[0] = ''
      path = hostparts[0] + '#'.join(hash)
  return path


httpd = {}


async def fetchResponse(req, host):
  connection = {}
  try:
    connectionPromise = await promise(connectClient, [host])
    await connectionPromise.start()
    reqBodyPromise = await promise(readBody, [req, host])
    await reqBodyPromise.start()
    reqHeaders = {}
    for header in req.headers:
      reqHeaders[header] = req.headers[header].replace(req.localhost, host)
    reqHeaders['Localhost'] = req.localhost
    reqHeaders['Cache-Control'] = 'max-age='
    reqHeaders['Expires'] = 'Tue, 19 Jan 2000 03:14:07 GMT'
    delete(reqHeaders, 'Etag')
    delete(reqHeaders, 'Expect-Ct')
    delete(reqHeaders, 'Cookie')
    reqBody = await reqBodyPromise
    connection = await connectionPromise
    await connectRequest(connection, req.command, req.path, reqBody,
                         reqHeaders)
    res = await connectResponse(connection)
    res.connection = connection
    return res
  except:
    res = http.client.HttpResponse(status=500)
    res.connection = connection
    return res
