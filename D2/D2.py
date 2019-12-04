#D2

def add(sub, line):
	"""
	>>> add([1,0,0,0],[1,0,0,0,99])
	[2, 0, 0, 0, 99]
	"""
	line[sub[3]] = line[sub[1]] + line[sub[2]]
	return line

def mul(sub, line):
	"""
	>>> mul([2,3,0,3],[2,3,0,3,99])
	[2, 3, 0, 6, 99]

	>>> mul([2,4,4,5],[2,4,4,5,99,0])
	[2, 4, 4, 5, 99, 9801]
	"""
	line[sub[3]] = line[sub[1]] * line[sub[2]]
	return line

def reset_mem():
	# Process input :
    with open('input.data','r') as f:
		l = [int(s) for s in f.readline().split(',')]
		# print l[:4]
    return l

def compute_ad0(l):
	wl = l[:]
	for i in range(4,len(l),4):
		sub = wl[i-4:i]
		opcode = sub[0]
		if opcode == 99 : 
			break
		elif opcode == 1 :
			wl = add(sub, wl)
		elif opcode == 2 :
			wl = mul(sub, wl)
		else : 
			break 
	return wl[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    for noun in range(0,100):
    	for verb in range(0,100):
    		l = reset_mem()
    		# print l
			#1202 program state
    		l[1] = noun
    		l[2] = verb

    		if compute_ad0(l) == 19690720:
    			print 'noun :', noun
    			print 'verb :', verb
    			print '100*noun+verb :', 100*noun+verb
