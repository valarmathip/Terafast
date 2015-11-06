import pycurl
from StringIO import StringIO
import json
from urllib import urlencode


class flowEngine():

    def __init__(self,sdnIp,sdnPort):
        self.sdnIp = sdnIp
        self.sdnPort = sdnPort
        self.url = 'http://' + sdnIp +':'+ sdnPort + '/'
        self.curlObj =pycurl.Curl()
# get a dictionary of switch IP to dpid
        self.dpidList = self.getSwitchIds();

    def getSwitchIds(self):

        print "get the switch id"
        buffer = StringIO()
        url_id = self.url + 'stats/switches'
        self.curlObj.setopt(pycurl.URL, url_id)
        self.curlObj.setopt(pycurl.WRITEFUNCTION, buffer.write)
        self.curlObj.perform()
        body = buffer.getvalue()
        #value = json.loads(body)
        return json.loads(body)[0]

    def getSwitchList(self):
        return self.dpidList

    def flowAdd(self,flowDict):
        print "inside flowpush"
        push_url = self.url +'stats/flowentry/add'
        self.curlObj.setopt(pycurl.URL, push_url)
		#form the data from flowdict argument
		#post_data = GetPostDataFromFlowDictArgument(flowDict)
        post_data= '{"dpid": "244319785614920", "priority": "101", "match": {"in_port":"1","ipv4_src":"10.6.6.111","eth_type":"2048"}, "actions": [{"type":"OUTPUT","port":"2"}]}'
	
        dataDict = eval(post_data)
        self.curlObj.setopt(pycurl.HTTPHEADER, ["Content-Type: application/x-www-form-urlencoded"])
        self.curlObj.setopt(pycurl.POST, 1)
        self.curlObj.setopt(self.curlObj.POSTFIELDS, post_data);
        result = self.curlObj.perform()

    def flowDelete(self, flowDict):
        pass

    def flowModify(self, flowDict):
        pass

    def getFlows(self):
        pass

    def getFlow(self, flowId):
        pass

    def deleteAllFlows():
        pass
    

f = flowEngine('10.6.0.190','8080')
switchid = f.getSwitchIds()
print "switchid:", switchid
f.flowAdd(switchid)


