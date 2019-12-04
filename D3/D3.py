#D3

def read_input():
	with open('input.data','r') as f:
		wires = []
		for line in f.readlines():
			wires.append(line.split(','))
	return wires

def get_min_max(wire):
	"""
	wire must be sorted by up/down and left/right
	"""
	i = 0
	max = 0
	min = 0
	for ind in wire :
		if 'U' in ind or 'R' in ind:
			i += int(ind[1:])
		elif 'D' in ind or 'L' in ind :
			i -= int(ind[1:])
		if i > max :
			max = i
		if i < min :
			min = i
	return min, max

def sortw(wire):
	updown = []
	leftright = []
	for i in wire : 
    	# print i
		if 'U' in i or 'D' in i:
    		# print 'add updown'
			updown.append(i)
		elif 'L' in i or 'R' in i:
    		# print 'add leftright'
			leftright.append(i)
	return updown, leftright

def add_point(coord, U,D,R,L):
	coord_i = coord[0]+R-L
	coord_j = coord[1]+U-D
	return coord_i, coord_j

def get_all_point(wire):
	coord_w1 = [(0,0)]
	for i in w1 :
		incr = int(i[1:])
    	last_pt = coord_w1[-1]
    	if 'R' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, 0, j, 0))
    	elif 'L' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, 0, 0, j))
    	elif 'U' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, j, 0, 0, 0))
    	elif 'D' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, j, 0, 0))
	return coord_w1

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    w1,w2 = read_input()

    coord_w1 = [(0,0)]
    for i in w1 :
    	incr = int(i[1:])
    	last_pt = coord_w1[-1]
    	if 'R' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, 0, j, 0))
    	elif 'L' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, 0, 0, j))
    	elif 'U' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, j, 0, 0, 0))
    	elif 'D' in i : 
    		for j in range(1,incr+1) :
    			coord_w1.append(add_point(last_pt, 0, j, 0, 0))

    print coord_w1
    # ud_w1, lr_w1 = sortw(w1)
    # jmin_w1, jmax_w1 = get_min_max(ud_w1)
    # imin_w1, imax_w1 = get_min_max(lr_w1)
    
    # ud_w2, lr_w2 = sortw(w2)
    # jmin_w2, jmax_w2 = get_min_max(ud_w2)
    # imin_w2, imax_w2 = get_min_max(lr_w2)

    # print "w1 : imin, imax", imin_w1, imax_w1
    # print "w1 : jmin, jmax", jmin_w1, jmax_w1
    # print "w2 : imin, imax", imin_w2, imax_w2
    # print "w2 : jmin, jmax", jmin_w2, jmax_w2

