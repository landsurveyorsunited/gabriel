#!/usr/bin/python

import json

def get_config():
	with open("es.json", "r") as config_file:
		return json.loads(config_file.read())

def get_es_endpoint():
	config = get_config()
	protocol = "https" if config["secure"] else "http"
	return "%s://%s" % (protocol, config["host"])