import json

import requests

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession

API = 'https://hack.halcom.com/api/v1/accounts'

HEADERS = {'apiKey': 'ddc0a89a-cd5a-437c-a089-4cf47ee32a2d'}

class BackendSession(ApplicationSession):

	@inlineCallbacks
	def onJoin(self, details):
		print("Backend session joined: {}".format(details))

		def get_account():
			return json.loads(requests.get(API, headers=HEADERS).content)[0]
		
		def get_details(account_id):
			return json.loads(requests.get('%s/%s' % (API, account_id), headers=HEADERS).content)[0]
		
		def get_transactions(account_id):
			return json.loads(requests.get('%s/%s/transactions' % (API, account_id), headers=HEADERS).content)	

		yield self.register(get_account, 'com.admin.get_account')
		yield self.register(get_details, 'com.admin.get_details')
		yield self.register(get_transactions, 'com.admin.get_transactions')
		
		while True:
			yield self.publish('com.admin.news', get_account())
			yield sleep(5)
		
