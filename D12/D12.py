#D12
import logging, sys
import math
import itertools

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def load_moon_map():
  # Process input :
  with open('input.data','r') as f:
    om = [ l.replace('\n','') \
            .replace(', ',' ') \
            .replace('<','')  \
            .replace('>','') for l in f.readlines()]
    #
    moons = {}
    for o in om :
      coord = []
      for p in o.split(' '):
        coord.append(int(p.split('=')[1]))
      moons['m'+str(om.index(o))] = [coord, [0,0,0]]

    return moons

def add_dico(val, dic, ind):
  try :
    dic[ind].append(val)
  except :
    dic[ind] = [val]
  return dic

def calculate_gravity(m1, m2):
  # velocity_m1 = m1[1]
  #
  print m1[1]
  # vx, vy, vz = m1[1]

  # vel = [vx,vy,vz]
  # velout = []
  for ind in range(3):
    if m1[0][ind] < m2[0][ind]:
      v = -1
    elif m1[0][ind] > m2[0][ind]:
      v = 1
    else:
      v = 0
    print m1[0]
    print m1[1]
    print v
    m1[1][ind] += v
  # m1[1]=velout
  return m1



if __name__ == "__main__":
  import doctest
  doctest.testmod()

  moons = load_moon_map()
  # print moon_map
  moons_couple = itertools.permutations(moons,2)
    # print i
  for i in moons_couple:
    cur_moon = i[0]
    cpl_moon = i[1]
    print moons
    print cur_moon
    moons[cur_moon] = calculate_gravity(moons[cur_moon], moons[cpl_moon])

  for m in moons:
    print moons[m]
    for c in moons[m]:
      print c



  