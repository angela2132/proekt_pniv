import pygame
import sys
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mathematical Sudoku")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BACKGROUND_COLOR = (230, 240, 255)


OPERATOR_COLORS = {
    '+': (46, 204, 113),  # Green
    '-': (231, 76, 60),  # Red
    '*': (155, 89, 182),  # Purple
    '/': (52, 152, 219)  # Blue
}


font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 80)
title_font = pygame.font.SysFont(None, 60)


MATRIX_SIZE = 600
CELL_SIZE = MATRIX_SIZE // 5
TOP_MARGIN = 150
MATRIX_START_X = (SCREEN_WIDTH - MATRIX_SIZE) // 2
MATRIX_START_Y = TOP_MARGIN


def generate_equation():
#random odbiranje na operator
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)

    #odbiranje random broevi
    if operator == '+':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        result = num1 + num2
    elif operator == '-':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, num1)  #da sbideme sigurni deka ke bide pozitivem broj
        result = num1 - num2
    elif operator == '*':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        result = num1 * num2
    else:  # division
        num2 = random.randint(1, 10)
        result = random.randint(1, 10)
        num1 = num2 * result  #da bideme sigurni deka delenjeto e tocno

    #random da bira prazno pole
    blank_position = random.randint(0, 1)
    equation = []

    if blank_position == 0:
        correct_answer = num1
        equation = ["_", operator, str(num2), "=", str(result)]
    else:
        correct_answer = num2
        equation = [str(num1), operator, "_", "=", str(result)]

    return equation, correct_answer


def generate_game_board():

    equations = []
    answers = []

    for _ in range(5):
        eq, ans = generate_equation()
        equations.append(eq)
        answers.append(ans)

    return equations, answers


