import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, status, Query, Depends
from tictactoe_db import AsyncTicTacToeDB, TicTacToe
from user_db import UserDB
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

USER_DB = UserDB()
TicTacToe_DB = AsyncTicTacToeDB(USER_DB)
app = FastAPI(
    title="Tic-Tac-Toe Server",
    description="Implementation of a simultaneous multi-game Tic-Tac-Toe server by Juan Avila."
)

security = HTTPBasic()


async def mqtt_setup():

    async with Client("localhost") as client:
        await client.subscribe("get_game")
        async with client.unfiltered_messages() as messages:
            async for message in messages:
                message_str = message.payload.decode()

                if message_str.startswith("create_user"):
                    # Delete the command portion of the message ("create_user")
                    message_params = message_str.replace("create_user", '')
                    # Then feed the remaining message of only the parameter(s) (username).
                    await create_user(client, message_params)

                elif message_str.startswith("create_game"):
                    message_params = message_str.replace("create_game", '')
                    await create_game(client, message_params)

                elif message_str.startswith("add_player"):
                    message_params = message_str.replace("add_player", '')
                    await add_player(client, message_params)

                elif message_str.startswith("get_player_idx"):
                    message_params = message_str.replace("get_player_idx", '')
                    await get_player_idx(client, message_params)

                elif message_str.startswith("init_game"):
                    message_params = message_str.replace("init_game", '')
                    await init_game(client, message_params)

                elif message_str.startswith("get_winners"):
                    message_params = message_str.replace("get_winners", '')
                    await get_winners(client, message_params)

                elif message_str.startswith("delete_game"):
                    message_params = message_str.replace("delete_game", '')
                    await delete_game(client, message_params)


async def get_game(game_id: str) -> TicTacToe:
    """
    Get a game from the tictactoe game database, otherwise raise a 404.

    :param game_id: the uuid in str of the game to retrieve
    """
    the_game = await TicTacToe_DB.get_game(game_id)
    if the_game is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found.")
    return the_game


@app.get('/')
async def home():
    return {"message": "Welcome to TicTacToe! :D"}


@app.post('/user/create')
async def create_user(client, message_param):
    try:
        new_username, new_password = USER_DB.create_user(message_param)
    except ValueError:
        await client.publish(("users/" + str(message_param) + "/error"),
                             "That username already exists!", qos=1)
        raise MqttError("That username already exists!")
    await client.publish(("users/" + str(new_username) + "/create_success"), "True", qos=1)


@app.get('/game/create/{num_players}', status_code=status.HTTP_201_CREATED)
async def create_game(credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if UserDB.is_valid(self=USER_DB, username=user, password=password):
        owner_username = user
        new_uuid, new_term_pass, game_owner = await TicTacToe_DB.add_game()
        game_info = await TicTacToe_DB.get_game_info(new_uuid)
        player_list = game_info.players
        player_list.append(owner_username)
        return {'success': True,
                'game_id': new_uuid,
                'termination_password': new_term_pass,
                'game_owner': owner_username}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Game unauthorized access and command.")


@app.post('/game/{game_id}/add_player', status_code=status.HTTP_400_BAD_REQUEST)
async def add_player(game_id: str, username: str, credentials: HTTPBasicCredentials = Depends(security)):
    if username is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Username {username} not entered or found.")
    else:
        game_info = await TicTacToe_DB.get_game_info(game_id)
        player_list = game_info.players
        if len(player_list) == game_info.num_players:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Game, Max players capped.")
        else:
            if credentials.username == game_info.owner:
                if username not in player_list:
                    player_list.append(username)
                    player_idx = player_list.index(username)
                    return {'success': True,
                            'game_id': game_id,
                            'player_username': username,
                            'player_idx': player_idx}
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f"player already added.")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail=f"Game unauthorized access and command.")


@app.get('/game/{game_id}/get_player_idx')
async def get_player_idx(game_id: str = Path(..., description='the unique game id'),
                         username: str = Query(..., description='the unique game id'),
                         credentials: HTTPBasicCredentials = Depends(security)):
    game_info = await TicTacToe_DB.get_game_info(game_id)
    player_list = game_info.players
    idx = 0
    if credentials.username in player_list:
        for player in player_list:
            if player == username:
                player_idx = idx
                player_username = username
                return {'success': True,
                        'game_id': game_id,
                        'player_username': player_username,
                        'player_idx': player_idx}
            idx += 1
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Game unauthorized access and command.")


@app.post('/game/{game_id}/initialize')
async def init_game(game_id: str = Path(..., description='the unique game id'),
                    credentials: HTTPBasicCredentials = Depends(security)):
    game_info = await TicTacToe_DB.get_game_info(game_id)
    if credentials.username == game_info.owner:
        the_game = await get_game(game_id)
        the_game.initial_deal()
        return {'success': True}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Game unauthorized access and command.")


@app.get('/game/{game_id}/winners')
async def get_winners(game_id: str = Path(..., description='the unique game id')):
    the_game = await get_game(game_id)
    winner_list = the_game.check_win()
    return {'game_id': game_id,
            'winners': winner_list}


@app.post('/game/{game_id}/terminate')
async def delete_game(game_id: str = Path(..., description='the unique game id'),
                      password: str = Query(..., description='the termination password'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    the_game = await TicTacToe_DB.del_game(game_id, password, credentials.username)
    if password is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Game {password} not entered or found.")
    if the_game is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Game not found.")
    return {'success': True, 'deleted_id': game_id}

"""
if __name__ == '__main__':
    # running from main instead of terminal allows for debugger
    # TODO: modify the below to add HTTPS (SSL/TLS) support
    # uvicorn.run('web_tictactoe:app', port=8000, log_level='info', reload=True,
    #             ssl_keyfile='C:/Users/Juan Avila/Documents/GitHub/module-1-hw-2-juan-728/keys/public.pem',
    #             ssl_certfile='C:/Users/Juan Avila/Documents/GitHub/module-1-hw-2-juan-728/keys/private.pem')
    uvicorn.run('web_tictactoe:app', port=8000, log_level='info', reload=True)
"""


async def main():
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await mqtt_setup()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)

# Change to the "Selector" event loop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# Run your async application as usual
asyncio.run(main())
