#D8 

def load_space_image_format():
  # Process input :
  with open('input.data','r') as f:
    pixels = f.readline()
    return pixels

def separate_layers(pix_image, width, height):
  layers = []
  ind = 0
  for i in range(width*height,len(pix)+1,width*height):
    layers.append(pix[ind:i])
    ind = i
  return layers

def check_layers(layers):
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
  return check[min0l][0] * check[min0l][1]

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  pix = load_space_image_format()
  layers = separate_layers(pix, 25, 6)
  chk = check_layers(layers)

  curi = 0
  image = ''
  for px in layers[0]:
    print "#######"
    print "pix : ", curi
    if px == '0' or px == '1':
      print "L1 noir ou blanc"
      image += px
      # curi += 1
      # pass
    elif px == '2':
      px_bottom_layers = [ layers[i][curi] for i in range(1,len(layers))]
      # print px_bottom_layers
      found_bw = False
      for dpx in px_bottom_layers :
        if px == '2':
          pass
        elif px == '0' or px == '1':
          print "L noir ou blanc"
          image += ' '
          found_bw = True
          break
      if not found_bw :
        print 'L transparent'
        image += ' '
    curi += 1

  # print image

  ind = 0
  for i in range(25,25*6+1,25):
    print image[ind:i]
    ind = i


