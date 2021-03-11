import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, status, Query, Depends
from tictactoe_db import AsyncTicTacToeDB, TicTacToe
from user_db import UserDB
from fastapi.security import HTTPBasic, HTTPBasicCredentials

USER_DB = UserDB()
TicTacToe_DB = AsyncTicTacToeDB(USER_DB)
app = FastAPI(
    title="Tic-Tac-Toe Server",
    description="Implementation of a simultaneous multi-game Tic-Tac-Toe server by Juan Avila."
)

security = HTTPBasic()


async def get_game(game_id: str) -> TicTacToe:
    """
    Get a game from the blackjack game database, otherwise raise a 404.

    :param game_id: the uuid in str of the game to retrieve
    """
    the_game = await TicTacToe_DB.get_game(game_id)
    if the_game is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found.")
    return the_game
