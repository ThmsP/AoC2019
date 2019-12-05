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
  return subl, opcode, param1, param2, param3

def get_value(sub, line, p1, p2, p3):
  logging.debug('get_value, p1, p2, p3 : %i, %i, %i', p1, p2, p3)
  if p1 : 
    v1 = sub[1]
  else :
    v1 = line[sub[1]]
  if p2 :
    v2 = sub[2]
  else :
    v2 = line[sub[2]]
  return v1, v2

def add(sub, line, p1, p2, p3):
  """
  opcode 1

  >>> add([1,0,0,0],[1,0,0,0,99], 0, 0, 0)
  [2, 0, 0, 0, 99]
  """
  v1, v2 = get_value(sub, line, p1, p2, p3)
  line[sub[3]] = v1 + v2
  return line

def mul(sub, line, p1, p2, p3):
  """
  opcode 2

  >>> mul([2,3,0,3],[2,3,0,3,99], 0, 0, 0)
  [2, 3, 0, 6, 99]

  >>> mul([2,4,4,5],[2,4,4,5,99,0], 0, 0, 0)
  [2, 4, 4, 5, 99, 9801]
  """
  v1, v2 = get_value(sub, line, p1, p2, p3)
  line[sub[3]] = v1 * v2
  return line

def linput(pos, line, p1, p2, p3):
  """
  opcode 3
  """
  line[pos] = input('Input whatever\n')
  return line

def loutput(pos, line, p1, p2, p3):
  """
  opcode 4
  """
  logging.info('Diagnostic code : %i', line[pos])
  return line

def process(opcode, sub, line, p1, p2, p3):
  logging.debug('opcode %i ',opcode)
  if opcode == 1:
    ml = add(sub, line, p1, p2, p3)
  elif opcode == 2:
    ml = mul(sub, line, p1, p2, p3)
  elif opcode == 3:
    ml = linput(sub[1], line, p1, p2, p3)
  elif opcode == 4:
    ml = loutput(sub[1], line, p1, p2, p3)
  return ml

if __name__ == "__main__":
  import doctest
  doctest.testmod()

  line = reset_mem()
  index = 0
  lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
  while opcode != 99:
    # lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
    sub = line[index:index+lenop]
    logging.debug(sub)
    line = process(opcode, sub, line, p1, p2, p3)
    logging.debug(line[:20])
    index += lenop
    lenop, opcode, p1, p2, p3 = get_len_instruct(line[index])
  logging.info('End')





