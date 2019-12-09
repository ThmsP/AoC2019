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
  width = 25
  height = 6
  layers = separate_layers(pix, width, height)
  chk = check_layers(layers)

  img_size = width*height

  pxl_layers = []
  for px in range(img_size):
    tmp = []
    for lay in layers:
      tmp.append(lay[px])
    pxl_layers.append(tmp)

  image = ''
  for px in pxl_layers:
    px_found = False
    for l in px :
      if l == '0' or l == '1':
        image += l
        break
    if not px:
      image += ' '

  image = image.replace('0',' ')
  ind = 0
  for i in range(25,25*6+1,25):
    print image[ind:i]
    ind = i


