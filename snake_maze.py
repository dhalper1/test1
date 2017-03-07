import pygame
import maze_wall_generator

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0, 0, 255)
PURPLE = (135, 50, 132)

pygame.init()
 
# Set the width and height of the screen [width, height]
screen_width = 700
screen_height = 500
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Snake Game by David M Halpern")

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


segment_size = 16
box_size = 20
table_width = int(screen_width / box_size)
table_height = int(screen_height / box_size)
ending_goal_column = table_width - 1
ending_goal_row = 13 - 1


def draw_grid(box_size):
    for i in range(box_size, screen_width, box_size):
        '''
        pygame.draw.line(screen, WHITE, [i,0], [screen_width , i])
        pygame.draw.line(screen, WHITE, [0,i], [i, screen_height])
        '''
        pygame.draw.line(screen, WHITE, [i,0], [i, screen_height])
        pygame.draw.line(screen, WHITE, [0,i], [screen_width, i])
class Segment(pygame.sprite.Sprite):
    # The class for each segment of our snake
    def __init__(self, delay):
        super().__init__()
        self.image = pygame.Surface([segment_size,segment_size])
        self.image.fill(GREEN)
        
        self.rect = self.image.get_rect()
        self.move_delay = delay
        self.segment_number = delay
        self.direction_x = self.rect.width + int(segment_size / 4)
        self.direction_y = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        
        # The snake starts at the 13th row and in the -1 column.
        self.rect.x = int(segment_size / 4) - (self.rect.width + int(segment_size / 4)) * (self.move_delay) - 2
        self.rect.y = (screen_height - self.rect.height) / 2 #- 2
               
    def update(self):
        # Checking which direction it should go
        if self.left == True:
            self.direction_x = - self.rect.width - int(segment_size / 4)
            self.direction_y = 0
        elif self.up == True:
            self.direction_x = 0
            self.direction_y = - self.rect.width - int(segment_size / 4)
        elif self.down == True:
            self.direction_x = 0
            self.direction_y = self.rect.width + int(segment_size / 4)
        elif self.right == True:
            self.direction_x = self.rect.width + int(segment_size / 4)
            self.direction_y = 0
        
        # Taking on the right, up, down, and left variables of the segment in front of it, so it can move in the same way but one frame after.
        segment_list[self.segment_number].right = segment_list[self.segment_number - 1].right
        segment_list[self.segment_number].down = segment_list[self.segment_number - 1].down
        segment_list[self.segment_number].left = segment_list[self.segment_number - 1].left
        segment_list[self.segment_number].up = segment_list[self.segment_number - 1].up        
        
        
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y

        

class Head_segment(Segment):
    # The head is a sub-class of segment.
    def __init__(self, delay):
        super().__init__(delay)
        self.image.fill(GREEN)
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.segment_number = 0
        self.last_direction_right = True
        self.last_direction_down = False
        self.last_direction_left = False
        self.last_direction_up = False
        
    def update(self):
        # The head has a different update than segment because it has to learn when to turn from the keys instead of the segment in front of it.
        if self.left == True:
            self.direction_x = - self.rect.width - int(segment_size / 4)
            self.direction_y = 0
            self.last_direction_left = True
            self.last_direction_right = False
            self.last_direction_down = False
            self.last_direction_up = False            
        elif self.up == True:
            self.direction_x = 0
            self.direction_y = - self.rect.width - int(segment_size / 4)
            self.last_direction_right = False
            self.last_direction_down = False
            self.last_direction_left = False
            self.last_direction_up = True         
        elif self.down == True:
            self.direction_x = 0
            self.direction_y = self.rect.width + int(segment_size / 4)
            self.last_direction_right = False
            self.last_direction_down = True
            self.last_direction_left = False
            self.last_direction_up = False            
        elif self.right == True:
            self.direction_x = self.rect.width + int(segment_size / 4)
            self.direction_y = 0
            self.last_direction_right = True
            self.last_direction_down = False
            self.last_direction_left = False
            self.last_direction_up = False            
            
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y

