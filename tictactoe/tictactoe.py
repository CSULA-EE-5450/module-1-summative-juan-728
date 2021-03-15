import logging
from typing import List, Union, Tuple
import random
from dataclasses import dataclass
import numpy as np

TicTacToe_INSTRUCTIONS = {
    'English': {
        'WELCOME': 'Welcome to Tic-Tac-Toe! :D',
        'PLAY_AGAIN': 'Type y to play another game: '
    }
}


@dataclass
class TicTacToe(object):
    """ TicTacToe game
    """
    def __init__(self, num_player: int = 2):
        """
        Constructor for the TicTacToe game object.
        """

        self._VALUES = [' ' for x in range(9)]
        self._PLAYER_POS = {'X': [], 'O': []}
        self._PLAYER_CHOICE = {'X': "", 'O': ""}
        self._CUR_PLAYER_NAME = ''
        self._PLAYER1 = ''
        self._PLAYER2 = ''
        self._CUR_SIGN = ''

    def initial_setup(self):
        print("Player 1 - ")
        self._PLAYER1 = input("Enter the name: ")
        print("\n")

        print("Player 2 - ")
        self._PLAYER2 = input("Enter the name: ")
        print("\n")

        self._CUR_PLAYER_NAME = self._PLAYER1

        return self._CUR_PLAYER_NAME, self._PLAYER1, self._PLAYER2

    def player_choice(self):
        self.initial_setup()
        while True:
            print("Turn to choose for", self._CUR_PLAYER_NAME)
            print("Enter 1 for X")
            print("Enter 2 for O")

            try:
                choice = int(input())
            except ValueError:
                print("Invalid Input!Try Again! :( \n")
                continue

            if choice == 1:
                self._PLAYER_CHOICE['X'] = self._CUR_PLAYER_NAME
                if self._CUR_PLAYER_NAME == self._PLAYER1:
                    self._PLAYER_CHOICE['O'] = self._PLAYER2
                else:
                    self._PLAYER_CHOICE['O'] = self._PLAYER1
                return False

            elif choice == 2:
                self._PLAYER_CHOICE['O'] = self._CUR_PLAYER_NAME
                if self._CUR_PLAYER_NAME == self._PLAYER1:
                    self._PLAYER_CHOICE['X'] = self._PLAYER2
                else:
                    self._PLAYER_CHOICE['X'] = self._PLAYER1
                return False
            else:
                print("Invalid Choice! :( Try Again\n")
                return True

    def current_sign(self):
        for key, value in self._PLAYER_CHOICE.items():
            if value == self._CUR_PLAYER_NAME:
                self._CUR_SIGN = key
        return self._CUR_SIGN

    def print_tic_tac_toe(self):
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self._VALUES[0], self._VALUES[1], self._VALUES[2]))
        print('\t_____|_____|_____')

        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self._VALUES[3], self._VALUES[4], self._VALUES[5]))
        print('\t_____|_____|_____')

        print("\t     |     |")

        print("\t  {}  |  {}  |  {}".format(self._VALUES[6], self._VALUES[7], self._VALUES[8]))
        print("\t     |     |")
        print("\n")

    def player_move_req(self):
        print("Player ", self._CUR_PLAYER_NAME, " turn. Which box? : ", end="")
        move = int(input())
        return move

    def player_move_check(self, move):
        if move < 1 or move > 9:
            return False

        if self._VALUES[move - 1] != ' ':
            return False
        else:
            return True

    def update_board(self, move):
        cur_sign = self.current_sign()
        self._VALUES[move - 1] = cur_sign
        self._PLAYER_POS[cur_sign].append(move)
        self.print_tic_tac_toe()

    def player_move_exe(self):
        while True:
            move = self.player_move_req()

            if self.player_move_check(move) == True:
                self.update_board(move)
                return False
            elif self.player_move_check(move) == False:
                print("Invalid Input! Try again!")

    def switch_turn(self):
        if self._CUR_PLAYER_NAME == self._PLAYER1:
            self._CUR_PLAYER_NAME = self._PLAYER2
        else:
            self._CUR_PLAYER_NAME = self._PLAYER1
        self.current_sign()
        return self._CUR_PLAYER_NAME, self._CUR_SIGN

    def check_draw(self):
        if len(self._PLAYER_POS['X']) + len(self._PLAYER_POS['O']) == 9:
            return True
        return False

    def check_winner(self):
        win_cond = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for x in win_cond:
            if all(y in (self._PLAYER_POS[self._CUR_SIGN]) for y in x):
                return True
        return False

    def run(self):

        self.player_choice()
        self.print_tic_tac_toe()
        while True:
            self.player_move_exe()

            if self.check_winner():
                print(" ", self._CUR_PLAYER_NAME, " has won the game! :D")
                print("\n")
                break
            if self.check_draw():
                print("Game Drawn :(")
                print("\n")
                break

            self.switch_turn()


def main():
    play_another = True
    while play_another:
        print(f"{TicTacToe_INSTRUCTIONS['English']['WELCOME']}")
        the_game = TicTacToe()
        the_game.run()
        play_another_input = input(f"{TicTacToe_INSTRUCTIONS['English']['PLAY_AGAIN']}")
        if play_another_input != 'y':
            play_another = False
    return False


if __name__ == '__main__':
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=print)
    main()
