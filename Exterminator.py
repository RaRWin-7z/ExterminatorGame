import pygame
import sys
import os
import subprocess
from random import randint

def recurso(caminho_relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, caminho_relativo)
    return os.path.join(os.path.abspath("."), caminho_relativo)

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((900, 1020))
title = pygame.display.set_caption("Exterminator")

sky = pygame.image.load(recurso('imgs/sky.png'))
wall = pygame.image.load(recurso('imgs/wall.png'))

winpage = pygame.image.load(recurso('imgs/You Win Page.png'))
losepage = pygame.image.load(recurso('imgs/You Lose Page.png'))

monsterkill = 0
monstercnt = pygame.image.load(recurso(f'imgs/monstercnt{monsterkill}.png'))

pygame.mixer.music.load(recurso("sounds/Pixel Party Dash.mp3"))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)

damage = pygame.mixer.Sound(recurso("sounds/damage.mp3"))
effect = pygame.mixer.Sound(recurso("sounds/effect.mp3"))

monster = pygame.image.load(recurso('imgs/monster.png'))
monster = pygame.transform.scale(monster, (260, 370))

projectile_img = pygame.image.load(recurso('imgs/projectile.png'))
projectile_img = pygame.transform.scale(projectile_img, (70, 70))

inseticida = pygame.image.load(recurso('imgs/inseticide.png'))
inseticida = pygame.transform.scale(inseticida, (180.67, 271))

gameover = False
monsters = []

pos_x_e = 50
pos_y_e = -370

def generate_monster_e():
    global monster
    colidder = monster.get_rect()
    colidder.topleft = (pos_x_e, pos_y_e)
    monsters.append([monster, pos_x_e, pos_y_e, colidder, False])

pos_x_d = 575
pos_y_d = -370

def generate_monster_d():
    global monster
    colidder = monster.get_rect()
    colidder.topleft = (pos_x_d, pos_y_d)
    monsters.append([monster, pos_x_d, pos_y_d, colidder, False])

lifebarcnt = 1

def lifebarc_draw():
    global lifebarcnt
    global gameover
    if lifebarcnt >= 10:
        gameover = True
    if monsterkill < 19:
        lifebar = pygame.image.load(recurso(f'imgs/lifebar{lifebarcnt}.png'))
        lifebar = pygame.transform.scale(lifebar, (384.23, 80.3))
        window.blit(lifebar, (-10, 20))

def spawn():
    number = randint(1, 2)
    if number == 1:
        generate_monster_e()
    else:
        generate_monster_d()

last_spawn = 0

def cooldown():
    global last_spawn
    cooldown_time = 1700
    if monsterkill >= 5:
        cooldown_time = 1300
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - last_spawn >= cooldown_time:
        spawn()
        last_spawn = tempo_atual

    if monsterkill > 19:
        cooldown_time = 0

projectiles = []
last_shot_time = 0

insE = False
insD = False

def draw1():
    window.blit(sky, (0, 0))
    window.blit(wall, (400, -100))

def draw2():
    if insE:
        window.blit(inseticida, (100, 730))
    if insD:
        window.blit(inseticida, (600, 730))

noWin = True

loop = True
while loop:

    if monsterkill < 19:
        draw1()
        draw2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                insE = True
                insD = False
            elif event.key == pygame.K_d:
                insD = True
                insE = False

    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= 700:
        if insE:
            proj_x = 100 + inseticida.get_width() // 2 - 15
        elif insD:
            proj_x = 600 + inseticida.get_width() // 2 - 15
        else:
            proj_x = None
        if proj_x is not None:
            proj_y = 730
            proj_rect = pygame.Rect(proj_x, proj_y, projectile_img.get_width(), projectile_img.get_height())
            projectiles.append(proj_rect)
            last_shot_time = current_time

    for proj in projectiles[:]:
        proj.y -= 25
        window.blit(projectile_img, (proj.x, proj.y))
        if proj.y < 0:
            projectiles.remove(proj)

    for m in monsters[:]:
        m[2] += 5
        m[3].topleft = (m[1], m[2])
        window.blit(m[0], (m[1], m[2]))

        if m[2] >= 509 and not m[4]:
            lifebarcnt += 1
            damage.play()
            m[4] = True
            

        for proj in projectiles[:]:
            if proj.colliderect(m[3]) and monsterkill < 19:
                monsters.remove(m)
                projectiles.remove(proj)
                effect.play()
                monsterkill += 1
                monstercnt = pygame.image.load(recurso(f'imgs/monstercnt{min(monsterkill, 19)}.png'))
                break

            if proj.y == 20:
                projectiles.remove(proj)

    cooldown()
    lifebarc_draw()
    if gameover:
        loop = False
    if gameover and monsterkill >= 19:
        pass

    window.blit(monstercnt, (700, 20))
    if monsterkill >= 19:
        window.blit(winpage, (0, 0))
        effect.set_volume(0.0)
        damage.set_volume(0.0)

    if lifebarcnt == 4:
        window.blit(losepage, (0, 0))
        effect.set_volume(0.0)
        damage.set_volume(0.0)
    pygame.display.update()

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
