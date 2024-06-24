from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIR = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        """Инациализация объекта."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объекта."""
        pass

    def draw_cell(self, rect):
        """Общая отрисовка"""
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self):
        """Инациализация Apple."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        self.draw_cell(rect)

    def randomize_position(self):
        """Вычисление случайного положения Apple."""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self):
        """Инициализация Snake."""
        super().__init__()
        self.reset()
        self.body_color = SNAKE_COLOR

    def draw(self):
        """Отрисовка Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            self.draw_cell(rect)
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        self.draw_cell(head_rect)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновление направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращение позиции головы змейки"""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice(DIR)
        self.next_direction = None
        self.last = None

    def move(self):
        """Обновление позиции змейки."""
        head_now = self.get_head_position()
        coordinate_x, coordinate_y = head_now
        new_head = ((coordinate_x + self.direction[0]) % SCREEN_WIDTH,
                    (coordinate_y + self.direction[1]) % SCREEN_HEIGHT)
        if new_head in self.positions:
            self.reset()
        self.positions.insert(0, new_head)
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Обработка действиий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        handle_keys(snake)
        snake.move()
        snake.update_direction()
        if snake.get_head_position == apple.position:
            snake.lenght += 1
            while True:
                if apple.randomize_position() in snake.positions:
                    apple.randomize_position()
                    return False

        pygame.display.update()


if __name__ == '__main__':
    main()
