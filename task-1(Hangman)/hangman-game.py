import tkinter as tk
import random
from tkinter import messagebox
import string

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Word list - can be expanded or loaded from a file
        self.word_list = [
            "python", "algorithm", "machine", "learning", "intelligence", 
            "neural", "network", "computer", "science", "programming",
            "development", "artificial", "data", "analysis", "model",
            "training", "validation", "testing", "precision", "accuracy"
        ]
        
        # Game variables
        self.max_attempts = 6
        self.current_attempts = 0
        self.guessed_letters = set()
        self.word_to_guess = ""
        self.word_display = []
        
        # Create UI components
        self.create_widgets()
        
        # Start new game
        self.new_game()
    
    def create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self.root, 
            text="Hangman Game", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        self.title_label.pack(pady=20)
        
        # Hangman display frame
        self.hangman_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.hangman_frame.pack(pady=10)
        
        # Canvas for hangman drawing
        self.canvas = tk.Canvas(
            self.hangman_frame, 
            width=300, 
            height=300, 
            bg="white",
            highlightbackground="#cccccc"
        )
        self.canvas.pack()
        
        # Word display
        self.word_label = tk.Label(
            self.root, 
            text="", 
            font=("Arial", 22),
            bg="#f0f0f0"
        )
        self.word_label.pack(pady=20)
        
        # Attempts remaining
        self.attempts_label = tk.Label(
            self.root, 
            text=f"Attempts remaining: {self.max_attempts}", 
            font=("Arial", 14),
            bg="#f0f0f0"
        )
        self.attempts_label.pack(pady=5)
        
        # Guessed letters
        self.guessed_label = tk.Label(
            self.root, 
            text="Guessed letters: ", 
            font=("Arial", 14),
            bg="#f0f0f0"
        )
        self.guessed_label.pack(pady=5)
        
        # Letter buttons frame
        self.letters_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.letters_frame.pack(pady=20)
        
        # Create letter buttons
        self.letter_buttons = {}
        row, col = 0, 0
        
        for letter in string.ascii_lowercase:
            self.letter_buttons[letter] = tk.Button(
                self.letters_frame,
                text=letter.upper(),
                width=4,
                font=("Arial", 12),
                command=lambda l=letter: self.guess_letter(l)
            )
            self.letter_buttons[letter].grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 8:  # 9 buttons per row
                col = 0
                row += 1
        
        # New game button
        self.new_game_button = tk.Button(
            self.root,
            text="New Game",
            font=("Arial", 14),
            command=self.new_game,
            bg="#4CAF50",
            fg="white"
        )
        self.new_game_button.pack(pady=20)
    
    def new_game(self):
        # Reset game state
        self.current_attempts = 0
        self.guessed_letters = set()
        
        # Choose a random word
        self.word_to_guess = random.choice(self.word_list).lower()
        self.word_display = ["_" for _ in self.word_to_guess]
        
        # Reset UI
        self.update_word_display()
        self.attempts_label.config(text=f"Attempts remaining: {self.max_attempts}")
        self.guessed_label.config(text="Guessed letters: ")
        self.canvas.delete("all")
        self.draw_gallows()
        
        # Reset letter buttons
        for letter in self.letter_buttons:
            self.letter_buttons[letter].config(state=tk.NORMAL, bg="SystemButtonFace")
    
    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        
        # Add to guessed letters
        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state=tk.DISABLED, bg="#cccccc")
        
        # Update guessed letters display
        self.guessed_label.config(text=f"Guessed letters: {', '.join(sorted(self.guessed_letters))}")
        
        # Check if letter is in the word
        if letter in self.word_to_guess:
            # Update word display
            for i, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.word_display[i] = letter
            self.update_word_display()
            
            # Check if won
            if "_" not in self.word_display:
                messagebox.showinfo("Congratulations!", f"You won! The word was: {self.word_to_guess.upper()}")
                self.disable_all_buttons()
        else:
            # Wrong guess
            self.current_attempts += 1
            self.attempts_label.config(text=f"Attempts remaining: {self.max_attempts - self.current_attempts}")
            self.draw_hangman(self.current_attempts)
            
            # Check if lost
            if self.current_attempts >= self.max_attempts:
                messagebox.showinfo("Game Over", f"You lost! The word was: {self.word_to_guess.upper()}")
                self.disable_all_buttons()
    
    def update_word_display(self):
        display_text = " ".join(char.upper() for char in self.word_display)
        self.word_label.config(text=display_text)
    
    def disable_all_buttons(self):
        for letter in self.letter_buttons:
            self.letter_buttons[letter].config(state=tk.DISABLED)
    
    def draw_gallows(self):
        # Base
        self.canvas.create_line(50, 250, 150, 250, width=3)
        # Vertical pole
        self.canvas.create_line(100, 250, 100, 50, width=3)
        # Horizontal beam
        self.canvas.create_line(100, 50, 200, 50, width=3)
        # Rope
        self.canvas.create_line(200, 50, 200, 70, width=3)
    
    def draw_hangman(self, attempts):
        if attempts == 1:
            # Head
            self.canvas.create_oval(175, 70, 225, 120, width=3)
        elif attempts == 2:
            # Body
            self.canvas.create_line(200, 120, 200, 190, width=3)
        elif attempts == 3:
            # Left arm
            self.canvas.create_line(200, 140, 160, 170, width=3)
        elif attempts == 4:
            # Right arm
            self.canvas.create_line(200, 140, 240, 170, width=3)
        elif attempts == 5:
            # Left leg
            self.canvas.create_line(200, 190, 160, 230, width=3)
        elif attempts == 6:
            # Right leg
            self.canvas.create_line(200, 190, 240, 230, width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
