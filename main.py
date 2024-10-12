import tkinter as tk
import random
from tkinter import messagebox
import tkinter.font as tkFont
from datetime import datetime


class Snake:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake")

        # 设置加粗字体
        self.bold_font = tkFont.Font(weight="bold")

        # 设置窗口的最小尺寸
        self.master.minsize(600, 400)

        # 创建画布
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # 创建排行榜界面
        self.score_frame = tk.Frame(self.master, bg="lightgray", width=400)  # 固定宽度
        self.score_frame.grid(row=0, column=1, sticky="ns")  # 仅垂直填充
        self.score_label = tk.Label(self.score_frame, text="排行榜", bg="lightgray", font=("Arial", 14))
        self.score_label.pack()

        # 显示当前分数的文本框
        self.score_text = tk.Text(self.score_frame, width=50, height=15, wrap=tk.WORD)
        self.score_text.pack(fill="both", expand=True)

        # 添加输入框让玩家输入昵称
        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        self.name_label = tk.Label(self.button_frame, text="输入昵称：")
        self.name_label.pack(side="top")

        self.name_entry = tk.Entry(self.button_frame)
        self.name_entry.pack(side="top")

        # 按钮布局在昵称输入框下方
        self.start_button = tk.Button(self.button_frame, text="开始游戏", command=self.start_game, state=tk.NORMAL)
        self.start_button.pack(side="top", pady=5)

        self.pause_button = tk.Button(self.button_frame, text="暂停游戏", command=self.pause_game, state=tk.DISABLED)
        self.pause_button.pack(side="top", pady=5)

        self.resume_button = tk.Button(self.button_frame, text="继续游戏", command=self.resume_game, state=tk.DISABLED)
        self.resume_button.pack(side="top", pady=5)

        self.restart_button = tk.Button(self.button_frame, text="重新开始", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack(side="top", pady=5)

        # 初始化游戏数据
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.food = (5, 5)
        self.direction = "Right"
        self.score = 0
        self.game_running = False
        self.game_paused = False
        self.default_name = "玩家"

        # 边界值初始化
        self.canvas_width = 400
        self.canvas_height = 400

        # 绑定窗口尺寸变化事件
        self.master.bind("<Configure>", self.on_resize)
        self.master.bind("<Key>", self.on_key_press)

        # 允许调整窗口大小
        self.master.rowconfigure(0, weight=3)
        self.master.columnconfigure(0, weight=3)

        # 绘制初始网格
        self.draw_background()

    def on_resize(self, event):
        """在窗口调整大小时更新画布尺寸并重新绘制背景"""
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.draw_background()

    def draw_background(self):
        """绘制背景，边缘不足一格的部分填充为灰色"""
        self.canvas.delete("background")
        grid_size = 20

        # 填充背景
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="white", tags="background")

        # 绘制完整的网格背景
        for x in range(0, self.canvas_width, grid_size):
            for y in range(0, self.canvas_height, grid_size):
                # 绘制网格
                if x + grid_size <= self.canvas_width and y + grid_size <= self.canvas_height:
                    self.canvas.create_rectangle(x, y, x + grid_size, y + grid_size, outline="black", tags="background")

        # 绘制边缘的灰色区域
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, outline="black", width=2,
                                     tags="background")

    def start_game(self):
        if not self.game_running:
            self.score = 0  # 重置分数
            self.name = self.name_entry.get() or self.default_name  # 记录当前昵称，默认为“玩家”
            self.game_running = True
            self.game_paused = False
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)  # 禁用继续游戏按钮
            self.start_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.DISABLED)
            self.update_game()

    def pause_game(self):
        if self.game_running and not self.game_paused:
            self.game_paused = True
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)  # 启用继续游戏按钮

    def resume_game(self):
        if self.game_paused:
            self.game_paused = False
            self.resume_button.config(state=tk.DISABLED)  # 禁用继续游戏按钮
            self.pause_button.config(state=tk.NORMAL)  # 启用暂停按钮

    def restart_game(self):
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.food = (5, 5)
        self.direction = "Right"
        self.score = 0
        self.game_running = False
        self.game_paused = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)

    def update_game(self):
        if not self.game_paused:
            head_x, head_y = self.snake[-1]
            if self.direction == "Left":
                new_head = (head_x - 1, head_y)
            elif self.direction == "Right":
                new_head = (head_x + 1, head_y)
            elif self.direction == "Up":
                new_head = (head_x, head_y - 1)
            else:
                new_head = (head_x, head_y + 1)
            self.snake.append(new_head)
            del self.snake[0]

            # 计算边界基于当前窗口大小
            max_x = (self.canvas_width // 20) - 1
            max_y = (self.canvas_height // 20) - 1

            # 检查游戏是否结束
            if new_head[0] < 0 or new_head[0] > max_x or new_head[1] < 0 or new_head[1] > max_y or new_head in self.snake[:-1]:
                self.game_running = False
                messagebox.showinfo("Game Over", f"Score: {self.score}")
                self.restart_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.resume_button.config(state=tk.DISABLED)
                self.update_scoreboard()
                return

            # 检查贪吃蛇是否吃掉食物
            if new_head == self.food:
                while True:
                    food_x = random.randint(0, max_x)
                    food_y = random.randint(0, max_y)
                    if (food_x, food_y) not in self.snake:
                        break
                self.food = (food_x, food_y)
                tail_x, tail_y = self.snake[0]
                self.snake.insert(0, (tail_x, tail_y))
                self.score += 1

            # 绘制贪吃蛇和食物
            self.draw_snake()
            self.draw_food()

        self.master.after(200, self.update_game)

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            x1 = x * 20
            y1 = y * 20
            x2 = x1 + 20
            y2 = y1 + 20
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x1 = self.food[0] * 20
        y1 = self.food[1] * 20
        x2 = x1 + 20
        y2 = y1 + 20
        self.canvas.create_oval(x1, y1, x2, y2, fill="red", tags="food")

    def update_scoreboard(self):
        if not self.game_running and not self.game_paused:
            grid_length = self.canvas_width // 20
            grid_width = self.canvas_height // 20
            score_entry = f"{self.name}: {self.score} "

            # 在 Text 中插入名称和分数，并设置名称和分数为加粗
            self.score_text.insert(tk.END, score_entry, "bold")

            # 插入尺寸部分并添加下划线样式
            size_part = f"({grid_length} × {grid_width}) "
            self.score_text.insert(tk.END, size_part, "size_part")

            # 插入时间戳
            timestamp = f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
            self.score_text.insert(tk.END, timestamp)

            # 设置样式
            self.score_text.tag_config("bold", font=self.bold_font)
            self.score_text.tag_config("size_part", underline=True)

            # 绑定双击事件到最新插入的尺寸部分
            self.score_text.tag_bind("size_part", "<Double-Button-1>", self.on_double_click)

    def on_double_click(self, event):
        """双击某条尺寸记录时，调整窗口的网格尺寸"""
        index = self.score_text.index(f"@{event.x},{event.y}")
        current_line = self.score_text.get(f"{index} linestart", f"{index} lineend")

        # 查找尺寸部分
        try:
            dimensions_string = current_line.split("(")[-2].strip().rstrip(')')
            grid_length, grid_width = map(int, dimensions_string.replace('×', 'x').split('x'))

            # 计算每个网格大小为 20 像素，得到画布的宽度和高度
            new_canvas_width = grid_length * 20
            new_canvas_height = grid_width * 20

            # 获取排行榜宽度
            score_frame_width = self.score_frame.winfo_width()

            # 获取按钮框架的高度
            button_frame_height = self.button_frame.winfo_height()

            # 计算新的窗口宽度和高度
            new_window_width = new_canvas_width + score_frame_width
            new_window_height = new_canvas_height + button_frame_height + 20

            # 取消最大化状态
            self.master.state('normal')

            # 更新画布的尺寸
            self.canvas.config(width=new_canvas_width, height=new_canvas_height)

            # 调整窗口尺寸
            self.master.geometry(f"{new_window_width}x{new_window_height}")

            # 更新画布宽度和高度属性
            self.canvas_width = new_canvas_width
            self.canvas_height = new_canvas_height

            # 重新绘制背景
            self.draw_background()

        except (IndexError, ValueError):
            messagebox.showerror("Error", "无法解析尺寸信息。")

    def on_key_press(self, event):
        if event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"


if __name__ == "__main__":
    root = tk.Tk()
    snake = Snake(root)
    root.mainloop()