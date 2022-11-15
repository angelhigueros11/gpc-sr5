# Graficas por computador
# Angel Higueros - 20460
# SR5

class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.vertex = [] 
    self.tvertex = []
    self.faces = []

    for line in self.lines:
      if line := line.strip():
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          temp = value.split(' ')
          arr = [float(tempValue) for tempValue in temp]

          self.vertex.append(arr)

        elif prefix == 'vt':
          temp = value.split(' ')
          arr = [float(tempValue) for tempValue in temp]

          if(len(arr)==2):
            arr.append(0)

          self.tvertex.append(arr)


        elif prefix == 'f':
          temp = value.split(' ')
          arr = []

          for tempValue in temp:
            temp2 = tempValue.split('/')
            arr2 = [int(tempValue2) for tempValue2 in temp2]

            arr.append(arr2)

          self.faces.append(arr)
  