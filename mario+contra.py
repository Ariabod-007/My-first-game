
import pygame
pygame.init()
# settings:
level_map =[
'X                           ',
'X                           ',
'X                           ',
'X                           ',
'X                           ',
'X                           ',
'X                           ',
'X P      1  X               ',
'XYYYYYYYYYY X               ',
'X       3   X4  4  3  4     ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXX']
tile_size = (64,64)
roof_size = (64,32)
screen_width=1200
screen_height=len(level_map)*tile_size[0]
screen=pygame.display.set_mode((screen_width,screen_height))
print(screen_height)
# player:
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,width,height):
        super().__init__()
        self.size = [width,height]
        self.image = pygame.Surface(self.size)
        self.image.fill('blue')
        self.status='crouch'
        #self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect(topleft=pos)
        #ready variables:
        self.ready_jump = True
        self.ready_shoot = True
        self.ready_dg = True
        ###
        #extra variables:
        
        self.max_health = 100
        self.current_health = 3
        #
        self.recharge_time_jump = 1000
        self.jump_time = 0
        self.shoot_time = 0
        self.dg_time = 0
        #recharges:
        self.recharge_time_shoot = 300
        self.recharge_time_dg = 4000
        self.look_dir = 'right'
        #bullet group:
        self.bullet = pygame.sprite.Group()
        #player movement
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 1
        self.jump_speed = -20
        #status
        self.on_ground = False
        self.on_cilling = False
        self.on_right = False
        self.on_left = False
        self.crouched = False
        
    def getting_dg(self):
        for enemy in game.level.enemy:
            if pygame.sprite.collide_rect(self,enemy):
                if self.vel_y > 0 and self.rect.bottom > enemy.rect.top:
                    enemy.kill()
                    self.vel_y = -20
                else:
                    if self.ready_dg:
                        self.dg_time = pygame.time.get_ticks()
                        self.ready_dg = False
                        self.current_health -= 1
                        self.vel_y = self.jump_speed
                        self.rect.x -= 10
            
    def apply_gravity(self):
        self.vel_y += self.gravity
    def animation(self):
        self.image = pygame.Surface(self.size)
        self.image.fill('blue')
        
        if self.status =='stand':
            self.size = [32,64]

        elif self.status == 'crouch':
            self.size = [64,32]
        ######rects:
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            
        elif self.on_cilling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_cilling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_cilling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def jump(self):
        if self.ready_jump:
            self.vel_y = self.jump_speed
            self.ready_jump = False
            self.jump_time = pygame.time.get_ticks()
            
    def shoot(self):
        if self.ready_shoot:
            bullet = p_Bullet(self.rect.center,self.look_dir)
            self.bullet.add(bullet)
            self.ready_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    def recharge(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.shoot_time >= self.recharge_time_shoot:
            self.ready_shoot = True
        if self.current_time - self.dg_time >= self.recharge_time_dg:
            self.ready_dg = True
    def get_input(self):
        keys = pygame.key.get_pressed()
        '''if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.vel_x = 1
            self.look_dir = 'right_down'
            print('shoot')
            self.shoot()
        elif keys[pygame.K_LEFT]and keys[pygame.K_DOWN]:
            self.vel_x = -1
            self.look_dir = 'left_down'
            print('shoot')
            self.shoot()'''
        if keys[pygame.K_DOWN]:
            if keys[pygame.K_RIGHT]:
                self.vel_x=1
                self.look_dir ='right_down'
            elif keys[pygame.K_LEFT]:
                self.vel_x=-1
                self.look_dir ='left_down'
            else:
                self.vel_x=0
                self.status = 'crouch'
        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]:
            self.vel_x=1
            self.look_dir='right'
        if keys[pygame.K_LEFT] and not keys[pygame.K_DOWN]:
            self.vel_x=-1
            self.look_dir='left'
        
        if not keys[pygame.K_DOWN]:
            self.status = 'stand'
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.vel_x=0
        
        if keys[pygame.K_UP]:
            self.jump()
            self.status = 'stand'
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        if self.status=='crouch':
            self.vel_x=0
            '''if 'right' in self.look_dir:
                self.look_dir = 'right'
            elif 'left' in self.look_dir:
                self.look_dir = 'left'''
    def update(self,x_shift):
        self.animation()
        self.get_input()
        self.getting_dg()
        self.apply_gravity()
        self.recharge()

        #bullet update:
        self.bullet.update(x_shift)
        self.bullet.draw(screen)
