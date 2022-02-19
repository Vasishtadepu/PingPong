import pygame
import os
pygame.font.init()
pygame.mixer.init()

# defining window widths
width = 900
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong!")
fps = 60  # fps is 60

score_font = pygame.font.SysFont('comicsans',40)
winner_font = pygame.font.SysFont('comicsans',100)

#defining missing sounds and hit sounds
ball_hit = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
ball_miss = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))

# defining colors
cblack = (0, 0, 0)
cwhite = (255, 255, 255)

#defining reset ball
def reset_ball(ball):
  pygame.time.delay(500)
  ball.x = width//2-2
  ball.y = height//2


# defining top and bottom borders
top = pygame.Rect(0, 40, width, 10)
bottom = pygame.Rect(0, height-10, width, 10)

# defining User events
player1_out = pygame.USEREVENT + 1
player2_out = pygame.USEREVENT + 2
border_hit = pygame.USEREVENT+3
player_hit = pygame.USEREVENT + 4

# displaying the window


def display_window(player1, player2, ball,player1_score,player2_score):
    win.fill(cblack)
    player1_score_text = score_font.render("Score: "+str(player1_score),1,cwhite)
    player2_score_text = score_font.render("Score: "+str(player2_score),1,cwhite)

    win.blit(player2_score_text,(width-player2_score_text.get_width()-10,20-player2_score_text.get_height()//2))
    win.blit(player1_score_text,(10,20-player1_score_text.get_height()//2))

    pygame.draw.rect(win, cwhite, top)
    pygame.draw.rect(win, cwhite, bottom)
    pygame.draw.rect(win, cwhite, player1)
    pygame.draw.rect(win, cwhite, player2)
    pygame.draw.rect(win, cwhite, ball)
    pygame.display.update()

# defining player movements
# Player 1



  


def Player1_Movement(keys_pressed, player1):
    if keys_pressed[pygame.K_w] and player1.y >= 40+top.height+2:
        player1.y -= 10

    if keys_pressed[pygame.K_s] and player1.y+player1.height <= height-2:
        player1.y += 10


def Player2_Movement(keys_pressed, player2):
    if keys_pressed[pygame.K_UP] and player2.y >= 40+top.height+2:
        player2.y -= 10

    if keys_pressed[pygame.K_DOWN] and player2.y+player2.height <= height-2:
        player2.y += 10

# Ball Movement


def ball_moving(ball, player1, player2, top, bottom):
    if top.colliderect(ball) or bottom.colliderect(ball):
        pygame.event.post(pygame.event.Event(border_hit))

    if player1.colliderect(ball) or player2.colliderect(ball):
        pygame.event.post(pygame.event.Event(player_hit))

    if ball.x>width-ball.width:
      pygame.event.post(pygame.event.Event(player2_out))    
    
    if ball.x<=0:
      pygame.event.post(pygame.event.Event(player1_out))


def draw_winner(text):
  draw_text = winner_font.render(text,1,cwhite)
  win.blit(draw_text,(width//2-draw_text.get_width()//2,height//2-draw_text.get_height()//2))
  pygame.display.update()
  pygame.time.delay(2000)
  

# Writing the main game loop


def main():
    # player rectangles
    player1 = pygame.Rect(25, height//2-40, 10, 80)
    player2 = pygame.Rect(width-10-25, height//2-40, 10, 80)
    ball_yvel = 8
    ball_xvel = 7
    winner_text=""
    player1_score = 0
    player2_score = 0

    # ball rectangle
    ball = pygame.Rect(width//2-2, height//2, 7, 7)
    run = True
    clock = pygame.time.Clock()
    while(run):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == border_hit:
                ball_yvel = -ball_yvel
                ball_hit.play()
            if event.type == player_hit:
                ball_xvel = -ball_xvel
                ball_hit.play()

            if event.type == player1_out:
              reset_ball(ball)
              player2_score+=1
              ball_miss.play()

            if event.type == player2_out:
              reset_ball(ball)  
              player1_score+=1
              ball_miss.play()  

        keys_pressed = pygame.key.get_pressed()
        if player1_score == 5:
          winner_text="Player 1 Wins!"

        if player2_score == 5:
          winner_text = "Player 2 Wins!"

        if winner_text!="":
          
          display_window(player1, player2, ball,player1_score,player2_score)
          draw_winner(winner_text)
          
          break

        ball.x += ball_xvel
        ball.y += ball_yvel
        ball_moving(ball, player1, player2, top, bottom)
        Player1_Movement(keys_pressed, player1)
        Player2_Movement(keys_pressed, player2)
        display_window(player1, player2, ball,player1_score,player2_score)

    main()


if __name__ == "__main__":
    main()
