from D7 import amplifier

# import pytest
# @pytest.fixture()
# def create_amplifier():
#     return amplifier()

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
  # assert main_loop([3,9,7,9,10,9,4,9,99,-1,8], 9) == 0

def test_main_loop_imode_equalto():
  a = amplifier(0, 8, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 1
  # assert main_loop([3,3,1108,-1,8,3,4,3,99], 8) == 1

def test_main_loop_imode_ntequalto1():
  a = amplifier(0, 6, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 0
  # assert main_loop([3,3,1108,-1,8,3,4,3,99], 6) == 0

def test_main_loop_imode_ntequalto2():
  a = amplifier(0, 12, [3,3,1108,-1,8,3,4,3,99])
  assert a.amplify() == 0
  # assert main_loop([3,3,1108,-1,8,3,4,3,99], 12) == 0

def test_main_loop_imode_lessth():
  a = amplifier(0, 8, [3,3,1107,-1,8,3,4,3,99])
  assert a.amplify() == 1
  # assert main_loop([3,3,1107,-1,8,3,4,3,99], 8) == 1

def test_main_loop_imode_lessth():
  a = amplifier(0, 9, [3,3,1107,-1,8,3,4,3,99])
  assert a.amplify() == 0
  # assert main_loop([3,3,1107,-1,8,3,4,3,99], 9) == 0

# def test_main_loop_pmode_jump():
#   assert main_loop([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0) == 0

def test_main_loop_pmode_jump2():
  a = amplifier(0, 1, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
  assert a.amplify() == 1
  # assert main_loop([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1) == 1

def test_main_loop_large_below():
  a = amplifier(0, 7, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 999
  # assert main_loop([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7) == 999

def test_main_loop_large_equal():
  a = amplifier(0, 8, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 1000
  # assert main_loop([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8) == 1000

def test_main_loop_large_bigger():
  a = amplifier(0, 9, [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
  assert a.amplify() == 1001
  # assert main_loop([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9) == 1001