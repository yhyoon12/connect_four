from ai import *
from board import *
import pygame

# Asset definitions ============================================================
fontname = "font/HelveticaNeueLTStd-Th.otf"
fontname_b = "font/HelveticaNeueLTStd-MdCnO.otf"
fontname_c = "font/HelveticaNeueLTStd-UltLt.otf"
fontname_d = "font/HelveticaNeueLTStd-Cn.otf"

# Constant definitions =========================================================
# Color definitions
white = (255,255,255)
black = (0,0,0)
red = (231,76,60)
blue = (52,152,219)
green = (46,204,113)
orange = (230,126,34)

# Game state enum types
MENU = 0
SUBMENU_PLAY = 1
SUBMENU_WATCH = 2
HUMAN_AI = 3
AI_AI = 4


# Heuristic enum types
RANDOM = 1
BALANCED = 2
OFFENSIVE = 3
DEFENSIVE = 4

# Depth enum types
SHALLOW = 1
NORMAL = 3
DEEP = 5

# Function definitions =========================================================
# Initialize the game variables
def init():
  global player2
  global board
  global turn
  global invalid_move
  global victory
  global player1_locs
  global player2_locs

  board = Board()
  turn = 1
  victory = 0
  player1_locs = []
  player2_locs = []
  invalid_move = False

# Function to create a text string in the game
def create_text(screen, font_path, size, text, color, center):
  font = pygame.font.Font(font_path, size)
  text = font.render(text, True, color)
  textpos = text.get_rect()
  textpos.centerx = center[0]
  textpos.centery = center[1]
  screen.blit(text, textpos)

# Function to create a rectangle in the game
def create_rect(screen, rect, color, center, thickness):
  rectangle = pygame.Rect(rect)
  rectangle.center = center
  pygame.draw.rect(screen, color, rectangle, thickness)
  return rectangle

def main_menu():
  center = screen.get_rect().center

  play_rect = create_rect(screen, [10, 10, 200, 80], black, (400, 450), 1)
  watch_rect = create_rect(screen, [20, 10, 200, 80], black, (400, 550), 1)

  create_text(screen, fontname, 25, "PLAY", black, center)
  create_text(screen, fontname, 25, "WATCH", black, (center[0], center[1]+100))
  create_text(screen, fontname_b, 85, "Connect Four", black, (screen.get_rect().centerx, screen.get_rect().centery -200))
  create_text(screen, fontname, 30, "By: Mark Yoon and Charles Tark", black, (screen.get_rect().centerx, screen.get_rect().centery -150))

  return (play_rect, watch_rect)

