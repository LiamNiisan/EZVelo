import json
import math

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


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def getReversePosition(points, coor):
    if (points[0] == coor):
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
            for num in range(1, len(points) - 2):
                liste.append(points[num])


def addMissingSegments(data, liste, coorDebut, coorFin, isRecurcive):
    #print(coorDebut, coorFin)
    DsegmentList = list()
    LsegmentList = list()
    coorDX = coorDebut[0]
    coorDY = coorDebut[1]
    coorFX = coorFin[0]
    coorFY = coorFin[1]
    X = 0
    Y = 1
    for geometry in data['features']:
        points = (geometry['geometry']['coordinates'])
        for point in points:
            coorX = point[X]
            coorY = point[Y]
            if (coorX == coorDX and coorY == coorDY):
                DsegmentList.append(points)
            if (coorX == coorFX and coorY == coorFY):
                LsegmentList.append(points)

    nomatch = 0
    i = 0
    while(nomatch == 0 or i >= 5):
        if (DsegmentList != [] and LsegmentList != []):
            #print(DsegmentList)
            #print("----------------------")
            #print(LsegmentList)
            for Dsegment in DsegmentList:
                for Dpoints in Dsegment:
                    for Lsegment in LsegmentList:
                        for Lpoints in Lsegment:
                            if (Dpoints[0] == Lpoints[0]) and (Dpoints[1] == Lpoints[1]):
                                #print("You won")
                                nomatch = 1
                                for DsamePoint in DsegmentList:
                                    #for point in DsamePoint:
                                    liste.append(DsamePoint)
                                for LsamePoint in LsegmentList:
                                    #for point in reversed(LsamePoint):
                                    liste.append(LsamePoint)

        if(isRecurcive == 1):
            nomatch = 1
        i += 1
        if(isRecurcive == 0):

            closestDSegList = list()
            for CDPOoint in DsegmentList:
                closestDSegList.append(closestPoint(data, CDPOoint, coorFin))
            closestDSeg = closestPoint(data, closestDSegList, coorFin)

            closestLSegList = list()
            for CLPOoint in DsegmentList:
                closestLSegList.append(closestPoint(data, CLPOoint, coorDebut))
            closestLSeg = closestPoint(data, closestLSegList, coorDebut)

            tempList = list()

            recNomatch = addMissingSegments(data, tempList, closestDSeg, closestLSeg, 1)

            if(recNomatch == 1):
                nomatch = 1
                for DsamePoint in DsegmentList:
                    for point in DsamePoint:
                        liste.append(point)

                for midpoints in tempList:
                    for midpoint in midpoints:
                        liste.append(midpoint)

                for LsamePoint in LsegmentList:
                    for point in reversed(LsamePoint):
                        liste.append(point)



    return nomatch



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


def closestPoint(data, pointsList, point):
    closestSegment = pointsList[0]
    distanceMinimale = 100000.00
    for comparePoint in pointsList:
        currentDistance = distance(point[0], point[1], comparePoint[0], comparePoint[1])
        if currentDistance < distanceMinimale:
            distanceMinimale = currentDistance;
            closestSegment = comparePoint
    return closestSegment


from pprint import pprint

