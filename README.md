# Chess Game
A Python chess game with multiple game modes, built using Pygame.

## Features

- Beautiful chess board with classic brown colors
- Multiple game modes
- Piece promotion when pawns reach the opposite side
- Check and checkmate detection
- Simple and intuitive interface

## Game Modes

### 1v1 Mode
Play chess with a friend on the same computer. This is a free-form chess game where moves are not restricted by traditional chess rules - players can make any physically possible move, even if it would leave their king in check. The game still provides informational messages about check and checkmate states.

Features:
- Turn-based gameplay (white moves first)
- Piece selection highlighting
- Available move indicators
- Check and checkmate detection (informational only)
- Pawn promotion to queen when reaching the opposite side

### Player vs AI Mode
Play against an artificial intelligence that adapts to your skill level. Before starting the game, you'll be asked to describe your chess skill level, and the AI will adjust its difficulty accordingly.

Features:
- Customizable AI difficulty based on player's self-described skill level
- All standard chess rules enforced
- AI provides appropriate challenge without being frustratingly difficult

### Player vs AI Progressive Mode
A learning mode designed to help you improve your chess skills gradually. This mode tracks your progress over time and adapts the AI's difficulty as you improve.

Features:
- Progress tracking in a save file named suivi_(name).txt
- Game summary saved after each match to track improvement
- Option to create a new profile or load an existing one
- Gradually increasing difficulty as your skills improve
- Personalized learning experience

## Installation

1. Make sure you have Python 3.6+ installed
2. Install Pygame:
3. Download or clone this repository
4. Make sure you have the required chess piece images in the 'assets' folder named according to the pattern: piece_color.png (e.g., pawn_white.png, queen_black.png)

## How to Run

Run the main file to start the game: ./main

## Controls

- Left-click to select a piece
- Left-click again on a valid destination to move the piece
- When a game ends, you can click "New Game" to restart or "Return to Menu" to go back to the main menu

## Requirements

- Python 3.6+
- Pygame library