# tiles:
class Tile(pygame.sprite.Sprite):
    color = 'gray'
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self,x_shift):
        self.rect.x += x_shift
#gates:
class Gate(pygame.sprite.Sprite):
    color = 'pink'
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
    def update(self,x_shift):
        self.rect.x += x_shift
######shelters
class Shelter(Tile):
    color ='brown'
    
#limiter:
class Limit(Tile):
    pass
#ui
class UI:
    def __init__(self,surface):
        self.display_surface = surface
        self.health_bar = pygame.Surface((200,50))
        self.coin = pygame.Surface((12,12))
    def show_health(self):
        self.display_surface.blit(self.health_bar,(0,0))
    def show_coins(self):
        pass
#Icon design:
class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
#overworld design:
class Overworld:
    def __init__(self,menu_data):
        #icons:
        self.icon = pygame.sprite.Group()
        self.x_shift = 0
        self.y_shift = 0
        self.setup_world(menu_data)
        
    def setup_world(self,menu_data):
        x = 100
        y = 50
        for i in range (0,menu_data,1):
            icon = Icon((x,y))
            self.icon.add(icon)
            if x + 180 >= screen_width:
                y += 100
                x=100
            else:
                x += 80
    def run(self):
        screen.fill('gray')
        self.icon.draw(screen)
