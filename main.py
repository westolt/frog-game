import pygame
import random

class FrogGame:
    def __init__(self):
        pygame.init()

        self.new_game()

        self.width = 640
        self.height = 480
        self.scale = self.fly.get_width()
        self.screen = pygame.display.set_mode((self.width, self.height + self.scale))

        self.font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Frog Game")
        self.clock = pygame.time.Clock()

        self.game_loop()

    def new_game(self):
        self.load_frog()
        self.load_fly()
        self.collected_flies = 0

        self.bird_counter = 1
        self.birds = []
        self.load_bird()

        self.escaping = False
        self.won = False
        self.lost = False

        self.lily_pad = pygame.Surface((0, 0))
        self.lily_pad_x = -1000
        self.lily_pad_y = -1000

    def load_frog(self):
        self.frog = pygame.image.load("frog.png")
        width = self.frog.get_width()
        height = self.frog.get_height()

        self.x = random.randint(0, 640 - width - 1)
        self.y = random.randint(0, 480 - height - 1)

        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def load_fly(self):
        self.fly = pygame.image.load("fly.png")
        width = self.fly.get_width()
        height = self.fly.get_height()

        if self.x < 320:
            self.fly_x = random.randint(320, 640 - width)
        else:
            self.fly_x = random.randint(0, 300 - width)

        self.fly_y = random.randint(0, 480 - height)

    def load_bird(self):
        bird_image = pygame.image.load("bird.png")
        width = bird_image.get_width()
        height = bird_image.get_height()

        if self.x < 320:
            x = random.randint(320, 640 - width)
        else:
            x = random.randint(0, 300 - width)

        y = random.randint(0, 480 - height)

        bird = {
            "image": bird_image,
            "x": x,
            "y": y,
            "x_speed": 3,
            "y_speed": 3
        }
        self.birds.append(bird)

    def load_lily_pad(self):
        self.lily_pad = pygame.image.load("lily_pad.png")
        width = self.lily_pad.get_width()
        height = self.lily_pad.get_height()

        if self.x < 320:
            self.lily_pad_x = random.randint(320, 640 - width)
        else:
            self.lily_pad_x = random.randint(0, 300 - width)

        self.lily_pad_y = random.randint(0, 480 - height)

    def game_loop(self):
        while True:
            self.handle_events()
            self.move()
            self.bird_movement()
            self.draw_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.right = True
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False
                if event.key == pygame.K_UP:
                    self.up = False
                if event.key == pygame.K_DOWN:
                    self.down = False

                if event.key == pygame.K_n:
                    self.new_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def move(self):
        if self.won or self.lost:
            return

        # Screen bounds
        if self.y + self.frog.get_height() >= 480:
            self.y = 480 - self.frog.get_height()
            self.down = False
        if self.y <= 0:
            self.up = False
        if self.x + self.frog.get_width() >= 640:
            self.x = 640 - self.frog.get_width()
            self.right = False
        if self.x <= 0:
            self.left = False

        # Movement
        if self.right:
            self.x += 4
        if self.left:
            self.x -= 4
        if self.up:
            self.y -= 4
        if self.down:
            self.y += 4

        # Fly collision
        if self.x < self.fly_x + self.fly.get_width() and self.x + self.frog.get_width() > self.fly_x and self.y < self.fly_y + self.fly.get_height() and self.y + self.frog.get_height() > self.fly_y:
            self.load_fly()
            self.bird_counter += 1
            if self.bird_counter % 2 == 0:
                self.load_bird()
            self.collected_flies += 1
            if self.collected_flies == 10:
                self.escape_lily_pad()

        # Lily pad collision
        if self.x < self.lily_pad_x + self.lily_pad.get_width() - 20 and self.x + self.frog.get_width() - 20 > self.lily_pad_x and self.y < self.lily_pad_y + self.lily_pad.get_height() - 20 and self.y + self.frog.get_height() - 20 > self.lily_pad_y:
            self.win_game()

        # Bird collision
        for bird in self.birds:
            if self.x < bird["x"] + bird["image"].get_width() - 20 and self.x + self.frog.get_width() - 20 > bird["x"] and self.y < bird["y"] + bird["image"].get_height() - 20 and self.y + self.frog.get_height() - 20 > bird["y"]:
                self.lose_game()

    def bird_movement(self):
        for bird in self.birds:
            bird["x"] += bird["x_speed"]
            bird["y"] += bird["y_speed"]

            if bird["x"] <= 0 or bird["x"] + bird["image"].get_width() >= self.width:
                bird["x_speed"] *= -1
            if bird["y"] <= 0 or bird["y"] + bird["image"].get_height() >= self.height:
                bird["y_speed"] *= -1

    def draw_screen(self):
        self.screen.fill((135, 206, 235))  # Light blue background

        # Win message
        if self.won:
            text = self.font.render("Congratulations! You escaped!", True, (255, 255, 255))
            text_x = self.width / 2 - text.get_width() / 2
            text_y = self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (0, 0, 0), (text_x, text_y, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y))

        # Lose message
        if self.lost:
            text = self.font.render("You were eaten!", True, (255, 255, 255))
            text_x = self.width / 2 - text.get_width() / 2
            text_y = self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (0, 0, 0), (text_x, text_y, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y))

        # Lily pad escape
        if self.escaping:
            text = self.font.render("Hide under the lily pad!", True, (255, 255, 255))
            self.screen.blit(self.lily_pad, (self.lily_pad_x, self.lily_pad_y))
            self.screen.blit(text, (self.width / 2 - text.get_width() / 2, (self.height / 2 - text.get_height() / 2) - 30))

        # Draw frog
        if not self.lost and not self.won:
            self.screen.blit(self.frog, (self.x, self.y))

        # Draw fly
        if not self.won and not self.escaping:
            text = self.font.render(f"Eat all the flies: {self.collected_flies} / 10", True, (255, 255, 255))
            self.screen.blit(self.fly, (self.fly_x, self.fly_y))

        # Draw birds
        if not self.won:
            for bird in self.birds:
                self.screen.blit(bird["image"], (bird["x"], bird["y"]))

        # Draw instructions
        instr1 = self.font.render(f"Eat all the flies: {self.collected_flies} / 10", True, (255, 255, 255))
        instr2 = self.font.render("n = new game", True, (255, 255, 255))
        instr3 = self.font.render("Esc = close game", True, (255, 255, 255))

        padding = 5
        bottom_y = self.height
        bottom_width = self.width
        bottom_height = instr1.get_height() + instr2.get_height() + 2 * padding + 5
        pygame.draw.rect(self.screen, (50, 50, 50), (0, bottom_y, bottom_width, bottom_height))

        self.screen.blit(instr1, (padding, bottom_y + padding))
        self.screen.blit(instr2, (self.width - instr2.get_width() - 200, bottom_y + padding))
        self.screen.blit(instr3, (self.width - instr3.get_width() - 5, bottom_y + padding))

        pygame.display.flip()
        self.clock.tick(60)

    def win_game(self):
        self.won = True

    def lose_game(self):
        self.lost = True

    def escape_lily_pad(self):
        self.escaping = True
        self.load_lily_pad()

if __name__ == "__main__":
    FrogGame()