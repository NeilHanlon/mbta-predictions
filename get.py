import pprint
import xml.etree.ElementTree as ET
import json
import urllib2

pp = pprint.PrettyPrinter(indent = 4)

conf_file = open("conf.json")
conf = json.load(conf_file)
conf_file.close()
baseUrl = conf["baseurl"]
service = conf["a"]

routes = conf["routes"]


routelist = []

for route in routes:
	stopId = route["stopId"]
	routeTitles = route["routeTitles"]
	
	req = urllib2.Request(str(baseUrl) + "&a=" + str(service) + "&stopId=" + str(stopId))	
	response = urllib2.urlopen(req)
	#res = response.read()
	
	tree = ET.parse(response)
	root = tree.getroot()
	
	for predictions in root.iter('predictions'):
		title = ""
		seconds = 0
		routeTitle = predictions.attrib['routeTitle']
		pp.pprint(routeTitles)
		pp.pprint(routeTitle)
		pp.pprint(routeTitle not in routeTitles)
		if routeTitle not in routeTitles:
			pass
		else:
			for prediction in predictions.iter('direction'):
				title = prediction.attrib['title']
				for direction in prediction.iter('prediction'):
					seconds = direction.attrib['seconds']
		if seconds:
			routelist += [{ "stopId": stopId, "busses": {"busNumber": routeTitle, "route": title,"seconds": seconds}}]

with open('data.json','w') as out:
	json.dump(routelist,out)

