from D6 import process, orbit_mvt


def test_process():
  assert process({'C': 'B', 'B': 'COM', 'E': 'D', 'D': 'C', 'G': 'B', 'F': 'E', 'I': 'D', 'H': 'G', 'K': 'J', 'J': 'E', 'L': 'K'}) == 42

def test_orbit_mvt():
  assert orbit_mvt({'C': ['B', 'COM'], 'B': ['COM'], 'E': ['D', 'C', 'B', 'COM'], 'D': ['C', 'B', 'COM'], 'G': ['B', 'COM'], 'F': ['E', 'D', 'C', 'B', 'COM'], 'I': ['D', 'C', 'B', 'COM'], 'H': ['G', 'B', 'COM'], 'K': ['J', 'E', 'D', 'C', 'B', 'COM'], 'J': ['E', 'D', 'C', 'B', 'COM'], 'L': ['K', 'J', 'E', 'D', 'C', 'B', 'COM'], 'YOU': ['K', 'J', 'E', 'D', 'C', 'B', 'COM'], 'SAN': ['I', 'D', 'C', 'B', 'COM']}) == 4