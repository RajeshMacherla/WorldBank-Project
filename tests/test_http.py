import io
import json
import tempfile
import unittest
from pathlib import Path
from app import core, server
class MemorySocket:
 def __init__(self,raw):self.input=io.BytesIO(raw);self.output=bytearray()
 def makefile(self,*args):return self.input
 def sendall(self,data):self.output.extend(data)
class HTTPTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=core.DATA;core.DATA=Path(self.tmp.name)
 def tearDown(self):core.DATA=self.old;self.tmp.cleanup()
 def request(self,path='/',payload=None,token=None,host='127.0.0.1'):
  body=json.dumps(payload).encode() if payload is not None else b''
  headers=[f'{"POST" if payload is not None else "GET"} {path} HTTP/1.0',f'Host: {host}',f'Content-Length: {len(body)}']
  if token:headers.append('X-App-Token: '+token)
  sock=MemorySocket(('\r\n'.join(headers)+'\r\n\r\n').encode()+body)
  server.Handler(sock,('127.0.0.1',1234),None)
  head,data=bytes(sock.output).split(b'\r\n\r\n',1)
  return int(head.split()[1]),data
 def test_health_and_ui(self):
  status,data=self.request('/health');self.assertEqual(status,200);self.assertTrue(json.loads(data)['local_only'])
  status,data=self.request();self.assertIn(server.TOKEN.encode(),data);self.assertNotIn(b'__TOKEN__',data)
 def test_mutation_requires_token(self):self.assertEqual(self.request('/api/run',{})[0],403)
 def test_review_end_to_end(self):
  payload={'question':'competitive bidding','request':{'amount':75000,'vendor_id':'V002'},'session':'http-test'}
  status,data=self.request('/api/run',payload,server.TOKEN);self.assertEqual(status,200);result=json.loads(data)
  self.assertTrue(result['review_required'])
  status,data=self.request('/api/review',{'run_id':result['id'],'status':'needs_follow_up','note':'Synthetic review verified'},server.TOKEN)
  self.assertEqual(status,200);self.assertTrue(json.loads(data)['saved'])
 def test_dns_rebinding_host_rejected(self):self.assertEqual(self.request('/health',host='untrusted.example')[0],403)