class Bad_block(pygame.sprite.Sprite):
    def __init__(self, table_row, table_column):
        super().__init__()
        self.image = pygame.Surface([box_size, box_size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        self.rect.x = table_column * box_size
        self.rect.y = table_row * box_size

class End_goal(Bad_block):
    def __init__(self, table_row, table_column):
        super().__init__(table_row, table_column)
        self.image.fill(BLUE)
     
def add_new_segment():
    # A function that creates a new segment for our snake
    segment = Segment(number_of_segments)
    segment_list.append(segment)
    segment_group.add(segment)
    all_sprites_group.add(segment)
    # Assigns the starting direction of our new segment
    if segment_list[number_of_segments - 1].direction_x != 0:
        segment_list[number_of_segments].rect.x = segment_list[number_of_segments - 1].rect.x + (-1 * (int(segment_list[number_of_segments - 1].direction_x / abs(segment_list[number_of_segments - 1].direction_x)))) * (segment.rect.width + int(segment_size / 4))
    else:
        segment_list[number_of_segments].rect.x = segment_list[number_of_segments - 1].rect.x
    if segment_list[number_of_segments - 1].direction_y != 0:
        segment_list[number_of_segments].rect.y = segment_list[number_of_segments - 1].rect.y + (-1 * (int(segment_list[number_of_segments - 1].direction_y / abs(segment_list[number_of_segments - 1].direction_y)))) * (segment.rect.height + int(segment_size / 4))
    else:
        segment_list[number_of_segments].rect.y = segment_list[number_of_segments - 1].rect.y   
    segment_list[number_of_segments].direction_x = segment_list[number_of_segments - 1].direction_x
    segment_list[number_of_segments].direction_y = segment_list[number_of_segments - 1].direction_y

def intro_screen():
    # The intro screen
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    #intro_font = pygame.font.SysFont(None, 50, True, False)
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # For done and superdone
                return True, True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False, False
    
     
        # --- Game logic should go here
    
        # --- Screen-clearing code goes here
        screen.fill(BLACK)
        
        
        bad_block_group.draw(screen)
        end_goal_group.draw(screen)
        
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(10)
score = 0
super_done = False
while not super_done:
    number_of_segments = 0
    segment_group = pygame.sprite.Group()
    segment_list = []
    all_sprites_group = pygame.sprite.Group()
    collectibles_group = pygame.sprite.Group()
    bad_block_group = pygame.sprite.Group()
    end_goal_group = pygame.sprite.Group()
    # The snake will start with 8 segments
    starting_number_of_segments = 8
    
    # Creating the head segment
    head_segment = Head_segment(0)
    segment_group.add(head_segment)
    segment_list.append(head_segment)
    all_sprites_group.add(head_segment)
    
    
    table, number_of_ones = maze_wall_generator.create_map()
    print(number_of_ones)
    
    for i in range(len(table)):
        for s in range(len(table[i])):
            if table[i][s] == 1:
                bad_block = Bad_block(i,s)
                bad_block_group.add(bad_block)
                all_sprites_group.add(bad_block)
    
    end_goal = End_goal(ending_goal_row, ending_goal_column)
    end_goal_group.add(end_goal)
    all_sprites_group.add(end_goal)
    
    # Creating the rest of the snake
    for i in range(1,starting_number_of_segments):
        number_of_segments += 1
        segment = Segment(i)
        segment_group.add(segment)
        segment_list.append(segment)
        all_sprites_group.add(segment)
    
    
    super_done,done = intro_screen()
    while not done:
                # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                super_done = True
            elif event.type == pygame.KEYDOWN:
                # For each movement, I only change the direction of the head segment.  And the rest of the segments will check on the one in front of it.
                if event.key == pygame.K_RIGHT:
                    if head_segment.last_direction_left != True:
                        
                        head_segment.right = True
                        head_segment.down = False
                        head_segment.up = False
                        head_segment.left = False
    
                elif event.key == pygame.K_DOWN:
                    if head_segment.last_direction_up != True:
                        
                        head_segment.right = False
                        head_segment.down = True
                        head_segment.up = False
                        head_segment.left = False
        
                elif event.key == pygame.K_LEFT:
                    if head_segment.last_direction_right != True:
                        
                        head_segment.left = True
                        head_segment.down = False
                        head_segment.up = False
                        head_segment.right = False                
        
                elif event.key == pygame.K_UP:
                    if head_segment.last_direction_down != True:
                        
                        head_segment.up = True
                        head_segment.down = False
                        head_segment.right = False
                        head_segment.left = False           
    
                    
    
        # --- Game logic should go here
        # I need the segments to update in order so they don't mess up.
        for i in range(len(segment_list) - 1,-1,-1):
            segment_list[i].update()
        
        head_collide = pygame.sprite.groupcollide(bad_block_group, segment_group, False, True)
            
        goal_hit = pygame.sprite.spritecollide(end_goal, segment_group, False)
        
        for item in head_collide:
            number_of_segments -= 1
            if number_of_segments == 0:
                done = True
                #super_done = True
                print("Your final score is", score)
                
                #super_done = False
                score = 0
                
            
        for item in goal_hit:
            done = True
            score += number_of_ones
    
        screen.fill(BLACK)
                     
        # --- Drawing code should go here
        segment_group.draw(screen)
        bad_block_group.draw(screen)
        end_goal_group.draw(screen)
        #draw_grid(20) # using 20 x 20 box sizes.  The total grid is 35 x 25.
        
        pygame.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(6)
pygame.quit()