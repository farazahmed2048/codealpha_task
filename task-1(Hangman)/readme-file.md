# Hangman Game

A Python implementation of the classic Hangman game with a graphical user interface (GUI) using Tkinter.

## Project Overview


- A clean and intuitive graphical interface
- A collection of ML/CS-themed words
- Visual representation of the hangman as incorrect guesses accumulate
- Easy-to-use letter selection buttons
- Game state tracking (attempts remaining, guessed letters)


## Installation

1. Clone this repository:
```
git clone https://github.com/farazahmed2048/codealpha_task.git
cd task-1(Hangman)
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```
python hangman.py
```

2. The game will select a random word and display placeholders for each letter.
3. Click on letter buttons to make guesses.
4. You have 6 incorrect guesses before the game ends.
5. Try to guess the word before the hangman is fully drawn!

## Game Rules

- Each blank represents a letter in the word
- Click letter buttons to guess a letter
- Correct guesses reveal the letter in the word
- Incorrect guesses build the hangman piece by piece
- 6 incorrect guesses result in a loss
- Guess all letters correctly to win

## Project Structure

```
hangman-game/
├── hangman.py           # Main game implementation
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
└── screenshots/        # Game screenshots
    └── hangman_game.png
```

## Future Enhancements

- Add difficulty levels with different word lists
- Implement a scoring system
- Add sound effects
- Create a word database with categories
- Add machine learning features to predict player's next guess based on patterns

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project was created as part of a machine learning internship assignment
- Word list includes machine learning and computer science terminology
