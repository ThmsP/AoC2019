#D10
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def load_asteroid_map():
  # Process input :
  with open('input.data','r') as f:
    # Reversion the map : 
    # list of planet orbiting around planet
    om = [ l.replace('\n','') for l in f.readlines()]
    return om

def add_dico(val, dic, ind):
  try :
    dic[ind].append(val)
  except :
    dic[ind] = [val]
  return dic

def find_ast_coord(ast_map):
  ast_pos = []
  ast_y = {}
  ast_x = {}
  y = 0
  for ast_line in ast_map:
    x = 0
    for ast in ast_line:
      if ast == "#":
        ast_coord = (x, y)
        ast_pos.append(ast_coord)
        ast_y = add_dico(ast_coord, ast_y, y)
        ast_x = add_dico(ast_coord, ast_x, x)
      x += 1
    y += 1
  return ast_pos

def find_best_spot(ast_pos):
  coef_dir = {}
  for ast in ast_pos:
    cur_ast = ast
    other_pos = ast_pos[:]
    other_pos.pop(ast_pos.index(cur_ast))
    for other_ast in other_pos:
      ast_x = float(cur_ast[0])
      ast_y = float(cur_ast[1])
      oth_ast_x = float(other_ast[0])
      oth_ast_y = float(other_ast[1])
      if (oth_ast_y-ast_y) == 0. :
        if oth_ast_x-ast_x < 0 :
          coef_dir = add_dico(('h1',other_ast), coef_dir, cur_ast)
        else :
          coef_dir = add_dico(('h2',other_ast), coef_dir, cur_ast)
      elif (oth_ast_x-ast_x) == 0. :
        if oth_ast_y-ast_y < 0 :
          coef_dir = add_dico(('v1',other_ast), coef_dir, cur_ast)
        else :
          coef_dir = add_dico(('v2',other_ast), coef_dir, cur_ast)
      else:
        coef = (oth_ast_x-ast_x)/(oth_ast_y-ast_y)
        if ast_y > oth_ast_y :
          coef = 'b'+str(coef)
        coef_dir = add_dico((coef,other_ast), coef_dir, cur_ast)

  # print coef_dir
  ast_view = {}
  for ast in coef_dir:
    coef_val = [i[0] for i in coef_dir[ast]]
    ast_view[ast] = len(set(coef_val))

  best_ast = max(ast_view, key=lambda k: ast_view[k])
  return best_ast, ast_view[best_ast], coef_dir

def process(ast_map):
  ast_pos = find_ast_coord(ast_map)
  bst_ast, nbr_ast_view, coef_map = find_best_spot(ast_pos)
  return (bst_ast, nbr_ast_view)

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  ast_map = load_asteroid_map()
  # logging.debug('Asteroids map : %s',ast_map)

  ast_pos = find_ast_coord(ast_map)
  bst_ast, nbr_ast_view, coef_map = find_best_spot(ast_pos)

  logging.info('Best asteroid coord : %s',bst_ast)
  logging.info('Asteroids viewed    : %i',nbr_ast_view)  

  print coef_map
  

  # for i in ast_pos:
  #   print ast_view[i]









