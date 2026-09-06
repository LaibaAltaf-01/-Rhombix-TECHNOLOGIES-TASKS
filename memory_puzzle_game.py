"""
Memory Puzzle Game
-------------------
Match pairs of cards on a grid before the countdown timer runs out.

No external dependencies -- uses only Python's built-in tkinter library.

Usage:
    python memory_puzzle_game.py
"""

import random
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------- settings
ROWS = 4
COLS = 4
TIME_LIMIT_SECONDS = 60
SYMBOLS = ["🍎", "🍌", "🍇", "🍉", "🍒", "🍋", "🍑", "🥝",
           "🍍", "🥥", "🍓", "🍈", "🍏", "🥭", "🍐", "🍊"]

CARD_BACK = "❓"
CARD_WIDTH = 4
CARD_HEIGHT = 2

MATCH_COLOR = "#8fd694"
MISMATCH_COLOR = "#f4a5a5"
DEFAULT_COLOR = "#e6e6e6"
HIGHLIGHT_COLOR = "#c9dfff"


class MemoryGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Memory Puzzle Game")
        self.root.resizable(False, False)

        needed_pairs = (ROWS * COLS) // 2
        if needed_pairs > len(SYMBOLS):
            raise ValueError("Not enough symbols for the requested grid size.")

        self.values = SYMBOLS[:needed_pairs] * 2
        random.shuffle(self.values)

        self.buttons = {}
        self.revealed = {}
        self.matched = set()
        self.first_choice = None
        self.second_choice = None
        self.locked = False  # prevents clicks while checking a mismatched pair

        self.moves = 0
        self.pairs_found = 0
        self.total_pairs = needed_pairs
        self.time_left = TIME_LIMIT_SECONDS
        self.timer_id = None
        self.game_over = False

        self._build_ui()
        self._tick()

    # -------------------------------------------------------------- UI
    def _build_ui(self):
        top_frame = tk.Frame(self.root, pady=8)
        top_frame.pack()

        self.timer_label = tk.Label(
            top_frame, text=f"Time left: {self.time_left}s",
            font=("Helvetica", 14, "bold"), fg="#333"
        )
        self.timer_label.grid(row=0, column=0, padx=15)

        self.moves_label = tk.Label(
            top_frame, text="Moves: 0",
            font=("Helvetica", 14, "bold"), fg="#333"
        )
        self.moves_label.grid(row=0, column=1, padx=15)

        self.pairs_label = tk.Label(
            top_frame, text=f"Pairs: 0/{self.total_pairs}",
            font=("Helvetica", 14, "bold"), fg="#333"
        )
        self.pairs_label.grid(row=0, column=2, padx=15)

        grid_frame = tk.Frame(self.root, padx=10, pady=10)
        grid_frame.pack()

        index = 0
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(
                    grid_frame,
                    text=CARD_BACK,
                    font=("Helvetica", 18),
                    width=CARD_WIDTH,
                    height=CARD_HEIGHT,
                    bg=DEFAULT_COLOR,
                    command=lambda i=index: self._on_card_click(i)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[index] = btn
                index += 1

        bottom_frame = tk.Frame(self.root, pady=8)
        bottom_frame.pack()

        restart_btn = tk.Button(
            bottom_frame, text="Restart", font=("Helvetica", 12),
            command=self._restart
        )
        restart_btn.pack()

    # ------------------------------------------------------------ timer
    def _tick(self):
        if self.game_over:
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")

        if self.time_left <= 0:
            self._end_game(won=False)
            return

        self.time_left -= 1
        self.timer_id = self.root.after(1000, self._tick)

    # --------------------------------------------------------- gameplay
    def _on_card_click(self, index):
        if self.game_over or self.locked:
            return
        if index in self.matched or index == self.first_choice:
            return

        self._reveal(index)

        if self.first_choice is None:
            self.first_choice = index
        elif self.second_choice is None:
            self.second_choice = index
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.locked = True
            self.root.after(500, self._check_match)

    def _reveal(self, index):
        self.buttons[index].config(text=self.values[index], bg=HIGHLIGHT_COLOR)

    def _check_match(self):
        i, j = self.first_choice, self.second_choice

        if self.values[i] == self.values[j]:
            self.buttons[i].config(bg=MATCH_COLOR, state="disabled")
            self.buttons[j].config(bg=MATCH_COLOR, state="disabled")
            self.matched.add(i)
            self.matched.add(j)
            self.pairs_found += 1
            self.pairs_label.config(text=f"Pairs: {self.pairs_found}/{self.total_pairs}")

            if self.pairs_found == self.total_pairs:
                self._end_game(won=True)
        else:
            self.buttons[i].config(bg=MISMATCH_COLOR)
            self.buttons[j].config(bg=MISMATCH_COLOR)
            self.root.after(400, lambda: self._hide(i, j))

        self.first_choice = None
        self.second_choice = None
        self.locked = False

    def _hide(self, i, j):
        for idx in (i, j):
            if idx not in self.matched:
                self.buttons[idx].config(text=CARD_BACK, bg=DEFAULT_COLOR)

    # ------------------------------------------------------------- end
    def _end_game(self, won: bool):
        self.game_over = True
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)

        for btn in self.buttons.values():
            btn.config(state="disabled")

        if won:
            messagebox.showinfo(
                "You Win!",
                f"Congratulations! You matched all {self.total_pairs} pairs "
                f"in {self.moves} moves with {self.time_left}s to spare."
            )
        else:
            messagebox.showinfo(
                "Time's Up!",
                f"Out of time! You found {self.pairs_found}/{self.total_pairs} pairs."
            )

    def _restart(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)


def main():
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
