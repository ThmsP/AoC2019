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

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  ast_map = load_asteroid_map()

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
        # ast_y = add_dico(ast_coord, ast_y, y)
        # ast_x = add_dico(ast_coord, ast_y, y)
        try :
          ast_y[y].append(ast_coord)
        except :
          ast_y[y] = [ast_coord]
        try :
          ast_x[x].append(ast_coord)
        except :
          ast_x[x] = [ast_coord]
      x += 1
    y += 1
  # print ast_pos
  # print ast_y
  # print ast_x

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
          try :
            coef_dir[cur_ast].append('h1')
          except :
            coef_dir[cur_ast] = ['h1']
        else :
          try :
            coef_dir[cur_ast].append('h2')
          except :
            coef_dir[cur_ast] = ['h2']
      elif (oth_ast_x-ast_x) == 0. :
        if oth_ast_y-ast_y < 0 :
          try :
            coef_dir[cur_ast].append('v1')
          except :
            coef_dir[cur_ast] = ['v1']
        else :
          try :
            coef_dir[cur_ast].append('v2')
          except :
            coef_dir[cur_ast] = ['v2']
      else:
        coef = (oth_ast_x-ast_x)/(oth_ast_y-ast_y)
        if ast_y > oth_ast_y :
          coef = 'b'+str(coef)
        try :
          coef_dir[cur_ast].append(coef)
        except:
          coef_dir[cur_ast] = [coef]

  print coef_dir
  ast_view = {}
  for ast in coef_dir:
    # print ast, len(set(coef_dir[ast]))
    ast_view[ast] = len(set(coef_dir[ast]))

  best_ast = max(ast_view, key=lambda k: ast_view[k])
  print best_ast, ast_view[best_ast]

  for i in ast_pos:
    print ast_view[i]









