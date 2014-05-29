#!/usr/bin/python

import urllib2
import base64
import json

class quickhttp:

	def __init__(self):
		self.opener = urllib2.build_opener()

	def execute(self, method, url, content, username, password):
		request = urllib2.Request(url)
		request.add_data(json.dumps(content))
		request.add_header("Content-Type", "application/json;charset=UTF-8")
		request.get_method = lambda: method
		if username or password:
			base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string)

		res = self.opener.open(request)
		data = res.read()
		if len(data) > 0 and data[0] == "{":
			data = json.loads(data)
		return data