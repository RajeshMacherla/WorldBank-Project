"""Loopback-only HTTP server. No cloud credentials or third-party Python packages."""
import argparse
import json
import logging
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from app.core import ROOT, run, reviews, resolve_review, history
TOKEN=secrets.token_urlsafe(32)
LOCK=threading.Lock()
class Handler(BaseHTTPRequestHandler):
 def log_message(self,fmt,*args):pass  # Avoid recording query strings or submitted text.
 def send(self,status,payload,kind='application/json'):
  body=payload.encode() if isinstance(payload,str) else json.dumps(payload).encode()
  self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)))
  self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY')
  self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
 def allowed(self):
  host=self.headers.get('Host','').split(':')[0]
  return host in ('localhost','127.0.0.1')
 def do_GET(self):
  if not self.allowed():return self.send(403,{'error':'Invalid host'})
  route=urlparse(self.path)
  if route.path=='/':return self.send(200,(ROOT/'app/static/index.html').read_text().replace('__TOKEN__',TOKEN),'text/html; charset=utf-8')
  if route.path=='/health':return self.send(200,{'status':'ok','local_only':True})
  if route.path=='/api/reviews':return self.send(200,reviews())
  if route.path=='/api/history':return self.send(200,history(parse_qs(route.query).get('session',['default'])[0]))
  self.send(404,{'error':'Not found'})
 def do_POST(self):
  if not self.allowed() or self.headers.get('X-App-Token')!=TOKEN:return self.send(403,{'error':'Reload the local app to obtain a valid token'})
  if not LOCK.acquire(blocking=False):return self.send(429,{'error':'A review is running. Please wait.'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=32768:return self.send(413,{'error':'Request too large or empty'})
   payload=json.loads(self.rfile.read(length))
   if not isinstance(payload,dict):raise ValueError('Expected JSON object')
   if self.path=='/api/run':return self.send(200,run(**payload))
   if self.path=='/api/review':
    resolve_review(**payload);return self.send(200,{'saved':True})
   self.send(404,{'error':'Not found'})
  except (ValueError,TypeError) as exc:self.send(400,{'error':str(exc)})
  except RuntimeError as exc:self.send(503,{'error':str(exc)})
  except Exception:
   logging.exception('Request failed')
   self.send(500,{'error':'Internal error. Check terminal diagnostics.'})
  finally:LOCK.release()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);args=parser.parse_args()
 print(f'Policy Risk Assistant: http://127.0.0.1:{args.port} — Ctrl+C to stop')
 ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
if __name__=='__main__':main()
