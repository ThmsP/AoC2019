#D5
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def reset_mem():
  # Process input :
  with open('input.data','r') as f:
    l = [int(s) for s in f.readline().split(',')]
    return l

def get_len_instruct(num):
  l = len(str(num))
  # default : position mode
  param1 = param2 = param3 = 0
  subl = 4
  logging.debug('get_len_instruct, num : %i', num)
  logging.debug('get_len_instruct, l   : %s', l)
  if l == 1:
    opcode = num
  else :
    # warning we are in this case with opcode 99
    opcode = int(str(num)[-2:])

    try :
      param1 = int(str(num)[-3:-2])
    except :
      pass
    try :
      param2 = int(str(num)[-4:-3])
    except :
      pass
    try :
      param3 = int(str(num)[-5:-4])
    except :
      pass
  if opcode == 3 or opcode == 4:
    subl = 2
  elif opcode == 5 or opcode == 6:
    subl = 3
  logging.debug('get_len_instruct, subl, opcode, param1, param2, param3   : %i, %i, %i, %i, %i', subl, opcode, param1, param2, param3)
  return subl, opcode, param1, param2, param3

def get_value(sub, line, p1, p2, p3):
  logging.debug('########  get_value ########')
  logging.debug('line, %s', line)
  logging.debug('sub, %s', sub)
  logging.debug('get_value, p1, p2, p3 : %i, %i, %i', p1, p2, p3)

  params = [p1, p2, p3]
  values = []
  i = 1
  logging.debug('params[:len(sub), %s', params[:len(sub)])
  for p in params[:len(sub)-1]:
    logging.debug('p, %i', p)
    logging.debug('i, %i', i)
    if p:
      values.append(sub[i])
    else :
      values.append(line[sub[i]])
    i += 1

  if len(values) < 3:
    values += [0 for j in range(3-len(values))]
  v1, v2, v3 = values

  # if p1 : 
  #   v1 = sub[1]
  # else :
  #   v1 = line[sub[1]]
  #   logging.debug('get_value, sub[1], %i',sub[1])
  #   logging.debug('get_value, line[sub[1]], %i',line[sub[1]])
  #   logging.debug('get_value, v1, %i',v1)
  # if p2 :
  #   v2 = sub[2]
  # else :
  #   v2 = line[sub[2]]
  #   logging.debug('get_value, sub[2], %i',sub[2])
  #   logging.debug('get_value, line[sub[2]], %i',line[sub[2]])
  #   logging.debug('get_value, v2, %i',v2)
  # # if p3 :
  # #   v3 = sub[3]
  # # else :
  # #   v3 = line[sub[3]]
  # #   logging.debug('get_value, sub[3], %i',sub[3])
  # #   logging.debug('get_value, line[sub[3]], %i',line[sub[3]])
  # #   logging.debug('get_value, v3, %i',v3)
  # v3 = 0
  logging.debug('get_value, v1, v2, v3 : %i, %i, %i', v1, v2, v3)
  return v1, v2, v3

def add(sub, line, p1, p2, p3):
  """
  opcode 1

  >>> add([1,0,0,0],[1,0,0,0,99], 0, 0, 0)
  ([2, 0, 0, 0, 99], 0)
  """
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  line[sub[3]] = v1 + v2
  return line, 0

def mul(sub, line, p1, p2, p3):
  """
  opcode 2

  >>> mul([2,3,0,3],[2,3,0,3,99], 0, 0, 0)
  ([2, 3, 0, 6, 99], 0)

  >>> mul([2,4,4,5],[2,4,4,5,99,0], 0, 0, 0)
  ([2, 4, 4, 5, 99, 9801], 0)
  """
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  line[sub[3]] = v1 * v2
  return line, 0

def linput(pos, line, p1, p2, p3):
  """
  opcode 3
  """
  if not test_input :
    line[pos] = input('Input whatever\n')
  else :
    line[pos] = test_input
  return line, 0

def loutput(sub, line, p1, p2, p3):
  """
  opcode 4
  """
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  logging.info('Diagnostic code : %i', v1)
  global return_code
  return_code = v1
  return line, 0

def jumpiftrue(sub, line, p1, p2, p3):
  """
  opcode 5
  """
  index = 0
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  if v1 != 0:
    index = v2
  return line, index

def jumpiffalse(sub, line, p1, p2, p3):
  """
  opcode 6
  """
  index = 0
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  if v1 == 0:
    index = v2
  return line, index

def lessthan(sub, line, p1, p2, p3):
  """
  opcode 7
  """
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  if v1 < v2:
    line[sub[3]] = 1
  else: 
    line[sub[3]] = 0
  return line, 0

def equals(sub, line, p1, p2, p3):
  """
  opcode 8
  """
  v1, v2, v3 = get_value(sub, line, p1, p2, p3)
  if v1 == v2:
    line[sub[3]] = 1
  else: 
    line[sub[3]] = 0
  return line, 0

def process(opcode, sub, line, p1, p2, p3):
  logging.debug('opcode %i ',opcode)
  if opcode == 1:
    ml, ind = add(sub, line, p1, p2, p3)
  elif opcode == 2:
    ml, ind = mul(sub, line, p1, p2, p3)
  elif opcode == 3:
    ml, ind = linput(sub[1], line, p1, p2, p3)
  elif opcode == 4:
    ml, ind = loutput(sub, line, p1, p2, p3)
  elif opcode == 5:
    ml, ind = jumpiftrue(sub, line, p1, p2, p3)
  elif opcode == 6:
    ml, ind = jumpiffalse(sub, line, p1, p2, p3)
  elif opcode == 7:
    ml, ind = lessthan(sub, line, p1, p2, p3)
  elif opcode == 8:
    ml, ind = equals(sub, line, p1, p2, p3)
  return ml, ind

def main_loop(inputdata, tinput=0):
  index = 0
  lenop, opcode, p1, p2, p3 = get_len_instruct(inputdata[index])
  
  global test_input
  test_input = tinput
  global return_code
  return_code = 12
  
  while opcode != 99:
    # lenop, opcode, p1, p2, p3 = get_len_instruct(inputdata[index])
    logging.debug('####')
    logging.debug('index %i',index)
    logging.debug('inputdata %s', inputdata)
    logging.debug('####')
    sub = inputdata[index:index+lenop]
    logging.debug(sub)
    inputdata, ind = process(opcode, sub, inputdata, p1, p2, p3)
    # logging.debug(inputdata[index:index+10])
    logging.debug('inputdata %s', inputdata)
    if not ind :
      index += lenop
    else :
      index = ind
    logging.debug('new index %i',index)
    lenop, opcode, p1, p2, p3 = get_len_instruct(inputdata[index])
  return return_code

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  test_input = 0
  return_code = 6546449646469

  line = reset_mem()
  main_loop(line)
  # index = 0
  # lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
  # while opcode != 99:
  #   # lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
  #   logging.debug('####')
  #   logging.debug('index %i',index)
  #   logging.debug('line %s', line)
  #   logging.debug('####')
  #   sub = line[index:index+lenop]
  #   logging.debug(sub)
  #   line, ind = process(opcode, sub, line, p1, p2, p3)
  #   # logging.debug(line[index:index+10])
  #   logging.debug('line %s', line)
  #   if not ind :
  #     index += lenop
  #   else :
  #     index = ind
  #   logging.debug('new index %i',index)
  #   lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
  logging.info('Diagnostic code : %i', return_code)
  logging.info('End')





