import pygame as pg
import os

WIDTH = 800
HEIGHT = 500
FPS = 60
UFO_WIDTH = 55
UFO_HEIGHT = 45
WHITE = (255,255,255)
BLACK = (0, 0, 0)
VELOCITY = 5
B_VELOCITY = 8
BULLET_WIDTH = 3
BULLET_HEIGHT = 5
MAX_BULLETS = 3
BORDER_WIDTH = 10
BORDER = pg.Rect(WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)

# List of bullets
yellow_bullets = []
red_bullets = []

# Define user event for bullet hit
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

# Make the main window for the game
window = pg.display.set_mode( (WIDTH, HEIGHT) )
# Set the name of the window
pg.display.set_caption("Space Wars")

# Load graphics
YELLOW_UFO = pg.image.load(os.path.join('graphics', 'yellow_ufo.png'))
YELLOW_UFO = pg.transform.scale(YELLOW_UFO, (UFO_WIDTH, UFO_HEIGHT))
YELLOW_UFO = pg.transform.rotate(YELLOW_UFO, 90)
RED_UFO = pg.image.load(os.path.join('graphics', 'red_ufo.png'))
RED_UFO = pg.transform.scale(RED_UFO, (UFO_WIDTH, UFO_HEIGHT))
RED_UFO = pg.transform.rotate(RED_UFO, 270)
BG = pg.image.load(os.path.join('graphics', 'bg.jpg'))
BG = pg.transform.scale(BG, (WIDTH, HEIGHT))
BULLET_R = pg.image.load(os.path.join('graphics', 'red_bullet.png'))
BULLET_Y = pg.image.load(os.path.join('graphics', 'yellow_bullet.png'))

# Function to draw graphics on the window
def draw_window(red, yellow, red_bullets, yellow_bullets):
    #window.fill(WHITE)
    window.blit(BG, (0,0))
    pg.draw.rect(window, BLACK, BORDER)
    window.blit(YELLOW_UFO, (yellow.x, yellow.y))
    window.blit(RED_UFO, (red.x, red.y))
    
    for bullet in red_bullets:
        window.blit(BULLET_R, (bullet.x, bullet.y))
    for bullet in yellow_bullets:
        window.blit(BULLET_Y, (bullet.x, bullet.y))
    pg.display.update()

# Function to move Yellow UFO
def moveYellowUFO(keys_pressed, yellow):
    if keys_pressed[pg.K_a] and yellow.x-VELOCITY > 0: 
        yellow.x-= VELOCITY; #Left
    if keys_pressed[pg.K_s] and yellow.y+VELOCITY+yellow.height < HEIGHT:
        yellow.y+= VELOCITY; #Down
    if keys_pressed[pg.K_d] and yellow.x+VELOCITY+yellow.width < BORDER.x:
        yellow.x+= VELOCITY; #Right
    if keys_pressed[pg.K_w] and yellow.y-VELOCITY > 0:
        yellow.y-= VELOCITY; #Up

# Function to move Red UFO
def moveRedUFO(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and red.x-VELOCITY > BORDER.x+BORDER.width : 
        red.x-= VELOCITY; #Left
    if keys_pressed[pg.K_DOWN] and red.y+VELOCITY+red.height < HEIGHT:
        red.y+= VELOCITY; # Down
    if keys_pressed[pg.K_RIGHT] and red.x+VELOCITY+red.width < WIDTH:
        red.x+= VELOCITY; #Right
    if keys_pressed[pg.K_UP] and red.y-VELOCITY > 0:
        red.y-= VELOCITY; #Up

# Function to control the movement of bullets
def moveBullets(red, yellow, red_bullets, yellow_bullets):
    for bullet in yellow_bullets:
        bullet.x+= B_VELOCITY
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x-= B_VELOCITY
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 1:
            red_bullets.remove(bullet)

# Function to handle main game loop
def supervisor():
    clock =pg.time.Clock()
    # Rectangles to represent the UFOs
    red = pg.Rect(750, 230, UFO_WIDTH, UFO_HEIGHT)
    yellow = pg.Rect(10, 230, UFO_WIDTH, UFO_HEIGHT)
    run=True
    while(run):
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
            
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_CAPSLOCK and len(yellow_bullets)<MAX_BULLETS:
                    b = pg.Rect(yellow.x+yellow.width, 
                                yellow.y+yellow.height//2,
                                BULLET_WIDTH,
                                BULLET_HEIGHT)
                    yellow_bullets.append(b)
                if event.key==pg.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    b = pg.Rect(red.x, 
                                red.y+red.height//2,
                                BULLET_WIDTH,
                                BULLET_HEIGHT)
                    red_bullets.append(b)

        keys_pressed = pg.key.get_pressed()
        moveRedUFO(keys_pressed, red)
        moveYellowUFO(keys_pressed, yellow)   
        moveBullets(red, yellow, red_bullets, yellow_bullets)
        draw_window(red, yellow, red_bullets, yellow_bullets)
    pg.quit()


if __name__ == "__main__":
    supervisor()
