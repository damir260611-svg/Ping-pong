from pygame import *
win = display.set_mode((700, 500))
display.set_caption('Пинг-понг')
background = transform.scale(image.load('sportivnoe-pole-vid-sverhu.jpg'), (700, 500))
clock = time.Clock()
FPS = 60
game = True
finish = False
score_left = 0
score_right = 0
font.init()
font_1 = font.SysFont('Arial', 25)
font_2 = font.SysFont('Arial', 50)
mixer.init()
mixer.music.load('Paradise_Found.mp3')
mixer.music.set_volume(0.1)
mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 400:
            self.rect.y += self.speed
    def update_right(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image, x, y, speed, widht, height):
        super().__init__(image, x, y, speed, widht, height)
        self.speed_x = speed
        self.speed_y = speed
    def update(self):
        global score_left, score_right
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > 450 or self.rect.y < 0:
            self.speed_y *= -1
        if sprite.collide_rect(self, player_1) or sprite.collide_rect(self, player_2):
            self.speed_x *= -1
        if self.rect.x < 0:
            score_right += 1
            self.rect.x = 325
            self.rect.y = 225
            self.speed_x *= -1
        if self.rect.x > 650:
            score_left += 1
            self.rect.x = 325
            self.rect.y = 225
            self.speed_x *= -1
player_1 = Player('Stick.png', 50, 200, 5, 20, 100)
player_2 = Player('Stick.png', 630, 200, 5, 20, 100)
tennis_ball = Ball('tennis_ball.png', 325, 225, 5, 50, 50)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    win.blit(background, (0, 0))
    if not finish:
        player_1.update_left()
        player_2.update_right()
        tennis_ball.update()
        player_1.reset()
        player_2.reset()
        tennis_ball.reset()
        score_left_text = font_1.render('Счёт:' + str(score_left), True, (255, 255, 255))
        win.blit(score_left_text, (10, 10))
        score_right_text = font_1.render('Счёт:' + str(score_right), True, (255, 255, 255))
        win.blit(score_right_text, (625, 10))
    if score_left >= 10:
        finish = True
        text_left_win = font_2.render('Игрок слева победил!', True, (0, 255, 0))
        win.blit(text_left_win, (160, 200))
        mixer.music.stop()
    if score_right >= 10:
        finish = True
        text_right_win = font_2.render('Игрок справа победил!', True, (0, 255, 0))
        win.blit(text_right_win, (150, 200))
        mixer.music.stop()
    display.update()
    clock.tick(FPS)