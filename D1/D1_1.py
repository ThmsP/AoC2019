## Day 1 1/2

def fuel_req(mass): 
  """
  Calculate the fuel required by a module
  Exemple :

  >>> fuel_req(14)
  2
  >>> fuel_req(1969)
  654
  >>> fuel_req(100756)
  33583
  
  """
  return (mass/3)-2

def fuel_fuel(fuel):
  """
  Calculate fuel required for fuel
  Exemple : 

  >>> fuel_fuel(2)
  0
  >>> fuel_fuel(654)
  312
  >>> fuel_fuel(33583)
  16763
  """
  res = fuel
  ff = 0
  while res > 0 :
    res = fuel_req(res)
    if res > 0 :
      ff += res
  return ff

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    fuel_mod = 0
    fuel_tot = 0
    with open('input.data','r') as f :
      for m in f.readlines():
        fuel_mod = fuel_req(int(m))
        fuel_tot += fuel_mod + fuel_fuel(fuel_mod)
    print fuel_tot