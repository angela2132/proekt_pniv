# Project Mathematical Sudoku

Angela Azhieska 213217
Mia Stevkovska 213172

"Mathematical Sudoku" е логичка игра базирана на решавање на едноставни математички равенки поставени во матрица од 5x5 полиња. Играчот треба да го пронајде точниот број што недостасува во равенката. Ако одговорот е точен, полето се пополнува и играчот добива поен. Ако одговорот е неточен, играчот губи живот. Играта завршува кога ќе се решат сите равенки или кога ќе се изгубат сите животи.

# Клучни функционалности
# Генерирање равенки: Се создаваат случајни равенки со оператори (+, -, *, /) и еден празен елемент кој играчот треба да го пополни.
def generate_equation():
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)
    if operator == '+':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        result = num1 + num2
    elif operator == '-':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, num1)
        result = num1 - num2
    elif operator == '*':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        result = num1 * num2
    else:  
        num2 = random.randint(1, 10)
        result = random.randint(1, 10)
        num1 = num2 * result  
    blank_position = random.randint(0, 1)
    equation = []
    if blank_position == 0:
        correct_answer = num1
        equation = ["_", operator, str(num2), "=", str(result)]
    else:
        correct_answer = num2
        equation = [str(num1), operator, "_", "=", str(result)]
    return equation, correct_answer

# Проверка на точноста на одговорите: Ако играчот внесе точен број, полето се пополнува; ако е погрешно, се губи живот.
def check_equation(equation, answer):
    try:
        answer = float(answer)
        blank_pos = equation.index("_")
        operator = equation[1]
        result = float(equation[4])
        if blank_pos == 0:
            num2 = float(equation[2])
            if operator == "+": return abs(answer + num2 - result) < 0.0001
            if operator == "-": return abs(answer - num2 - result) < 0.0001
            if operator == "*": return abs(answer * num2 - result) < 0.0001
            if operator == "/": return abs(answer / num2 - result) < 0.0001
        elif blank_pos == 2:
            num1 = float(equation[0])
            if operator == "+": return abs(num1 + answer - result) < 0.0001
            if operator == "-": return abs(num1 - answer - result) < 0.0001
            if operator == "*": return abs(num1 * answer - result) < 0.0001
            if operator == "/": return abs(num1 / answer - result) < 0.0001
        return False
    except (ValueError, ZeroDivisionError):
        return False

# Систем за животи: Играчот има три животи и ако ги изгуби сите, играта завршува.
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

# Приказ на резултат и повратна информација: Играчот добива визуелна повратна информација за точноста на одговорот.

def draw_victory_screen(self, screen):
    screen.fill(BACKGROUND_COLOR)
    victory_text = large_font.render("You Won!", True, GREEN)
    text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(victory_text, text_rect)
    
def draw_game_over_screen(self, screen):
    screen.fill(BACKGROUND_COLOR)
    game_over_text = large_font.render("Game Over!", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(game_over_text, text_rect)

# Графички приказ: Матрицата, бројките, боите за операторите и различните ефекти се прикажани со Pygame.
# Екрани за победа/пораз: При завршување на играта, се прикажува екран за победа или пораз.
