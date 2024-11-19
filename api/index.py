from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
import sys, threading
from api.xhttp import *

def globalThis():
  return

#globalThis.env = 'test'
#if sys.version_info.minor >= 9:
globalThis.env = 'prod'

globalThis.staticPrefix = 'https://raw.githubusercontent.com/Patrick-ring-motive/Async-Python-Reverse-Proxy/main/static'
#print(globalThis.env)


globalThis.hostTargetList = [
  'www.python.org',
  'www.python.org'
 # 'packaging-python-org.vercel.app',
 # 'docs-python-org.vercel.app',
 # 'pypi.org',
 # 'www-pypa-io.vercel.app',
 # 'wiki.python.org',
 # 'peps.python.org',
 # 'mail.python.org',
 # 'bugs-python-org.vercel.app',
 # 'discuss.python.org',
 # 'devguide-python-org.vercel.app',
 # 'planetpython.org',
 # 'pyfound.blogspot.com'
]
globalThis.hostShortCircuit = ['planetpython.org']


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
        '/sw.js', 
        '/boa.js', 
        '/favicon.js',
        '/get-prism.js', 
        '/@@file/main.css',
        '/injects.css', '/_static/jquery.js',
          '/static/js/warehouse.c431b9ad.js',
        '/static/favicon.ico',
          '/plugins/discourse-client-performance/javascripts/discourse-client-performance.js',
          '/wiki/common/js/common.js'
      ]):
        res = await fetchURL(globalThis.staticPrefix + request.path)
        resBody = res.read()
        await zsendResponse(request,200)
        if '.js' in request.path:
          request.send_header('Content-type', 'text/javascript')
        await zendHeaders(request)
        request.wfile.write(resBody)
        res.connection.close()
        return rtrn
      try:
        print(len(request.headers.get('Bot-Protection',"")))
        if len(request.headers.get('Bot-Protection',"")) > 0:
          pass
        else:
          #pass
         # print('send_response')
          await zsendResponse(request,200)
         # print('send_header')
          request.send_header('Content-type', 'text/html')
         # print('end_headers')
          await zendHeaders(request)
         # print('wfile.write')
          request.wfile.write(bytes('<meta http-equiv="refresh" content="0; url=https://python.patrickring.net/"><script>location.replace("https://python.patrickring.net/");/script>', 'utf-8'))
         # print('return')
          return rtrn
      except:
        print("Here")
      hostFirst = str(at(globalThis.hostTargetList,[0]))
      if (at(request.headers,['Referer'])):
        referer = str(at(request.headers,['Referer']))
        if ("hostname=" in referer):
          hostFirst = str(at(str(at(str(at(str(referer).split("hostname="),[1])).split('&'),[0])).split('#'),[0]))
      if ("hostname=" in request.path):
        hostFirst = str(at(str(at(str(at(str(request.path).split("hostname="),[1])).split('&'),[0])).split('#'),[0]))
      if hostFirst == request.localhost:
        hostFirst = str(at(globalThis.hostTargetList,[0]))
      request.path = str(stripHostParam(request.path))
      request.hostTarget = hostFirst
      response = await zfetchResponse(request, request.hostTarget)
      lastHost = hostFirst
      if hostFirst not in [
          'packaging.python.org', 'packaging-python-org.weblet.repl.co',
          'packaging-python-org.vercel.app','docs.python.org', 'docs-python-org.weblet.repl.co',
        'docs-python-org.vercel.app'
      ]:
        for hostTarget in globalThis.hostTargetList:
          if response.status == 304:
            requestPath = str(request.path)
            request.path = bustCache(request.path)
            request.hostTarget = lastHost
            response = await zfetchResponse(request, request.hostTarget)
            request.path = requestPath
            if response.status < 200:
              break
          lastHost = hostTarget
          if response.status < 300:
            break
          for header in response.getheaders():
            if 'ocation' in str(at(header,[0])):
              redirectHost = str(at(str(at(header,[1])).split('/'),[2]))
              requestPath = str(request.path)
              request.path = str(at(str(at(header,[1])).split(redirectHost),[1]))
              request.hostTarget = redirectHost
              response = await zfetchResponse(request, request.hostTarget)
              request.path = requestPath
              if response.status < 300:
                break
          if response.status > 299:
            request.hostTarget = hostTarget
            response = await zfetchResponse(request, request.hostTarget)
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
          contentType = str(at(header,[1]))
        if header[0] == 'Content-Encoding':
          contentEncoding = str(at(header,[1]))
        if header[0] == 'Content-Length':
          contentLength = int(at(header,[1]))
        if 'ecurity' in str(at(header,[0])):
          continue
        if 'olicy' in str(at(header,[0])):
          continue
        try:
          reheader=str(at(header,[1])).replace(request.hostTarget,request.localhost,1)
          if at(header,[0]) == 'Location':
            char = '?'
            if('?' in reheader):
              char='&'
              if 'hostname=' not in reheader:
                reheader=str(at(reheader.split('#'),[0]))+char+'hostname='+str(request.hostTarget)
          request.send_header(str(at(header,[0])),reheader)
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
        ct = 'text/html'
        code = 200
        writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/\x03\x04'
        if '.css' in request.path:
          ct = 'text/css'
          code = 200
          writeEnd = b'\x03\x04'
        if '.js' in request.path:
          ct = 'text/javascript'
          code = 200
          writeEnd = b'\x03\x04'
        request.send_response(code)
        request.send_header('Content-type', ct)
        await endHeaders(request)
        rtrn = await writeResponseBody(request, writeEnd)
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
