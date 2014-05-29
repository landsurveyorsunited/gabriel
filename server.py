#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys
import json
import quickhttp
import esutils
import urllib
import md5

http = quickhttp.quickhttp()

es_config = esutils.get_config()

port = 8888
if len(sys.argv) > 1:
	port = int(sys.argv[1])

class ImportIoCrawlerHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		try:
			json_data = json.loads(data)
			if len(json_data["results"]) < 1:
				self.send_response(200)
				self.end_headers()
				return
			for position, index_data in enumerate(json_data["results"]):
				index_data = json_data["results"][0]
				index_data["_hash"] = md5.new("%i_%s" % (position, json_data["pageUrl"])).hexdigest()
				index_data["_url"] = json_data["pageUrl"]
				index_data["_idx"] = position
				http.execute("POST", "%s/%s/%s" % (esutils.get_es_endpoint(), es_config["index"], es_config["object"]), index_data, es_config["auth"]["credentials"]["username"], es_config["auth"]["credentials"]["password"])
			self.send_response(200);
			self.end_headers()
		except Exception as e:
			print "Unable to process: %s; %s" % (data, e)
			self.send_response(500)
			self.end_headers()

def main():
	try:
		server = HTTPServer(('', port), ImportIoCrawlerHandler)
		print "Server started on port %i" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "Server shutting down"
		server.socket.close()

if __name__ == '__main__':
	main()
