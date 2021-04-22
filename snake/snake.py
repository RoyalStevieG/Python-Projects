import random
from spritesheet import Spritesheet
import os
import pygame
pygame.init()

# make the window/box
width = 500
height = 500
screen = pygame.display.set_mode((700, 700))
win = pygame.Surface((width, height))
# win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Snake')

bg = pygame.image.load('snake_bg.png')
bg = pygame.transform.smoothscale(bg, (700, 700))

bg2 = pygame.image.load('bg.png')
bg2 = pygame.transform.scale(bg2, (500, 500))

# variables
global pause
pause = True


snake_spritesheet = Spritesheet('snakes.png')
snake_heads = [snake_spritesheet.parse_sprite('head_right.png'), snake_spritesheet.parse_sprite(
    'head_up.png'), snake_spritesheet.parse_sprite('head_left.png'), snake_spritesheet.parse_sprite('head_down.png')]
snake_tails = [snake_spritesheet.parse_sprite('tail_right.png'), snake_spritesheet.parse_sprite(
    'tail_up.png'), snake_spritesheet.parse_sprite('tail_left.png'), snake_spritesheet.parse_sprite('tail_down.png')]
snake_body = [snake_spritesheet.parse_sprite('body_horizontal.png'), snake_spritesheet.parse_sprite(
    'body_vertical.png'), snake_spritesheet.parse_sprite('body_turn1.png'), snake_spritesheet.parse_sprite('body_turn2.png'), snake_spritesheet.parse_sprite('body_turn3.png'), snake_spritesheet.parse_sprite('body_turn4.png')]
apples = pygame.transform.scale(
    snake_spritesheet.parse_sprite('apple.png'), (20, 20))

# head = pygame.transform.scale(
#     snake_spritesheet.parse_sprite('head_right.png'), (18, 18))
for I in range(len(snake_heads)):
    snake_heads[I] = pygame.transform.scale(snake_heads[I], (22, 22))
for I in range(len(snake_body)):
    snake_body[I] = pygame.transform.scale(snake_body[I], (20, 20))
for I in range(len(snake_tails)):
    snake_tails[I] = pygame.transform.scale(snake_tails[I], (20, 20))


############################################################################################### Classes and stuff #############################################################################


class snake(object):
    def __init__(self):
        self.head = (40, 120, 'D')
        self.body = [(40, 100, 'D'), (40, 80, 'D'),
                     (40, 60, 'D'), (40, 40, 'D')]
        self.tail = (40, 20, 'D')
        self.vel = 20
        self.direction = 'R'
        self.score = 0
        self.died = False

    def draw(self, win):
        # Draw head
        (x, y, direction) = self.head
        if direction == 'R':
            img = snake_heads[0]
        elif direction == 'U':
            img = snake_heads[1]
        elif direction == 'L':
            img = snake_heads[2]
        elif direction == 'D':
            img = snake_heads[3]
        win.blit(img, (x-1, y-1))

        # Draw Body
        for (x, y, direction) in self.body:
            if direction == 'R':
                img = snake_body[0]  # horizontal
            elif direction == 'U':
                img = snake_body[1]  # vertical
            elif direction == 'L':
                img = snake_body[0]  # horizontal
            elif direction == 'D':
                img = snake_body[1]  # vertical
                # up turn
            elif direction == 'UR':
                img = snake_body[2]
            elif direction == 'UL':
                img = snake_body[3]
                # down turn
            elif direction == 'DR':
                img = snake_body[5]
            elif direction == 'DL':
                img = snake_body[4]
                # right turn
            elif direction == 'RD':
                img = snake_body[3]
            elif direction == 'RU':
                img = snake_body[4]
                # left turn
            elif direction == 'LU':
                img = snake_body[5]
            elif direction == 'LD':
                img = snake_body[2]

            win.blit(img, (x+1, y+1))

        # Draw Tail
        (x, y, direction) = self.tail
        if direction == 'R':
            img = snake_tails[0]
        elif direction == 'U':
            img = snake_tails[1]
        elif direction == 'L':
            img = snake_tails[2]
        elif direction == 'D':
            img = snake_tails[3]
        win.blit(img, (x+1, y+1))

    def move(self):
        if self.died == False:
            # get new tail section
            self.tail = self.body[-1]

            # move body section to new places
            reverse = self.body[::-1]
            for I in range(len(reverse)-1):
                reverse[I] = reverse[I+1]
            self.body = reverse[::-1]

            x, y, direction = self.head
            if self.direction != direction:
                self.body[0] = x, y, (direction+self.direction)
            else:
                self.body[0] = self.head

            # determine location of new head
            x, y, direction = self.head
            if self.direction == 'R':
                self.head = (x+self.vel, y, self.direction)
            elif self.direction == 'L':
                self.head = (x-self.vel, y, self.direction)
            elif self.direction == 'U':
                self.head = (x, y-self.vel, self.direction)
            elif self.direction == 'D':
                self.head = (x, y+self.vel, self.direction)

    def eat(self, apple):
        self.body.append(self.tail)
        self.tail = self.tail
        self.score += 1

    def checkCollision(self):
        x, y, direction = self.head
        if x < 0 or x > 500:
            global pause
            pause = True
            self.died = True
        if y < 0 or y > 500:
            self.died = True
            pause = True
            # print('Die')

        for I in self.body:
            x, y, z = I
            a, b, c = self.head
            if (a, b) == (x, y):
                self.died = True
                pause = True

    def reset(self):
        self.head = (40, 120, 'D')
        self.body = [(40, 100, 'D'), (40, 80, 'D'),
                     (40, 60, 'D'), (40, 40, 'D')]
        self.tail = (40, 20, 'D')
        self.vel = 20
        self.direction = 'R'
        self.score = 0
        self.died = False


