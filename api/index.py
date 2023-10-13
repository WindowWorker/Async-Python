from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.promises import *
import sys,threading



def handle_exception(exc_type, exc_value, exc_traceback):
  print("Unhandled Exception")
sys.excepthook = handle_exception

run_old = threading.Thread.run
def run(*args, **kwargs):
    try:
        run_old(*args, **kwargs)
    except:
        handle_exception()
threading.Thread.run = run



#async def AsyncHTTPServer():
hostTargetList = ['www.python.org',
                  'packaging-python-org.weblet.repl.co',
                  #'packaging.python.org',
           #      'docs.python.org',
                  'docspythonorg.weblet.repl.co',
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
                 'pyfound.blogspot.com']
hostShortCircuit = ['planetpython.org','docspythonorg.weblet.repl.co']
#astart() starts unawaited async tasks declared at this level

async def sendResponse(request,status):
  return request.send_response(status) 
async def endHeaders(request):
  return request.end_headers()
async def readResponseBody(res,length):
  try:
    bdy = bytearray(length + 16)
    res.readinto(bdy)
    return bdy
  except:
    try:
      return res.read()
    except:
      return b'';
def killRequest(request):
  if 'kill' in request.kill:
    none()
def reboot():
  #httpd.shutdown()
  httpd.serve_forever()
async def atimeout(request,seconds):
    await asyncio.sleep(seconds)
    request.isTimedOut = true
    ct = 'text/html'
    code = 408
    writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/';
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
    request.send_header('Content-type',ct )
    await endHeaders(request)
    rtrn = await  writeResponseBody(request,writeEnd)
    if 'planetpython' in request.headers['Host']:
      killRequest(request)
    await AQ(streamDetach,[request.wfile])
    if request.headers['Host'] in hostShortCircuit:
      killRequest(request)
    return rtrn
async def writeResponseBody(req,body):
  await promise(atimeout,[req,1])
  await astart()
  try:
    #print('Ending '+req.headers['Host']+req.path)
    return req.wfile.write(body)
  except:
    return
async def readRequest(req,length):
  if length < 5:
    return b''
  return req.rfile.read(length)
async def connectClient(host):
  return http.client.HTTPSConnection(host)
async def connectRequest(connection, requestCommand, requestPath, requestBody, requestHeaders):
  return connection.request(requestCommand, requestPath, body=requestBody, headers=requestHeaders)
async def connectResponse(connection):
  return connection.getresponse()
async def connectClose(connection):
  connection.close()
async def streamDetach(stream):
  stream.detach()
async def readBody(req,host):
  reqBody = None
  requestBodyLength = req.headers['Content-Length']
  ##print('Request Content-Length: '+requestBodyLength)
  if (req.rfile.readable() and requestBodyLength):  
    reqBody = await readRequest(req,int(requestBodyLength));
    if len(reqBody) < 5:
      reqBody = None
  return reqBody
def bustCache(path):
  hash=''
  if '#' in path:
    hash = '#'+path.split('#')[1]
  char = '?'
  if '?' in path:
    char = '&'
  return path.split('#')[0]+char+'bustcache='+str(time.time()).replace('.','');
def stripHostParam(path):
  if '?hostname=' in path:
    if '&' in path:
      hostparts = path.split('?hostname=')
      params = hostparts[1].split('&')
      params[0] = ''
      params = '&'.join(params).split()
      params[0]='?'
      path = hostparts[0] + ''.join(params)
    elif '#' in path:
      hostparts = path.split('?hostname=')
      hash = hostparts[1].split('#')
      hash[0]=''
      path = hostparts[0] + '#'.join(hash);
  elif '&hostname=' in path:
    hostparts = path.split('&hostname=')
    if '&' in hostparts[1]:
      params = hostparts[1].split('&')
      params[0]=''
      path = hostparts[0] + '&'.join(params)
    elif '#' in path:
      hostparts = path.split('&hostname=')
      hash = hostparts[1].split('#')
      hash[0]=''
      path = hostparts[0] + '#'.join(hash);
  return path
httpd = {}

def delete(obj,attr):
  try:
    del obj[attr]
    return obj
  except:
    return obj
async def fetchResponse(req,host):
  connection = {}
  try:
    connectionPromise = await promise(connectClient,[host])
    reqBodyPromise = await promise(readBody,[req,host])
    await astart()
    localhost = req.headers['Host']
    reqHeaders = {}
    for header in req.headers:
      reqHeaders[header] = req.headers[header].replace(localhost,host)
    reqHeaders['Localhost']=localhost
    reqHeaders['Cache-Control'] = 'max-age=';
    reqHeaders['Expires'] = 'Tue, 19 Jan 2000 03:14:07 GMT'
    delete(reqHeaders,'Etag')
    delete(reqHeaders,'Expect-Ct')
    delete(reqHeaders,'Cookie')
    reqBody = await reqBodyPromise
    connection = await connectionPromise
    await connectRequest(connection,req.command,req.path,reqBody,reqHeaders)
    #print(host)
    #print(req.path)
    res = await connectResponse(connection)
    #print(res.status) 
    res.connection = connection
    return res
  except:
    res = http.client.HttpResponse(status=500)
    res.connection = connection
    return res

