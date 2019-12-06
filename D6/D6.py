#D6
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def load_orbit_map():
  # Process input :
  with open('input.data','r') as f:
    # Reversin the map : 
    # list of planet orbiting around planet
    om = {s.replace('\n','').split(')')[1] : s.replace('\n','').split(')')[0]
          for s in f.readlines()}
    return om

def get_planet(p, om):
  try :
    planet = om[p]
  except :
    planet = False
    pass
  return planet



def orbit_graph(om):
  od = {}
  for p in om:
    ol = [om[p]]
    searching = True
    while searching :
      planet = get_planet(ol[-1], om)
      if planet :
        ol.append(planet)
        searching = True
      else :
        searching = False
    od[p] = ol
  return od


def graph_orbit_map(om):
  og = {}
  for o in om:
    try : 
      og[o[0]].append(o[1])
    except :
      og[o[0]] = list(o[1])
  return og

def reverse_orbit_graph(og):
  rog = {}
  for p in og.keys():
    logging.debug('process : %s', p)
    orbit_found = True
    to_search = p
    ind_o = []
    while orbit_found:
      if ind_o :
        to_search = ind_o[-1]
      for lp in og.keys():
        found = False
        logging.debug('searching : %s', to_search)
        if to_search in og[lp]:
          logging.debug('found in : %s', lp)
          ind_o.append(lp)
          found = True
          orbit_found = True
          break
        orbit_found = False
    rog[p] = ind_o
  return rog

def count_orbit(revog):
  co = 0
  for p in revog:
    co += len(revog[p])
  return co


def process(om):
  orlis = orbit_graph(om)
  print orlis
  # orgra = graph_orbit_map(ormap)
  # print orgra
  # revog = reverse_orbit_graph(orgra)
  # print revog
  count = count_orbit(orlis)
  
  return count

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  ormap = load_orbit_map()
  print ormap

  c = process(ormap)
  print c
  
