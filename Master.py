import uuid
from enum import Enum


class Game(object):
    def __init__(self):
        self.game_id = uuid.uuid1()
        self.game_status = 0
        self.game_type = 0

    def get_game_status(self):
        return self.game_status

    def set_game_status(self, game_status):
        self.game_status = game_status


class Character(Enum):
    Nill = '无'
    hhd = '花蝴蝶'
    jc = '警察'
    jjs = '狙击手'
    ys = '医生'
    ss = '杀手'
    mfs = '魔法师'
    sl = '森林老人'
    sm = '善民'
    em = '饿民'
    wy = '乌鸦'
    Master = '神'

    def heal(self, player_healed):
        self.set_player_healed(True)


class Player(object):
    def __init__(self, player_id):
        self.player_id = player_id
        self.player_status = 0
        self.player_character = 0
        self.player_hugged = False
        self.player_healed = False
        self.player_empty = 0

    def get_player_status(self):
        return self.player_status

    def set_player_status(self, player_status):
        self.player_status = player_status

    def get_player_character(self):
        return self.player_character

    def set_player_character(self, player_character):
        self.player_character = player_character

    def get_player_hugged(self):
        return self.player_hugged

    def set_player_hugged(self, player_hugged):
        self.player_hugged = player_hugged

    def get_player_healed(self):
        return self.player_healed

    def set_player_healed(self, player_healed):
        self.player_healed = player_healed

    def get_player_empty(self):
        return self.player_empty

    def set_player_empty(self, player_empty):
        self.player_empty = player_empty
