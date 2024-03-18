import sys
import pygame
from pygame.locals import QUIT
import math
import random
import time


def notpos(grid, x, y):
  s = set()
  for i in range(cells):
    if not y == i:
      s.add(grid[x][i])
    if not x == i:
      s.add(grid[i][y])
  for i in range(box):
    for j in range(box):
      x0 = x - x % box + i
      y0 = y - y % box + j
      if x0 == x and y0 == y:
        continue
      s.add(grid[x0][y0])
  s.discard(0)
  return s


def check_filled():
  for i in range(cells):
    for j in range(cells):
      if grid[i][j] == 0:
        return False
  return True


def check_grid():
  for i in range(cells):
    for j in range(cells):
      if grid[i][j] in notpos(grid, i, j):
        return False
  return True


def make_vis():

  fcells = (cells**2 // 2) - 1
  counter = 0

  while counter < fcells:
    x = random.randint(0, cells - 1)
    y = random.randint(0, cells - 1)
    if vis_cells[x][y] == 1:
      continue
    vis_cells[x][y] = 1
    grid[x][y] = og_grid[x][y]
    counter += 1


def fill():
  for i in range(cells):
    for j in range(cells):
      if og_grid[i][j] == 0:
        numbers = list(range(1, cells + 1))
        random.shuffle(numbers)
        for num in numbers:
          if num not in notpos(og_grid, i, j):
            og_grid[i][j] = num
            if fill():
              return True
            og_grid[i][j] = 0
        return False
  return True


def make_grid(WIN, myfont):
  buffer = 10
  color = (38, 38, 38)
  for i in range(1, cells):
    if i % box == 0:
      pygame.draw.line(WIN, color, (0, dif * i), (DIM, dif * i), 1)
      pygame.draw.line(WIN, color, (dif * i, 0), (dif * i, DIM), 1)
    for z in range(cells):
      pygame.draw.line(WIN, color, (dif * z + buffer, dif * i),
                       (dif * (z + 1) - buffer, dif * i), 1)
      pygame.draw.line(WIN, color, (dif * i, dif * z + buffer),
                       (dif * i, dif * (z + 1) - buffer), 1)


def make_board(WIN, myfont):

  buffer = 3

  for i in range(cells):
    for j in range(cells):
      if grid[i][j] != 0 and vis_cells[i][j] == 0:
        value = myfont.render(str(grid[i][j]), True, (0, 0, 0))
      elif grid[i][j] != 0 and vis_cells[i][j] == 1:
        value = myfont.render(str(grid[i][j]), True, (0, 0, 0))
        pygame.draw.rect(WIN, (111, 162, 237),
                         (j * dif, i * dif, dif + 1, dif + 1))
      else:
        continue
      WIN.blit(value, (dif * j + (120 / cells), dif * i + (48 / cells)))

  make_grid(WIN, myfont)
  pygame.display.update()


def option_screen(WIN, myfont, button1Pos, button2Pos, buttonWidth,
                  buttonHeight):

  value = myfont.render("SUDOKU", True, (0, 0, 0))
  WIN.blit(value, (70, 75))

  pygame.draw.rect(WIN, (199, 163, 255),
                   (button1Pos[0], button1Pos[1], buttonWidth, buttonHeight))
  pygame.draw.rect(WIN, (199, 163, 255),
                   (button2Pos[0], button2Pos[1], buttonWidth, buttonHeight))

  myfont = pygame.font.SysFont("Segoe UI Black", 40)

  value = myfont.render("4 x 4", True, (0, 0, 0))
  WIN.blit(value, (button1Pos[0] + 70, button1Pos[1] + 15))

  value = myfont.render("9 x 9", True, (0, 0, 0))
  WIN.blit(value, (button2Pos[0] + 70, button2Pos[1] + 15))

  pygame.display.update()


def won(WIN, cancelPos, tryAgainPos, bWidth, bHeight):
  myfont = pygame.font.SysFont("Arial", 14)

  pygame.draw.rect(WIN, (33, 33, 33), (80, 162, 240, 96))
  pygame.draw.rect(WIN, (199, 163, 255),
                   (cancelPos[0], cancelPos[1], bWidth, bHeight))
  pygame.draw.rect(WIN, (199, 163, 255),
                   (tryAgainPos[0], tryAgainPos[1], bWidth, bHeight))

  value = myfont.render("Congrats! Try again?", True, (255, 255, 255))
  WIN.blit(value, (125, 180))
  value = myfont.render("Cancel", True, (0, 0, 0))
  WIN.blit(value, (119, 222))
  value = myfont.render("Try again", True, (0, 0, 0))
  WIN.blit(value, (222, 222))

  pygame.display.update()


def insert(WIN, pos):
  i, j = int(pos[1] / dif), int(pos[0] / dif)
  myfont = pygame.font.SysFont("monospace", 270 // cells)
  if vis_cells[i][j] == 1:
    return
  buffer = 6
  pygame.draw.rect(WIN, (2, 79, 194),
                   (j * dif + buffer, i * dif + buffer, dif + 1 - buffer * 2,
                    dif + 1 - buffer * 2))
  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        return
      if event.type == pygame.KEYDOWN:
        num = event.key - 48
        if event.key == 48:
          grid[i][j] = 0
          pygame.draw.rect(WIN, (255, 255, 255),
                           (j * dif + buffer, i * dif + buffer,
                            dif + 1 - buffer * 2, dif + 1 - buffer * 2))
          pygame.display.update()
        if (1 <= num <= cells):
          grid[i][j] = num
          pygame.draw.rect(WIN, (255, 255, 255),
                           (j * dif + buffer, i * dif + buffer,
                            dif + 1 - buffer * 2, dif + 1 - buffer * 2))
          value = myfont.render(str(event.key - 48), True, (1, 56, 138))
          WIN.blit(value, (dif * j + (120 / cells), dif * i + (48 / cells)))
          pygame.display.update()
        return


def main():

  global DIM, cells, box, dif, og_grid, grid, vis_cells

  DIM = 400
  again = True

  pygame.init()
  WIN = pygame.display.set_mode((DIM, DIM))
  pygame.display.set_caption('Sudoku')
  clock = pygame.time.Clock()

  #option screen

  while again:
    again = False
    WIN.fill((114, 23, 255))
    myfont = pygame.font.SysFont("Segoe UI Black", 90)

    button1Pos, button2Pos, buttonWidth, buttonHeight = (100,
                                                         190), (100,
                                                                285), 200, 57

    option_screen(WIN, myfont, button1Pos, button2Pos, buttonWidth,
                  buttonHeight)

    run = True
    while run:
      clock.tick(60)
      for event in pygame.event.get():

        if event.type == QUIT:
          run = False
          break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
          pos = pygame.mouse.get_pos()

          if pos[0] > button1Pos[0] and pos[
              0] < button1Pos[0] + buttonWidth and pos[1] > button1Pos[
                  1] and pos[1] < button1Pos[1] + buttonHeight:
            cells = 4
            run = False
            break
          elif pos[0] > button2Pos[0] and pos[
              0] < button2Pos[0] + buttonWidth and pos[1] > button2Pos[
                  1] and pos[1] < button2Pos[1] + buttonHeight:
            cells = 9
            run = False
            break

    #grid screen

    box = int(math.sqrt(cells))
    dif = DIM / cells
    og_grid = [[0 for x in range(cells)] for y in range(cells)]
    grid = [[0 for x in range(cells)] for y in range(cells)]
    vis_cells = [[0 for x in range(cells)] for y in range(cells)]
    win_screen = False

    myfont = pygame.font.SysFont("monospace", 270 // cells)
    WIN.fill((255, 255, 255))

    fill()
    make_vis()
    make_board(WIN, myfont)

    run = True
    while run:
      clock.tick(60)
      if check_filled():
        if not check_grid():
          WIN.fill((255, 99, 99))
          make_board(WIN, myfont)
        else:
          WIN.fill((82, 255, 119))
          make_board(WIN, myfont)
          win_screen = True
          run = False
          break
      for event in pygame.event.get():
        if event.type == QUIT:
          run = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
          pos = pygame.mouse.get_pos()
          insert(WIN, pos)

    #win_screen

    if win_screen:
      cancelPos, tryAgainPos, bWidth, bHeight = (96, 215), (208, 215), 96, 30

      won(WIN, cancelPos, tryAgainPos, bWidth, bHeight)

      while win_screen:
        clock.tick(60)

        for event in pygame.event.get():
          if event.type == QUIT:
            win_screen = False
          elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if pos[0] > cancelPos[0] and pos[0] < cancelPos[0] + bWidth and pos[
                1] > cancelPos[1] and pos[1] < cancelPos[1] + bHeight:
              win_screen = False
              break
            elif pos[0] > tryAgainPos[0] and pos[
                0] < tryAgainPos[0] + bWidth and pos[1] > tryAgainPos[
                    1] and pos[1] < tryAgainPos[1] + bHeight:
              again = True
              win_screen = False
              break

  pygame.quit()


main()
