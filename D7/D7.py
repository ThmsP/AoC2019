#D7
import logging, sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class amplifier:

  _input_value = 0
  _input_phase = 0
  _output_code = 0
  # Differenciate the input call for the phase and the one for the value
  _first_call  = True
  # Can be used for save the state of the memory
  _inputdata   = {}
  _index       = None

  def __init__(self, iv=None, ip=None, inputdata={}):
    self._input_value = iv
    self._input_phase = ip
    self._first_call  = True
    self._inputdata   = inputdata
    self._index       = 0
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
    status = 0
    if self._first_call :
      logging.info('Loading phase code : %i', self._input_phase)
      line[pos] = self._input_phase
      self._first_call = False
    else :
      if self._input_value != None :
        logging.info('Loading input code : %i', self._input_value)
        line[pos] = self._input_value
        self._input_value = None
      else :
        status = 1
      
      
    return line, 0, status
  
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
    status = 0 #Useful to halt the program
    if opcode == 1:
      ml, ind = self.add(sub, line, p1, p2, p3)
    elif opcode == 2:
      ml, ind = self.mul(sub, line, p1, p2, p3)
    elif opcode == 3:
      ml, ind, status = self.linput(sub[1], line, p1, p2, p3)
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
    return ml, ind, status
  
  def amplify(self, inputcode=None, inputphase=None):
    # index = 0

    if inputcode != None:
      self._input_value=inputcode
    if inputphase != None:
      self._input_phase=inputphase

    line = self.reset_mem()
    lenop, opcode, p1, p2, p3 = self.get_len_instruct(line[self._index])
    # self._output_code = opcode

    while opcode != 99:
      sub = line[self._index:self._index+lenop]
      line, ind, status = self.process(opcode, sub, line, p1, p2, p3)
      if status : 
        #Save the state of the amplifier memory
        self._inputdata = line
        break

      if not ind :
        self._index += lenop
      else :
        self._index = ind
      lenop, opcode, p1, p2, p3 = self.get_len_instruct(line[self._index])


    #Save the state of the amplifier memory
    # self._inputdata = line
    return self._output_code, opcode
  
  # def amplify(self):
  #   line = self.reset_mem()
  #   self.main_loop(line)
  #   logging.info('End')
  #   return
  
  
if __name__ == "__main__":
  import doctest
  doctest.testmod(extraglobs={'a': amplifier()})

  # Best phase for part1 is [2,1,0,4,3]
  # phase_permut = itertools.permutations([0,1,2,3,4])
  # Now we're searching best phase for part2 :
  phase_permut = itertools.permutations([5,6,7,8,9])
  thrust = {}
  for phase_test in phase_permut:
    # logging.debug('phase %s',phase)
    amp_list = [amplifier(None,p) for p in phase_test]
    amp_out = 0
    opcode = 0
    first_tour = True
    while opcode != 99:
      for amp in amp_list:
        amp_out, opcode = amp.amplify(amp_out)
        logging.info('amp_out %i ',amp_out)
    thrust[amp_out]=phase_test
    # logging.info('amp_out %i ',amp_out)
  maxthrust = max(thrust.keys())
  print "maxthrust", maxthrust
  print "thrust[maxthrust]", thrust[maxthrust]
  print "thrust", thrust

  # thrust = {}
  # for phase in phase_permut :
  #   logging.debug('phase %s',phase)
  #   # Input of first amplifier
  #   # amp_out = 51679 # Best score thrust of part1
  #   # for amp in amp_dic:
  #     # amp = amplifier(amp_out,phase[ind])
  #   amp_out, line = amp.amplify(amp_out, phase[-1])
  #   thrust[amp_out]=phase
  # # code = amp.amplify()
  # maxthrust = max(thrust.keys())
  # print maxthrust
  # print thrust[maxthrust]
  # amp.main_loop()

  





