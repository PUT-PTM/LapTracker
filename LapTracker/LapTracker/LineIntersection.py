def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def contains(segment, ps):
    Min = (min(segment[0][0], segment[1][0]), min(segment[0][1], segment[1][1]))
    Max = (max(segment[0][0], segment[1][0]), max(segment[0][1], segment[1][1]))
    if (Min[0] <= ps[0] <= Max[0] and Min[1] <= ps[1] <= Max[1]):
        return True
    else:
        return False

def intersects(segment1, segment2):
    intersection_p = line_intersection(segment1, segment2)
    if intersection_p is not None and contains(segment1, intersection_p) and contains(segment2, intersection_p):
        print("Intersection!!!")
        return intersection_p
    else:
        return None

#A = (0,2)
#B = (6,2)
#C = (4,3)
#D = (4,8)

#print (intersects((A,B),(C,D)))
#Motor2 = False
#if Motor:
#    Motor2 = contains(C, D, R)

#if Motor2:
#    print ("Intersection detected:", Motor2)
#else:
#    print ("No single intersection point detected")


