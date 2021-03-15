from uuid import uuid4
from typing import List, Tuple, Dict, Union
from dataclasses import dataclass
from fastapi import HTTPException, status
import asyncio
from user_db import UserDB
from tictactoe.tictactoe import TicTacToe


@dataclass
class TicTacToeInfo:
    game_uuid: str
    players: List[str]
    termination_password: str


class AsyncTicTacToeDB(object):
    def __init__(self, user_db: UserDB):
        self._current_games: Dict[str, TicTacToe] = {}
        self._current_games_info: Dict[str, TicTacToeInfo] = {}
        self._QUERY_TIME: float = 0.05
        self._user_db = user_db  # pointer to the Web API's UserDB

    async def add_game(self) -> Tuple[str, str]:
        """
        Asks the database to create a new game.

        :return: the UUID (universally-unique ID) of the game, termination password, and owner username
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        game_uuid = str(uuid4())
        game_term_password = str(uuid4())
        self._current_games[game_uuid] = TicTacToe()
        self._current_games_info[game_uuid] = TicTacToeInfo(
            list(),
            game_term_password)
        return game_uuid, game_term_password

    async def get_game_info(self, game_id: str):
        """
        Asks the database for the blackjack info in a specific game.

        :param game_id: the UUID of the specific game
        :return: all game info
        """
        return self._current_games_info[game_id]

    async def add_player(self, game_id: str, username: str):
        if not self._current_games_info[game_id].players:
            self._current_games_info[game_id].players += 1
            self._current_games_info[game_id].players.append(username)
            self._current_games[game_id].players = self._current_games_info[game_id].players
        return self._current_games[game_id].players

    async def list_games(self) -> List[str]:
        """
        Asks the database for a list of all active games.

        :return: list of (game_id, number of players in game)
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        return [game_id for game_id, game in self._current_games.items()]

    async def get_game(self, game_id: str) -> Union[TicTacToe, None]:
        """
        Asks the database for a pointer to a specific game.

        :param game_id: the UUID of the specific game
        :return: None if the game was not found, otherwise pointer to the Blackjack object
        """
        await asyncio.sleep(self._QUERY_TIME)  # simulate query time
        return self._current_games.get(game_id, None)

    async def del_game(self, game_id: str, term_pass: str) -> bool:
        """
        Asks the database to terminate a specific game.

        :param game_id: the UUID of the specific game
        :param term_pass: the termination password for the game
        :return: False or exception if not found, True if success
        """
        try:
            await asyncio.sleep(self._QUERY_TIME)  # simulate query time
            if self._current_games_info[game_id].termination_password == term_pass:
                del self._current_games[game_id]
                return True
            else:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authorized")
        except KeyError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "game_id not found")