import tkinter as tk
import pygame

# Configuration
CELL_SIZE =15 
HEIGHT =33 
WIDTH =50 
DELAY = 0.1  # delay between generations in seconds

# Initialize pygame mixer for sound
pygame.mixer.init()
click_sound = pygame.mixer.Sound("/home/admin-cse/Sounds/mouse-click-290204.mp3")
loop_sound = pygame.mixer.Sound("/home/admin-cse/Sounds/be-more-serious-loop-275528.mp3")

class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.running = False
        self.paused = False
        self.generation = 0

        self.root.configure(bg="black")
        self.root.resizable(True, True)

        self.canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Labels
        self.gen_label = tk.Label(root, text="Generation: 0", bg="black", fg="white", font=("Arial", 12))
        self.gen_label.pack()
        self.population_label = tk.Label(root, text="Population: 0", bg="black", fg="white", font=("Arial", 12))
        self.population_label.pack()

        # Buttons
        btn_style = {
            "bg": "#222222", "fg": "white", "activebackground": "#444444",
            "activeforeground": "lime", "font": ("Arial", 11), "width": 15
        }
        self.start_button = tk.Button(root, text="▶ Start", command=self.start_simulation, **btn_style)
        self.start_button.pack(pady=3)

        self.pause_button = tk.Button(root, text="⏸ Pause", command=self.toggle_pause, state="disabled", **btn_style)
        self.pause_button.pack(pady=3)

        # Go to Generation
        gen_frame = tk.Frame(root, bg="black")
        gen_frame.pack(pady=5)
        self.gen_entry = tk.Entry(gen_frame, width=10, font=("Arial", 11))
        self.gen_entry.pack(side="left", padx=(0, 5))
        self.goto_button = tk.Button(gen_frame, text="⏩ Go to Gen", command=self.go_to_generation, **btn_style)
        self.goto_button.pack(side="left")

        self.reset_button = tk.Button(root, text="🔄 Reset", command=self.reset_simulation, **btn_style)
        self.reset_button.pack(pady=3)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        population = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if self.grid[y][x] == 1:
                    fill = "#00FF00"
                    population += 1
                else:
                    fill = "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#444444")
        self.gen_label.config(text=f"Generation: {self.generation}")
        self.population_label.config(text=f"Population: {population}")

    def toggle_cell(self, event):
        if self.running and not self.paused:
            return
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.grid[y][x] ^= 1
            click_sound.play()
            self.draw_grid()

    def count_neighbors(self, y, x):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny = (y + dy) % HEIGHT
                nx = (x + dx) % WIDTH
                count += self.grid[ny][nx]
        return count

    def next_generation(self):
        new_grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                neighbors = self.count_neighbors(y, x)
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if neighbors == 3 else 0
        self.grid = new_grid
        self.generation += 1

    def simulation_step(self):
        if self.running and not self.paused:
            self.next_generation()
            self.draw_grid()
        if self.running:
            self.root.after(int(DELAY * 1000), self.simulation_step)
        else:
            loop_sound.stop()
            self.pause_button.config(state="disabled")

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.pause_button.config(state="normal", text="⏸ Pause")
            loop_sound.play(-1)
            self.simulation_step()

    def toggle_pause(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text="▶ Resume")
                loop_sound.stop()
            else:
                self.pause_button.config(text="⏸ Pause")
                loop_sound.play(-1)

    def go_to_generation(self):
        try:
            target = int(self.gen_entry.get())
            if target < self.generation:
                return  # Don't go backward
            while self.generation < target:
                self.next_generation()
            self.draw_grid()
        except ValueError:
            pass  # Invalid input

    def reset_simulation(self):
        self.running = False
        self.paused = False
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.generation = 0
        loop_sound.stop()
        self.draw_grid()

def show_rules():
    rules_window = tk.Toplevel()
    rules_window.title("Game Rules")
    rules_window.geometry("500x300")
    rules_window.configure(bg="#f0f4f7")

    title = tk.Label(rules_window, text="Rules of Conway's Game of Life", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#333")
    title.pack(pady=10)

    rules_text = (
    "Introduction.\n\n"
         "John Conway’s Game of Life\n\n"
    "The Game of Life is not a typical computer game. It is a cellular automaton, invented by Cambridge mathematician John Horton Conway.\n\n"
    "It consists of a collection of cells which, based on a few mathematical rules, can live, die or multiply. Depending on the initial conditions, the cells form various patterns throughout the course of the game.\n\n"
    "In the game, each cell can only be in 'live' or 'dead' states. According to the following rules, calculate the state of each cell in the next generation and draw the life and death distribution map of the next generation of cells.\n\n"
    "The state of each cell after iteration is determined by the state of the cell and the surrounding eight cells.\n\n" 
        "Rules:\n\n"
        "1. Any live cell with fewer than two live neighbours dies (underpopulation).\n\n"
        "2. Any live cell with two or three live neighbours lives on to the next generation (survival).\n\n"
        "3. Any live cell with more than three live neighbours dies (overpopulation).\n\n"
        "4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction)."
    )

    text_widget = tk.Text(rules_window, wrap="word", font=("Helvetica", 12), bg="#ffffff", fg="#000000", bd=2, relief="groove")
    text_widget.insert("1.0", rules_text)
    text_widget.config(state="disabled")
    text_widget.pack(padx=20, pady=10, expand=True, fill="both")

def launch_game():
    welcome_root.destroy()
    main_root = tk.Tk()
    main_root.title("Conway's Game of Life")
    app = GameOfLife(main_root)
    main_root.mainloop()

if __name__ == "__main__":
    welcome_root = tk.Tk()
    welcome_root.title("Game of Life - Start Screen")
    welcome_root.geometry("600x400")
    welcome_root.configure(bg="#1c1c1c")
    welcome_root.resizable(True, True)
    frame = tk.Frame(welcome_root, bg="#1c1c1c")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    welcome_label = tk.Label(frame, text="Welcome to Conway's Game of Life", 
                             font=("Helvetica", 20, "bold"), bg="#1c1c1c", fg="white")
    welcome_label.pack(pady=(0, 20))

    start_button = tk.Button(frame, text="Let's Begin", font=("Helvetica", 14),
                             bg="#333333", fg="white", bd=0, relief="flat",
                             padx=20, pady=10, activebackground="#444444",
                             activeforeground="lime", command=launch_game)
    start_button.pack()

    rules_button = tk.Button(frame, text="View Rules", font=("Helvetica", 12),
                             bg="#e6e6e6", fg="#333333", bd=1, relief="ridge",
                             padx=15, pady=4, command=show_rules)
    rules_button.pack(pady=5)

    welcome_root.mainloop()

      
               

   
            
    
    
    
    
