# D3


def read_input():
    with open('input.data', 'r') as f:
        wires = []
        for line in f.readlines():
            wires.append(line.split(','))
    return wires


def get_min_max(wire):
    """
    UNUSED
    """
    i = 0
    max = 0
    min = 0
    for ind in wire:
        if 'U' in ind or 'R' in ind:
            i += int(ind[1:])
        elif 'D' in ind or 'L' in ind:
            i -= int(ind[1:])
        if i > max:
            max = i
        if i < min:
            min = i
    return min, max


def sortw(wire):
    """
    UNUSED
    """
    updown = []
    leftright = []
    for i in wire:
        # print i
        if 'U' in i or 'D' in i:
            # print 'add updown'
            updown.append(i)
        elif 'L' in i or 'R' in i:
            # print 'add leftright'
            leftright.append(i)
    return updown, leftright


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
    coord_w1 = [(0, 0)]
    for i in wire:
        incr = int(i[1:].replace('\n',''))
        last_pt = coord_w1[-1]
        if 'R' in i:
            for j in range(1, incr+1):
                coord_w1.append(add_point(last_pt, 0, 0, j, 0))
        elif 'L' in i:
            for j in range(1, incr+1):
                coord_w1.append(add_point(last_pt, 0, 0, 0, j))
        elif 'U' in i:
            for j in range(1, incr+1):
                coord_w1.append(add_point(last_pt, j, 0, 0, 0))
        elif 'D' in i:
            for j in range(1, incr+1):
                coord_w1.append(add_point(last_pt, 0, j, 0, 0))
    return set(coord_w1)

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    w1, w2 = read_input()

    set_w1 = get_all_point(w1)
    set_w2 = get_all_point(w2)

    intersect = set_w1 & set_w2
    print manhattan_dst(intersect)
