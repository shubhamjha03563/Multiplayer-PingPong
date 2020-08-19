import pygame
import time
import random

pygame.init()
bounce_sound = pygame.mixer.Sound("bounce.mp3")
pygame.mixer.music.load("back2.mp3")

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
display_width = 800
display_height = 600
ball_radius = 8
rect_width = 160
rect_height = 10
gameDisplay = pygame.display.set_mode((display_width, display_height))
score_font = pygame.font.SysFont("comicsansms", 20)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed() 

    if x+w > mouse[0] > x and y+h > mouse[1] >y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
 
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg,smallText )
    textRect.center = ((x+(w/2)), y+(h/2))
    gameDisplay.blit(textSurf, textRect)

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    
    clock = pygame.time.Clock()
    intro = False
    while not intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill((128, 128, 128))
        largeText = pygame.font.SysFont("comicsansms", 115)
        textSurf, textRect = text_objects("Ping Pong", largeText)
        textRect.center = ((display_width / 2), (display_height / 2 - 100))   
        gameDisplay.blit(textSurf, textRect)
        button("v/s COM", 150, 350, 120, 50, green, bright_green, game_loop_single_player) 
        button("v/s Player", 550, 350, 120, 50, red, bright_red, game_loop_multiplayer)
        pygame.display.update()
        clock.tick(15)

def draw_text_middle( text, size, color):  
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)

    gameDisplay.blit(label, (display_width/6, display_height/2 - 200)) 

def my_score(player, score, x, y):
    if player == 0:
        value = score_font.render("Player " + " -  " + str(score), True, white)
    else:
        value = score_font.render("Player "+ str(player) + " -  " + str(score), True, white)
    gameDisplay.blit(value, (x, y))

def my_score2(score, x, y):
    value = score_font.render("COM " + " -  " + str(score), True, white)
    gameDisplay.blit(value, (x, y))

