# D4

range_min = 172851
range_max = 675869

def never_dec(num):
	init = num[0]
	for i in num:
		if int(i) >= int(init):
			init = i
		else :
			return False
	return True

def two_same(num):
	init = num[0]
	found = False
	for i in num:
		if i == init:
			found = True
	return found

pwd_found=[]
for pwd in range(range_min, range_max):
	if never_dec(str(pwd)) and two_same(str(pwd)):
		pwd_found.append(pwd)

print pwd_found
print len(pwd_found)