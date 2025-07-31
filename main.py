import pygame
pygame.init()
from random import randint

window = pygame.display.set_mode((900, 1020))
title = pygame.display.set_caption("Exterminator")

sky = pygame.image.load('sky.png')
wall = pygame.image.load('wall.png')

monster = pygame.image.load('monster.png')
monster = pygame.transform.scale(monster, (260, 370))

projectile_img = pygame.image.load('projectile.png')
projectile_img = pygame.transform.scale(projectile_img, (70, 70))

inseticida = pygame.image.load('inseticide.png')
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

    if lifebarcnt >= 4:
        gameover = True
    lifebar = pygame.image.load('lifebar' + str(lifebarcnt) + '.png')
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
    cooldown_time = 1000
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - last_spawn >= cooldown_time:
        spawn()
        last_spawn = tempo_atual

projectiles = []
last_shot_time = 0

insE = False
insD = False

loop = True
while loop:
    window.blit(sky, (0, 0))
    window.blit(wall, (400, 0))

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

    if insE:
        window.blit(inseticida, (100, 730))
    if insD:
        window.blit(inseticida, (600, 730))

    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= 1000:
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
        proj.y -= 7
        window.blit(projectile_img, (proj.x, proj.y))
        if proj.y < 0:
            projectiles.remove(proj)

    for m in monsters[:]:
        m[2] += 3
        m[3].topleft = (m[1], m[2])
        window.blit(m[0], (m[1], m[2]))

        if m[2] >= 509 and not m[4]:
            lifebarcnt += 1
            m[4] = True

        for proj in projectiles[:]:
            if proj.colliderect(m[3]):
                monsters.remove(m)
                projectiles.remove(proj)
                break

    cooldown()
    lifebarc_draw()
    if gameover:
        loop = False

    pygame.display.update()
