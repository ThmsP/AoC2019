#D9
import logging, sys
# import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class amplifier:

  _input_value = 0
  _input_phase = 0
  _output_code = 0
  # Differenciate the input call for the phase and the one for the value
  _first_call  = True
  # Can be used for save the state of the memory
  _inputdata   = {}
  _rel_base    = 0

  def __init__(self, iv=0, ip=0, inputdata={}):
    self._input_value = iv
    self._input_phase = ip
    self._first_call  = True
    self._inputdata   = inputdata
    return


  def reset_mem(self):
    # Process input :
    if not self._inputdata :
      logging.info('Running from file input')
      with open('input.data','r') as f:
        l = [int(s) for s in f.readline().split(',')]
    else :
      logging.info('Running from previous state')
      l = self._inputdata
    # Increasing memory after
    l += [0]*10*len(l)
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
    if opcode == 3 or opcode == 4 or opcode == 9:
      subl = 2
    elif opcode == 5 or opcode == 6:
      subl = 3

    return subl, opcode, param1, param2, param3
  
  def get_value(self, sub, line, p1, p2, p3):
    # logging.debug('line %s', line)
    # logging.debug('len(line) %s', len(line))
    # logging.debug('sub %s',sub)
    # logging.debug('param %i %i %i', p1, p2, p3)
    # logging.debug('self._rel_base %i',self._rel_base)
    params = [p1, p2, p3]
    values = []
    i = 1
    for p in params[:len(sub)-1]:
      if p:
        if p == 1:
          values.append(sub[i])
        elif p == 2:
          values.append(line[sub[i]+ self._rel_base]) 
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
    if p3 == 2:
      # print "pp"
      pos = sub[3]+self._rel_base
    else:
      pos = sub[3]

    line[pos] = v1 + v2
    return line, 0
  
  def mul(self, sub, line, p1, p2, p3):
    """
    opcode 2
  
    >>> a.mul([2,3,0,3],[2,3,0,3,99], 0, 0, 0)
    ([2, 3, 0, 6, 99], 0)
  
    >>> a.mul([2,4,4,5],[2,4,4,5,99,0], 0, 0, 0)
    ([2, 4, 4, 5, 99, 9801], 0)
    """
    # logging.debug('len(line) %s', len(line))
    # logging.debug('sub %s',sub)
    # logging.debug('param %i %i %i', p1, p2, p3)
    # logging.debug('self._rel_base %i',self._rel_base)
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if p3 == 2:
      # print "pp"
      pos = sub[3]+self._rel_base
    else:
      pos = sub[3]
      
    line[pos] = v1 * v2
    return line, 0
  
  def linput(self, sub, line, p1, p2, p3):
    """
    opcode 3
    """
    # if not tinput :
    #   line[pos] = input('Input whatever\n')
    # else :
    #   line[pos] = tinput
    
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if p1:
      # print "pp"
      pos = sub[1]+self._rel_base
    else:
      pos = sub[1]

    if self._first_call :
      logging.info('Loading phase code : %i', self._input_phase)
      line[pos] = self._input_phase
      self._first_call = False
    else :
      logging.info('Loading input code : %i', self._input_value)
      line[pos] = self._input_value
      
      
    return line, 0
  
  def loutput(self, sub, line, p1, p2, p3):
    """
    opcode 4
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    logging.info('Diagnostic code : %i', v1)
    self._output_code = v1
    # if v1 == 203:
    #   line = None
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
    if p3 == 2:
      # print "pp"
      pos = sub[3]+self._rel_base
    else:
      pos = sub[3]

    if v1 < v2:
      line[pos] = 1
    else: 
      line[pos] = 0
    return line, 0
  
  def equals(self, sub, line, p1, p2, p3):
    """
    opcode 8
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    if p3 == 2:
      # print "pp"
      pos = sub[3]+self._rel_base
    else:
      pos = sub[3]

    if v1 == v2:
      line[pos] = 1
    else: 
      line[pos] = 0
    return line, 0

  def base_offset(self, sub, line, p1, p2, p3):
    """
    opcode 9 
    relative base offset
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    self._rel_base += v1
    return line, 0

  
  def process(self, opcode, sub, line, p1, p2, p3):
    logging.debug('opcode p* [%i] : %i %i %i ',opcode, p1, p2, p3)
    if opcode == 1:
      ml, ind = self.add(sub, line, p1, p2, p3)
    elif opcode == 2:
      ml, ind = self.mul(sub, line, p1, p2, p3)
    elif opcode == 3:
      ml, ind = self.linput(sub, line, p1, p2, p3)
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
    elif opcode == 9:
      ml, ind = self.base_offset(sub, line, p1, p2, p3)
    return ml, ind
  
  def amplify(self, inputcode=0, inputphase=0):
    index = 0

    if inputcode:
      self._input_value=inputcode
    if inputphase:
      self._input_phase=inputphase

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

    #Save the state of the amplifier memory
    self._inputdata = line
    return self._output_code
  
  # def amplify(self):
  #   line = self.reset_mem()
  #   self.main_loop(line)
  #   logging.info('End')
  #   return
  
  
if __name__ == "__main__":
  import doctest
  doctest.testmod(extraglobs={'a': amplifier()})

  amp = amplifier(0,1)
  amp.amplify()

  





