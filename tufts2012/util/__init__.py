def in_polygon(x,y,poly):
    """ Function that checks if (x,y) is within a polygon specificied by poly
        Code taken from http://www.ariel.com.au/a/python-point-int-poly.html
        x and y are floats, poly is a pairs of (x,y)
    """
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
