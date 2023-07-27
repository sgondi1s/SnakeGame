import pygame
import random


# Global Variables
FINAL_SCORE = 0
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE
FPS = 10

CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

STOP = (0, 0)
LIFE = 1

class Snake:
    def __init__(self):
        self.length = 1
        self.score = 0
        self.positions = [CENTER]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = pygame.Color("darkgreen")
        self.outline_color = pygame.Color("slategrey")

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_dir):
        if self.length > 1 and (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        else:
            self.direction = new_dir

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        global LIFE
        new_pos = ((cur[0] + (x * GRID_SIZE)), cur[1] + (y * GRID_SIZE))
        if new_pos[0] < 0 or new_pos[0] >= SCREEN_WIDTH or new_pos[1] < 0 or new_pos[1] >= SCREEN_HEIGHT:
            if LIFE == 0:
                self.die()
            else:
                LIFE=LIFE-1
                self.positions = [CENTER]
                self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
                self.color = pygame.Color("darkgreen")
                self.outline_color = pygame.Color("slategrey")

        elif len(self.positions) > 2 and new_pos in self.positions[2:]:
            if LIFE == 0:
                self.die()
            else:
                LIFE = LIFE - 1
                self.positions = [CENTER]
                self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
                self.color = pygame.Color("darkgreen")
                self.outline_color = pygame.Color("slategrey")
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def die(self):
        global FINAL_SCORE
        self.length = 1
        self.positions = [CENTER]
        self.direction = STOP
        FINAL_SCORE = self.score
        self.score = 0
        gameEnd()

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.outline_color, r, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = pygame.Color("darkgoldenrod3")
        self.outline_color = pygame.Color("slategrey")
        self.randomize_position()

    def randomize_position(self):
        rand_x = random.randint(0, int(GRID_WIDTH - 1))
        rand_y = random.randint(0, int(GRID_HEIGHT - 1))
        self.position = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.outline_color, r, 1)


class World:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def update(self):
        self.snake.move()
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1
            self.food.randomize_position()

    def draw(self, surface):
        self.snake.draw(surface)
        self.food.draw(surface)

    def score(self):
        return self.snake.score

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.turn(RIGHT)


def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("lightslategrey"), r)
            else:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("slategrey"), r)


def run():
    pygame.init()
    global LIFE
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Pygame")
    LIFE = 1
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    draw_grid(surface)

    world = World()

    font = pygame.font.SysFont("monospace", 16)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    world.handle_keys(event)

        clock.tick(FPS)
        world.update()

        draw_grid(surface)
        world.draw(surface)

        screen.blit(surface, (0, 0))
        text = font.render("Score {0}:".format(world.score()), 1, pygame.Color("black"))
        screen.blit(text, (5, 10))
        text1 = font.render("Life :"+ str(LIFE), 1, pygame.Color("pink"))
        screen.blit(text1,(300,10))
        pygame.display.update()

def gameEnd():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global FINAL_SCORE
    pygame.display.set_caption("Snake Pygame ")
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    draw_grid(surface)

    screen.fill("blue")

    my_font1 = pygame.font.SysFont('times new roman', 20)

    with open("score.txt", "a") as f:
        f.write("\n swetha"
                " " + str(+FINAL_SCORE) + " ")

    with open("score.txt", "r") as f:
        score = f.readlines()
        j = 20
        head = my_font1.render(str("       Score"), 1, pygame.Color("red"))
        screen.blit(head, (5, 10))
        for line in score:
            text = my_font1.render(str(line), 1, pygame.Color("green"))
            j += 20
            screen.blit(text, (5, j))

    my_font = pygame.font.SysFont('times new roman', 25)
    scoresdis = my_font.render('   Current Score is'+str(FINAL_SCORE),True,"red")
    screen.blit(scoresdis, (10, j + 20))
    game_over_surface = my_font.render('click space bar ', True, "pink")
    screen.blit(game_over_surface, (30, j + 50))
    running = True
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    run()

def gamePlay():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake Pygame Example")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)
    my_font1 = pygame.font.SysFont('times new roman', 20)

    screen.fill("blue")
    with open("score.txt", "r") as f:
        score = f.readlines()
        j = 50
        head = my_font1.render(str("                                 SCORE "), 1, pygame.Color("red"))
        screen.blit(head, (5, 10))
        nameScore=my_font1.render('NAME  SCORE',True,"green")
        screen.blit(nameScore,(10,40))
        for line in score:
            text = my_font1.render(str(line), 1, pygame.Color("green"))
            j += 20
            screen.blit(text, (5, j))

    my_font = pygame.font.SysFont('times new roman', 25)
    game_over_surface = my_font.render('Click Space Bar to start the game', True, "pink")
    screen.blit(game_over_surface, (30,j+20))

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    run()



if __name__ == '__main__':
    gamePlay()
    pygame.quit()
