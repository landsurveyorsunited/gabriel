#!/usr/bin/python

import json
import quickhttp
import esutils

http = quickhttp.quickhttp()

es_config = esutils.get_config()

http.execute("DELETE", "%s/%s" % (esutils.get_es_endpoint(), es_config["index"]), False, es_config["auth"]["credentials"]["username"], es_config["auth"]["credentials"]["password"])
