from D10 import process

def test_process1():
  assert process(['.#..#', '.....', '#####', '....#', '...##']) == ((3, 4), 8)

def test_process2():
  assert process(['......#.#.', '#..#.#....', '..#######.', '.#.#.###..', '.#..#.....', '..#....#.#', '#..#....#.', '.##.#..###', '##...#..#.', '.#....####']) == ((5, 8), 33)

def test_process3():
  assert process(['#.#...#.#.', '.###....#.', '.#....#...', '##.#.#.#.#', '....#.#.#.', '.##..###.#', '..#...##..', '..##....##', '......#...', '.####.###.']) == ((1, 2), 35)

def test_process4():
  assert process(['.#..#..###', '####.###.#', '....###.#.', '..###.##.#', '##.##.#.#.', '....###..#', '..#.#..#.#', '#..#.#.###', '.##...##.#', '.....#.#..']) == ((6, 3), 41)

def test_process5():
  assert process(['.#..##.###...#######', '##.############..##.', '.#.######.########.#', '.###.#######.####.#.', '#####.##.#.##.###.##', '..#####..#.#########', '####################', '#.####....###.#.#.##', '##.#################', '#####.##.###..####..', '..######..##.#######', '####.##.####...##..#', '.#####..#.######.###', '##...#.##########...', '#.##########.#######', '.####.#.###.###.#.##', '....##.##.###..#####', '.#.#.###########.###', '#.#.#.#####.####.###', '###.##.####.##.#..##']) == ((11, 13), 210)