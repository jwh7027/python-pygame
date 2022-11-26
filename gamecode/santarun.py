import pygame
from pygame.locals import *
from pygame import mixer
import random

#배경 음악 추가
mixer.init()
mixer.music.load("jingle-bells-violin-loop-8645.mp3")
mixer.music.set_volume(0.1)
mixer.music.play()

#사운드 추가
break_sound = mixer.Sound("422669__lynx-5969__ice-break-with-hand.wav")
break_sound.set_volume(0.3)

clear_sound = mixer.Sound("270402__littlerobotsoundfactory__jingle-win-00.wav")
clear_sound.set_volume(0.5)

fail_sound = mixer.Sound("454786__carloscarty__silent-night-intro-pan-flute-glissando.wav")
fail_sound.set_volume(0.4)

shoot_sound = mixer.Sound("174464__yottasounds__ending-effect-001.wav")
shoot_sound.set_volume(0.3)

item_pickup = mixer.Sound("544015__mr-fritz__item-pick-up.wav")
item_pickup.set_volume(0.5)

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0.0, vx=0.0, vy=0.0, av=0.0, ds=0.0):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle  # 회전
        self.vx = vx
        self.vy = vy
        self.av = av  # angular velocity (각속도)
        self.ds = ds  # 스프라이트 변화 속도
        self.sprites = self.init_sprites()
        self.sprite_id = 0
        self.image = self.sprites[int(self.sprite_id)]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    def init_sprites(self):
        raise NotImplementedError("init_sprites() not implemented")
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.av
        self.rect.center = (self.x, self.y)
        self.sprite_id += self.ds
        self.sprite_id %= len(self.sprites)
        if self.angle != 0:
            self.image = pygame.transform.rotate(
                self.sprites[int(self.sprite_id)], self.angle
            )
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.sprites[int(self.sprite_id)]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
    def draw_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


