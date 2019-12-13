#D12
# import logging, sys
# import math
import itertools

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

def add_dico(val, dic, ind):
  try :
    dic[ind].append(val)
  except :
    dic[ind] = [val]
  return dic

def apply_gravity(m1, m2):
  for ind in range(3):
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

def apply_velocity(ms):
  hist = ''
  for m in ms:
    for ind in range(3):
      ms[m][0][ind] += ms[m][1][ind]
    hist += ''.join(map(str,ms[m][0]))+''.join(map(str,ms[m][1]))
  return ms, hist

def mem_pos(moons):
  hist = ''
  # print moons
  for m in moons:
    for c in moons[m]:
      for cc in c:
        # print cc
        hist+=str(cc)
  # print hist
  return hist


#pythran export iterations(((int, int, int) list,(int, int, int) list) : int dict, int)
def iterations(moons, ite=0):
  # moons_couple = [i for i in itertools.permutations(moons,2)]
  moons_cpl_iterator = itertools.permutations(moons,2)
  moons_couple = []
  for i in moons_cpl_iterator:
    if i not in moons_couple and (i[1],i[0]) not in moons_couple:
      moons_couple.append(i)

  # print moons_couple

  moons_pos = mem_pos(moons)
  ite =1
  while True:
    if not ite % 10000:
      # logging.info('ieration %i ', ite)
      print 'ite %i'%ite
    # for m in moons:
      # logging.info("moon %s %s",m, moons[m])
    for mc in moons_couple:
      moons[mc[0]], moons[mc[1]] = apply_gravity(moons[mc[0]], moons[mc[1]])
    # for m in moons:
    moons, pos = apply_velocity(moons)
    # pos = mem_pos(moons)
    # print pos
    if pos in moons_pos:
      # logging.info('Universe repeat ! %i', ite)
      print 'Universe repeat ! %i '%ite
      break
    else:
      moons_pos+=pos
    ite += 1

  return moons

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






# if __name__ == "__main__":
  # import doctest
  # doctest.testmod()

  # moons = iterations(load_moon_map(), 1000)  
  # system_energy = total_energy(moons)
  # logging.info('total energy of the system : %i', system_energy)



  