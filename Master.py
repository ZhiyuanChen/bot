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


class Player(object):
    def __init(self, player_id):
        self.player_id = player_id
        self.player_status = 0
        self.player_character = 0
        self.player_hugged = False
        self.player_healed = False
        self.player_empty = 0

