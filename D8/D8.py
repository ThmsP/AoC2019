#D8 

def load_space_image_format():
  # Process input :
  with open('input.data','r') as f:
    pixels = f.readline()
    return pixels

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  pix = load_space_image_format()
  # print pix
  width = 25
  height = 6

  layers = []
  ind = 0
  for i in range(width*height,len(pix)+1,width*height):
  	layers.append(pix[ind:i])
  	ind = i

  print len(pix)
  print width*height
  print layers
  print len(layers)

  check = {}
  for lay in layers:
  	c0 = 0
  	c1 = 0
  	c2 = 0
  	for px in lay :
  		if px == '0' :
  			c0 += 1
  		if px == '1' :
  			c1 += 1
  		if px == '2' :
  			c2 += 1
  	check[c0] = (c1, c2)

  min0l = min(check.keys())
  print check[min0l][0] * check[min0l][1]
