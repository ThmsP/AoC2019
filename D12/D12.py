#D12
# import logging, sys
# import math
import itertools
import multiprocessing

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def load_moon_map():
  # Process input :
  f = open('input.data','r')
  om = [ l.replace('\n','') \
          .replace(', ',' ') \
          .replace('<','')  \
          .replace('>','') for l in f.readlines()]
  f.close()
  #
  moons = {}
  for o in om :
    coord = []
    for p in o.split(' '):
      coord.append(int(p.split('=')[1]))
    moons['m'+str(om.index(o))] = [coord, [0,0,0]]

  return moons

def apply_gravity(m1, m2, ind):
  # for ind in range(3):
  if m1[0][ind] < m2[0][ind]:
    v1 = 1
    v2 = -1
  elif m1[0][ind] > m2[0][ind]:
    v1 = -1
    v2 = 1
  else:
    v1 = v2 = 0
  m1[1][ind] += v1
  m2[1][ind] += v2
  return m1, m2

def apply_velocity(ms, ind):
  hist = ''
  for m in ms:
    ms[m][0][ind] += ms[m][1][ind]
    hist += str(ms[m][0][ind])+str(ms[m][1][ind])
  return ms, hist

def mem_pos(ms, ind):
  hist = ''
  for m in ms:
    hist += str(ms[m][0][ind])+str(ms[m][1][ind])

  return hist


#pythran export iterations(((int, int, int) list,(int, int, int) list) list : str dict, int)
def iterations(ind):

  moons = load_moon_map()
  moons_couple = [i for i in itertools.combinations(moons,2)]


  moons_pos = mem_pos(moons, ind)
  found = []
  while len(found)<2000:

    for mc in moons_couple:
      moons[mc[0]], moons[mc[1]] = apply_gravity(moons[mc[0]], moons[mc[1]], ind)
    moons, pos = apply_velocity(moons, ind)

    if pos in moons_pos:
      found.append(ite)
      print len(found)


  return found

# def potential_energy(m):
#   ep = 0
#   for i in range(3):
#     ep += abs(m[0][i])
#   logging.info('moon %s',m)
#   logging.info('ep %i', ep)
#   return ep

# def kinetic_energy(m):
#   ek = 0
#   for i in range(3):
#     ek += abs(m[1][i])
#   logging.info('moon %s',m)
#   logging.info('ek %i', ek)
#   return ek

# def total_energy(moons):
#   et = 0
#   for m in moons:
#     ep = potential_energy(moons[m])
#     ek = kinetic_energy(moons[m])
#     et += ep*ek
#   return et





# 
if __name__ == "__main__":
  pool = multiprocessing.Pool(8)
  results = []
  for x in pool.imap_unordered(iterations, range(3)):
    results.append(x)
    pass
  pool.close()
  pool.join()
  min_ite_per_axis = set(results[0]) & set(results[1]) & set(results[2])
  min_ite          = min(min_ite_per_axis)
  print "FINAL FOUND : %i"%min_ite


  