# Returns button list with following order:
# For state == SUBMENU_PLAY: [go, [bal, off, def, rand], [shal, norm, deep], back]
# For state == SUBMENU_WATCH: [go, [bal, off, def, rand], [shal, norm, deep],
#   [bal, off, def, rand], [shal, norm, deep], back]
def sub_menu(state):
  center = screen.get_rect().center
  y_off = 0

  create_text(screen, fontname_c, 65, "+", black, (screen.get_rect().centerx -348, screen.get_rect().centery -380))
  create_text(screen, fontname_b, 55, "AI Parameters", black, (screen.get_rect().centerx -195, screen.get_rect().centery -350))

  depth_row = screen.get_rect().centery -270
  button_offset = 180
  x_off = 280
  create_text(screen, fontname_d, 35, "Depth:", black, (screen.get_rect().centerx -280, depth_row))
  if ai_a_depth is SHALLOW:
    shal_a_rect = create_rect(screen, [20, 10, 160, 50], red, (x_off, depth_row), 0)
    create_text(screen, fontname, 25, "SHALLOW", white, (x_off, depth_row))
  else:
    shal_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off, depth_row), 1)
    create_text(screen, fontname, 25, "SHALLOW", black, (x_off, depth_row))
  if ai_a_depth is NORMAL:
    norm_a_rect = create_rect(screen, [20, 10, 160, 50], blue, (x_off+button_offset, depth_row), 0)
    create_text(screen, fontname, 25, "NORMAL", white, (x_off+button_offset, depth_row))
  else:
    norm_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off+button_offset, depth_row), 1)
    create_text(screen, fontname, 25, "NORMAL", black, (x_off+button_offset, depth_row))
  if ai_a_depth is DEEP:
    deep_a_rect = create_rect(screen, [20, 10, 160, 50], green, (x_off+button_offset*2, depth_row), 0)
    create_text(screen, fontname, 25, "DEEP", white, (x_off+button_offset*2, depth_row))
  else:
    deep_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off+button_offset*2, depth_row), 1)
    create_text(screen, fontname, 25, "DEEP", black, (x_off+button_offset*2, depth_row))

  heur_row = screen.get_rect().centery -185
  x_off = 320
  create_text(screen, fontname_d, 35, "Heuristic:", black, (screen.get_rect().centerx -260, heur_row))
  if ai_a_heur is BALANCED:
    bal_a_rect = create_rect(screen, [20, 10, 160, 50], red, (x_off, heur_row), 0)
    create_text(screen, fontname, 25, "BALANCED", white, (x_off, heur_row))
  else:
    bal_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off, heur_row), 1)
    create_text(screen, fontname, 25, "BALANCED", black, (x_off, heur_row))
  if ai_a_heur is OFFENSIVE:
    off_a_rect = create_rect(screen, [20, 10, 160, 50], blue, (x_off+button_offset, heur_row), 0)
    create_text(screen, fontname, 25, "OFFENSIVE", white, (x_off+button_offset, heur_row))
  else:
    off_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off+button_offset, heur_row), 1)
    create_text(screen, fontname, 25, "OFFENSIVE", black, (x_off+button_offset, heur_row))
  if ai_a_heur is DEFENSIVE:
    def_a_rect = create_rect(screen, [20, 10, 160, 50], green, (x_off, heur_row +70), 0)
    create_text(screen, fontname, 25, "DEFENSIVE", white, (x_off, heur_row +70))
  else:
    def_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off, heur_row +70), 1)
    create_text(screen, fontname, 25, "DEFENSIVE", black, (x_off, heur_row +70))
  if ai_a_heur is RANDOM:
    rand_a_rect = create_rect(screen, [20, 10, 160, 50], orange, (x_off+button_offset, heur_row +70), 0)
    create_text(screen, fontname, 25, "RANDOM", white, (x_off+button_offset, heur_row +70))
  else:
    rand_a_rect = create_rect(screen, [20, 10, 160, 50], black, (x_off+button_offset, heur_row +70), 1)
    create_text(screen, fontname, 25, "RANDOM", black, (x_off+button_offset, heur_row +70))

  if state == SUBMENU_WATCH:
    y_off = 200
    # More buttonz

  create_text(screen, fontname, 25, "_________", black, (center[0], center[1]+y_off))

  create_text(screen, fontname, 25, "PLAY", black, (center[0]+30, center[1]+100+y_off))
  go_rect = create_rect(screen, [10, 10, 180, 60], black, (center[0]+30, center[1]+100+y_off), 1)
  create_text(screen, fontname, 25, "<", black, (center[0]-105, center[1]+100+y_off))
  back_rect = create_rect(screen, [10, 10, 60, 60], black, (center[0]-105, center[1]+100+y_off), 1)

  return [go_rect, [bal_a_rect, off_a_rect, def_a_rect, rand_a_rect],[shal_a_rect, norm_a_rect, deep_a_rect],back_rect]

def draw_game_boxes(x_center, y_center):
  game_rects = []
  for i in range(0, 7):
    x_center += 100
    y_center = 900
    col = []
    for j in range(0, 6):
      y_center -= 100
      if (i, j) in player1_locs:
        col.append(create_rect(screen, [10, 10, 99, 99], red, (x_center, y_center), 0))
      elif (i, j) in player2_locs:
        col.append(create_rect(screen, [10, 10, 99, 99], blue, (x_center, y_center), 0))
      else:
        col.append(create_rect(screen, [10, 10, 100, 100], black, (x_center, y_center), 1))
    game_rects.append(col)
  return game_rects

