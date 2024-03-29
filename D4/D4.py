# D4

range_min = 172851
range_max = 675869

def never_dec(num):
	"""
	>>> never_dec('111111')
	True
	>>> never_dec('223450')
	False
	"""
	init = num[0]
	for i in num:
		if int(i) >= int(init):
			init = i
		else :
			return False
	return True

def two_same(num):
	"""
	>>> two_same('123789')
	False
	"""
	init = '0' 
	found = False
	for i in num:
		if i == init:
			found = True
		init=i
	return found

def only_two_same(num):
	"""
	>>> only_two_same('123789')
	False
	>>> only_two_same('112233')
	True
	>>> only_two_same('123444')
	False
	>>> only_two_same('111122')
	True
	"""
	match = ['0']
	found = False
	for i in num:
		if i == match[0]:
			match.append(i)
		else : 
			if len(match) == 2 :
				found = True
			match = [i]
	if len(match) == 2 :
				found = True
	return found

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	pswd_found=[]
	for pswd in range(range_min, range_max):
		if never_dec(str(pswd)) and only_two_same(str(pswd)):
			pswd_found.append(pswd)
	
	print pswd_found
	print len(pswd_found)