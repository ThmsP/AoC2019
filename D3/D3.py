# D3


def read_input():
    with open('input.data', 'r') as f:
        wires = []
        for line in f.readlines():
            wires.append(line.split(','))
    return wires


def add_point(coord, U, D, R, L):
    """
    Return the point fonction of the increment
    """
    coord_i = coord[0]+R-L
    coord_j = coord[1]+U-D
    return coord_i, coord_j


def get_all_point(wire):
    """
    Assemble all the point of trajectory in a set
    """
    coord = [(0, 0)]
    for i in wire:
        incr = int(i[1:].replace('\n',''))
        last_pt = coord[-1]
        if 'R' in i:
            for j in range(1, incr+1):
                coord.append(add_point(last_pt, 0, 0, j, 0))
        elif 'L' in i:
            for j in range(1, incr+1):
                coord.append(add_point(last_pt, 0, 0, 0, j))
        elif 'U' in i:
            for j in range(1, incr+1):
                coord.append(add_point(last_pt, j, 0, 0, 0))
        elif 'D' in i:
            for j in range(1, incr+1):
                coord.append(add_point(last_pt, 0, j, 0, 0))
    return coord

def manhattan_dst(intersect):
    """
    Compute min manhattan distance excluding point 0
    """
    mindst = 0
    for i in intersect :
        dst = abs(i[0])+abs(i[1])
        if not mindst :
            mindst = dst
        elif dst < mindst:
            mindst = dst
    return mindst

def minmize_delay(wire1, wire2, intersect):
    return wire1.index(intersect)+wire2.index(intersect)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    w1, w2 = read_input()

    coord_w1 = get_all_point(w1)
    coord_w2 = get_all_point(w2)


    intersect = set(coord_w1) & set(coord_w2)
    print intersect
    min_delay = []
    for crois in intersect:
        min_delay.append(minmize_delay(coord_w1, coord_w2, crois))
    if 0 in min_delay:
        min_delay.pop(min_delay.index(0))

    print min(min_delay)
    print manhattan_dst(intersect)
