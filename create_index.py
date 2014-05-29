#!/usr/bin/python

import json
import quickhttp
import esutils

http = quickhttp.quickhttp()

es_config = esutils.get_config()

with open("index_mapping.json", "r") as mapping_file:
	mapping_data = json.loads(mapping_file.read())
	mapping_request = { "mappings": { } }
	mapping_request["mappings"][es_config["object"]] = mapping_data
	http.execute("PUT", "%s/%s" % (esutils.get_es_endpoint(), es_config["index"]), mapping_request, es_config["auth"]["credentials"]["username"], es_config["auth"]["credentials"]["password"])
