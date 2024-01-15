#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
import pygame
import random
from astar import astar

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255,   0)

GRID_WIDTH = 11  # Fewer cells, but each cell is larger
GRID_HEIGHT = 11
CELL_SIZE = 40  # Size of each cell (room)
PATH_WIDTH = 30 # Width of the paths

Trollicon=pygame.image.load('images/Trollman.png')
pygame.display.set_icon(Trollicon)

#Add music
pygame.mixer.init()
pygame.mixer.music.load('pacman.mp3')
pygame.mixer.music.play(-1, 0.0)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

def setupRoomOne(all_sprites_list):
    # Initialize all cells as walls
    # Initialize all cells as walls
    grid = [[True for _ in range(GRID_WIDTH * 2 + 1)] for _ in range(GRID_HEIGHT * 2 + 1)]

    def remove_wall_between(current, next):
        x1, y1 = current
        x2, y2 = next
        grid[x1][y1] = False
        grid[x2][y2] = False
        grid[(x1 + x2) // 2][(y1 + y2) // 2] = False

    def visit_cell(start_x, start_y):
        stack = [(start_x, start_y)]
        grid[start_x][start_y] = False

        while stack:
            x, y = stack[-1]
            neighbors = []

            # Check for unvisited neighbors
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny]:
                    neighbors.append((nx, ny))

            if neighbors:
                next_x, next_y = random.choice(neighbors)
                remove_wall_between((x, y), (next_x, next_y))
                stack.append((next_x, next_y))
            else:
                stack.pop()

    # Start the maze generation from a random cell
    start_x = random.randrange(1, GRID_WIDTH * 2, 2)
    start_y = random.randrange(1, GRID_HEIGHT * 2, 2)
    visit_cell(start_x, start_y)

    # Create wall objects based on the grid
    wall_list = pygame.sprite.RenderPlain()
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y]:  # If the cell is a wall
                # Correctly calculate the position and size of each wall segment
                wall_x = x * (CELL_SIZE + PATH_WIDTH) // 2
                wall_y = y * (CELL_SIZE + PATH_WIDTH) // 2
                wall = Wall(wall_x, wall_y, PATH_WIDTH, PATH_WIDTH, blue)
                wall_list.add(wall)
                all_sprites_list.add(wall)

    return wall_list, grid

def get_open_spaces(grid):
    open_spaces = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if not grid[x][y]:  # If the cell is not a wall
                open_spaces.append((x, y))
    return open_spaces

def mark_space_as_occupied(grid, position):
    x, y = position
    grid[x][y] = True  # Marking the space as occupied

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

ghost_list = []
#Inheritime Player klassist
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x606 sized screen
screen = pygame.display.set_mode([806, 806])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)



clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#default locations for Pacman and monstas
w = 303-16 #Width
p_h = (7*60)+19 #Pacman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Binky height
i_w = 303-16-32 #Inky width
c_w = 303+(32-16) #Clyde width

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list, grid = setupRoomOne(all_sprites_list)
  open_spaces = get_open_spaces(grid)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  pacman_pos = random.choice(open_spaces)
  Pacman = Player(pacman_pos[0] * (CELL_SIZE + PATH_WIDTH) // 2, pacman_pos[1] * (CELL_SIZE + PATH_WIDTH) // 2, "images/Trollman.png")
  mark_space_as_occupied(grid, pacman_pos)
  open_spaces.remove(pacman_pos)
  # Create the player paddle object
  #Pacman = Player( w, p_h, "images/Trollman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  spawn_ghosts(all_sprites_list, monsta_list, grid, open_spaces, pacman_pos)

  last_spawn_time = pygame.time.get_ticks()

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  done = False

  i = 0

  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-10,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(10,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-10)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,10)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(10,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-10,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,10)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-10)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)

      current_time = pygame.time.get_ticks()
      if current_time - last_spawn_time >= 10000:  # 60 seconds
          
          if spawn_ghosts(all_sprites_list, monsta_list, grid, open_spaces, pacman_pos, limit=1):
            last_spawn_time = current_time

      # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      for gho in ghost_list:
        ghost_grid_pos = game_position_to_grid((gho.rect.x, gho.rect.y))
        pacman_grid_pos = game_position_to_grid((Pacman.rect.x, Pacman.rect.y))

        if manhattan_distance(ghost_grid_pos, pacman_grid_pos) <= 10:
          path = astar(grid, ghost_grid_pos, pacman_grid_pos)
          if path:
              # Move the ghost along the path
              next_step = path[1]  # Get the next step towards Pacman
              next_game_pos = grid_position_to_game(next_step)
              # Update ghost position
              gho.rect.x, gho.rect.y = next_game_pos

      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      if score == bll:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def is_pacman_in_range(ghost_pos, pacman_pos, range=10):
    return manhattan_distance(ghost_pos, pacman_pos) <= range

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def spawn_ghosts(all_sprites_list, monsta_list, grid, open_spaces, pacman_pos, limit=None):
    available_positions = [pos for pos in open_spaces if manhattan_distance(pos, pacman_pos) >= 10]
    if not available_positions:
        return False
    ghost_pos = random.choice(available_positions)
    # Initialize Ghost here...
    Ghosty = Ghost(ghost_pos[0]* (CELL_SIZE + PATH_WIDTH) // 2, ghost_pos[1]* (CELL_SIZE + PATH_WIDTH) // 2, "images/Pinky.png")  # Replace with actual ghost image
    monsta_list.add(Ghosty)
    all_sprites_list.add(Ghosty)
    mark_space_as_occupied(grid, ghost_pos)
    open_spaces.remove(ghost_pos)
    available_positions.remove(ghost_pos)
    ghost_list.append(Ghosty)

    return True

def game_position_to_grid(position):
    """Converts game (pixel) position to grid position."""
    x, y = position
    grid_x = x // (CELL_SIZE + PATH_WIDTH)
    grid_y = y // (CELL_SIZE + PATH_WIDTH)
    return (grid_x, grid_y)

def grid_position_to_game(position):
    """Converts grid position back to game (pixel) position."""
    grid_x, grid_y = position
    x = grid_x * (CELL_SIZE + PATH_WIDTH)
    y = grid_y * (CELL_SIZE + PATH_WIDTH)
    return (x, y)

def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()