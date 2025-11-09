import tkinter as tk
import random


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Синяя змейка с манго")
        self.window.resizable(False, False)

        # Настройки игры
        self.cell_size = 25
        self.grid_width = 25
        self.grid_height = 25
        self.speed = 120

        # Создание холста
        self.canvas = tk.Canvas(
            self.window,
            width=self.grid_width * self.cell_size,
            height=self.grid_height * self.cell_size,
            bg="black"
        )
        self.canvas.pack()

        # Создание счета
        self.score = 0
        self.score_label = tk.Label(
            self.window,
            text=f"Счет: {self.score}",
            font=("Arial", 16),
            fg="white",
            bg="black"
        )
        self.score_label.pack()

        # Инструкция
        self.instruction_label = tk.Label(
            self.window,
            text="Управление: Стрелки ←↑↓→ | Перезапуск: R",
            font=("Arial", 10),
            fg="gray",
            bg="black"
        )
        self.instruction_label.pack()

        # Инициализация игры
        self.reset_game()

        # Привязка клавиш
        self.window.bind("<KeyPress>", self.on_key_press)
        self.window.focus_set()

    def reset_game(self):
        # Позиция змейки
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.next_direction = "Right"

        # Создание манго
        self.create_mango()

        self.score = 0
        self.score_label.config(text=f"Счет: {self.score}")
        self.game_over = False
        self.speed = 120

    def create_mango(self):
        while True:
            x = random.randint(2, self.grid_width - 3)
            y = random.randint(2, self.grid_height - 3)
            if (x, y) not in self.snake:
                self.mango_pos = (x, y)
                break

    def on_key_press(self, event):
        if self.game_over and event.keysym == "r":
            self.reset_game()
            return

        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            # Запрет движения в противоположном направлении
            if (key == "Up" and self.direction != "Down") or \
                    (key == "Down" and self.direction != "Up") or \
                    (key == "Left" and self.direction != "Right") or \
                    (key == "Right" and self.direction != "Left"):
                self.next_direction = key

    def move_snake(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        # Получаем текущую позицию головы
        head_x, head_y = self.snake[0]

        # Вычисляем новую позицию головы
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)

        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over = True
            return

        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over = True
            return

        # Добавляем новую голову
        self.snake.insert(0, new_head)

        # Проверка съедания манго
        if new_head == self.mango_pos:
            self.score += 1
            self.score_label.config(text=f"Счет: {self.score}")
            self.create_mango()

            # Увеличиваем скорость каждые 5 очков
            if self.score % 5 == 0 and self.speed > 50:
                self.speed -= 10
        else:
            # Удаляем хвост, если не съели манго
            self.snake.pop()

    def draw_mango(self, x, y):
        size = self.cell_size
        center_x = x * size + size // 2
        center_y = y * size + size // 2
        mango_width = size // 2
        mango_height = size // 1.5

        # Основная часть манго (оранжевый овал)
        self.canvas.create_oval(
            center_x - mango_width,
            center_y - mango_height // 2,
            center_x + mango_width,
            center_y + mango_height // 2,
            fill="#FFA500",
            outline="#FF8C00",
            width=2
        )

        # Текстура манго (светлые пятна)
        spot_radius = size // 8
        self.canvas.create_oval(
            center_x - spot_radius,
            center_y - spot_radius // 2,
            center_x + spot_radius,
            center_y + spot_radius // 2,
            fill="#FFD700",
            outline=""
        )

        # Черенок (коричневый прямоугольник)
        stem_width = size // 10
        stem_height = size // 6
        self.canvas.create_rectangle(
            center_x - stem_width // 2,
            center_y - mango_height // 2 - stem_height,
            center_x + stem_width // 2,
            center_y - mango_height // 2,
            fill="#8B4513",
            outline=""
        )

        # Листик (зеленый овал)
        leaf_width = size // 4
        leaf_height = size // 8
        self.canvas.create_oval(
            center_x + stem_width,
            center_y - mango_height // 2 - leaf_height,
            center_x + stem_width + leaf_width,
            center_y - mango_height // 2 + leaf_height,
            fill="#32CD32",
            outline=""
        )

    def draw(self):
        self.canvas.delete("all")

        if not self.game_over:
            # Рисуем змейку (синюю)
            for i, (x, y) in enumerate(self.snake):
                if i == 0:  # Голова
                    color = "#1E90FF"  # Ярко-синий
                    # Добавляем глаза на голову
                    size = self.cell_size
                    self.canvas.create_rectangle(
                        x * size, y * size,
                        (x + 1) * size, (y + 1) * size,
                        fill=color, outline="#4169E1"
                    )
                    # Глаза змейки (белые с черными зрачками)
                    eye_size = size // 6
                    # Левый глаз
                    self.canvas.create_oval(
                        x * size + size // 3 - eye_size,
                        y * size + size // 3 - eye_size,
                        x * size + size // 3 + eye_size,
                        y * size + size // 3 + eye_size,
                        fill="white"
                    )
                    self.canvas.create_oval(
                        x * size + size // 3 - eye_size // 2,
                        y * size + size // 3 - eye_size // 2,
                        x * size + size // 3 + eye_size // 2,
                        y * size + size // 3 + eye_size // 2,
                        fill="black"
                    )
                    # Правый глаз
                    self.canvas.create_oval(
                        x * size + 2 * size // 3 - eye_size,
                        y * size + size // 3 - eye_size,
                        x * size + 2 * size // 3 + eye_size,
                        y * size + size // 3 + eye_size,
                        fill="white"
                    )
                    self.canvas.create_oval(
                        x * size + 2 * size // 3 - eye_size // 2,
                        y * size + size // 3 - eye_size // 2,
                        x * size + 2 * size // 3 + eye_size // 2,
                        y * size + size // 3 + eye_size // 2,
                        fill="black"
                    )
                else:  # Тело
                    # Чередующиеся оттенки синего
                    color = "#4169E1" if i % 2 == 0 else "#1E90FF"
                    self.canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill=color,
                        outline="#0000CD"
                    )

            # Рисуем манго
            self.draw_mango(*self.mango_pos)

        else:
            self.show_game_over()

    def show_game_over(self):
        self.canvas.create_rectangle(
            self.grid_width * self.cell_size // 4,
            self.grid_height * self.cell_size // 3,
            3 * self.grid_width * self.cell_size // 4,
            2 * self.grid_height * self.cell_size // 3,
            fill="#2F4F4F",
            outline="#1E90FF",
            width=3
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2 - 30,
            text="ИГРА ОКОНЧЕНА!",
            fill="#1E90FF",
            font=("Arial", 24, "bold"),
            justify=tk.CENTER
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2,
            text=f"Собрано манго: {self.score}",
            fill="white",
            font=("Arial", 16),
            justify=tk.CENTER
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2 + 30,
            text="Нажми R для новой игры",
            fill="#FFA500",
            font=("Arial", 14),
            justify=tk.CENTER
        )

    def game_loop(self):
        if not self.game_over:
            self.move_snake()
        self.draw()
        self.window.after(self.speed, self.game_loop)

    def start(self):
        self.game_loop()
        self.window.mainloop()


# Создание и запуск игры
game = SnakeGame()
game.start()