def draw_game_text(victory, turn, invalid_move):
  # Back Button
  create_text(screen, fontname, 25, "<", black, (80, 100))
  back_rect = create_rect(screen, [10, 10, 60, 60], black, (80, 100), 1)
  if invalid_move:
    if turn == 1:
      create_text(screen, fontname, 25, "Your turn!", black, (400, 100))
    else:
      create_text(screen, fontname, 25, "AI's turn!", black, (400, 100))
    create_text(screen, fontname, 25, "Invalid move!", black, (400, 175))
    create_text(screen, fontname, 25, "Human: " + str(human), black, (115 , 230))
    create_text(screen, fontname, 25, "AI: " + str(ai), black, (700 , 230))
  elif victory != 0:
    create_text(screen, fontname, 25, "Try again?", black, (400, 175))
    try_again = create_rect(screen, [10, 10, 200, 50], black, (400, 175), 1)
    if victory == 1:
      create_text(screen, fontname, 40, "You won!!", black, (400, 100))
    else:
        create_text(screen, fontname, 40, "You lost...", black, (400, 100))
    create_text(screen, fontname, 25, "Human: " + str(human), black, (115 , 230))
    create_text(screen, fontname, 25, "AI: " + str(ai), black, (700 , 230))
    return [try_again, back_rect]
  else:
    if turn == 1:
      create_text(screen, fontname_b, 45, "Your turn!", black, (400, 100))
    else:
      create_text(screen, fontname_b, 45, "AI's turn!", black, (400, 100))
    create_text(screen, fontname, 25, "Human: " + str(human), black, (115 , 230))
    create_text(screen, fontname, 25, "AI: " + str(ai), black, (700 , 230))
  return ['should not be accessed', back_rect]

# Main =========================================================================

# Initialize the game screen
pygame.init()
size = (800,900)
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption("Connect 4")
running = True
game_state = MENU

# Initialize the game states
init()
human = 0
ai = 0
ai_a_depth = NORMAL
ai_a_heur = BALANCED
ai_b_depth = NORMAL
ai_b_heur = BALANCED
player2 = AI(2, False, ai_a_depth, ai_a_heur)

