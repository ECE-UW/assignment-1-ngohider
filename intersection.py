
def get_intersect(x1, y1, x2, y2, x3, y3, x4, y4):

    x1 = float(x1)
    x2 = float(x2)
    x3 = float(x3)
    x4 = float(x4)
    y1 = float(y1)
    y2 = float(y2)
    y3 = float(y3)
    y4 = float(y4)

    a1 = y2 - y1
    b1 = x1 - x2
    c1 = (a1*x1) + (b1*y1)
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = (a2*x3) + (b2*y3)

    try:
        xInt = ((b2*c1) - (b1*c2))/((b2*a1) - (b1*a2))
        yInt = ((a2*c1) - (a1*c2))/((b1*a2) - (b2*a1))
    except ZeroDivisionError:
        return None, None

    ###  Check if the calculated point is a valid intersection or not

    if (((min(x1,x2) <= xInt) & (xInt <= max(x1,x2))) & ((min(y1,y2) <= yInt) & (yInt <= max(y1,y2)))) & \
        (((min(x3,x4) <= xInt) & (xInt <= max(x3,x4))) & ((min(y3,y4) <= yInt) & (yInt <= max(y3,y4)))):
        return xInt, yInt

    else:
        return None, None
