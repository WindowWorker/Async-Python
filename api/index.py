from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.promises import *
import sys, threading
from api.excepts import *
from api.xhttp import *


def globalThis():
  return

globalThis.env = 'test'
if sys.version_info.minor == 9:
  globalThis.env = 'prod'

globalThis.staticPrefix = 'https://raw.githubusercontent.com/Patrick-ring-motive/Async-Python-Reverse-Proxy/main/static'
#print(globalThis.env)


globalThis.hostTargetList = [
  'www.python.org',
  'packaging-python-org.vercel.app',
#  'packaging-python-org.weblet.repl.co',
  #'packaging.python.org',
  #      'docs.python.org',
  'docs-python-org.weblet.repl.co',
  'pypi.org',
  'wwwpypaio.weblet.repl.co',
  #'www.pypa.io',
  'wiki.python.org',
  'peps.python.org',
  'mail.python.org',
  'bugspythonorg.weblet.repl.co',
  'discuss.python.org',
  'devguidepythonorg.weblet.repl.co',
  'planetpython.org',
  'pyfound.blogspot.com'
]
globalThis.hostShortCircuit = ['planetpython.org', 'docspythonorg.weblet.repl.co']


class handler(BaseHTTPRequestHandler):

  async def do_METHOD(request, data):
    request.globalThis=globalThis
    rtrn = {}
    request.isTimedOut = False
    hostFirst = ''
    try:
      request.localhost = request.headers['Host']
      request.timeout = 5
      if globalThis.env == 'test':
        await go(await promise(atimeout, [request, 2]))
      if 'jquery.js' in request.path:
        request.path = '/_static/jquery.js'
      if (request.path.split('?')[0] in [
          '/injects.js', 
        '/boa.js', 
        '/favicon.js',
        '/get-prism.js', 
        '/injects.css', '/_static/jquery.js',
          '/static/js/warehouse.c431b9ad.js',
        '/static/favicon.ico',
          '/plugins/discourse-client-performance/javascripts/discourse-client-performance.js',
          '/wiki/common/js/common.js'
      ]):
        if globalThis.env == 'test':
          with open('static' + request.path.split('?')[0], 'r') as f:
            content = f.read()
          request.send_response(200)
          if '.js' in request.path:
            request.send_header('Content-type', 'text/javascript')
          request.end_headers()
          return await writeResponseBody(request, bytes(content, 'utf8'))
        else:
          res = await fetchURL(globalThis.staticPrefix + request.path)
          resBody = res.read()
          request.send_response(200)
          if '.js' in request.path:
            request.send_header('Content-type', 'text/javascript')
          request.end_headers()
          request.wfile.write(resBody)
          res.connection.close()
          return
      hostFirst = globalThis.hostTargetList[0]
      if (request.headers['Referer']):
        referer = request.headers['Referer']
        if ("hostname=" in referer):
          hostFirst = referer.split("hostname=")[1].split('&')[0].split('#')[0]
      if ("hostname=" in request.path):
        hostFirst = request.path.split("hostname=")[1].split('&')[0].split(
          '#')[0]
      if hostFirst == request.localhost:
        hostFirst = globalThis.hostTargetList[0]
      request.path = stripHostParam(request.path)
      request.hostTarget = hostFirst
      response = await fetchResponse(request, request.hostTarget)
      lastHost = hostFirst
      if hostFirst not in [
          'packaging.python.org', 'packaging-python-org.weblet.repl.co',
          'packaging-python-org.vercel.app','docs.python.org', 'docs-python-org.weblet.repl.co',
        'docs-python-org.vercel.app'
      ]:
        for hostTarget in globalThis.hostTargetList:
          if response.status == 304:
            requestPath = request.path
            request.path = bustCache(request.path)
            request.hostTarget = lastHost
            response = await fetchResponse(request, request.hostTarget)
            request.path = requestPath
            if response.status < 200:
              break
          lastHost = hostTarget
          if response.status < 300:
            break
          for header in response.getheaders():
            if 'ocation' in header[0]:
              redirectHost = header[1].split('/')[2]
              requestPath = request.path
              request.path = header[1].split(redirectHost)[1]
              request.hostTarget = redirectHost
              response = await fetchResponse(request, request.hostTarget)
              request.path = requestPath
              if response.status < 300:
                break
          if response.status > 299:
            request.hostTarget = hostTarget
            response = await fetchResponse(request, request.hostTarget)
      sendResponsePromise = await go(await promise(sendResponse,
                                                   [request, response.status]))
      headers = response.getheaders()
      await sendResponsePromise
      contentType = ''
      contentEncoding = ''
      contentLength = 2000000
      for header in headers:
        if header[0] == 'Transfer-Encoding':
          continue
        if header[0] == 'Connection':
          continue
        if header[0] == 'Content-Type':
          contentType = header[1]
        if header[0] == 'Content-Encoding':
          contentEncoding = header[1]
        if header[0] == 'Content-Length':
          contentLength = int(header[1])
        if 'ecurity' in header[0]:
          continue
        if 'olicy' in header[0]:
          continue
        try:
          reheader=header[1].replace(request.hostTarget,request.localhost,1)
          if header[0] == 'Location':
            char = '?'
            if('?' in reheader):
              char='&'
              if 'hostname=' not in reheader:
                reheader=reheader.split('#')[0]+char+'hostname='+request.hostTarget
          request.send_header(header[0],reheader)
        except:
          none()
      resBodyPromise = await go(await promise(readResponseBody,
                                              [response, contentLength]))
      await endHeaders(request)
      resBody = await resBodyPromise
      if 'text/html' in contentType:
        if len(contentEncoding) == 0:
          resBody = str(resBody, encoding='utf-8').replace(
            '</head>', '<script src="/injects.js"></script></head>')
          resBody = bytes(resBody, 'utf-8')
      if 'javascript' in contentType:
        if len(contentEncoding) == 0:
          resBody = bytes(
            (' import("/injects.js"); ' + str(resBody, encoding='utf-8')),
            'utf-8')
      return await writeResponseBody(request, resBody)
    except:
      if hostFirst != 'packaging.python.org':
        if request.isTimedOut == true:
          if globalThis.env == 'test':
            closeRequest(request)
        ct = 'text/html'
        code = 200
        writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/\x03\x04'
        if '.css' in request.path:
          ct = 'text/css'
          code = 200
          writeEnd = b'\x03\x04'
        if '.js' in request.path:
          if globalThis.env == 'test':
            return closeRequest(request)
          ct = 'text/javascript'
          code = 200
          writeEnd = b'\x03\x04'
        request.send_response(code)
        request.send_header('Content-type', ct)
        await endHeaders(request)
        rtrn = await writeResponseBody(request, writeEnd)
        if request.headers['Host'] in globalThis.hostShortCircuit:
            if globalThis.env == 'test':
              closeRequest(request)
    if hostFirst == 'packaging.python.org':
      request.wfile.flush()
      if globalThis.env == 'test':
        request.wfile.close()
    return rtrn

  async def done_OPTIONS(request, data):
    request.send_response(200)
    await endHeaders(request)
    return await writeResponseBody(request, b'*')

  def do_GET(request):
    asyncio.run(request.do_METHOD(request))

  def do_OPTIONS(request):
    asyncio.run(request.do_METHOD(request))

  def do_POST(request):
    asyncio.run(request.do_METHOD(request))

  def do_PUT(request):
    asyncio.run(request.do_METHOD(request))

  def do_PATCH(request):
    asyncio.run(request.do_METHOD(request))

  def do_HEAD(request):
    asyncio.run(request.do_METHOD(request))

  def do_DELETE(request):
    asyncio.run(request.do_METHOD(request))

  def do_CONNECT(request):
    asyncio.run(request.do_METHOD(request))

  def do_TRACE(request):
    asyncio.run(request.do_METHOD(request))


#asyncio.run(AsyncHTTPServer())