while running:
  screen.fill(white)
  # Main menu screen
  if game_state == MENU:
    buttons = main_menu()
    play_rect = buttons[0]
    watch_rect = buttons[1]
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if play_rect.collidepoint(event.pos):
          game_state = SUBMENU_PLAY
        elif watch_rect.collidepoint(event.pos):
          game_state = SUBMENU_WATCH
      pygame.display.update()

  # Play submenu screen
  elif game_state == SUBMENU_PLAY:
    sub_menu(game_state)
    buttons = sub_menu(game_state)
    go_rect = buttons[0]
    bal_heur_rect = buttons[1][0]
    off_heur_rect = buttons[1][1]
    def_heur_rect = buttons[1][2]
    rand_heur_rect = buttons[1][3]
    shal_depth_rect = buttons[2][0]
    norm_depth_rect = buttons[2][1]
    deep_depth_rect = buttons[2][2]
    back_rect = buttons[3]

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if go_rect.collidepoint(event.pos):
          player2 = AI(2, False, ai_a_depth, ai_a_heur)
          game_state = HUMAN_AI
        elif bal_heur_rect.collidepoint(event.pos):
          ai_a_heur = BALANCED
        elif off_heur_rect.collidepoint(event.pos):
          ai_a_heur = OFFENSIVE
        elif def_heur_rect.collidepoint(event.pos):
          ai_a_heur = DEFENSIVE
        elif rand_heur_rect.collidepoint(event.pos):
          ai_a_heur = RANDOM
        elif shal_depth_rect.collidepoint(event.pos):
          ai_a_depth = SHALLOW
        elif norm_depth_rect.collidepoint(event.pos):
          ai_a_depth = NORMAL
        elif deep_depth_rect.collidepoint(event.pos):
          ai_a_depth = DEEP
        elif back_rect.collidepoint(event.pos):
          game_state = DEEP

      pygame.display.update()

  # Watch submenu screen
  elif game_state == SUBMENU_WATCH:
    buttons = sub_menu(game_state)
    go_rect = buttons[0]

    # Options for Bot A
    bal_heur_rect_a = buttons[1][0]
    off_heur_rect_a = buttons[1][1]
    def_heur_rect_a = buttons[1][2]
    rand_heur_rect_a = buttons[1][3]
    shal_depth_rect_a = buttons[2][0]
    norm_depth_rect_a = buttons[2][1]
    deep_depth_rect_a = buttons[2][2]

    # Options for Bot B
    bal_heur_rect_b = buttons[3][0]
    off_heur_rect_b = buttons[3][1]
    def_heur_rect_b = buttons[3][2]
    rand_heur_rect_b = buttons[3][3]
    shal_depth_rect_b = buttons[4][0]
    norm_depth_rect_b = buttons[4][1]
    deep_depth_rect_b = buttons[4][2]

    back_rect = buttons[5]

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if go_rect.collidepoint(event.pos):
          player1 = AI(1, False, ai_b_depth, ai_b_heur)
          player2 = AI(2, False, ai_a_depth, ai_a_heur)
          game_state = AI_AI

        # Options for A
        elif bal_heur_rect_a.collidepoint(event.pos):
          ai_a_heur = BALANCED
        elif off_heur_rect_a.collidepoint(event.pos):
          ai_a_heur = OFFENSIVE
        elif def_heur_rect_a.collidepoint(event.pos):
          ai_a_heur = DEFENSIVE
        elif rand_heur_rect_a.collidepoint(event.pos):
          ai_a_heur = RANDOM
        elif shal_depth_rect_a.collidepoint(event.pos):
          ai_a_depth = SHALLOW
        elif norm_depth_rect_a.collidepoint(event.pos):
          ai_a_depth = NORMAL
        elif deep_depth_rect_a.collidepoint(event.pos):
          ai_a_depth = DEEP
        elif back_rect.collidepoint(event.pos):
          game_state = MENU

        # Options for B
        elif bal_heur_rect_b.collidepoint(event.pos):
          ai_b_heur = BALANCED
        elif off_heur_rect_b.collidepoint(event.pos):
          ai_b_heur = OFFENSIVE
        elif def_heur_rect_b.collidepoint(event.pos):
          ai_b_heur = DEFENSIVE
        elif rand_heur_rect_b.collidepoint(event.pos):
          ai_b_heur = RANDOM
        elif shal_depth_rect_b.collidepoint(event.pos):
          ai_b_depth = SHALLOW
        elif norm_depth_rect_b.collidepoint(event.pos):
          ai_b_depth = NORMAL
        elif deep_depth_rect_b.collidepoint(event.pos):
          ai_b_depth = DEEP

      pygame.dislay.update()


  # Play game scene
  elif game_state == HUMAN_AI:
    game_rects = draw_game_boxes(0, 900)
    try_again = draw_game_text(victory, turn, invalid_move)[0]
    back_rect = draw_game_text(victory, turn, invalid_move)[1]
    pygame.display.update()

    if turn == 1:
      # Human turn
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          # If player has won, if user clicks try again, reinitialize game
          if victory:
            if try_again.collidepoint(event.pos):
              init()
          elif back_rect.collidepoint(event.pos):
            game_state = SUBMENU_PLAY
          else:
            # Check which column was clicked
            for col in range(0, len(game_rects)):
              for rect in game_rects[col]:
                if rect.collidepoint(event.pos):
                  # Add player move to board
                  add = board.add(col, 1)
                  # If valid move, append location
                  if add[0]:
                    invalid_move = False
                    player1_locs.append((add[1], add[2]))
                    # If win, mark victory as true, change turn otherwise
                    if board.check_win(turn)[0]:
                      victory = turn
                      human += 1
                    else:
                      turn = 2
                  else:
                    invalid_move = True

    elif turn == 2:
      # Bot turn
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

      col = player2.next_move(board)
      print board
      add = board.add(col, 2)
      if add[0]:
        invalid_move = False
        player2_locs.append((add[1], add[2]))
        if board.check_win(turn)[0]:
          victory = turn
          ai += 1
          turn = 1
        else:
          turn = 1

  elif game_state == AI_AI:
    game_rects = draw_game_boxes(0, 900)
    try_again = draw_game_text(victory, turn, invalid_move)
    pygame.display.update()

    if turn == 1:
      # Bot a turn
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

      col = player1.next_move(board)
      print board
      add = board.add(col, 1)
      if add[0]:
        invalid_move = False
        player1_locs.append((add[1], add[2]))
        if board.check_win(turn)[0]:
          victory = turn
          human += 1
          turn = 1
        else:
          turn = 2

    elif turn == 2:
      # Bot b turn
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

      col = player2.next_move(board)
      print board
      add = board.add(col, 2)
      if add[0]:
        invalid_move = False
        player2_locs.append((add[1], add[2]))
        if board.check_win(turn)[0]:
          victory = turn
          ai += 1
          turn = 1
        else:
          turn = 1

    pygame.display.update()
