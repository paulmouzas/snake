import random
import pygame

class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())
    
    def Update(self):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0,0,0))
        pygame.font.init()
        font = pygame.font.SysFont('helvetica', 32)
        text = font.render("Press Space To Start", 1, (255,255,255))
        screen.blit(text, (100,100))
        



class Block(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((30, 30))
        
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        
        self.score = 0
        
        lose = False
        
        x_pos = 0
        
        self.blocks = pygame.sprite.Group()
        self.block_list = []
        
        self.old_head = []
        self.new_head = []
        
        self.x = 0
        self.y = 0

        self.x_speed = 32
        self.y_speed = 0
        
        for block in range(5):
            x_pos += 32
            block = Block(x_pos,0)
            self.blocks.add(block)
            self.block_list.append(block)
        
        self.foods = pygame.sprite.Group()
        num = random.randint(0,465)
        self.food = Food(num,num)
        self.foods.add(self.food)
        
    def ProcessInput(self, events, pressed_keys):
    
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not self.y_speed == 32:
                        self.x_speed = 0
                        self.y_speed = -(32)
                elif event.key == pygame.K_DOWN:
                    if not self.y_speed == -32:
                        self.x_speed = 0
                        self.y_speed = 32
                elif event.key == pygame.K_LEFT:
                    if not self.x_speed == 32:
                        self.x_speed = -(32)
                        self.y_speed = 0
                elif event.key == pygame.K_RIGHT:
                    if not self.x_speed == -32:
                        self.x_speed = 32
                        self.y_speed = 0
        
    def Update(self):
        self.old_head = self.block_list.pop(0)
        self.blocks.remove(self.old_head)
        
        
        self.x = self.block_list[-1].rect.x + self.x_speed
        self.y = self.block_list[-1].rect.y + self.y_speed
        
        self.new_head = Block(self.x,self.y)
        
        self.block_list.append(self.new_head)
        self.blocks.add(self.new_head)
        
        if self.lose():
            self.Terminate()
        
        if pygame.sprite.collide_rect(self.food, self.new_head):
            self.updateScore()
            self.foods.empty()
            num = random.randint(0,465)
            self.food = Food(num,num)
            self.foods.add(self.food)
            
            x = self.block_list[-1].rect.x
            y = self.block_list[-1].rect.y
            new_tail = Block(x,y)
            self.block_list.insert(-1,new_tail)
            self.blocks.add(new_tail)
            

            
    def Render(self, screen):
        
        screen.fill((0, 0, 0))
        self.blocks.draw(screen)
        self.foods.draw(screen)
        font = pygame.font.SysFont('helvetica', 16)
        text = font.render("%s" % self.score, 1, (255,255,255))
        screen.blit(text, (10,450))
        
    def lose(self):
        copy = self.block_list[:]
        head = copy.pop(-1)
        
        for block in copy:
            if block.rect.x == head.rect.x and block.rect.y == head.rect.y:
                self.SwitchToScene(TitleScene())
                
        if self.new_head.rect.x < 0 or self.new_head.rect.x >= 465 or self.new_head.rect.y < 0 or self.new_head.rect.y >= 465:
            self.SwitchToScene(TitleScene())
        return False
        
    def updateScore(self):
    
        self.score += 1
        
class Food(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        #self.image = pygame.Surface((15,15))
        
        #self.image.fill((255,0,0))
        #self.rect = self.image.get_rect()
        self.image = pygame.image.load('food.png')
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        

        
run_game(480,480,8,TitleScene())