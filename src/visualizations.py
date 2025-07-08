import tkinter as tk
from tkinter import messagebox, ttk
from pda_logic import PDA  # Ensure your PDA logic file has this class

class PDAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA Palindrome Visualizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f2f5")

        self.pda = None
        self.steps = []
        self.current_step = 0

        self.FONT = ("Segoe UI", 11)
        self.BOLD_FONT = ("Segoe UI", 11, "bold")

        # Title label
        title = ttk.Label(root, text="PDA Palindrome Visualizer", font=("Segoe UI", 16, "bold"), anchor="center")
        title.pack(pady=10)

        # Canvas for visualizing PDA
        self.canvas = tk.Canvas(root, width=880, height=400, bg="#ffffff", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame for input and buttons
        ribbon_frame = ttk.Frame(root)
        ribbon_frame.pack(side=tk.TOP, pady=10)

        self.input_entry = ttk.Entry(ribbon_frame, width=30, font=self.FONT)
        self.input_entry.grid(row=0, column=0, padx=10)

        self.start_button = ttk.Button(ribbon_frame, text="Start", command=self.start_pda)
        self.start_button.grid(row=0, column=1, padx=5)

        self.prev_button = ttk.Button(ribbon_frame, text="Previous", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=2, padx=5)

        self.next_button = ttk.Button(ribbon_frame, text="Next", command=self.next_step, state=tk.DISABLED)
        self.next_button.grid(row=0, column=3, padx=5)

        self.end_button = ttk.Button(ribbon_frame, text="End", command=self.root.destroy)
        self.end_button.grid(row=0, column=4, padx=5)

        # Status label
        self.status_label = ttk.Label(root, text="Enter a string and press Start", anchor='w', relief=tk.SUNKEN, padding=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def start_pda(self):
        input_string = self.input_entry.get().strip()
        if not input_string or len(input_string) == 1:
            messagebox.showerror("Error", "String must have at least 2 characters.")
            return

        self.pda = PDA(input_string)
        accepted = self.pda.is_palindrome()
        self.steps = self.pda.path
        self.current_step = 0

        if not self.steps:
            messagebox.showinfo("Result", "Rejected")
            self.status_label.config(text="Rejected")
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
        else:
            result = "Accepted" if accepted else "Rejected"
            messagebox.showinfo("Result", result)
            self.status_label.config(text=f"{result}: {input_string}")
            self.next_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.draw_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step()
            self.next_button.config(state=tk.NORMAL)
        if self.current_step == 0:
            self.prev_button.config(state=tk.DISABLED)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.draw_step()
            self.prev_button.config(state=tk.NORMAL)
        if self.current_step == len(self.steps) - 1:
            self.next_button.config(state=tk.DISABLED)

    def draw_step(self):
        if not (0 <= self.current_step < len(self.steps)):
            return

        self.canvas.delete("all")
        step = self.steps[self.current_step]

        q_push_x, q_push_y = 100, 100
        q_skip_x, q_skip_y = 300, 100
        q_pop_x, q_pop_y = 500, 100
        q_accept_x, q_accept_y = 700, 100

        def draw_state(x, y, label, active=False, double=False):
            fill_color = "#4A90E2" if active else "#e6e6e6"
            self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=fill_color, outline="#333", width=2)
            if double:
                self.canvas.create_oval(x - 35, y - 35, x + 35, y + 35, outline="#333", width=2)
            self.canvas.create_text(x, y, text=label, font=self.BOLD_FONT, fill="#000000")

        draw_state(q_push_x, q_push_y, "q_push", step['state'] == 'q_push')
        draw_state(q_skip_x, q_skip_y, "q_skip", step['state'] == 'q_skip')
        draw_state(q_pop_x, q_pop_y, "q_pop", step['state'] == 'q_pop')
        draw_state(q_accept_x, q_accept_y, "q_accept", step['state'] == 'ACCEPT', double=True)

        # Transitions
        self.canvas.create_line(q_push_x + 40, q_push_y, q_skip_x - 40, q_skip_y, arrow=tk.LAST, width=2)
        self.canvas.create_line(q_skip_x + 40, q_skip_y, q_pop_x - 40, q_pop_y, arrow=tk.LAST, width=2)
        self.canvas.create_line(q_pop_x + 40, q_pop_y, q_accept_x - 40, q_accept_y, arrow=tk.LAST, width=2)

        rect_y = q_push_y + 100
        self.canvas.create_line(q_push_x, q_push_y + 40, q_push_x, rect_y, width=2)
        self.canvas.create_line(q_push_x, rect_y, q_pop_x, rect_y, width=2)
        self.canvas.create_line(q_pop_x, rect_y, q_pop_x, q_pop_y + 40, arrow=tk.LAST, width=2)

        def draw_loop(x, y):
            loop_height = 30  # Height above the state
            loop_width = 30   # How far left/right the loop goes
            # Up from the top of the state
            self.canvas.create_line(x-20, y - 35, x-20, y - 35 - loop_height, width=2)
            # Across to the right
            self.canvas.create_line(x-20, y - 35 - loop_height, x + loop_width, y - 35 - loop_height, width=2)
            # Down to the right side of the state (with arrow)
            self.canvas.create_line(x + loop_width, y - 35 - loop_height, x + loop_width, y - 28, arrow=tk.LAST, width=2)


        draw_loop(q_push_x, q_push_y)
        draw_loop(q_pop_x, q_pop_y)

        # Input tape
        self.canvas.create_text(100, 220, text="Input Tape:", anchor=tk.W, font=self.BOLD_FONT)
        x = 100
        y = 250
        for i, char in enumerate(self.pda.input):
            fill = "#FFD700" if i == step['position'] else "#ffffff"
            self.canvas.create_rectangle(x, y, x + 30, y + 30, fill=fill, outline="#333")
            self.canvas.create_text(x + 15, y + 15, text=char, font=self.FONT)
            x += 35

        # Divider
        self.canvas.create_line(525, 200, 525, 600, fill="#ccc", dash=(4, 2))

        # Stack
        self.canvas.create_text(550, 220, text="Stack:", anchor=tk.W, font=self.BOLD_FONT)
        stack_x = 550
        stack_y = 250
        for symbol in reversed(step['stack']):
            self.canvas.create_rectangle(stack_x, stack_y, stack_x + 30, stack_y + 30, fill="#a0e7a0", outline="#333")
            self.canvas.create_text(stack_x + 15, stack_y + 15, text=symbol, font=self.FONT)
            stack_y += 35

        # Update status
        self.status_label.config(text=f"Step {self.current_step + 1}/{len(self.steps)} - State: {step['state']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAGUI(root)
    root.mainloop()