class apple(object):
    def __init__(self):
        self.x, self.y = 0, 0
        self.generate()

    def generate(self):
        self.x = random.randrange(40, 460, 20)
        self.y = random.randrange(40, 460, 20)

    def draw(self, win):
        win.blit(apples, (self.x, self.y))
        # pygame.draw.rect(win, (103, 25, 148), (self.x + 5, self.y + 5, 10, 10))

    def eaten(self, win):
        self.generate()
        self.draw(win)

############################################################################## Functions and stuff ##########################################################


btn_escape = [50, 50, 100, 50]
text_quit = pygame.font.SysFont('Corbel', 30).render(
    'QUIT', True, (0, 0, 0))

btn_resume = [250, 50, 100, 50]
text_resume = pygame.font.SysFont('Corbel', 30).render(
    'Start', True, (0, 0, 0))

btn_restart = [50, 150, 150, 50]
text_restart = pygame.font.SysFont('Corbel', 30).render(
    'RESTART', True, (0, 0, 0))

btn_add_highscore = [250, 150, 250, 50]
text_add_highscore = pygame.font.SysFont('Corbel', 30).render(
    'ADD HIGHSCORE', True, (0, 0, 0))


def drawPauseWindow():
    # win.fill((80, 80, 80))

    # draw exit button and add text
    pygame.draw.rect(win, (235, 74, 68), btn_escape)
    win.blit(text_quit, (btn_escape[0] + 10, btn_escape[1] + 10))
    # draw resume button and add text
    pygame.draw.rect(win, (19, 117, 11), btn_resume)
    win.blit(text_resume, (btn_resume[0] + 10, btn_resume[1] + 10))
    # restart button
    pygame.draw.rect(win, (194, 113, 33), btn_restart)
    win.blit(text_restart, (btn_restart[0] + 10, btn_restart[1] + 10))

    pygame.draw.rect(win, (61, 52, 235), btn_add_highscore)
    win.blit(text_add_highscore,
             (btn_add_highscore[0]+10, btn_add_highscore[1]+10))

    scoreBoard(screen, player1.score)

    # TEMP
    # win.blit(head, (300, 300))

    pygame.display.update()


# Scoreboard
def scoreBoard(win, score):
    Score = pygame.font.SysFont('Bebas', 50).render(
        f'Score: {score}', True, (27, 102, 194))
    win.blit(Score, (500, 50))


def drawGameWindow():
    # win.fill((0, 0, 0))
    win.blit(bg2, (0, 0))
    player1.draw(win)  # DRAW snake body
    snack.draw(win)

    scoreBoard(screen, player1.score)
    # GRID
    # for x in range(25):
    #     for y in range(25):
    #         pygame.draw.rect(win, (0, 255, 0), (x*20, y*20, 20, 20), 1)

    pygame.display.update()


