import json
import math, numpy

from random import randint

class coordonnee(object):
    x = 0
    y = 0

    def __init(self, x, y):
        self.x = x
        self.y = y

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

def addMissingPoints(data, liste, coorDebut, coorFin):
    coorDX = coorDebut[0]
    coorDY = coorDebut[1]
    coorFX = coorFin[0]
    coorFY = coorFin[1]
    for geometry in data['features']:
        points = (geometry['geometry']['coordinates'])
        same = 0
        for point in points:
            coorX = point[0]
            coorY = point[1]
            if (coorX == coorDX and coorY == coorDY):
                same += 1
            if (coorX == coorFX and coorY == coorFY):
                same += 1
        if (same > 1):
            for num in range(1, len(points)-2):
                liste.append(points[num])


def addMissingSegments(data, liste, coorDebut, coorFin):
    DsegmentList = list()
    LsegmentList = list()
    coorDX = coorDebut[0]
    coorDY = coorDebut[1]
    coorFX = coorFin[0]
    coorFY = coorFin[1]
    for geometry in data['features']:
        points = (geometry['geometry']['coordinates'])
        for point in points:
            coorX = point[0]
            coorY = point[1]
            if (coorX == coorDX and coorY == coorDY):
                DsegmentList.append(points)
            if (coorX == coorFX and coorY == coorFY):
                LsegmentList.append(points)

    if(DsegmentList != [] and LsegmentList != []):
        for Dsegment in DsegmentList:
            for Dpoints in DsegmentList:
                for Dpoint in Dpoints:
                    for Lsegment in LsegmentList:
                        for Lpoints in LsegmentList:
                            for Lpoint in Lpoints:
                                #if Dpoint[0] == Lpoint[0] and Dpoint[1] == Lpoint[1]:
                                print(Lpoint[0])
                                if Dpoint[1] == Lpoint[1]:
                                    print("You won")
                                    for DsamePoint in DsegmentList:
                                        liste.append(DsamePoint)
                                    for LsamePoint in LsegmentList:
                                        liste.append(LsamePoint)


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

debut = coordonnee()
fin = coordonnee()
debut.x = -73.6398556612252
debut.y = 45.5952415912627
fin.x = -73.7091820442561
fin.y = 45.4450198040751

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

sortie = 1
lastUsedSegment = startSegment[len(startSegment) - 1]
destinationSegment = endSegment[len(endSegment) - 1]
routeList = []
lastSegmentPointList = list()
currentSegment = lastUsedSegment
closestSegment = lastUsedSegment

i = 16
j = 1
compteur = 0

for initNum in range (0, 16, 1):
    routeList.append(list())

while(j<=16):

    rangeMin = 0
    rangeMax = i

    for num1 in range(0,j,1):
        lastSegmentPointList = list()
        trouverIntersection(data, lastSegmentPointList, lastUsedSegment)
        distanceMinimale = 100000.00
        for point in lastSegmentPointList:
            currentDistance = distance(point[0], point[1], destinationSegment[0], destinationSegment[1])
            currentSegment = lastSegmentPointList[0]
            if ((currentDistance < distanceMinimale) and (lastUsedSegment != currentSegment) and (len(lastSegmentPointList)) > 1):
                distanceMinimale = currentDistance;
                currentSegment = point
                closestSegment = currentSegment
        lastUsedSegment = closestSegment

        for num in range(rangeMin, rangeMax):
            tempList = routeList[num]
            if(len(tempList) > 2):
                addMissingPoints(data, tempList, tempList[len(tempList)-1], closestSegment)
                addMissingSegments(data, tempList, tempList[len(tempList)-1], closestSegment)
            tempList.append(closestSegment)
            routeList[num] = tempList
            tempList = list()
        rangeMin += i
        rangeMax += i
    i = int(i/2)
    j = j*2

print(compteur)
#pprint(routeList)



