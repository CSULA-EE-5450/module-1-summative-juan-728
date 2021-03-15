import unittest
from unittest import TestCase, mock
from tictactoe import TicTacToe

USER1 = 'user1'
USER2 = 'user2'


class TestTicTacToe(TestCase):
    def setUp(self) -> None:
        self.tictactoe = TicTacToe()

    @mock.patch('tictactoe.input', side_effect=[USER1, USER2])
    def test__initial_setup(self, mock_inputs):
        self.tictactoe.initial_setup()
        self.assertEqual(self.tictactoe.initial_setup(), [USER1, USER2])

    def test__current_sign(self):
        self.tictactoe._PLAYER_CHOICE = {'X': "user1", 'O': "user2"}
        self.tictactoe._CUR_PLAYER_NAME = 'user1'
        self.assertEqual(self.tictactoe.current_sign(), 'X')
        self.tictactoe._CUR_PLAYER_NAME = 'user2'
        self.assertEqual(self.tictactoe.current_sign(), 'O')

    def test__player_move_req(self, cur_sign='X', move: int = None):
        if move is None:
            move = 5
            self.assertEqual(self.tictactoe.player_move_req(), move)

    def test__player_move_check(self):
        move = 3
        self.tictactoe._VALUES[4] = 'X'
        self.assertEqual(self.tictactoe.player_move_check(move), True)
        move = 5
        self.assertEqual(self.tictactoe.player_move_check(move), False)
        move = 21
        self.assertEqual(self.tictactoe.player_move_check(move), False)

    def test__update_board(self):
        move = 5
        cur_sign = 'X'
        self.assertEqual(self.tictactoe.update_board(move), ([' ', ' ', ' ', ' ',
                                                              'X', ' ', ' ', ' ', ' '],
                                                             {'X': [5], 'O': []}))

    def test__switch_player(self):
        player1 = USER1
        player2 = USER2
        self.tictactoe._PLAYER_CHOICE = {'X': "user1", 'O': "user2"}
        self.tictactoe._CUR_PLAYER_NAME = player1
        self.assertEqual(self.tictactoe.switch_turn(), ('O', 'user2'))

    def test__check_draw(self):
        self.tictactoe._PLAYER_POS['X'] = [2, 3, 4, 5, 9]
        self.tictactoe._PLAYER_POS['O'] = [1, 6, 7, 8]
        self.assertEqual(self.tictactoe.check_draw(), True)
        self.tictactoe._PLAYER_POS['X'] = [2, 3, 4, 5]
        self.tictactoe._PLAYER_POS['O'] = [1, 6, 7, 8]
        self.assertEqual(self.tictactoe.check_draw(), False)

    def test__check_win(self):
        self.tictactoe._PLAYER_POS['X'] = [3, 1, 2]
        self.tictactoe._PLAYER_POS['O'] = [4, 5]
        self.assertEqual(self.tictactoe.check_winner(), True)
        self.tictactoe._PLAYER_POS['X'] = [3, 1, 9]
        self.tictactoe._PLAYER_POS['O'] = [4, 5]
        self.assertEqual(self.tictactoe.check_winner(), False)


if __name__ == '__main__':
    unittest.main()