class Bullet(pygame.sprite.Sprite):
    img_src = None

    def __init__(self, x, y):
        super().__init__()
        if Bullet.img_src == None:
            Bullet.img_src = pygame.image.load("present/present-gift-box-reward-full.png").convert_alpha()
            w, h = Bullet.img_src.get_size()
            Bullet.img_src = pygame.transform.scale(Bullet.img_src, (w // 10, h // 10))
        self.image = Bullet.img_src # 첫 프레임은 회전이 없음
        self.vx = 20.0 # 총알 속도
        self.vy = 0.0
        self.x = x
        self.y = y
        self.angle = 0.0
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x += self.vx # dt 곱하기를 생략 (작은 속도값 사용)
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        self.angle -= 20.0
        self.image = pygame.transform.rotate(Bullet.img_src, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Obstacle(pygame.sprite.Sprite): # class Bullet과 비슷합니다.
    img_src = None

    def __init__(self, x, y, vx=0.0, vy=0.0, av=0.0, scale=1):
        super().__init__()
        if Obstacle.img_src == None:
            Obstacle.img_src = pygame.image.load("wintertileset/png/Object/IceBox.png").convert_alpha()
            w, h = Obstacle.img_src.get_size()
            Obstacle.img_src = pygame.transform.scale(Obstacle.img_src, (w // scale, h // scale))
        self.image = Obstacle.img_src # 첫 프레임은 회전이 없음
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.av = av # 각 속도 (angular velocity)
        self.angle = 0.0
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x += self.vx # dt 곱하기 생략
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        self.angle -= self.av
        self.image = pygame.transform.rotate(Obstacle.img_src, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
class Item(MovingObject):
    source_sprites = []
    IMAGE_FILENAMES = [
        "yaycandies/size1/candycane.png",
        "yaycandies/size1/bean_blue.png",
        "yaycandies/size1/bean_green.png",
        "yaycandies/size1/bean_orange.png",
        "yaycandies/size1/candycorn.png",
        "yaycandies/size1/jelly_green.png",
        "yaycandies/size1/jelly_orange.png",
        "yaycandies/size1/candyhumbug.png",
        "yaycandies/size1/jellybig_yellow.png",
        "yaycandies/size1/lollipop_blue.png",
        "yaycandies/size1/lollipop_pink.png",
        "yaycandies/size1/swirl_red.png",
        "yaycandies/size1/wrappedsolid_purple.png",
        "yaycandies/size1/wrappedsolid_green.png",
        "yaycandies/size1/wrappedtrans_yellow.png",
    ]
    def __init__(self, x, y):
        super().__init__(x,y, vx= -10)
    def init_sprites(self):
        if not Item.source_sprites:
            for f in Item.IMAGE_FILENAMES:
                i = pygame.image.load(f).convert_alpha() 
                Item.source_sprites.append(i)
        return [random.choice(Item.source_sprites)] 
         
class Player(MovingObject):
    source_sprites = []
    def __init__(self):
         super().__init__(240, 530, ds=1.0)
    def init_sprites(self):
        if not Player.source_sprites:
            for i in range(1,12):
                img= pygame.image.load(f"santasprites/png/Run ({i}).png").convert_alpha() 
                w, h = img.get_size()
                img = pygame.transform.scale(img, (w // 4, h // 4))
                rect = img.get_rect()
                rect.width = 140
                img = img.subsurface(rect)
                Player.source_sprites.append(img)
        return Player.source_sprites
    def update(self):
        self.vy += 0.8
        super().update()
        #바닥 충돌 반응
        if self.y >= 520 and self.vy > 0.0:
             self.y = 520
             self.vy = 0.0
    def Jump(self):
         self.vy = -15         

pygame.init()
pygame.display.set_caption("Santa Run")
screen = pygame.display.set_mode((1024,768)) #윈도우 크기

clock = pygame.time.Clock() #FPS 조절에 사용


santa = Player()


moving_sprites = pygame.sprite.Group()
moving_sprites.add(santa)
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
item = pygame.sprite.Group()

#배경이미지
background = pygame.image.load("wintertileset/png/BG/BG.png").convert()
bgx = 0

#바닥 타일
tile2 = pygame.image.load("wintertileset/png/Tiles/2.png").convert_alpha()
tile2 = pygame.transform.scale(tile2, (64, 64)) # 적당한 크기로 조정
tile5 = pygame.image.load("wintertileset/png/Tiles/5.png").convert_alpha()
tile5 = pygame.transform.scale(tile5, (64, 64))
gx = 0

#스코어
scorefont = pygame.font.SysFont("system",40)
titlefont = pygame.font.SysFont("system",200)

running = True
draw_rect = False
score = 0
while running:
     
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                elif event.type == KEYUP:
                    if event.key == K_LCTRL:
                        bullets.add(Bullet(santa.x - 20, santa.y)) #총알
                    elif event.key == K_SPACE:
                        santa.Jump()
        """업데이트"""        
        bgx -= 0.01
        bgx %= background.get_width()

        gx +=10.0
        gx %= tile2.get_width()


        moving_sprites.update()
        bullets.update()
        obstacles.update()
        item.update()
        

        for b in bullets.copy(): # copy 주의
            if b.rect.left > 1024:
                bullets.remove(b)

        #충알 충돌    
        for b in bullets.copy():
            for o in obstacles.copy(): # copy 주의
                if b.rect.colliderect(o.rect):
                        score += 1
                        bullets.remove(b)
                        obstacles.remove(o)
                        break_sound.play()

        if random.random() > 0.97: #아이템 생성
            new_item = Item(1024, random.randrange(150,450))
            item.add(new_item)
              
        if random.random() > 0.97:  # 프레임당 2%의 확률로 장애물 생성
            obstacles.add(Obstacle(1000, 530, vx=-6))
            #obstacles.add(Obstacle(1000, random.randrange(100,530), vx=-6))
            
        #아이템 충돌
        for i in item.copy():
            if santa.rect.colliderect(i.rect):
                 score += 1
                 item.remove(i)
                 item_pickup.play() 
            elif i.rect.right < 0:
                 item.remove(i) 

        #클리어 조건
        if score >= 100:
             mixer.music.stop()
             clear_sound.play()
             clear_text = titlefont.render("Cleared!", True, (255,255,255))
             screen.blit(clear_text, (220,220))
             pygame.display.flip()
             pygame.time.wait(int(clear_sound.get_length() * 1000))
             running = False
        else: # 장애물 충돌
             for o in obstacles.copy():
                  if santa.rect.colliderect(o.rect):
                       mixer.music.stop()
                       fail_sound.play()
                       fail_text = titlefont.render("Game over", True, (255,0 ,0))
                       screen.blit(fail_text, (150, 300))
                       pygame.display.flip()
                       pygame.time.wait(int(fail_sound.get_length() * 1000))
                       running = False
                       break  
        
        """그리기 시작"""
        screen.fill((255,255,255))
        screen.blit(background, dest= (-bgx, 0))
        screen.blit(background, dest= (-bgx + background.get_width(), 0))

        for i in range(-1,17):
                screen.blit(tile2,(-gx + i*64,64* 9))
                screen.blit(tile5,(-gx + i*64,64* 10)) 
                screen.blit(tile5,(-gx + i*64,64* 11)) 

        bullets.draw(screen)
        obstacles.draw(screen)
        item.draw(screen)
        moving_sprites.draw(screen)
        if draw_rect:
            santa.draw_rect(screen)
            for i in item:
                item.draw(screen)
        scoretext = scorefont.render("Score:" + str(score), True,(255,255,255))
        screen.blit(scoretext, (850, 50))
        pygame.display.flip()

        clock.tick(30)

pygame.quit() 