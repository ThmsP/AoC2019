from D6 import process


def test_process():
  assert process({'C': 'B', 'B': 'COM', 'E': 'D', 'D': 'C', 'G': 'B', 'F': 'E', 'I': 'D', 'H': 'G', 'K': 'J', 'J': 'E', 'L': 'K'}) == 42