import random
import curses


class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = curses.KEY_RIGHT
        self.food = self.generate_food()

    def generate_food(self):
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food

    def update(self):
        try:
            key = self.window.getkey()
        except:
            key = None

        if key is not None:
            if key.lower() == "w" and self.direction != curses.KEY_DOWN:
                self.direction = curses.KEY_UP
            elif key.lower() == "s" and self.direction != curses.KEY_UP:
                self.direction = curses.KEY_DOWN
            elif key.lower() == "a" and self.direction != curses.KEY_RIGHT:
                self.direction = curses.KEY_LEFT
            elif key.lower() == "d" and self.direction != curses.KEY_LEFT:
                self.direction = curses.KEY_RIGHT

        head = self.snake[0]
        if self.direction == curses.KEY_UP:
            new_head = (head[0], head[1] - 1)
        elif self.direction == curses.KEY_DOWN:
            new_head = (head[0], head[1] + 1)
        elif self.direction == curses.KEY_LEFT:
            new_head = (head[0] - 1, head[1])
        else:
            new_head = (head[0] + 1, head[1])

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def display(self):
        self.window.clear()
        self.window.border()

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.snake:
                    self.window.addch(y + 1, x + 1, "*")
                elif (x, y) == self.food:
                    self.window.addch(y + 1, x + 1, "#")

        self.window.refresh()

    def run(self):
        try:
            curses.initscr()
            curses.curs_set(0)
            self.window = curses.newwin(self.height + 2, self.width + 2, 0, 0)
            self.window.timeout(100)

            while True:
                self.display()
                self.update()
                if self.is_collision():
                    break

        except (curses.error, KeyboardInterrupt):
            pass

        finally:
            curses.endwin()

    def is_collision(self):
        head = self.snake[0]
        if (
            head[0] < 0
            or head[0] >= self.width
            or head[1] < 0
            or head[1] >= self.height
            or head in self.snake[1:]
        ):
            return True
        return False