#level design:
class Level:
    def __init__(self,level_data,surface):
        self.x_shift = 0
        self.display_surface = surface
        self.setup_level(level_data)
        self.current_x = 0
    def setup_level(self,layout):
        #anything elsee group:
        self.others = pygame.sprite.Group()
        ###
        self.enemy_bullet = pygame.sprite.Group()
        #tiles management:
        self.tiles = pygame.sprite.Group()
        self.roofs = pygame.sprite.Group()
        self.all_tiles = pygame.sprite.Group()
        #####
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.gate = pygame.sprite.GroupSingle()
        self.shelter = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size[0]
                y = row_index * tile_size[0]
                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                    self.all_tiles.add(tile)
                    self.others.add(tile)
                if cell == 'Y':
                    roof = Tile((x,y),roof_size)
                    self.roofs.add(roof)
                    self.all_tiles.add(roof)
                    self.others.add(roof)
                    
                if cell =='S':
                    shelter = Shelter((x,y),tile_size)
                    self.shelter.add(shelter)
                    self.others.add(shelter)
                if cell == 'G':
                    gate = Gate((x,y),tile_size)
                    self.gate.add(gate)
                    self.others.add(gate)
                if cell == 'P':
                    player = Player((x,y),32,64)
                    self.player.add(player)
                        
                if cell == '1':
                    enemy = Enemy1((x,y))
                    self.enemy.add(enemy)
                if cell == '2':
                    enemy = Enemy2((x,y))
                    self.enemy.add(enemy)
                if cell == '3':
                    enemy = Enemy3((x,y))
                    self.enemy.add(enemy)
                if cell == '4':
                    enemy = Enemy4((x,y))
                    self.enemy.add(enemy)
                
    def player_hort(self):
        player = self.player.sprite
        player.rect.x += player.vel_x * 5

        for sprite in self.tiles:
            if player.rect.colliderect(sprite.rect):
                if player.vel_x > 0 or self.x_shift <0:
                    player.rect.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = player.rect.right
                elif player.vel_x < 0 or self.x_shift >0:
                    player.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = player.rect.left
                    
        if player.on_right and (player.rect.right>self.current_x or player.vel_x<=0):
            player.on_right = False
        if player.on_left and (player.rect.left<self.current_x or player.vel_x>=0):
            player.on_left = False
    def player_vert(self):
        player = self.player.sprite
        player.rect.y += player.vel_y
        for sprite in self.all_tiles:
            if player.rect.colliderect(sprite.rect):
                # falling to a tile:
                if player.vel_y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.vel_y = 0
                    player.ready_jump = True
                    player.on_ground = True
                # heating to a tile from bottom:
        for sprite in self.tiles:
            if player.rect.colliderect(sprite.rect):
                if player.vel_y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.vel_y =1
                    player.on_cilling = True
                    
        if player.on_ground and player.vel_y<0 or player.vel_y>1:
            player.on_ground = False
        if player.on_cilling and player.vel_y>0:
            player.on_cilling = False
    def camera(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        
        if player_x < screen_width/2 and player.vel_x<0:
            player.vel_x =0
            self.x_shift = 5
        elif player_x > screen_width/2 and player.vel_x>0:
            player.vel_x =0
            self.x_shift = -5
        else:
            self.x_shift = 0
    def enemy_movement(self):
        for sprite in self.enemy.sprites():
            if pygame.sprite.spritecollide(sprite,self.limit,False):
                sprite.reverse()
        '''for enemy in self.enemy.sprites():
            for tile in self.tiles.sprites():
                if enemy.rect.colliderect(tile.rect):
                    if enemy.rect.right >= tile.rect.right:
                        enemy.reverse()
                    elif enemy.rect.left <= tile.rect.left:
                        enemy.reverse()'''
    
    def run(self):
        
        #updates
        self.others.update(self.x_shift)
        self.enemy.update(self.x_shift)
        self.enemy_bullet.update(self.x_shift)
        self.player.update(self.x_shift)
        self.camera()
        self.player_hort()
        self.player_vert()
        
        
        #self.enemy_movement()
        
        #draw
        '''self.tiles.draw(self.display_surface)
        self.gate.draw(self.display_surface)
        self.shelter.draw(self.display_surface)'''
        self.others.draw(self.display_surface)
        
        self.enemy.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.enemy_bullet.draw(screen)
# bullet:
class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,look_dir='right'):
        super().__init__()
        self.image = pygame.Surface((15,4))
        self.image.fill('pink')
        self.look_dir = look_dir
        self.rect = self.image.get_rect(center = pos)
        self.speedx = 0
        self.speedy = 0
    def death(self):
        if self.rect.x > screen_width or self.rect.x <0:
            self.kill()
        if pygame.sprite.spritecollide(self,game.level.tiles,False):
            self.kill()
            
    def dir(self):
        if 'right' in self.look_dir:
            self.speedx=12
        if 'left' in self.look_dir:
            self.speedx=-12
        if 'down' in self.look_dir:
            self.speedy=5
    def update(self,x_shift):
        self.rect.x += self.speedx
        #self.rect.x += x_shift
        self.rect.y += self.speedy
        self.death()
        self.dir()
#player bullets:
class p_Bullet(Bullet):
    def death(self):
        super().death()
        for i in game.level.enemy:
            if pygame.sprite.collide_rect(self,i):
                i.health -=1
                self.kill()
#enemy bullets:
class e_Bullet(Bullet):
    def death(self):
        super().death()
        if pygame.sprite.spritecollide(self,game.level.player,False):
            self.kill()
#enemy:
class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = pos)
        self.gravity = 1
        self.wall_collide = False
    def pathfind(self):
        self.rect.x+=self.vel_x* self.speed
        if pygame.sprite.spritecollide(self,game.level.all_tiles,False):
            self.move_able = False
            self.wall_collide=True
        else:
            self.wall_collide = False
        if not self.wall_collide:
            self.rect.y += self.size[1]
                        
            if pygame.sprite.spritecollide(self,game.level.all_tiles,False):
                self.move_able = True
            else:
                self.move_able = False
                     
            self.rect.y -= self.size[1]
        self.rect.x -= self.vel_x*self.speed
        ###
        
    def death(self):
        if self.health <= 0:
            self.kill()
            
    def update(self,x_shift):
        self.rect.x += x_shift
        self.death()
        self.pathfind()
