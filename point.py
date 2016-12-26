import numpy as np

## Parameters
names = {0: 'Wahyu',
         1: 'Suras',
         2: 'Surya',
         3: 'Agung',
         4: 'Nur',
         5: 'Mega',
         6: 'Ari',
         7: 'Nando'}

numEmployees = 8
numDays = 14
bonusPerPoint = 5000

#####################

def calculateBonus(points):
    """ calculate bonuses for each person working at the certain day.
    param: points a list of points. Person who takes the 
                  day off must be given -1 point.
    return: a numpy array
    """

    pointsTuple = zip(points, range(numEmployees))

    sortedPoints = sorted(pointsTuple)

    prevPoint = -1
    bonusSoFar = 0
    bonusesTuple = []
    for i in range(len(sortedPoints)):
        point, person = sortedPoints[i]
        additionalBonus = 0
        if point > 0:
            if point != prevPoint:
                if prevPoint > 0:
                    additionalBonus = (point - prevPoint) * bonusPerPoint
                else:
                    additionalBonus = point * bonusPerPoint

                additionalBonus //= (numEmployees-i)

        bonusSoFar += additionalBonus
        bonusesTuple.append((person, bonusSoFar))
        prevPoint = point

    bonusesTuple = sorted(bonusesTuple)
    return np.array([element[1] for element in bonusesTuple])

def writeToFile(filename, points):
    result = np.zeros((numEmployees, numDays))
    result = result.astype(int)
    for col in range(numDays):
        dayBonus = points[col]
        arrayBonus = calculateBonus(dayBonus)
        result[:,col] = arrayBonus

    print(result)
    with open(filename, 'w+') as out:
        for row in range(numEmployees):
            for col in range(numDays-1):
                out.write(str(result[row,col]) + ',')
            out.write(str(result[row,numDays-1]) + '\n')

def test():
    # input partition
    # some test cases are values specific

    allIsOff = [-1 for _ in range(numEmployees)]
    assert list(calculateBonus(allIsOff)) == [0 for _ in range(numEmployees)]
    
    allIsSame = [4 for _ in range(numEmployees)]
    assert list(calculateBonus(allIsSame)) == [(4*bonusPerPoint//numEmployees) for _ in range(numEmployees)]

    oneIsOff = [20 for _ in range(numEmployees)]
    oneIsOff[2] = -1
    result = [(20 * bonusPerPoint // (numEmployees-1)) for _ in range(numEmployees)]
    result[2] = 0
    assert list(calculateBonus(oneIsOff)) == result

    allIsDifferent = [i for i in range(numEmployees)]
    result = [0]
    bonus = 0
    for i in range(1, numEmployees):
        bonus += bonusPerPoint // (numEmployees-i)
        result.append(bonus)
    assert list(calculateBonus(allIsDifferent)) == result

    examplePoints = [13, -1, 13, 7, 4, 13, 13]
    assert list(calculateBonus(examplePoints)) == [13833, 0, 13833, 6333, 3333, 13833, 13833]

    exPoints = [23, 0, 14, 23, -1, 23, 23]
    assert list(calculateBonus(exPoints)) == [25250, 0, 14000, 25250, 0, 25250, 25250]

    example = [-1, 0, 13, -1, 13, 13, 13]
    assert list(calculateBonus(example)) == [0, 0, 16250, 0, 16250, 16250, 16250]

    print("Tests passed.")

#test()


#points = [[20,2,20,20,20,-1,-1],
#          [-1,4,13,13,5,13,13],
#          [20,20,-1,-1,20,20,20],
#          [-1,-1,16,16,16,-1,16],
#          [-1,0,28,28,28,28,28],
#          [-1,3,20,20,20,20,20],
#          [30,5,30,30,-1,30,30],
#          [27,27,27,27,27,-1,-1],
#          [22,6,-1,22,22,22,22],
#          [14,11,14,-1,14,14,14],
#          [20,20,10,20,20,20,20],
#          [-1,-1,-1,-1,-1,-1,-1],
#          [27,-1,27,14,27,27,27],
#          [29,29,29,29,-1,29,29]]
#writeToFile('bonuses.csv', points)
