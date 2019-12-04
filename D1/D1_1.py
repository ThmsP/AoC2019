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

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    fuel_mod = 0
    with open('input.data','r') as f :
      for m in f.readlines():
        fuel_mod += fuel_req(int(m))
    print fuel_mod