def check_equation(equation, answer):

    try:

        answer = float(answer)


        blank_pos = equation.index("_")


        operator = equation[1]
        result = float(equation[4])


        if blank_pos == 0:  #ako e prvata kocka prazna
            num2 = float(equation[2])
            if operator == "+": return abs(answer + num2 - result) < 0.0001
            if operator == "-": return abs(answer - num2 - result) < 0.0001
            if operator == "*": return abs(answer * num2 - result) < 0.0001
            if operator == "/": return abs(answer / num2 - result) < 0.0001

        elif blank_pos == 2:  #ako e vtorata kocka prazna
            num1 = float(equation[0])
            if operator == "+": return abs(num1 + answer - result) < 0.0001
            if operator == "-": return abs(num1 - answer - result) < 0.0001
            if operator == "*": return abs(num1 * answer - result) < 0.0001
            if operator == "/": return abs(num1 / answer - result) < 0.0001

        return False

    except (ValueError, ZeroDivisionError):
        return False


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.equations, self.correct_answers = generate_game_board()
        self.selected_cell = None
        self.answer = ""
        self.lives = 3
        self.score = 0
        self.correct_cells = set()
        self.game_over = False
        self.won = False
        self.feedback_message = ""
        self.feedback_timer = 0
        self.filled_answers = {}
        self.show_victory_screen = False
        self.show_game_over_screen = False

    def handle_answer(self, row, col):

        if self.answer and self.equations[row][col] == "_":
            if check_equation(self.equations[row], self.answer):
                # Correct answer - save it
                self.correct_cells.add((row, col))
                self.filled_answers[(row, col)] = self.answer
                blank_index = self.equations[row].index("_")
                self.equations[row][blank_index] = self.answer
                self.score += 1
                self.feedback_message = "Correct!"
                if len(self.correct_cells) == 5:
                    self.won = True
                    self.game_over = True
                    self.show_victory_screen = True
            else:

                self.lives -= 1
                self.feedback_message = "Wrong! Lost a life!"
                if self.lives <= 0:
                    self.game_over = True
                    self.show_game_over_screen = True

            self.feedback_timer = 60
            self.answer = ""
            self.selected_cell = None

    def draw_hearts(self, screen):

        heart_width = 30
        heart_spacing = 40
        start_x = SCREEN_WIDTH - 200

        for i in range(self.lives):
            x = start_x + (i * heart_spacing)
            pygame.draw.circle(screen, RED, (x, 70), 10)
            pygame.draw.circle(screen, RED, (x + 10, 70), 10)
            points = [(x - 10, 70), (x + 20, 70), (x + 5, 90)]
            pygame.draw.polygon(screen, RED, points)

    def draw_victory_screen(self, screen):
        screen.fill(BACKGROUND_COLOR)


        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice(list(OPERATOR_COLORS.values()))
            pygame.draw.circle(screen, color, (x, y), 5)

        victory_text = large_font.render("You Won!", True, GREEN)
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(victory_text, text_rect)

        score_text = font.render(f"Final Score: {self.score}", True, BLUE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        restart_text = font.render("Press R to Play Again", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(restart_text, restart_rect)

        border_width = 10
        pygame.draw.rect(screen, GREEN, (border_width, border_width,
                                         SCREEN_WIDTH - 2 * border_width, SCREEN_HEIGHT - 2 * border_width),
                         border_width)

    def draw_game_over_screen(self, screen):
        screen.fill(BACKGROUND_COLOR)

        game_over_text = large_font.render("Game Over!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, text_rect)

        score_text = font.render(f"Final Score: {self.score}", True, BLUE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        restart_text = font.render("Press R to Try Again", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(restart_text, restart_rect)

        border_width = 10
        pygame.draw.rect(screen, RED, (border_width, border_width,
                                       SCREEN_WIDTH - 2 * border_width, SCREEN_HEIGHT - 2 * border_width),
                         border_width)

    def draw(self, screen):
        if self.show_victory_screen:
            self.draw_victory_screen(screen)
            return

        if self.show_game_over_screen:
            self.draw_game_over_screen(screen)
            return

        screen.fill(BACKGROUND_COLOR)


        title_shadow = title_font.render("Mathematical Sudoku", True, (100, 100, 100))
        title = title_font.render("Mathematical Sudoku", True, BLACK)
        shadow_offset = 2
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title_shadow, (title_rect.x + shadow_offset, title_rect.y + shadow_offset))
        screen.blit(title, title_rect)


        score_bg = pygame.Rect(10, 60, 150, 40)
        pygame.draw.rect(screen, WHITE, score_bg, border_radius=10)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 70))

        self.draw_hearts(screen)

        if self.feedback_timer > 0:
            feedback_color = GREEN if "Correct" in self.feedback_message else RED
            feedback_surface = font.render(self.feedback_message, True, feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(feedback_surface, feedback_rect)
            self.feedback_timer -= 1


        for i in range(5):
            for j in range(5):
                cell_rect = pygame.Rect(MATRIX_START_X + j * CELL_SIZE,
                                        MATRIX_START_Y + i * CELL_SIZE,
                                        CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, cell_rect)
                pygame.draw.rect(screen, BLACK, cell_rect, 1)


        for i in range(6):
            pygame.draw.line(screen,
                             BLACK,
                             (MATRIX_START_X + i * CELL_SIZE, MATRIX_START_Y),
                             (MATRIX_START_X + i * CELL_SIZE, MATRIX_START_Y + MATRIX_SIZE),
                             3)
            pygame.draw.line(screen,
                             BLACK,
                             (MATRIX_START_X, MATRIX_START_Y + i * CELL_SIZE),
                             (MATRIX_START_X + MATRIX_SIZE, MATRIX_START_Y + i * CELL_SIZE),
                             3)


        for row in range(5):
            for col in range(5):
                x = MATRIX_START_X + col * CELL_SIZE
                y = MATRIX_START_Y + row * CELL_SIZE
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if self.selected_cell == (row, col):
                    pygame.draw.rect(screen, YELLOW, cell_rect)
                elif (row, col) in self.correct_cells:
                    pygame.draw.rect(screen, (200, 255, 200), cell_rect)

                if col < len(self.equations[row]):
                    if (row, col) in self.filled_answers:
                        text = self.filled_answers[(row, col)]
                        color = BLACK
                    else:
                        text = self.equations[row][col]
                        if text in OPERATOR_COLORS:
                            color = OPERATOR_COLORS[text]
                        else:
                            color = BLACK
                        if text == "_" and self.selected_cell == (row, col) and self.answer:
                            text = self.answer

                    text_surface = font.render(text, True, color)
                    text_rect = text_surface.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(text_surface, text_rect)


def main():
    game = Game()
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
                continue

            if not game.game_over and not game.show_victory_screen and not game.show_game_over_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (MATRIX_START_X <= x <= MATRIX_START_X + MATRIX_SIZE and
                            MATRIX_START_Y <= y <= MATRIX_START_Y + MATRIX_SIZE):
                        col = (x - MATRIX_START_X) // CELL_SIZE
                        row = (y - MATRIX_START_Y) // CELL_SIZE
                        if row < 5 and col < 5 and col < len(game.equations[row]):
                            if game.equations[row][col] == "_" and (row, col) not in game.filled_answers:
                                game.selected_cell = (row, col)
                                game.answer = ""
                            else:
                                game.selected_cell = None

                elif event.type == pygame.KEYDOWN:
                    if game.selected_cell:
                        row, col = game.selected_cell
                        if event.key == pygame.K_RETURN:
                            game.handle_answer(row, col)
                        elif event.key == pygame.K_BACKSPACE:
                            game.answer = game.answer[:-1]
                        elif event.unicode.isdigit() and len(game.answer) < 3:
                            game.answer += event.unicode

        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()