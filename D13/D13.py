#D11
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class term_colors:
    WALL = '\x1b[0;31;41m'
    BLOCK = '\x1b[0;32;42m'
    BALL = '\x1b[0;33;43m'
    PLATE = '\x1b[0;35;45m'
    ENDC = '\x1b[0m'

class arcade:

  _input_value = 0
  _input_phase = 0
  _output_code = []
  _total_output = []
  # Differenciate the input call for the phase and the one for the value
  # _first_call  = True
  # Can be used for save the state of the memory
  _inputdata   = {}
  _rel_base    = 0
  _index       = None
  # _output_mvt  = None
  # _pointing    = 0
  _input_color = None


  def __init__(self, ic=0, inputdata={}):
    # self._input_value = iv
    # self._input_phase = ip
    # self._first_call  = True
    self._inputdata   = inputdata
    self._index       = 0
    return


  def get_pointing_dir(self):
    return self._pointing


  def set_pointing_dir(self,newpointing):
    self._pointing += newpointing
    logging.debug('pointing dir %i', self._pointing)
    if self._pointing >= 360 or self._pointing <= -360:
      self._pointing = 0
    return


  def reset_mem(self):
    # Process input :
    if not self._inputdata :
      logging.debug('Running from file input')
      with open('input.data','r') as f:
        l = [int(s) for s in f.readline().split(',')]
      l += [0]*12*len(l)
    else :
      logging.debug('Running from previous state')
      l = self._inputdata
    # Increasing memory after
    
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

    status = 0
    if self._input_color != None :
      logging.debug('FIRST CALL self._input_color %i', self._input_color)
      line[pos] = self._input_color
      self._input_color = None
    else : 
      logging.debug('SECOND CALL saving state')
      # Do nothing, save the state, we are waiting the input
      status = 1

    # if self._first_call :
    #   logging.info('Loading phase code : %i', self._input_phase)
    #   line[pos] = self._input_phase
    #   self._first_call = False
    # else :
    #   logging.info('Loading input code : %i', self._input_value)
    #   line[pos] = self._input_value
      
      
    return line, 0, status
  

  def loutput(self, sub, line, p1, p2, p3):
    """
    opcode 4
    """
    v1, v2, v3 = self.get_value(sub, line, p1, p2, p3)
    # logging.info('Diagnostic code : %i', v1)
    # if self._first_call :
    logging.debug('FIRST OUTPUT %i', v1)
    self._output_code.append(v1)
    # self._first_call = False
    # else :
    #   logging.debug('SECOND OUTPUT %i', v1)
    #   self._output_mvt = v1

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
    # logging.info('opcode p* [%i] : %i %i %i ',opcode, p1, p2, p3)
    # logging.info('sub %s ',sub)
    status = 0 #Useful to halt the program
    if opcode == 1:
      ml, ind = self.add(sub, line, p1, p2, p3)
    elif opcode == 2:
      ml, ind = self.mul(sub, line, p1, p2, p3)
    elif opcode == 3:
      ml, ind, status = self.linput(sub, line, p1, p2, p3)
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
    return ml, ind, status


  def draw(self,):
    x, y, tile = self._output_code

  def run_game(self, color_code=0):
    # index = self._index

    self._input_color=color_code
    # self._first_call = True
    # if inputphase:
      # self._input_phase=inputphase

    line = self.reset_mem()
    #Play for free !
    line[0] = 2
    lenop, opcode, p1, p2, p3 = self.get_len_instruct(line[self._index])

    logging.debug('opcode %s ',opcode)
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
      if len(self._output_code) == 3:
        # self.draw()
        self._total_output.append(self._output_code)
        self._output_code = []
    
    return opcode #, self._output_mvt
  

  
if __name__ == "__main__":
  import doctest
  doctest.testmod(extraglobs={'a': arcade()})

  borne = arcade()

  joystick = 0
  opcode = 0
  score = 0
  nbr_block = 1
  tiles_memory = {'_':(0,0), '*':(1,1)}
  while opcode != 99:
    borne.run_game(joystick)
    tiles = { (i[0],i[1]):i[2] for i in borne._total_output}
    nbr_block = len({ (i[0],i[1]):i[2] for i in borne._total_output if i[2] == 2}.keys())
    # logging.info('D13 BLOCK TILES : %i',len({ (i[0],i[1]):i[2] for i in borne._total_output if i[2] == 2}.keys()))
    imax, jmax = max(tiles.keys())
    try:
      score = tiles[(-1,0)]
    except:
      pass

    for j in range(jmax):
      tiles_current = {'_':None, '*':(1,1)}
      line = ''
      for i in range(imax):
        if tiles[i,j] == 0:
          ti = ' '
        elif tiles[i,j] == 1:
          ti = term_colors.WALL+'#'+term_colors.ENDC
        elif tiles[i,j] == 2:
          ti = term_colors.BLOCK+'B'+term_colors.ENDC
        elif tiles[i,j] == 3:
          ti = term_colors.PLATE+'_'+term_colors.ENDC
          tiles_current['_'] = (i,j)
        elif tiles[i,j] == 4:
          ti = term_colors.BALL+'*'+term_colors.ENDC
          tiles_current['*'] = (i,j)
        line += ti
      # if tiles_current['_'] == tiles_current['*']:
      #   til
      print line
    print score
    joy_in = raw_input()
    if joy_in == "q":
      joystick = -1
    elif joy_in == "d":
      joystick = 1
    else :
      joystick = 0
  if nbr_block == 0 :
    print "WINNER, score : %i"%score
  else :
    print "LOSER,  score : %i"%score