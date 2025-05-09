import tkinter as tk
import random
import time

class SimonGame:
  def __init__(self, root):
    self.root = root
    self.root.title("Simon Game")
    self.sequence = []
    self.player_sequence = []
    self.colors = ["red", "blue", "yellow", "green"]
    self.buttons = {}
    self.create_widgets()
    self.is_player_turn = False

  def create_widgets(self):
    canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
    canvas.pack()

    self.buttons["red"] = tk.Button(self.root, bg="red", activebackground="darkred", command=lambda: self.player_input("red"))
    self.buttons["red"].place(x=50, y=50, width=150, height=150)

    self.buttons["blue"] = tk.Button(self.root, bg="blue", activebackground="darkblue", command=lambda: self.player_input("blue"))
    self.buttons["blue"].place(x=200, y=50, width=150, height=150)

    self.buttons["yellow"] = tk.Button(self.root, bg="yellow", activebackground="gold", command=lambda: self.player_input("yellow"))
    self.buttons["yellow"].place(x=50, y=200, width=150, height=150)

    self.buttons["green"] = tk.Button(self.root, bg="green", activebackground="darkgreen", command=lambda: self.player_input("green"))
    self.buttons["green"].place(x=200, y=200, width=150, height=150)

    self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
    self.start_button.place(x=175, y=375, width=50, height=25)

  def start_game(self):
    self.sequence = []
    self.player_sequence = []
    self.is_player_turn = False
    self.add_to_sequence()

  def add_to_sequence(self):
    self.sequence.append(random.choice(self.colors))
    self.play_sequence()

  def play_sequence(self):
    self.is_player_turn = False
    for i, color in enumerate(self.sequence):
      self.root.after(1000 * i, lambda c=color: self.flash_button(c))
    self.root.after(1000 * len(self.sequence), self.enable_player_turn)

  def flash_button(self, color):
    self.buttons[color].config(bg="white")
    self.root.after(500, lambda: self.buttons[color].config(bg=color))

  def enable_player_turn(self):
    self.is_player_turn = True
    self.player_sequence = []

  def player_input(self, color):
    if not self.is_player_turn:
      return
    self.player_sequence.append(color)
    self.flash_button(color)
    if self.player_sequence == self.sequence[:len(self.player_sequence)]:
      if len(self.player_sequence) == len(self.sequence):
        self.root.after(1000, self.add_to_sequence)
    else:
      self.game_over()

  def game_over(self):
    self.is_player_turn = False
    for color in self.colors:
      self.buttons[color].config(bg="gray")
    self.start_button.config(text="Game Over! Restart", command=self.start_game)

if __name__ == "__main__":
  root = tk.Tk()
  game = SimonGame(root)
  root.mainloop()