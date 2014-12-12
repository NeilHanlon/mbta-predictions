from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from jinja2.ext import loopcontrols
from jinja2 import Environment

import pprint
import xml.etree.ElementTree as ET
import json
import urllib2

conf_file = open("conf.json")
conf = json.load(conf_file)
conf_file.close()

locations = conf["locations"]

pp = pprint.PrettyPrinter(indent = 4)

app = Flask(__name__)

def create_app(configfile=None):

	app = Flask(__name__)
	app.jinja_env.add_extension('jinja2.ext.loopcontrols')
	Bootstrap(app)
	
	@app.context_processor
	def utility_processor():
		def format_time(unit):
			return u'{:.2f}'.format(unit)
		def hasany(item, needle, iterable):
			return any(d[item] == needle for d in iterable)
		def hasnext(item,item2,needle,iterable):
			return next((home[item] for home in iterable if home[item2] == needle), None)
		return dict(format_time=format_time,hasany=hasany,hasnext=hasnext)
	
	@app.route("/")
	def index():
		return render_template('index.html',data=get(), location=locations["home"], directions=["inbound","outbound"])
	
	return app


def get():
	baseUrl = conf["baseurl"]
	service = conf["a"]

	routes = conf["routes"]


	routelist = []

	for route in routes:
		stopId = route["stopId"]
		routeTitles = route["routeTitles"]

		req = urllib2.Request(str(baseUrl) + "&a=" + str(service) + "&stopId=" + str(stopId))
		response = urllib2.urlopen(req)

		tree = ET.parse(response)
		root = tree.getroot()

		for predictions in root.iter('predictions'):
			title = ""
			seconds = 0
			routeTitle = predictions.attrib['routeTitle']
			pp.pprint("routeTitle: "+routeTitle)
			if routeTitle not in routeTitles: 
				pass
			else:
				busses = []
				seconds = []
				stopTitle = predictions.attrib["stopTitle"]
				pp.pprint("stop Title: " +stopTitle)
				for prediction in predictions.iter('direction'):
					title = prediction.attrib['title']
					for direction in prediction.iter('prediction'):
						seconds.append(int(direction.attrib['seconds']))
					busses += [{"busNumber": routeTitle, "route": title,"seconds": seconds}]
				if seconds:
					routelist += [{"stopId": stopId,"stopTitle": stopTitle,  "busses": busses}]
	with open('data.json','w') as out:
		json.dump(routelist,out)
	return routelist

if __name__ == "__main__":
    create_app().run(debug = True, host='0.0.0.0')
