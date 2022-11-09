

def getNextNum(lineSegment):
    i = 0
    print('line segment', lineSegment)
    for char in lineSegment:
        print(char)
        if char != ' ' and char != '\n':
            i += 1
        else:
            break
    return i + 1