def drawHighScores():
    HighScores = open('Highscores.txt', 'r')
    line = HighScores.read()
    lines = line.split('\n')

    x, y = lines[1].split(',')
    text_scores1 = pygame.font.SysFont('Corbel', 15).render(
        f'1. {x}: {y}', True, (0, 0, 0))
    x, y = lines[2].split(',')
    text_scores2 = pygame.font.SysFont('Corbel', 15).render(
        f'2. {x}: {y}', True, (0, 0, 0))
    x, y = lines[3].split(',')
    text_scores3 = pygame.font.SysFont('Corbel', 15).render(
        f'3. {x}: {y}', True, (0, 0, 0))
    x, y = lines[4].split(',')
    text_scores4 = pygame.font.SysFont('Corbel', 15).render(
        f'4. {x}: {y}', True, (0, 0, 0))
    x, y = lines[5].split(',')
    text_scores5 = pygame.font.SysFont('Corbel', 15).render(
        f'5. {x}: {y}', True, (0, 0, 0))

    text_highscores = pygame.font.SysFont('Corbel', 30).render(
        'Highscores:', True, (0, 0, 0))

    win.blit(text_highscores, (50, 250))
    win.blit(text_scores1, (50, 280))
    win.blit(text_scores2, (50, 300))
    win.blit(text_scores3, (50, 320))
    win.blit(text_scores4, (50, 340))
    win.blit(text_scores5, (50, 360))


def addScore(newscore):
    HighScores = open('Highscores.txt', 'r')
    lines = HighScores.readlines()
    lines = lines[::-1]
    # print(lines)

    # TODO add an inputbox
    # Turns out its really hard..

    name, score = lines[0].split(',')
    if newscore > int(score):
        # if player score more than lowest highscore
        for I in range(5-1):
            name, score = lines[I+1].split(',')
            if newscore > int(score):
                lines[I] = lines[I+1]
            else:
                lines[I] = f'Challenger,{newscore}\n'
                break  # TODO Change newname to variable when inputbox implemented

        lines = lines[::-1]
        HighScores = open('Highscores.txt', 'w+')
        for I in lines:
            HighScores.write(I)

        drawGameWindow()

        ############################## Define Classes ##################


player1 = snake()
snack = apple()
drawGameWindow()

# main gameLoop
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        if pause:
            pause = False
        else:
            pause = True

    if pause:
        if pygame.mouse.get_pressed() == (1, 0, 0):
            x, y = pygame.mouse.get_pos()
            x -= 100
            y -= 100
            # check if click is in boxes/buttons
            if ((btn_escape[0]+btn_escape[2]) > x > btn_escape[0]):
                if (btn_escape[1] + btn_escape[3]) > y > btn_escape[1]:
                    run = False
            if ((btn_resume[0]+btn_resume[2]) > x > btn_resume[0]) and (player1.died == False):
                if (btn_resume[1] + btn_resume[3]) > y > btn_resume[1]:
                    pause = False
            if ((btn_restart[0]+btn_restart[2]) > x > btn_restart[0]):
                if (btn_restart[1] + btn_restart[3]) > y > btn_restart[1]:
                    # restart()
                    player1.reset()
                    pause = False
            if ((btn_add_highscore[0]+btn_add_highscore[2]) > x > btn_add_highscore[0]):
                if (btn_add_highscore[1] + btn_add_highscore[3]) > y > btn_add_highscore[1]:
                    addScore(player1.score)

        drawHighScores()
        drawPauseWindow()

    else:
        # GAME LOGIC
        player1.move()
        player1.checkCollision()

        x, y, direction = player1.head
        if (snack.x, snack.y) == (x, y):
            player1.eat(player1.head)
            snack.eaten(win)
            # print('eat')

        if keys[pygame.K_RIGHT]:
            if not(player1.direction == 'L'):
                player1.direction = 'R'
        if keys[pygame.K_LEFT]:
            if not(player1.direction == 'R'):
                player1.direction = 'L'
        if keys[pygame.K_UP]:
            if not(player1.direction == 'D'):
                player1.direction = 'U'
        if keys[pygame.K_DOWN]:
            if not(player1.direction == 'U'):
                player1.direction = 'D'

        drawGameWindow()
    # screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    screen.blit(win, (100, 100))
# end of while loop
pygame.quit()
