from D9 import amplifier

# import pytest
# @pytest.fixture()
# def create_amplifier():
#     return amplifier()

# Amplifier tests
# Tests from D5
# Phase pos used as input

def test_main_loop_pmode_equalto():
  a = amplifier(0, 8, [3,9,8,9,10,9,4,9,99,-1,8])
  assert a.amplify() == 1

def test_main_loop_pmode_ntequalto1():
  a = amplifier(0, 7, [3,9,8,9,10,9,4,9,99,-1,8])
  assert a.amplify() == 0

def test_main_loop_pmode_ntequalto2():
  a = amplifier(0, 12, [3,9,8,9,10,9,4,9,99,-1,8])
  assert a.amplify() == 0

def test_main_loop_pmode_lessth():
  a = amplifier(0, 7, [3,9,7,9,10,9,4,9,99,-1,8])
  assert a.amplify() == 1

def test_main_loop_pmode_moreth():
  a = amplifier(0, 9, [3,9,7,9,10,9,4,9,99,-1,8])
  assert a.amplify() == 0

def test_main_loop_imode_equalto():
  a = amplifier(0, 8, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 1

def test_main_loop_imode_ntequalto1():
  a = amplifier(0, 6, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 0

def test_main_loop_imode_ntequalto2():
  a = amplifier(0, 12, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 0

# def test_main_loop_imode_lessth():
#   a = amplifier(0, 8, [3,3,1107,-1,8,3,4,3,99])
#   assert a.amplify() == 1
  # assert main_loop([3,3,1107,-1,8,3,4,3,99], 8) == 1

def test_main_loop_imode_lessth2():
  a = amplifier(0, 9, [3,3,1107,-1,8,3,4,3,99])
  assert a.amplify() == 0

def test_main_loop_pmode_jump():
  a = amplifier(0, 0, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
  assert a.amplify() == 0

def test_main_loop_pmode_jump2():
  a = amplifier(0, 1, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
  assert a.amplify() == 1

def test_main_loop_large_below():
  a = amplifier(0, 7, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 999

def test_main_loop_large_equal():
  a = amplifier(0, 8, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 1000

def test_main_loop_large_bigger():
  a = amplifier(0, 9, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 1001

## SEQUENCING TEST D7
# def test_seq_p1_1():
#   phase = [4,3,2,1,0]
#   out = 0
#   for i in phase : 
#     a = amplifier(out, i, [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
#     out = a.amplify()
#     del a
#   assert out == 43210 

# def test_seq_p1_2():
#   phase = [0,1,2,3,4]
#   out = 0
#   for i in phase : 
#     a = amplifier(out, i, [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
#     out = a.amplify()
#     del a
#   assert out == 54321 

# def test_seq_p1_3():
#   phase = [9,8,7,6,5]
#   out = 0
#   for i in phase : 
#     a = amplifier(out, i, [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
#     out = a.amplify()
#     del a
#   assert out == 139629729 

# def test_seq_p2_1():
#   phase = [9,7,8,5,6]
#   out = 0
#   for i in phase : 
#     a = amplifier(out, i, [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
#     out = a.amplify()
#     del a
#   assert out == 18216 

## D9 TESTS

def test_amplify_relative():
  a = amplifier(0, 9, [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
  assert a.amplify() == 109

def test_amplify_relative1():
  a = amplifier(0, 9, [1102,34915192,34915192,7,4,7,99,0])
  assert len(str(a.amplify())) == 16

def test_amplify_relative2():
  a = amplifier(0, 9, [104,1125899906842624,99])
  assert a.amplify() == 1125899906842624