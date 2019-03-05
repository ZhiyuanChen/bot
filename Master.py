import uuid
from enum import Enum


class Game(object):
    def __init__(self):
        self.game_id = uuid.uuid1()
        self.game_status = 0
        self.game_type = 0

    def get_game_status(self, game_id):
        return game_id.game_status

    def set_game_status(self, game_id, game_status):
        game_id.game_status = game_status


class Player(object):
    def __init(self, player_id):
        self.player_id = player_id
        self.player_status = 0
        self.player_character = 0
        self.player_hugged = False
        self.player_healed = False
        self.player_empty = 0

