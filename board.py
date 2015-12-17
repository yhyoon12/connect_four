
class Board(object):
  """
  Board object that holds the board state
  Connect 4 rules state a 6 x 7 board, but can be expansible
  """

  cells = None
  player1_locs = None
  player2_locs = None
  x_max = None
  y_max = None

  def __init__(self, x = 7, y = 6):
    self.x_max = x
    self.y_max = y
    self.cells = [[0 for i in range(self.x_max)] for j in range(self.y_max)]
    self.player1_locs = []
    self.player2_locs = []

  def __str__(self):
    print " 0 1 2 3 4 5 6 "
    for x in range(0, len(self.cells[0])):
      x = self.x_max - x - 1
      output = ''
      for y in self.cells:
        output += "|"
        if y[x] == 0:
          output += " "
        elif y[x] == 1:
          output += "O"
        elif y[x] == 2:
          output += "X"
      output += "|"
      print output
    print "---------------"
    print " 0 1 2 3 4 5 6 "
    return ""

  def check_win(self, player):
    if player == 1:
      nodes = self.player1_locs
    else:
      nodes = self.player2_locs

    for node in nodes:
      x = node[0]
      y = node[1]

      if (x, y + 1) in nodes and (x, y + 2) in nodes and (x, y + 3) in nodes:
        return (True, player, [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)])

      if (x, y - 1) in nodes and (x, y - 2) in nodes and (x, y - 3) in nodes:
        return (True, player, [(x, y), (x, y - 1), (x, y - 2), (x, y - 3)])

      if (x + 1, y) in nodes and (x + 2, y) in nodes and (x + 3, y) in nodes:
        return (True, player, [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)])

      if (x - 1, y) in nodes and (x - 2, y) in nodes and (x - 3, y) in nodes:
        return (True, player, [(x, y), (x - 1, y), (x - 2, y), (x - 3, y)])

      if (x + 1, y + 1) in nodes and (x + 2, y + 2) in nodes and (x + 3, y + 3) in nodes:
        return (True, player, [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])

      if (x - 1, y + 1) in nodes and (x - 2, y + 2) in nodes and (x - 3, y + 3) in nodes:
        return (True, player, [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])

      if (x - 1, y - 1) in nodes and (x - 2, y - 2) in nodes and (x - 3, y - 3) in nodes:
        return (True, player, [(x, y), (x - 1, y - 1), (x - 2, y - 2), (x - 3, y - 3)])

      if (x + 1, y - 1) in nodes and (x + 2, y - 2) in nodes and (x + 3, y - 3) in nodes:
        return (True, player, [(x, y), (x + 1, y - 1), (x + 2, y - 2), (x + 3, y - 3)])

    return (False, player, [])

# IMPORTANT NEED TO COUNT DISJOINT SETS

  def fours(self, player):
    if player == 1:
      nodes = self.player1_locs
    else:
      nodes = self.player2_locs

    output = []

    for node in nodes:
      x = node[0]
      y = node[1]

      if (x, y + 1) in nodes and (x, y + 2) in nodes and (x, y + 3) in nodes:
        row = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)]
        output.append(row)

      if (x + 1, y) in nodes and (x + 2, y) in nodes and (x + 3, y) in nodes:
        row = [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)]
        output.append(row)

      if (x + 1, y + 1) in nodes and (x + 2, y + 2) in nodes and (x + 3, y + 3) in nodes:
        row = [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)]
        output.append(row)

      if (x - 1, y + 1) in nodes and (x - 2, y + 2) in nodes and (x - 3, y + 3) in nodes:
        row = [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)]
        output.append(row)

    return output

  # Returns a list of list of three-in-a-row pairs for player player
  def threes(self, player):
    if player == 1:
      nodes = self.player1_locs
    else:
      nodes = self.player2_locs

    output = []

    for node in nodes:
      x = node[0]
      y = node[1]

      if (x, y + 1) in nodes and (x, y + 2) in nodes and (x, y + 3) not in nodes and (x, y - 1) not in nodes:
        row = [(x, y), (x, y + 1), (x, y + 2)]
        output.append(row)

      if (x + 1, y) in nodes and (x + 2, y) in nodes and (x + 3, y) not in nodes and (x - 1, y) not in nodes:
        row = [(x, y), (x + 1, y), (x + 2, y)]
        output.append(row)

      if (x + 1, y + 1) in nodes and (x + 2, y + 2) in nodes and (x + 3, y + 3) not in nodes and (x - 1, y - 1) not in nodes:
        row = [(x, y), (x + 1, y + 1), (x + 2, y + 2)]
        output.append(row)

      if (x - 1, y + 1) in nodes and (x - 2, y + 2) in nodes and (x - 3, y + 3) not in nodes and (x + 1, y - 1) not in nodes:
        row = [(x, y), (x - 1, y + 1), (x - 2, y + 2)]
        output.append(row)

    return output

  # Returns a list of list of two-in-a-row pairs for player player
  def twos(self, player):
    if player == 1:
      nodes = self.player1_locs
    else:
      nodes = self.player2_locs

    output = []

    for node in nodes:
      x = node[0]
      y = node[1]

      if (x, y + 1) in nodes and (x, y + 2) not in nodes and (x, y - 1) not in nodes:
        row = [(x, y), (x, y + 1)]
        output.append(row)

      if (x + 1, y) in nodes and (x + 2, y) not in nodes and (x - 1, y) not in nodes:
        row = [(x, y), (x + 1, y)]
        output.append(row)

      if (x + 1, y + 1) in nodes and (x + 2, y + 2) not in nodes and (x - 1, y - 1) not in nodes:
        row = [(x, y), (x + 1, y + 1)]
        output.append(row)

      if (x - 1, y + 1) in nodes and (x - 2, y + 2) not in nodes and (x + 1, y - 1) not in nodes:
        row = [(x, y), (x - 1, y + 1)]
        output.append(row)

    return output

  def valid_moves(self):
    moves = []
    for x in range(self.x_max):
      if self.cells[self.y_max - 1][x] == 0:
        moves.append(x)
    return moves

  def add(self, x, player):
    for y in range(self.y_max):
      if self.cells[y][x] == 0:
        self.cells[y][x] = player
        if player == 1:
          self.player1_locs.append((x, y))
        else:
          self.player2_locs.append((x, y))
        return (True, x, y)
    return (False, -1, -1)