def draw_window(rect1_pos, rect2_pos, ball_pos, mode):
    global score1, score2, game_over
    gameDisplay.fill(black)
    pygame.draw.line(gameDisplay, white, (0, display_height/2), (display_width, display_height/2))
    pygame.draw.rect(gameDisplay, blue,(rect1_pos[0]-ball_radius, rect1_pos[1], rect_width, rect_height))
    pygame.draw.rect(gameDisplay, blue,(rect2_pos[0]-ball_radius, rect2_pos[1], rect_width, rect_height))
    pygame.draw.circle(gameDisplay, red, ball_pos, ball_radius)
    if mode == 2:
        my_score(1, score1, display_width/2 -60, (display_height/2) - 50)
        my_score(2, score2, display_width/2 -60, (display_height/2) + 20)
        if score2 == 10:
            draw_text_middle("Player 2 wins!", 100, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True
        elif score1 == 10:
            draw_text_middle("Player 1 wins!", 100, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True
    else:
        my_score2(score1, display_width/2 -60, (display_height/2) - 50)
        my_score(0, score2, display_width/2 -60, (display_height/2) + 20)
        if score2 == 10:
            draw_text_middle("Player wins!", 100, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True
        elif score1 == 10:
            draw_text_middle("COM wins!", 100, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(3000)
            game_over = True

    pygame.display.update()

def game_loop_multiplayer():
    global score1, score2, game_over
    pygame.mixer.music.play(-1)

    play = True
    while play:

        ball_speed_y = 0
        rect_speed = 10
        score1 = 0
        score2 = 0
        clock = pygame.time.Clock()

        game_over = False
        while not game_over:

            rect1_x = display_width/2 - rect_width/2
            rect1_y = 10
            rect2_x = display_width/2 - rect_width/2
            rect2_y = display_height-rect_height-10
            x1_change = 0
            x2_change = 0
            ball_x = rect1_x + rect_width/2
            ball_y = rect1_y + (rect_height*2)
            ball_speed_y = 8
            ball_speed_x = random.choice([5, -5])
            pygame.time.delay(500)
            player2 = 0

            restart = False
            while not restart:
                clock.tick(60)
                ball_x += ball_speed_x
                ball_y += ball_speed_y
                if ball_y <= rect1_y+rect_height+ball_radius:
                    if ball_x <= rect1_x+rect_width+ball_radius+2 and ball_x >= rect1_x-ball_radius: 
                        ball_y= rect1_y+rect_height+ball_radius
                        pygame.mixer.Sound.play(bounce_sound)
                        ball_speed_x *= 1
                        ball_speed_y *= -1
                        player2+=1
                    else:
                        player2 = 0
                        ball_x += ball_speed_x
                        ball_y = 0+ball_radius
                        score2 +=1
                        restart = True

                elif ball_y >= rect2_y-ball_radius:
                    if ball_x <= rect2_x+rect_width+ball_radius+2 and ball_x >= rect2_x-ball_radius: 
                        ball_y = rect2_y-ball_radius
                        pygame.mixer.Sound.play(bounce_sound)
                        ball_speed_x *= 1
                        ball_speed_y *= -1
                        player2+=1
                    else:
                        player2 = 0
                        ball_x += ball_speed_x
                        ball_y = display_height-ball_radius
                        score1 +=1
                        restart = True                             

                if ball_x+ball_radius >= display_width or ball_x <= 0:
                    ball_speed_x *= -1
                    ball_speed_y *= 1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    
                    if player2%2 == 0:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                x2_change = rect_speed
                            if event.key == pygame.K_LEFT:
                                x2_change = -rect_speed
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                                x2_change = 0

                    else:    
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_d:
                                x1_change = rect_speed
                            if event.key == pygame.K_a:
                                x1_change = -rect_speed
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_d or pygame.K_a:
                                x1_change = 0

                rect1_x += x1_change 
                if rect1_x+rect_width > display_width:
                    rect1_x = display_width- rect_width
                elif rect1_x < 0:
                    rect1_x -= x1_change
                
                rect2_x += x2_change 
                if rect2_x+rect_width > display_width:
                    rect2_x = display_width- rect_width
                elif rect2_x < 0:
                    rect2_x -= x2_change

                ball_pos = (ball_x, ball_y)
                rect1_pos = (rect1_x, rect1_y)
                rect2_pos = (rect2_x, rect2_y)
                draw_window(rect1_pos, rect2_pos, ball_pos, 2)

def game_loop_single_player():
    global score1, score2, game_over
    pygame.mixer.music.play(-1)

    play = True
    while play:

        ball_speed_y = 0
        rect_speed = 9
        score1 = 0
        score2 = 0
        clock = pygame.time.Clock()

        game_over = False
        while not game_over:

            rect1_x = display_width/2 - rect_width/2
            rect1_y = 10
            rect2_x = display_width/2 - rect_width/2
            rect2_y = display_height-rect_height-10
            x1_change = 0
            x2_change = 0
            ball_x = rect1_x + rect_width/2
            ball_y = rect1_y + (rect_height*2)
            ball_speed_y = 8
            ball_speed_x = random.choice([9, -9])
            pygame.time.delay(500)

            restart = False
            while not restart:
                clock.tick(60)
                ball_x += ball_speed_x
                ball_y += ball_speed_y
                if ball_y <= rect1_y+rect_height+ball_radius:
                    if ball_x <= rect1_x+rect_width+ball_radius+2 and ball_x >= rect1_x-ball_radius: 
                        ball_y= rect1_y+rect_height+ball_radius
                        pygame.mixer.Sound.play(bounce_sound)
                        ball_speed_x *= 1
                        ball_speed_y *= -1
                    else:
                        ball_x += ball_speed_x
                        ball_y = 0+ball_radius
                        score2 +=1
                        restart = True

                elif ball_y >= rect2_y-ball_radius:
                    if ball_x <= rect2_x+rect_width+ball_radius+2 and ball_x >= rect2_x-ball_radius: 
                        ball_y = rect2_y-ball_radius
                        pygame.mixer.Sound.play(bounce_sound)
                        ball_speed_x *= 1
                        ball_speed_y *= -1
                    else:
                        ball_x += ball_speed_x
                        ball_y = display_height-ball_radius
                        score1 +=1
                        restart = True                             

                if ball_x+ball_radius >= display_width or ball_x <= 0:
                    ball_speed_x *= -1
                    ball_speed_y *= 1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            x2_change = rect_speed
                        if event.key == pygame.K_LEFT:
                            x2_change = -rect_speed
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                            x2_change = 0
                if ball_speed_x>0:
                    rect1_x += rect_speed-1.3
                else:
                    rect1_x -= rect_speed-1
    
                if rect1_x+rect_width >= display_width:
                    rect1_x = display_width- rect_width
                elif rect1_x <= 0:
                    rect1_x = 0
                    
                rect2_x += x2_change                     
                if rect2_x+rect_width > display_width:
                    rect2_x = display_width- rect_width
                elif rect2_x < 0:
                    rect2_x -= x2_change
                
                ball_pos = (ball_x, ball_y)
                rect1_pos = (rect1_x, rect1_y)
                rect2_pos = (rect2_x, rect2_y)

                draw_window(rect1_pos, rect2_pos, ball_pos, 1)


game_intro()
pygame.quit()
quit()