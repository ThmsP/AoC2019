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

def apply_gravity(m1, m2):
  for ind in range(3):
    if m1[0][ind] < m2[0][ind]:
      v = 1
    elif m1[0][ind] > m2[0][ind]:
      v = -1
    else:
      v = 0
    m1[1][ind] += v
  return m1

def apply_velocity(m):
  for ind in range(3):
    m[0][ind] = m[0][ind] + m[1][ind]
  return m


def iterations(moons, ite=0):
  moons_couple = [i for i in itertools.permutations(moons,2)]
  print moons_couple

  for i in range(ite):
    logging.info('ieration %i ', i)
    # for m in moons:
      # logging.info("moon %s %s",m, moons[m])
    for mc in moons_couple:
      moons[mc[0]] = apply_gravity(moons[mc[0]], moons[mc[1]])
    for m in moons:
      moons[m] = apply_velocity(moons[m])

  return moons




if __name__ == "__main__":
  import doctest
  doctest.testmod()

  moons = iterations(load_moon_map(), 10)  



  