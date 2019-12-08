#D7
import logging, sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class amplifier:

  _input_value = 0
  _input_phase = 0
  _output_code = 0
  _first_call  = True
  _inputdata   = {}

  def __init__(self, iv=0, ip=0, inputdata={}):
    self._input_value = iv
    self._input_phase = ip
    self._first_call  = True
    self._inputdata   = inputdata
    return


  def reset_mem(self):
    # Process input :
    if not self._inputdata :
      with open('input.data','r') as f:
        l = [int(s) for s in f.readline().split(',')]
    else :
      l = self._inputdata
    return l
  
  def get_len_instruct(self, num):
    l = len(str(num))
    # default : position mode
    param1 = param2 = param3 = 0
    subl = 4
    if l == 1:
      opcode = num
    else :
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

    return subl, opcode, param1, param2, param3
  
  def get_value(self, sub, line, p1, p2, p3):
    
    params = [p1, p2, p3]
    values = []
    i = 1
    for p in params[:len(sub)-1]:
      if p:
        values.append(sub[i])
      else :
        values.append(line[sub[i]])
      i += 1
  
    if len(values) < 3:
      values += [0 for j in range(3-len(values))]
    v1, v2, v3 = values
  
    return v1, v2, v3
  
  def add(self, sub, line, p1, p2, p3):
    """
    opcode 1
  
    >>> a.add([1,0,0,0],[1,0,0,0,99], 0, 0, 0)
    ([2, 0, 0, 0, 99], 0)
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    line[sub[3]] = v1 + v2
    return line, 0
  
  def mul(self, sub, line, p1, p2, p3):
    """
    opcode 2
  
    >>> a.mul([2,3,0,3],[2,3,0,3,99], 0, 0, 0)
    ([2, 3, 0, 6, 99], 0)
  
    >>> a.mul([2,4,4,5],[2,4,4,5,99,0], 0, 0, 0)
    ([2, 4, 4, 5, 99, 9801], 0)
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    line[sub[3]] = v1 * v2
    return line, 0
  
  def linput(self, pos, line, p1, p2, p3):
    """
    opcode 3
    """
    # if not tinput :
    #   line[pos] = input('Input whatever\n')
    # else :
    #   line[pos] = tinput
    if self._first_call :
      line[pos] = self._input_value
      self._first_call = False
    else :
      line[pos] = self._input_phase
    return line, 0
  
  def loutput(self, sub, line, p1, p2, p3):
    """
    opcode 4
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    logging.info('Diagnostic code : %i', v1)
    self._output_code = v1
    # global return_code
    # return_code = v1
    return line, 0
  
  def jumpiftrue(self, sub, line, p1, p2, p3):
    """
    opcode 5
    """
    index = 0
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if v1 != 0:
      index = v2
    return line, index
  
  def jumpiffalse(self, sub, line, p1, p2, p3):
    """
    opcode 6
    """
    index = 0
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if v1 == 0:
      index = v2
    return line, index
  
  def lessthan(self, sub, line, p1, p2, p3):
    """
    opcode 7
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if v1 < v2:
      line[sub[3]] = 1
    else: 
      line[sub[3]] = 0
    return line, 0
  
  def equals(self, sub, line, p1, p2, p3):
    """
    opcode 8
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if v1 == v2:
      line[sub[3]] = 1
    else: 
      line[sub[3]] = 0
    return line, 0
  
  def process(self, opcode, sub, line, p1, p2, p3):
    logging.debug('opcode %i ',opcode)
    if opcode == 1:
      ml, ind = self.add(sub, line, p1, p2, p3)
    elif opcode == 2:
      ml, ind = self.mul(sub, line, p1, p2, p3)
    elif opcode == 3:
      ml, ind = self.linput(sub[1], line, p1, p2, p3)
    elif opcode == 4:
      ml, ind = self.loutput(sub, line, p1, p2, p3)
    elif opcode == 5:
      ml, ind = self.jumpiftrue(sub, line, p1, p2, p3)
    elif opcode == 6:
      ml, ind = self.jumpiffalse(sub, line, p1, p2, p3)
    elif opcode == 7:
      ml, ind = self.lessthan(sub, line, p1, p2, p3)
    elif opcode == 8:
      ml, ind = self.equals(sub, line, p1, p2, p3)
    return ml, ind
  
  def amplify(self):
    index = 0
    line = self.reset_mem()
    lenop, opcode, p1, p2, p3 = self.get_len_instruct(line[index])
    

    while opcode != 99:
      sub = line[index:index+lenop]
      line, ind = self.process(opcode, sub, line, p1, p2, p3)
      if not ind :
        index += lenop
      else :
        index = ind
      lenop, opcode, p1, p2, p3 = self.get_len_instruct(line[index])
    return self._output_code
  
  # def amplify(self):
  #   line = self.reset_mem()
  #   self.main_loop(line)
  #   logging.info('End')
  #   return
  
  
if __name__ == "__main__":
  import doctest
  doctest.testmod(extraglobs={'a': amplifier()})

  phase = itertools.permutations([0,1,2,3,4])
  # logging.debug('phase %s',phase)
  amp = amplifier(5,0)
  code = amp.amplify()
  print code
  # amp.main_loop()

  





