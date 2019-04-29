from character import Character
from enum import Enum

class PlayerStatus(Enum):
    dead = '死亡'
    alive = '存活'
    actioned = '已行动'
    voted = '已投票'

class Player(object):
    def __init__(self, player_id, player_nn):
        self._player_id = player_id
        self._player_nn = player_nn
        self._player_seat = 0
        self._player_status = PlayerStatus.dead
        self._player_character = 0
        self._player_aim = 0
        self._player_target = None
        self._player_hugged = False
        self._player_killed = 0
        self._player_healed = False
        self._player_failure = 0
        self._player_banned = False
        self._player_muted = False
        self._player_tickets = 0

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, player_id):
        self._player_id = player_id

    @property
    def player_nn(self):
        return self._player_nn

    @player_nn.setter
    def player_nn(self, player_nn):
        self._player_nn = player_nn

    @property
    def player_seat(self):
        return self._player_seat

    @player_seat.setter
    def player_seat(self, player_seat):
        self._player_seat = player_seat

    @property
    def player_status(self):
        return self._player_status

    @player_status.setter
    def player_status(self, player_status):
        self._player_status = player_status

    @property
    def player_character(self):
        return self._player_character

    @player_character.setter
    def player_character(self, player_character):
        self._player_character = player_character

    @property
    def player_aim(self):
        return self._player_aim

    @player_aim.setter
    def player_aim(self, player_aim):
        self._player_aim = player_aim

    @property
    def player_target(self):
        return self._player_target

    @player_target.setter
    def player_target(self, player_target):
        self._player_target = player_target

    @property
    def player_hugged(self):
        return self._player_hugged

    @player_hugged.setter
    def player_hugged(self, player_hugged):
        self._player_hugged = player_hugged

    @property
    def player_killed(self):
        return self._player_killed

    @player_killed.setter
    def player_killed(self, player_killed):
        self._player_killed = player_killed

    @property
    def player_healed(self):
        return self._player_healed

    @player_healed.setter
    def player_healed(self, player_healed):
        self._player_healed = player_healed

    @property
    def player_failure(self):
        return self._player_failure

    @player_failure.setter
    def player_failure(self, player_failure):
        self._player_failure = player_failure

    @property
    def player_banned(self):
        return self._player_banned

    @player_banned.setter
    def player_banned(self, player_banned):
        self._player_banned = player_banned

    @property
    def player_muted(self):
        return self._player_muted

    @player_muted.setter
    def player_muted(self, player_muted):
        self._player_muted = player_muted

    @property
    def player_tickets(self):
        return self._player_tickets

    @player_tickets.setter
    def player_tickets(self, player_tickets):
        self._player_tickets = player_tickets

    def player_faction(self):
        return False if self._player_character in [Character.ss, Character.mfs, Character.sl] else True

    def voted(self):
        self._player_tickets += 1

    def dead(self):
        self._player_status = PlayerStatus.dead