class handler(BaseHTTPRequestHandler):  
  async def do_METHOD(request,data):
    rtrn = {}
    request.isTimedOut=false
    hostFirst = '';
    try:  
      request.timeout=5
      #print('Starting '+request.headers['Host']+request.path)
      await promise(atimeout,[request,2])
      await astart()
      if 'jquery.js' in request.path:
          request.path='/_static/jquery.js'
      if(request.path.split('?')[0] in ['/injects.js','/injects.css','/_static/jquery.js','/static/js/warehouse.c431b9ad.js','/plugins/discourse-client-performance/javascripts/discourse-client-performance.js','/wiki/common/js/common.js']):
        with open('static'+request.path.split('?')[0], 'r') as f:
            content = f.read()
        request.send_response(200)
        request.send_header('Content-type', 'text/javascript')
        request.end_headers()
        rtrn = await writeResponseBody(request,bytes(content, 'utf8'))    
        #await AQ(connectClose,[response.connection])
        #await AQ(streamDetach,[request.wfile])
        return rtrn
      localhost = request.headers['Host']
      hostFirst = hostTargetList[0]
      if(request.headers['Referer']):
        referer = request.headers['Referer']
        #print('Referer '+referer)
        if("hostname=" in referer):
          hostFirst = referer.split("hostname=")[1].split('&')[0].split('#')[0]
      if("hostname=" in request.path):
        hostFirst = request.path.split("hostname=")[1].split('&')[0].split('#')[0]
      request.path = stripHostParam(request.path)
      response = await fetchResponse(request,hostFirst)
      print(hostFirst)
     # #print(response.status)
      lastHost = hostFirst
   #   #print("retry loop")
      if hostFirst not in ['packaging.python.org','packaging-python-org.weblet.repl.co']:
        for hostTarget in hostTargetList:
          if response.status == 304:
            requestPath = request.path
            request.path = bustCache(request.path)
            response = await fetchResponse(request,lastHost)
            request.path=requestPath
           # #print(response.status)
            if response.status < 200:
              break
          lastHost = hostTarget
          if response.status < 300:
            break
          for header in response.getheaders():
            if 'ocation' in header[0]:
              redirectHost=header[1].split('/')[2]
              requestPath=request.path
              request.path=header[1].split(redirectHost)[1]
              response = await fetchResponse(request,redirectHost)
              ##print(response.status)
              request.path=requestPath
              if response.status < 300:
                break
          if response.status > 299:
            response = await fetchResponse(request,hostTarget)
        #  #print(response.status)
       # #print("send res prom")
      sendResponsePromise = await promise(sendResponse,[request,response.status])
      await astart();

      headers = response.getheaders()
      await sendResponsePromise
      contentType=''
      contentEncoding=''
      contentLength=2000000
     # print("header loop")
      for header in headers:
        if header[0]=='Transfer-Encoding':
          continue
        if header[0]=='Connection':
          continue

        #print('Header: '+header[0]+':'+header[1])
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
          request.send_header(header[0], header[1])
        except:
          none()
      print('Response Content-Length: '+str(contentLength))
      resBodyPromise = await promise(readResponseBody,[response,contentLength])
      await astart()
      await endHeaders(request)
      resBody = await resBodyPromise
      if 'text/html' in contentType:
        if len(contentEncoding) == 0:
          resBody = str(resBody,encoding='utf-8').replace('</head>','<script src="/injects.js"></script></head>')
         # #print(resBody)
          resBody=bytes(resBody, 'utf-8')
      if 'javascript' in contentType:
        if len(contentEncoding) == 0:
          resBody = bytes((' import("/injects.js"); ' + str(resBody,encoding='utf-8')), 'utf-8')
      rtrn = await writeResponseBody(request,resBody)
      #await AQ(connectClose,[response.connection])
      #await AQ(streamDetach,[request.wfile])
      return rtrn
    except:
      if hostFirst != 'packaging.python.org':
        if request.isTimedOut == true:
          killRequest(request)
        ct = 'text/html'
        code = 200 
        writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/';
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
        request.send_header('Content-type',ct )
        await endHeaders(request)
        rtrn = await writeResponseBody(request,writeEnd)
       # await AQ(streamDetach,[request.wfile])
        #reboot()
        if request.headers['Host'] in hostShortCircuit:
          killRequest(request)
    if hostFirst == 'packaging.python.org':
      request.wfile.flush()
      request.wfile.close()
    return rtrn   
  async def done_OPTIONS(request,data):
    request.send_response(200)
    await endHeaders(request)
    return await writeResponseBody(request,b'*')
  def do_GET(request):
    asyncio.run(request.do_METHOD(request))
  def do_OPTIONS(request):
    asyncio.run(request.done_OPTIONS(request))
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




