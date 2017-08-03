import requests
from matplotlib import pyplot
import numpy as np

def readCoordinates(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	file.close()
	allCoordinates = []
	for line in lines:
		coordinates = [float(coordinate) for coordinate in line.split()]
		allCoordinates.append(coordinates)
	return allCoordinates

def createPath(allCoordinates):
	path = ""
	for coordinates in allCoordinates:
		path += ','.join(map(str, coordinates))
		path += "|"
	path = path[:-1]
	return path

def getAllResCoordinates(snappedPoints):
	allResCoordinates = []
	for obj in snappedPoints:
		resCoordinates = []
		resCoordinates.append(float("%.7f" % float(obj["location"]["latitude"])))
		resCoordinates.append(float("%.7f" % float(obj["location"]["longitude"])))
		allResCoordinates.append(resCoordinates)
	return allResCoordinates

def normalizePoints(gridPoints, scale):
	xGridPoints = [point[0] for point in gridPoints]
	yGridPoints = [point[1] for point in gridPoints]
	minP = [min(xGridPoints), min(yGridPoints)]
	maxP = [max(xGridPoints), max(yGridPoints)]
	xDiff, yDiff = float("%.7f" % (maxP[0]-minP[0])), float("%.7f" % (maxP[1]-minP[1]))
	ratio = float("%.7f" % (yDiff/xDiff))
	normalizedPoints = []
	for point in gridPoints:
		normalizedPoint = [float("%.7f" % ((point[0]-minP[0])/xDiff*scale)), float("%.7f" % ((point[1]-minP[1])/yDiff*scale*ratio))]
		normalizedPoints.append(normalizedPoint)
	return normalizedPoints

allCoordinates = readCoordinates("coordinates.txt")
xAllCoordinates = [point[0] for point in allCoordinates]
yAllCoordinates = [point[1] for point in allCoordinates]
minP = [min(xAllCoordinates), min(yAllCoordinates)]
maxP = [max(xAllCoordinates), max(yAllCoordinates)]
xDiff, yDiff = float("%.7f" % (maxP[0]-minP[0])), float("%.7f" % (maxP[1]-minP[1]))
allPoints = []
xAllPoints = []
yAllPoints = []
xlist = np.arange(minP[0], maxP[0]-xDiff/10, xDiff/10)
ylist = np.arange(minP[1], maxP[1]-yDiff/10, yDiff/10)
for x in xlist:
	for y in ylist:
		xAllPoints.append(float("%.7f" % x))
		yAllPoints.append(float("%.7f" % y))
		allPoints.append([float("%.7f" % x), float("%.7f" % y)])
baseUrl = "https://roads.googleapis.com/v1/snapToRoads?"
path = "path=" + createPath(allPoints)
interpolate = "&interpolate=true"
apiKey = "&key=[ Enter Your API key ]"
getUrl = baseUrl + path + interpolate + apiKey
res = requests.get(getUrl)
allResCoordinates = getAllResCoordinates(res.json()["snappedPoints"])
normalizedPoints = normalizePoints(allResCoordinates, 10)
xNormalizedPoints = [point[0] for point in normalizedPoints]
yNormalizedPoints = [point[1] for point in normalizedPoints]
pyplot.plot(yNormalizedPoints, xNormalizedPoints)
pyplot.axis([0, 25, 0, 25])
pyplot.show()