#enemy 1:
class Enemy1(Enemy):
    color = 'red'
    size = (32,64)
    health = 3
    kind = 1
    vel_x = 1
    vel_y = 0
    speed = 3
    move_able = False
    def move(self):
        if self.move_able:
            self.rect.x += self.vel_x * self.speed
            self.rect.y += self.vel_y
        else:
            self.reverse()
        
    def reverse(self):
        self.vel_x*=-1

    def update(self,x_shift):
        super().update(x_shift)
        
        self.move()
       
class Enemy2(Enemy):
    color = 'yellow'
    size = (32,64)
    kind = 2
    vel_x = 0
    vel_y = 0
    speed = 2
    health = 4
    move_able = False
    def tactics(self):
        if self.move_able:
            player = game.level.player.sprite
            if player.rect.x - self.rect.x <=400 and player.rect.x - self.rect.x>=0 and ((player.rect.top >self.rect.top and player.rect.top -self.rect.top<=25) or (player.rect.top <self.rect.top and self.rect.top -player.rect.top<=25)):
                self.vel_x = 1
            if self.rect.x - player.rect.x <= 400 and self.rect.x - player.rect.x >=0 and ((player.rect.top >self.rect.top and player.rect.top -self.rect.top<=25) or (player.rect.top <self.rect.top and self.rect.top -player.rect.top<=25)):
                self.vel_x = -1
            
    def move(self):
        if self.move_able:
            self.rect.x += self.vel_x * self.speed
        else:
            self.rect.x -= self.vel_x * self.speed
    def update(self,x_shift):
        super().update(x_shift)
        self.tactics()
        self.move()
# 3:    
class Enemy3(Enemy2):
    persuade = False
    def tactics(self):
        if self.move_able:
            player = game.level.player.sprite
            if player.rect.x - self.rect.x <=800 and player.rect.x - self.rect.x>=0 and ((player.rect.top >self.rect.top and player.rect.top -self.rect.top<=self.size[1]-20) or (player.rect.top <self.rect.top and self.rect.top -player.rect.top<=self.size[1]-20)):
                self.persuade = True
            elif self.rect.x - player.rect.x <= 800 and self.rect.x - player.rect.x >=0 and ((player.rect.top >self.rect.top and player.rect.top -self.rect.top<=self.size[1]-20) or (player.rect.top <self.rect.top and self.rect.top -player.rect.top<=self.size[1]-20)):
                self.persuade = True
    def attack(self):
        player = game.level.player.sprite
        if player.rect.x > self.rect.x:
            self.vel_x = 1
        elif player.rect.x < self.rect.x:
            self.vel_x = -1

    def move(self):
        if self.persuade and self.move_able:
            self.attack()
            self.rect.x += self.vel_x * self.speed
            self.rect.y += self.vel_y
        else:
            self.rect.x -= self.vel_x *self.speed
            self.persuade = False
            self.vel_x *=-1
