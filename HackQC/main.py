import json
import math
from random import randint

class coordonnee(object):
    x = 0
    y = 0


class route(object):
    road = list()
    scoreAtletique = 0.00
    scoreDistance = 0.00
    scoreSecurite = 0.00


def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))

def getReversePosition(points, coor):
    if(points[0] == coor):
        return points[len(points) - 1]
    else:
        return points[0]

def trouverIntersection(data, listeCoor, coor):
    coorAX = coor[0]
    coorAY = coor[1]
    for geometry in data['features']:
        points = (geometry['geometry']['coordinates'])
        # print(points[len(points) - 1])
        for point in points:
            coorX = point[0]
            coorY = point[1]
            if (coorX == coorAX and coorY == coorAY):
                listeCoor.append(getReversePosition(points, point))



from pprint import pprint
jsonfile = 'C:\\Users\\USER\\PycharmProjects\\HackQC\\geobase.geojson' # path to your json file
with open(jsonfile) as data_file:
    data = json.load(data_file)
#pprint(data['features'][0]['geometry']['coordinates'][0])

debut = coordonnee()
fin = coordonnee()
debut.x = -73.5841054355436
debut.y = 45.5302242959115
fin.x = -73.6751080554656
fin.y = 45.5093888210768

distanceInitiale = distance(debut.x,debut.y,fin.x,fin.y)
#print(distanceInitiale)

startSegment = coordonnee()
endSegment = coordonnee()
for geometry in data['features']:
    points = (geometry['geometry']['coordinates'])
    #print(points[len(points) - 1])
    for point in points:
        coorX = point[0]
        coorY = point[1]
        if(coorX == debut.x and coorY == debut.y):
            startSegment = geometry['geometry']['coordinates']
        if (coorX == fin.x and coorY == fin.y):
            endSegment = geometry['geometry']['coordinates']
#print(startSegment)
#print(endSegment)

sortie = 1
lastUsedSegment = startSegment[len(startSegment) - 1]
destinationSegment = endSegment[len(endSegment) - 1]
routeList = []
route = []
lastSegmentPointList = list()
currentSegment = lastUsedSegment

i = 16
j = 1

while(j<=16):
    for num1 in range(0,j,1):
        lastSegmentPointList = list()
        trouverIntersection(data, lastSegmentPointList, lastUsedSegment)
        distanceMinimale = 100000.00
        #pprint(lastSegmentPointList)
        for point in lastSegmentPointList:
            currentDistance = distance(point[0], point[1], destinationSegment[0], destinationSegment[1])
            currentSegment = lastSegmentPointList[0]
            if ((currentDistance < distanceMinimale) and (lastUsedSegment != currentSegment) and (len(lastSegmentPointList)) > 1):
                distanceMinimale = currentDistance;
                currentSegment = point

        for num in range(0,i):
            if(i==16):
                routeList.append(currentSegment)
            else:
                routeList[num].append(currentSegment)


    i = int(i/2)
    j = j*2
    lastUsedSegment = currentSegment
pprint(routeList)



