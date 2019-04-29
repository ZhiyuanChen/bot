import time
import itchat
import random
from character import Character
from player import Player, PlayerStatus
from enum import Enum


def send_message(dest, content):
    time.sleep(0.3 + random.random() / 5)
    print(content + ' is being sent to ' + dest)
    try:
        itchat.send(msg=content, toUserName=dest)
    except TimeoutError:
        send_message(dest, content)


EXIT_FLAG = False

CHARACTER6 = [Character.hhd, Character.jjs, Character.ys, Character.ss, Character.mfs, Character.sl]
CHARACTER7 = [Character.hhd, Character.jjs, Character.ys, Character.jc, Character.ss, Character.mfs, Character.sl]


class GameStatus(Enum):
    ready = '准备'
    begin = '开始'
    speech = '发言'
    vote_one = '投票-1'
    count_one = '计票-1'
    vote_two = '投票-2'
    count_two = '计票-2'
    action = '行动'
    settlement = '结算'


class Game(object):
    def __init__(self, game_id):
        self._game_id = game_id
        self._game_status = GameStatus.ready
        self._game_type = 0  # 角色类型
        self._game_mode = True  # 游戏类型 False：禁言转职 True：禁票不转职
        self._player_list = []
        self._alive_player_set = set()
        self._alive_good_player_set = set()
        self._alive_bad_player_set = set()
        self._actioned_player_set = set()
        self._muted_player_set = set()
        self._hhd = None
        self._jc = None
        self._ss = None
        self._mfs = None
        self._sl = None
        self._jz = None

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, game_id):
        self._game_id = game_id

    @property
    def game_status(self):
        return self._game_status

    @game_status.setter
    def game_status(self, game_status):
        self._game_status = game_status

    @property
    def game_type(self):
        return self._game_type

    @game_type.setter
    def game_type(self, game_type):
        self._game_type = game_type

    @property
    def game_mode(self):
        return self._game_mode

    @game_mode.setter
    def game_mode(self, game_mode):
        self._game_mode = game_mode

    @property
    def player_list(self):
        return self._player_list

    @player_list.setter
    def player_list(self, player_list):
        self._player_list = player_list

    @property
    def alive_good_player_set(self):
        return self._alive_good_player_set

    @alive_good_player_set.setter
    def alive_good_player_set(self, alive_good_player_set):
        self._alive_good_player_set = alive_good_player_set

    @property
    def alive_bad_player_set(self):
        return self._alive_bad_player_set

    @alive_bad_player_set.setter
    def alive_bad_player_set(self, alive_bad_player_set):
        self._alive_bad_player_set = alive_bad_player_set

    @property
    def alive_player_set(self):
        return self._alive_player_set

    @alive_player_set.setter
    def alive_player_set(self, alive_player_set):
        self._alive_player_set = alive_player_set

    @property
    def actioned_player_set(self):
        return self._actioned_player_set

    @actioned_player_set.setter
    def actioned_player_set(self, actioned_player_set):
        self._actioned_player_set = actioned_player_set

    @property
    def muted_player_set(self):
        return self._muted_player_set

    @muted_player_set.setter
    def muted_player_set(self, muted_player_set):
        self._muted_player_set = muted_player_set

    @property
    def hhd(self):
        return self._hhd

    @hhd.setter
    def hhd(self, hhd):
        self._hhd = hhd

    @property
    def jc(self):
        return self._jc

    @jc.setter
    def jc(self, jc):
        self._jc = jc

    @property
    def ss(self):
        return self._ss

    @ss.setter
    def ss(self, ss):
        self._ss = ss

    @property
    def mfs(self):
        return self._mfs

    @mfs.setter
    def mfs(self, mfs):
        self._mfs = mfs

    @property
    def sl(self):
        return self._sl

    @sl.setter
    def sl(self, sl):
        self._sl = sl

    @property
    def jz(self):
        return self._jz

    @jz.setter
    def jz(self, jz):
        self._jz = jz

    def alive_player_count(self):
        return len(self.alive_player_set)

    def good_player_count(self):
        return len(self.alive_good_player_set)

    def bad_player_count(self):
        return len(self.alive_bad_player_set)

    def actioned_player_count(self):
        return len(self.actioned_player_set)

    def add_player(self, player_id, player_nn):
        for player in self.player_list:
            if player_id == player.player_id:
                send_message(self.game_id, '@' + player_nn + '\u2005' + '您已加入游戏')
                return
        self.player_list.append(Player(player_id, player_nn))
        send_message(self.game_id, '@' + player_nn + '\u2005' + '加入游戏')

    def del_player(self, player_id, player_nn):
        for player in self.player_list:
            if player_id == player.player_id:
                self.player_list.remove(player)
                send_message(self.game_id, '@' + player_nn + '\u2005' + '离开游戏')
                return
        send_message(self.game_id, '@' + player_nn + '\u2005' + '您还不是玩家')

    def player_dead(self, player):
        self.alive_player_set.remove(player)
        if player.player_faction():
            self.alive_good_player_set.remove(player)
        else:
            self.alive_bad_player_set.remove(player)
        player.dead()

    def be_master(self, player_id):
        for player in self.alive_player_set:
            if player_id == player.player_id:
                send_message(player_id, '\n'.join(player.player_nn + '的身份是：' + player.player_character.value for player in self.player_list))
                return

    def action_status(self):
        return '未行动的玩家：\n' + '\n'.join(str(player.player_seat) + ' ' + player.player_nn for player in self.alive_player_set.difference(self.actioned_player_set))

    def start(self):
        if len(self.player_list) == 6:
            character_list = CHARACTER6
            self.game_mode = False
        elif len(self.player_list) == 7:
            character_list = CHARACTER7
            self.game_mode = True
        else:
            send_message(self.game_id, '玩家数量不合法')
            return
        random.shuffle(self.player_list)
        player_list_str = '玩家列表：\n'
        for seat, player in enumerate(self.player_list):
            self.alive_player_set.add(player)
            player.player_seat = seat + 1
            player.player_status = PlayerStatus.alive
            player_list_str += str(player.player_seat) + '  ' + player.player_nn + '\n'
        send_message(self.game_id, player_list_str + '\n身份发放开始')
        random.shuffle(character_list)
        for index, player in enumerate(self.player_list):
            player.player_character = character_list[index]
            if player.player_character == Character.hhd:
                self.hhd = player
            elif player.player_character == Character.jc:
                self.jc = player
            elif player.player_character == Character.ss:
                self.ss = player
            elif player.player_character == Character.mfs:
                self.mfs = player
            elif player.player_character == Character.sl:
                self.sl = player
            elif player.player_character == Character.jz:
                self.jz = player
            if player.player_faction():
                self.alive_good_player_set.add(player)
            else:
                self.alive_bad_player_set.add(player)
            send_message(player.player_id, '您的身份是：\n' + player.player_character.value)
        send_message(self.game_id, '身份发放完成\n请私戳法官进行夜间行动')
        self.game_status = GameStatus.action

    def night_control(self, player_id, message):
        if self.actioned_player_count() < self.alive_player_count():
            message = message.split()
            if message[0] == '行动':
                for player in self.alive_player_set:
                    if player_id == player.player_id and player.player_status == PlayerStatus.alive:
                        for target_player in self.alive_player_set:
                            if int(message[1]) == target_player.player_seat:
                                self.night_action(player, target_player)
                                global EXIT_FLAG
                                EXIT_FLAG = True
                                break
                        else:
                            send_message(player_id, '行动目标不正确')
                    if EXIT_FLAG:
                        EXIT_FLAG = False
                        break
                else:
                    send_message(player_id, '您无法行动')
            elif message[0] == '不行动':
                for player in self.alive_player_set:
                    if player_id == player.player_id:
                        self.night_action(player, None)
                        break
                else:
                    send_message(player_id, '您无法行动')
        if self.actioned_player_count() == self.alive_player_count():
            self.game_status = GameStatus.settlement
            self.night_settlement()

    def night_action(self, player, target_player):
        if target_player is not None:
            player.player_aim = target_player.player_seat
        else:
            player.player_aim = 0
        player.player_target = target_player
        player.player_status = PlayerStatus.actioned
        self.actioned_player_set.add(player)
        send_message(player.player_id, '行动目标设置为：' + str(player.player_aim))

    def night_settlement(self):
        dead_player_set = set()
        send_message(self.game_id, '夜间行动完成\n请等待法官结算')

        # 当花魔法师目标非花蝴蝶时，被花蝴蝶作用的玩家免疫一切效果
        if self.mfs.player_target != self.hhd:
            for player in self.alive_player_set:
                if player.player_target == self.hhd.player_target:
                    player.player_target = None

        # 被魔法师作用的玩家技能失去效果
        if self.mfs.player_target is not None:
            self.mfs.player_target.player_target = None
            self.mfs.player_target.player_banned = True

        for player in self.alive_player_set:
            if player.player_target is not None:
                # if player.player_target() == jz.player_seat():
                #     player.player_target(player.player_seat())
                if player.player_character == Character.ys:
                    player.player_target.player_healed = True
                elif player.player_character == Character.jjs:
                    player.player_target.player_killed += 1
                elif player.player_character == Character.ss:
                    player.player_target.player_killed += 1
                elif player.player_character == Character.sl:
                    player.player_target.player_muted = True
                elif player.player_character == Character.sm:
                    player.player_target.voted()
                elif player.player_character == Character.em:
                    player.player_target.voted()
                print('玩家：' + player.player_nn + ' 身份：' + player.player_character.value + ' 行动：' + player.player_target.player_nn)
            else:
                print('玩家：' + player.player_nn + ' 身份：' + player.player_character.value + ' 未行动')

        if self.hhd.player_target is not None:
            self.hhd.player_target.player_hugged = True
            self.hhd.player_target.player_banned = self.hhd.player_banned
            self.hhd.player_target.player_healed = self.hhd.player_healed
            self.hhd.player_target.player_killed = self.hhd.player_killed
            self.hhd.player_target.player_muted = self.hhd.player_muted
            self.hhd.player_target.player_ticket = self.hhd.player_ticket

        if self.jc.player_status != PlayerStatus.dead:
            if self.jc.player_target is not None:
                send_message(self.jc.player_id, '查验结果：\n' + ('非坏特殊' if self.jc.player_target.player_faction() else '坏特殊'))
            elif self.jc.player_aim != 0:
                send_message(self.jc.player_id, '查验结果：\n失败')

        # if 'wy' in locals():
        #     if self.wy.player_target is not None:
        #         if wy_target == wy:
        #             wy.dead()
        #             dead_player_set.add(wy)
        #         else:
        #             send_message(wy.player_id(),
        #                          '昨晚的行动目标：\n' + wy_tartarget)
        #     else:
        #         send_message(wy.player_id(), '昨晚的行动目标：\n失败')

        for player in self.alive_player_set:
            if player.player_killed == 0:
                if player.player_healed:
                    player.player_failure += 1
            elif player.player_killed == 1:
                if player.player_healed:
                    player.player_healed = False
                else:
                    self.player_dead(player)
                    dead_player_set.add(player)
            elif player.player_killed == 2:
                self.player_dead(player)
                dead_player_set.add(player)
            if player.player_failure == 2:
                self.player_dead(player)
                dead_player_set.add(player)
            if player.player_muted:
                self.muted_player_set.add(player)
            player.player_healed = False
            player.player_killed = 0
            player.player_banned = False
            player.player_status = PlayerStatus.alive
        briefing = '天亮了\n'
        if len(dead_player_set) > 0:
            briefing += '死亡的玩家有：'
            for dead_player in dead_player_set:
                briefing += dead_player.player_nn + '  '
        else:
            briefing += '平安夜'
        if self.game_mode and len(self.muted_player_set) > 0:
            briefing += '\n被禁言的玩家有：'
            for muted_player in self.muted_player_set:
                briefing += muted_player.player_nn + '  '
                muted_player.player_muted = False
        send_message(self.game_id, briefing)

        if len(dead_player_set) > 0:
            last_words = '请以下玩家留遗言：\n'
            if self.game_mode:
                dead_player_set = dead_player_set.difference(self.muted_player_set)
            for dead_player in dead_player_set:
                last_words += dead_player.player_nn + '\n'
            send_message(self.game_id, last_words)
        if self.game_mode:
            self.muted_player_set = set()
        self.actioned_player_set = set()
        self.game_status = GameStatus.speech
        self.judge()

    def day_control(self, player_id, message):
        if self.actioned_player_count() < self.alive_player_count():
            message = message.split()
            if message[0] == '投票':
                for player in self.alive_player_set:
                    if player_id == player.player_id and player.player_status == PlayerStatus.alive:
                        for target_player in self.alive_player_set:
                            if int(message[1]) == target_player.player_seat:
                                if not self.game_mode or (self.game_mode and player not in self.muted_player_set):
                                    target_player.voted()
                                print('玩家：' + player.player_nn + ' 身份：' + player.player_character.value + ' 投票：' + target_player.player_nn)
                                player.player_status = PlayerStatus.voted
                                self.actioned_player_set.add(player)
                                global EXIT_FLAG
                                EXIT_FLAG = True
                                break
                        else:
                            send_message(self.game_id, '投票目标不正确')
                    if EXIT_FLAG:
                        EXIT_FLAG = False
                        break
                else:
                    send_message(self.game_id, '您无法投票')
            else:
                send_message(self.game_id, '投票阶段，请勿发言')
        if self.actioned_player_count() == self.alive_player_count():
            if self.game_status == GameStatus.vote_one:
                self.game_status = GameStatus.count_one
            elif self.game_status == GameStatus.vote_two:
                self.game_status = GameStatus.count_two
            self.day_settlement()

    def day_settlement(self):
        voted_player_list = sorted(
            list(self.alive_player_set), key=lambda x: x.player_tickets, reverse=True)
        result = '投票结果:\n'
        briefing = '投票阶段结束\n'
        if voted_player_list[0].player_tickets > voted_player_list[1].player_tickets:
            for player in self.alive_player_set:
                player.player_status = PlayerStatus.alive
                if player.player_tickets > 0:
                    result += str(player.player_seat) + '  ' + player.player_nn + '\n'
            self.player_dead(voted_player_list[0])
            briefing += '玩家：' + voted_player_list[0].player_nn + ' 死亡\n' + '公布身份为： '
            if not voted_player_list[0].player_faction():
                briefing += '坏特殊\n没有遗言'
            else:
                briefing += '非坏特殊\n请在滴声之后留下遗言：'
            self.game_status = GameStatus.action
        elif voted_player_list[0].player_tickets == voted_player_list[1].player_tickets and self.game_status == GameStatus.count_one:
            for player in self.alive_player_set:
                player.player_status = PlayerStatus.alive
                if player.player_tickets > 0:
                    result += str(player.player_seat) + '  ' + player.player_nn + '\n'
            self.game_status = GameStatus.vote_two
            briefing += '平票\n进入第二阶段投票'
        else:
            for player in self.alive_player_set:
                player.player_status = PlayerStatus.alive
                if player.player_tickets > 0:
                    result += str(player.player_seat) + '  ' + player.player_nn + '\n'
            self.game_status = GameStatus.action
            briefing += '平票\n请私戳法官进行夜间行动'
        send_message(self.game_id, result)
        send_message(self.game_id, briefing)
        self.actioned_player_set = set()
        self.judge()

    def judge(self):
        # 判断转职
        if self.game_mode:
            if self.ss.player_status == PlayerStatus.dead:
                if self.mfs.player_status != PlayerStatus.dead:
                    self.mfs.player_character = Character.ss
                    print('魔法师转职')
                elif self.sl.player_status != PlayerStatus.dead:
                    self.sl.player_character = Character.ss
                    print('森林老人转职')
        if len(self.alive_good_player_set) == 0:
            self.game_status = GameStatus.ready
            send_message(self.game_id, '游戏结束\n坏人胜利')
        elif len(self.alive_bad_player_set) == 0:
            self.game_status = GameStatus.ready
            send_message(self.game_id, '游戏结束\n好人胜利')
