import unittest
from app.agents import collect, AgentError

def message(calls):
 return {'message':{'content':'','tool_calls':[{'function':{'name':n,'arguments':a}} for n,a in calls]}}
class AgentTests(unittest.TestCase):
 def invoke(self, responses, request=None):
  iterator=iter(responses);self.events=[];self.checked=[]
  return collect('bidding',request,'fake',lambda *a:next(iterator,message([])),
   lambda q:[{'chunk_id':'p:1','text':'evidence'}],
   lambda r:self.checked.append(r) or [],lambda t:True,
   lambda node,**kw:self.events.append((node,kw)))
 def test_tools_then_finish(self):
  request={'amount':75000}
  evidence,findings=self.invoke([message([('search_policy',{'query':'bidding'}),('check_procurement',{})]),message([])],request)
  self.assertEqual(evidence[0]['chunk_id'],'p:1');self.assertEqual(self.checked,[request])
  self.assertEqual(self.events[-1][0],'agent_complete')
 def test_unknown_tool_denied(self):
  with self.assertRaises(AgentError):self.invoke([message([('run_shell',{'cmd':'bad'})])])
 def test_model_cannot_change_amount(self):
  with self.assertRaises(AgentError):self.invoke([message([('check_procurement',{'amount':1})])],{'amount':75000})
 def test_missing_required_check_escalates(self):
  with self.assertRaises(AgentError):self.invoke([message([('search_policy',{'query':'bidding'})]),message([])],{'amount':75000})
 def test_infinite_tool_loop_bounded(self):
  with self.assertRaises(AgentError):self.invoke([message([('search_policy',{'query':'bidding'})])]*3,{'amount':75000})
 def test_no_evidence_escalates(self):
  with self.assertRaises(AgentError):self.invoke([message([])])

 def test_recovers_when_model_stops_after_procurement_check(self):
  evidence,_=self.invoke([message([('check_procurement',{})]),message([]),message([('search_policy',{'query':'bidding'})])],{'amount':75000})
  self.assertTrue(evidence)
  retries=[e for e in self.events if e[0]=='agent_retry']
  self.assertEqual(retries[0][1]['missing_tools'],['search_policy'])
 def test_no_final_llm_round_needed_after_required_tools(self):
  evidence,_=self.invoke([message([('search_policy',{'query':'bidding'}),('check_procurement',{})])],{'amount':75000})
  self.assertTrue(evidence)
  self.assertEqual(len([e for e in self.events if e[0]=='agent_tool']),2)