def main(departX, departY, finX, finY):

    jsonfile = 'C:\\Users\\USER\\PycharmProjects\\HackQC\\geobase.geojson'  # path to your json file
    with open(jsonfile) as data_file:
        data = json.load(data_file)

    debut = coordonnee()
    fin = coordonnee()
    if not departX:
        debut.x = -73.5717932176314
    else:
        debut.x = float(departX)
    if not departY:
        debut.y = 45.5148061021868
    else:
        debut.y = float(departY)
    if not finX:
        fin.x = -73.6603665191824
    else:
        fin.x = float(finX)
    if not finY:
        fin.y = 45.5692741805157
    else:
        fin.y = float(finY)

    distanceInitiale = distance(debut.x, debut.y, fin.x, fin.y)
    # print(distanceInitiale)

    startSegment = coordonnee()
    endSegment = coordonnee()
    for geometry in data['features']:
        points = (geometry['geometry']['coordinates'])
        # print(points[len(points) - 1])
        for point in points:
            coorX = point[0]
            coorY = point[1]
            if (coorX == debut.x and coorY == debut.y):
                startSegment = geometry['geometry']['coordinates']
            if (coorX == fin.x and coorY == fin.y):
                endSegment = geometry['geometry']['coordinates']

    lastUsedSegment = startSegment[len(startSegment) - 1]
    destinationSegment = endSegment[len(endSegment) - 1]
    routeList = []
    routeListChoisi = []
    lastSegmentPointList = list()
    currentSegment = lastUsedSegment
    closestSegment = lastUsedSegment

    i = 16
    j = 1

    for ini1 in range(0, 16):
        routeList.append(list())

    while (j <= 16):

        rangeMin = 0
        rangeMax = i

        for num1 in range(0, j, 1):
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
                if (len(tempList) > 2):
                    addMissingPoints(data, tempList, tempList[len(tempList) - 1], closestSegment)
                    #addMissingSegments(data, tempList, tempList[len(tempList) - 1], closestSegment, 0)
                tempList.append(closestSegment)
                routeList[num] = tempList
                tempList = list()
            rangeMin += i
            rangeMax += i
        i = int(i / 2)
        j = j * 2

    #pprint(routeList[0])
    """""
    nombreRoutes = int(distanceInitiale*10000)
    for ini1 in range(0, nombreRoutes):
        routeList.append(lastUsedSegment)
    
    for ini2 in range(0, nombreRoutes):
        routeListChoisi.append(lastUsedSegment)
    
    print(nombreRoutes)
    
    for routeNum in range(1,nombreRoutes):
        lastUsedSegment = startSegment[len(startSegment) - 1]
        for routeLimit in range(0,1+int(nombreRoutes/5000)):
            currentDistance = distance(lastUsedSegment[0], lastUsedSegment[1], fin.x, fin.y)
            segmentList = list()
            trouverIntersection(data, segmentList, lastUsedSegment)
            for compt in range(0,2):
                point = segmentList[randint(0,len(segmentList)-1)]
                nouvelleDistance = distance(point[0], point[1], fin.x, fin.y)
                if(nouvelleDistance < currentDistance):
                    lastUsedSegment = point
            routeList[routeNum].append(lastUsedSegment)
        distanceFinale = distance(routeList[routeNum][len(routeList[routeNum])-1][0], routeList[routeNum][len(routeList[routeNum])-1][1], fin.x, fin.y)
        if(math.pow(distanceFinale - distanceInitiale, 2) < 0.000001):
            routeListChoisi[routeNum] = routeList[routeNum]
        print(len(routeListChoisi))
        print(routeNum)
    
    pprint(routeList[22])
    
    
    
    
    
    
    
    """
    for num in range(0,15):
        currentDistance = distance(routeList[num][len(routeList[num])-1][0], routeList[num][len(routeList[num])-1][1], fin.x, fin.y)
        lastUsedSegment = routeList[num][len(routeList[num])-1]
        #while (currentDistance > 0):
        for i in range (0,50):
            #print(currentDistance)
            distanceMinimale = 100000.00
            segmentList = list()
            trouverIntersection(data, segmentList, lastUsedSegment)
            #for compt in range(0, 1):
            #    point = segmentList[randint(0, len(segmentList) - 1)]
            #    nouvelleDistance = distance(point[0], point[1], fin.x, fin.y)
            #    if (nouvelleDistance < distanceMinimale):
            #        lastUsedSegment = point
            #routeList[num].append(lastUsedSegment)
            for point in segmentList:
                currentDistance = distance(point[0], point[1], fin.x, fin.y)
                if(currentDistance < distanceMinimale) and (distanceMinimale - currentDistance > 0.0001):
                    distanceMinimale = currentDistance
                    currentSegment = point
            lastUsedSegment = currentSegment
            routeList[num].append(lastUsedSegment)
            currentDistance = distance(lastUsedSegment[0], lastUsedSegment[1], fin.x, fin.y)
        print(num)


    #pprint(routeList)