# 4:
class Enemy4(Enemy):
    color = 'white'
    size = (32,64)
    kind = 4
    vel_x = 1
    vel_y = 0
    speed = 2
    health = 2
    look_dir = 'right'
    move_able = False
    shoot_cooldown=50
    ready_shoot =False
    persuade = False
    move_able = False
    ready_per = True
    per_time = 0
    ready_surp = True
    status='stand'
    def __init__(self,pos):
        super().__init__(pos)
        self.bullet = pygame.sprite.Group()
    def recharge(self):
    
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.per_time >=3000 and not self.ready_per:
            self.persuade = False
            self.ready_per = True

        if self.persuade:
            self.shoot_cooldown-=1
            
        if self.shoot_cooldown <=0:
            self.shoot_cooldown =80
            self.ready_shoot =True
            self.status_change()
    def status_change(self):
        player=game.level.player.sprite
        if player.status == 'crouch':
            self.status = 'crouch'
        if player.status == 'stand' or not self.persuade:
            self.status = 'stand'
    def animation(self):
        self.image = pygame.Surface(self.size)
        self.image.fill('blue')
        
        if self.status =='stand':
            self.size = [32,64]
        elif self.status == 'crouch':
            self.size = [64,32]
            
        self.rect = self.image.get_rect(midbottom= self.rect.midbottom)
    def shoot(self):
        if self.ready_shoot:
            self.sh_y = self.rect.midtop[1]+10
            self.sh_x = self.rect.midtop[0]
            bullet = e_Bullet((self.sh_x,self.sh_y),self.look_dir)
            game.level.enemy_bullet.add(bullet)
            self.ready_shoot = False
                
    def move(self):
        #moving
        if self.move_able and not self.persuade:
            self.rect.x += self.vel_x * 2
        else:
            self.reverse()
    def reverse(self):
        self.vel_x*=-1
    def find_player(self,dx):
        self.static = self.rect.x
        player = game.level.player.sprite
        while self.rect.x!=player.rect.x:
            self.rect.x += dx
            if pygame.sprite.spritecollide(self,game.level.tiles,False):
                self.rect.x =self.static
                return False
        self.rect.x =self.static
        return True
    def find_dir(self):
        player = game.level.player.sprite
        player_y = player.rect.y
        enemy_y = self.rect.y
        if player.rect.x > self.rect.x and player.rect.x -self.rect.x <= 800 and player_y >= enemy_y and player_y - enemy_y<=self.size[1]:
            self.look_dir = 'right'
            self.persuade = self.find_player(1)
        elif player.rect.x > self.rect.x and player.rect.x -self.rect.x <= 800 and player_y <=enemy_y and enemy_y - player_y<=self.size[1]:
            self.look_dir = 'right'
            self.persuade = True
            self.persuade = self.find_player(1)
        elif self.rect.x > player.rect.x and self.rect.x - player.rect.x <= 800 and player_y >= enemy_y and player_y - enemy_y<=self.size[1]:
            self.persuade = True
            self.look_dir = 'left'
            self.persuade = self.find_player(-1)
        elif self.rect.x > player.rect.x and self.rect.x - player.rect.x <= 800 and enemy_y >=player_y and enemy_y - player_y<=self.size[1]:
            self.persuade = True
            self.look_dir = 'left'
            self.persuade = self.find_player(-1)
            
        elif self.ready_per:
            self.per_time = pygame.time.get_ticks()
            self.ready_per = False
        
    def update(self,x_shift):
        super().update(x_shift)
        self.find_dir()
        self.shoot()
        self.recharge()
        self.move()
        self.animation()
        
# main:
class Game:
    def __init__(self):
        #game settings:
        
        coins = 0
        self.lvl = 1
        menu_map = 10
        #map management:
        self.current_map = level_map
        #level:
        self.level = Level(level_map,screen)
        #overworld:
        self.overworld = Overworld(menu_map)
        #game status:
        self.status = 'overworld'
        
    def change_level(self):
        player =self.level.player.sprite
        gate = self.level.gate
        if pygame.sprite.spritecollide(player,gate,False):
            lvl+=1
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.status == 'overworld':
            self.change_status('game')
            
    def change_status(self,status):
        self.status =status
    def game_over(self):
        current_health = self.level.player.sprite.current_health
        if current_health <= 0:
            player = self.level.player.sprite
            self.change_status('overworld')
            self.level.setup_level(self.current_map)
            
    def create_game(self):
        if self.status == 'game':
            self.level.run()
    def create_overworld(self):
        if self.status == 'overworld':
            self.overworld.run()
    def run(self):
        self.change_level()
        self.game_over()
        self.get_input()
        self.create_game()
        self.create_overworld()

game_over = False
run = True
clock=pygame.time.Clock()
game = Game()
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
    screen.fill('black')
    game.run()
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
