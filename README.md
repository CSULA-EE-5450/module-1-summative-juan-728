# EE 5450 Module 1 Summative
This is a Tic-Tac-Toe game developed for a graduate level course. In this project, I not only created the game in Python but also implemented MQTT. 

## Installation
'''bash
pip install asyncio-mqtt
'''

## Tic-Tac-Toe in MQTT
Game Rules: The first player to get 3 of his/her marks in a row (up, down, across, or diagonally) is the winner.
When all 9 squares are full, the game is over.

## player_choice()
returns player's choice of mark (i.e 'X' or 'O')
  
## player_move_exe()
excecutes the move based off grid number chosen by player

## check_winner()
First player to get 3 of their marks ('X' or 'O') wins the game.
If by the time all 9 squares are full and no player has 3 in a row, the game will end on a DRAW
