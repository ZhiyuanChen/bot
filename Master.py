import uuid
from enum import Enum
import itchat
import time
import random


class Game(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_status = 0
        self.game_type = 0  # 角色类型
        self.game_mode = True  # 游戏类型 False：禁言转职 True：禁票不转职
        self.player_list = []
        self.alive_player_list = []
        self.alive_player = 0
        self.actioned_player = 0

    def get_game_id(self):
        return self.game_id

    def get_game_status(self):
        return self.game_status

    def set_game_status(self, game_status):
        self.game_status = game_status

    def get_game_type(self):
        return self.game_type

    def set_game_type(self, game_type):
        self.game_type = game_type

    def get_game_mode(self):
        return self.game_mode

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, player_list):
        self.player_list = player_list

    def get_alive_player_list(self):
        return self.alive_player_list

    def set_alive_player_list(self, alive_player_list):
        self.alive_player_list = alive_player_list

    def get_alive_player(self):
        return self.alive_player

    def set_alive_player(self, alive_player):
        self.alive_player = alive_player

    def get_hhd(self):
        for player in self.player_list:
            if player.get_player_character() == Character.hhd:
                return player

    def get_mfs(self):
        for player in self.player_list:
            if player.get_player_character() == Character.mfs:
                return player

    def get_sl(self):
        for player in self.player_list:
            if player.get_player_character() == Character.sl:
                return player

    def get_jz(self):
        for player in self.player_list:
            if player.get_player_character() == Character.jz:
                return player

    def add_player(self, player_id, player_nn):
        player_already_exist = False
        for player in self.player_list:
            if player_id == player.player_id:
                player_already_exist = True
                break
        if not player_already_exist:
            self.player_list.append(Player(player_id, player_nn))
            send_message(self.get_game_id(), '@' + player_nn + '\u2005' + '加入游戏')
        else:
            send_message(self.game_id, '@' + player_nn + '\u2005' + '您已加入游戏')

    def del_player(self, player_id, player_nn):
        player_already_exist = False
        for player in self.player_list:
            player_already_exist = True
            if player_id == player.player_id:
                self.player_list.remove(player)
                send_message(self.get_game_id(), '@' + player_nn + '\u2005' + '离开游戏')
                break
        if not player_already_exist:
            send_message(self.game_id, '@' + player_nn + '\u2005' + '您还不是玩家')

    def be_master(self, player_id):
        is_alive_player = False
        for player in self.player_list:
            if player_id == player.player_id and player in self.alive_player_list:
                is_alive_player = True
                break
        if not is_alive_player:
            send_message(player_id, '\n'.join(player.player_nn + '的身份是：' + player.player_character for player in self.player_list))

    def start(self):
        random.shuffle(self.player_list)
        player_list_str = '玩家列表\n'
        for seat, player in enumerate(self.player_list):
            self.alive_player_list.append(player)
            player.set_player_seat(seat + 1)
            player_list_str += str(player.get_player_seat()) + '  ' + (player.get_player_nn()) + '\n'
        send_message(self.game_id, player_list_str + '\n身份发放开始')
        if len(self.player_list) == 7:
            character_list = CHARACTER7
            self.game_mode = True
        else:
            character_list = CHARACTER6
            self.game_mode = False
        random.shuffle(character_list)
        for index, player in enumerate(self.player_list):
            player.name = character_list[index].name
            player.set_player_character(character_list[index])
            player.set_player_status(2)
            send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character().value)
        self.game_status = 1
        send_message(self.game_id, '身份发放完成\n请私戳法官进行夜间行动')
        self.game_status = 2
        for player in self.alive_player_list:
            send_message(player.get_player_id(), '请开始行动')

    def night_control(self, player_id, message):
        if self.actioned_player < len(self.alive_player_list):
            if message.split()[0] == '行动':
                can_act = False
                available_target = False
                for player in self.alive_player_list:
                    if player_id == player.get_player_id() and player.get_player_status() == 2:
                        can_act = True
                        break
                if can_act:
                    for target_player in self.alive_player_list:
                        if int(message.split()[1]) == target_player.get_player_seat():
                            available_target = target_player
                            break
                    if available_target is not None:
                        self.night_action(player, available_target)
                    else:
                        send_message(player_id, '行动目标不正确')
                else:
                    send_message(player_id, '您无法行动')
            elif message.split()[0] == '不行动':
                can_act = False
                for player in self.alive_player_list:
                    if player_id == player.get_player_id() and player.get_player_status() == 2:
                        can_act = True
                        break
                if can_act:
                    self.night_action(player, None)
                    self.actioned_player += 1
        if self.actioned_player == len(self.alive_player_list):
            self.game_status = 3
            self.night_settlement()

    def night_action(self, player, target):
        player.set_player_aims(target.get_player_seat())
        player.set_player_target(target.get_player_seat())
        player.set_player_status(3)
        send_message(player.get_player_id(), '行动目标设置为：' + str(player.get_player_target()))

    def night_settlement(self):
        dead_player_list = []
        muted_player_list = []
        send_message(self.game_id, '夜间行动完成\n请等待法官结算')
        # jz = self.get_jz()
        hhd = self.get_hhd()
        mfs = self.get_mfs()
        sl = self.get_sl()
        hhd_target = None
        mfs_target = None
        jc_target = None
        wy_target = None
        ss_dead = False
        mfs_dead = False
        sl_dead = False
        for player in self.alive_player_list:
            if hhd.get_player_target() == player.get_player_seat():
                hhd_target = player
            elif self.get_mfs().get_player_target() == player.get_player_seat():
                mfs_target = player
        if mfs_target != self.get_hhd().get_player_seat():
            for player in self.alive_player_list:
                if player.get_player_target() == hhd_target:
                    player.set_player_target(None)
        for player in self.alive_player_list:
            # if player.get_player_target() == jz.get_player_seat():
            #     player.set_player_target(player.get_player_seat())
            for target_player in self.alive_player_list:
                if player.get_player_target() == target_player.get_player_seat():
                    if player.get_player_seat() == mfs_target:
                        player.set_player_banned(True)
                        player.set_player_target(None)
                    if player.get_player_character() == Character.jc:
                        jc = player
                        jc_target = target_player
                        jc_target_character = target_player
                    elif player.get_player_character() == Character.wy:
                        wy = player
                        wy_target = target_player
                        for third_player in self.alive_player_list:
                            if target_player.get_player_target() == third_player.get_player_seat():
                                wy_target_target = third_player
                                break
                    elif player.get_player_character() == Character.ys:
                        target_player.set_player_healed(True)
                    elif player.get_player_character() == Character.jjs:
                        target_player.set_player_killed(target_player.get_player_killed()+1)
                    elif player.get_player_character() == Character.ss:
                        target_player.set_player_killed(target_player.get_player_killed()+1)
                    elif player.get_player_character() == Character.sl:
                        target_player.set_player_muted(True)
                    elif player.get_player_character() == Character.sm:
                        target_player.add_ticket()
                    elif player.get_player_character() == Character.em:
                        target_player.add_ticket()
                    print('玩家：' + player.get_player_nn() + '身份：' + player.get_player_character().value + '行动：' + target_player.get_player_nn())
                    break

        if hhd_target is not None:
            hhd_target.set_player_hugged(True)
            hhd_target.set_player_banned(hhd.get_player_banned())
            hhd_target.set_player_healed(hhd.get_player_healed())
            hhd_target.set_player_killed(hhd.get_player_killed())
            hhd_target.set_player_muted(hhd.get_player_muted())
            hhd_target.set_player_ticket(hhd.get_player_ticket())

        if 'jc' in locals():
            if jc_target is not None:
                send_message(jc.get_player_id(), '昨晚的查验结果：\n' + jc_target_character.get_player_character().value)
            else:
                send_message(jc.get_player_id(), '昨晚的查验结果：\n失败')

        if 'wy' in locals():
            if wy_target is not None:
                if wy_target == wy:
                    wy.death()
                    dead_player_list.append(wy)
                else:
                    send_message(wy.get_player_id(), '昨晚的行动目标：\n' + wy_target_target)
            else:
                send_message(wy.get_player_id(), '昨晚的行动目标：\n失败')

        for player in self.alive_player_list:
            if player.get_player_killed() == 0:
                if player.get_player_healed():
                    player.set_player_failure(player.get_player_failure() + 1)
            elif player.get_player_killed() == 1:
                if player.get_player_healed():
                    player.set_player_healed(False)
                else:
                    player.death()
                    dead_player_list.append(player)
            elif player.get_player_killed() == 2:
                player.death()
                dead_player_list.append(player)
            if player.get_player_failure() == 2:
                player.death()
                dead_player_list.append(player)
            if player.get_player_muted():
                muted_player_list.append(player)
            player.set_player_healed(False)
            player.set_player_killed(0)
            player.set_player_banned(False)
            player.set_player_muted(False)
            player.set_player_status(4)
        briefing = '天亮了\n死亡的玩家有：'
        for dead_player in dead_player_list:
            self.alive_player_list.remove(dead_player)
            if self.game_mode:
                if dead_player.get_player_character() in [Character.ss, Character.mfs, Character.sl]:
                    if dead_player.get_player_character() == Character.ss:
                        ss_dead = True
                    elif dead_player.get_player_character() == Character.mfs:
                        mfs_dead = True
                    elif dead_player.get_player_character() == Character.sl:
                        sl_dead = True
                    if ss_dead:
                        if not mfs_dead:
                            mfs.set_player_character(Character.ss)
                        elif not sl_dead:
                            sl.set_player_character(Character.ss)
            briefing += dead_player.get_player_nn()
            briefing += '  '
        if self.game_mode:
            briefing += '\n被禁言的玩家有：'
            for muted_player in muted_player_list:
                briefing += muted_player.get_player_nn()
                briefing += '  '
        send_message(self.game_id, briefing)

        if len(dead_player_list) > 0:
            last_words = '请以下玩家顺序遗言：\n'
            if self.game_mode:
                dead_player_list = list(set(dead_player_list).difference(set(muted_player_list)))
            for dead_player in dead_player_list:
                last_words += dead_player.get_player_nn()
                last_words += '\n'
            send_message(self.game_id, last_words)
        self.actioned_player = 0
        self.game_status = 4
        self.judge()

    def day_control(self, player_id, message):
        if self.actioned_player < len(self.alive_player_list):
            if message.split()[0] == '投票':
                can_vote = False
                available_target = None
                for player in self.alive_player_list:
                    if player_id == player.get_player_id() and player.get_player_status() == 4:
                        can_vote = True
                        break
                if can_vote:
                    for target_player in self.alive_player_list:
                        if int(message.split()[1]) == target_player.get_player_seat():
                            available_target = target_player
                            break
                    if available_target is not None:
                        available_target.add_ticket()
                        print(
                            '玩家：' + player.get_player_nn() + '身份：' + player.get_player_character().value + '行动：' + available_target.get_player_nn())
                        player.set_player_status(5)
                        self.actioned_player += 1
                    else:
                        send_message(self.game_id, '投票目标不正确')
                else:
                    send_message(player_id, '您无法投票')
        if self.actioned_player == len(self.alive_player_list):
            if self.game_status == 5:
                self.game_status = 6
            elif self.game_status == 7:
                self.game_status = 8
            self.day_settlement()

    def day_settlement(self):
        voted_player_list = sorted(self.alive_player_list, key=lambda x: x.player_ticket, reverse=True)
        result = '投票结果:\n'
        briefing = '投票阶段结束\n'
        if voted_player_list[0].get_player_ticket() > voted_player_list[1].get_player_ticket():
            briefing += '玩家：' + voted_player_list[0].get_player_nn() + ' 死亡\n' + '公布身份为： '
            if voted_player_list[0].get_player_character() in [Character.ss, Character.mfs, Character.sl]:
                briefing += '坏特殊\n没有遗言'
            else:
                briefing += '非坏特殊\n请在滴声之后留下遗言：'
            voted_player_list[0].death()
            self.alive_player_list.remove(voted_player_list[0])
            for player in self.alive_player_list:
                player.set_player_status(2)
                if player.get_player_ticket() > 0:
                    result += str(player.get_player_ticket()) + '  ' + player.get_player_nn() + '\n'
            self.game_status = 2
        elif voted_player_list[0].get_player_ticket() == voted_player_list[1].get_player_ticket() and self.game_status == 6:
            for player in self.alive_player_list:
                player.set_player_status(4)
                if player.get_player_ticket() > 0:
                    result += str(player.get_player_ticket()) + '  ' + player.get_player_nn() + '\n'
            briefing += '平票\n进入第二阶段投票'
            self.game_status = 7
        else:
            for player in self.alive_player_list:
                player.set_player_status(2)
                if player.get_player_ticket() > 0:
                    result += str(player.get_player_ticket()) + '  ' + player.get_player_nn() + '\n'
            briefing += '平票\n请私戳法官进行夜间行动'
            self.game_status = 2

        send_message(self.game_id, result)
        send_message(self.game_id, briefing)
        self.actioned_player = 0
        self.judge()

    def judge(self):
        good_list = []
        bad_list = []
        for player in self.get_alive_player_list():
            if player.get_player_character() in [Character.ss, Character.mfs, Character.sl]:
                bad_list.append(player)
            else:
                good_list.append(player)
        if len(good_list) == 0:
            self.game_status = 0
            send_message(self.game_id, '游戏结束\n坏人胜利')
        elif len(bad_list) == 0:
            self.game_status = 0
            send_message(self.game_id, '游戏结束\n好人胜利')


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
    jz = '镜子'
    Master = '神'


class Player(object):
    def __init__(self, player_id, player_nn):
        self.player_id = player_id
        self.player_nn = player_nn
        self.player_seat = 0
        self.player_status = 0
        self.player_character = 0
        self.player_aims = None
        self.player_target = 0
        self.player_hugged = False
        self.player_killed = 0
        self.player_healed = False
        self.player_failure = 0
        self.player_banned = False
        self.player_muted = False
        self.player_ticket = 0

    def get_player_id(self):
        return self.player_id

    def get_player_nn(self):
        return self.player_nn

    def get_player_seat(self):
        return self.player_seat

    def set_player_seat(self, player_seat):
        self.player_seat = player_seat

    def get_player_status(self):
        return self.player_status

    def set_player_status(self, player_status):
        self.player_status = player_status

    def get_player_character(self):
        return self.player_character

    def set_player_character(self, player_character):
        self.player_character = player_character

    def get_player_aims(self):
        return self.player_aims

    def set_player_aims(self, player_aims):
        self.player_aims = player_aims

    def get_player_target(self):
        return self.player_target

    def set_player_target(self, player_target):
        self.player_target = player_target

    def get_player_hugged(self):
        return self.player_hugged

    def set_player_hugged(self, player_hugged):
        self.player_hugged = player_hugged

    def get_player_killed(self):
        return self.player_killed

    def set_player_killed(self, player_killed):
        self.player_killed = player_killed

    def get_player_healed(self):
        return self.player_healed

    def set_player_healed(self, player_healed):
        self.player_healed = player_healed

    def get_player_failure(self):
        return self.player_failure

    def set_player_failure(self, player_failure):
        self.player_failure = player_failure

    def get_player_banned(self):
        return self.player_banned

    def set_player_banned(self, player_banned):
        self.player_banned = player_banned

    def get_player_muted(self):
        return self.player_muted

    def set_player_muted(self, player_muted):
        self.player_muted = player_muted

    def get_player_ticket(self):
        return self.player_ticket

    def set_player_ticket(self, player_ticket):
        self.player_ticket = player_ticket

    def add_ticket(self):
        self.player_ticket += 1

    def death(self):
        self.set_player_status(0)


CHARACTER6 = [Character.hhd, Character.jjs, Character.ys, Character.ss, Character.mfs, Character.sl]
CHARACTER7 = [Character.hhd, Character.jjs, Character.ys, Character.jc, Character.ss, Character.mfs, Character.sl]
GAME_LIST = []


def send_message(dest, content):
    time.sleep(0.2)
    print(content + ' is being sent to ' + dest)
    itchat.send(msg=content, toUserName=dest)


def create_game(group_id):
    game_already_exist = False
    for game in GAME_LIST:
        if game.get_game_id() == group_id:
            game_already_exist = True
            break
    if not game_already_exist:
        game = Game(group_id)
        GAME_LIST.append(game)
        send_message(group_id, '游戏 ' + game.get_game_id() + ' 已创建')


def main():
    itchat.auto_login(hotReload=True, enableCmdQR=False)

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
    def group_op(msg):
        print(msg)
        if msg['isAt']:
            content = msg['Content'].split()[2]
            if content == '创建游戏':
                create_game(msg['FromUserName'])
            for game in GAME_LIST:
                if game.get_game_id() == msg['FromUserName']:
                    if content == '删除游戏':
                        GAME_LIST.remove(game)
                        send_message(msg['FromUserName'], '游戏 ' + game.game_id + ' 已删除')
                        del game
                    elif content == '重建游戏':
                        GAME_LIST.remove(game)
                        del game
                        create_game(msg['FromUserName'])
                    elif content == '法官':
                        game.be_master(msg['ActualUserName'])
                    break

        for game in GAME_LIST:
            if msg['FromUserName'] == game.get_game_id():
                content = msg['Content'].split()[0]
                if game.get_game_status() == 0:
                    if content == '加入':
                        game.add_player(msg['ActualUserName'], msg['ActualNickName'])
                    elif content == '离开':
                        game.del_player(msg['ActualUserName'], msg['ActualNickName'])
                    elif content == '开始游戏':
                        game.start()
                elif content == '开始投票' and game.get_game_status() == 4:
                    game.set_game_status(5)
                    send_message(msg['FromUserName'], '投票阶段开始')
                elif game.get_game_status() in [5, 7]:
                    game.day_control(msg['ActualUserName'], msg['Content'])
                if content == '重发身份':
                    for player in game.get_player_list():
                        send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character().value)
                elif content == '玩家数量':
                    send_message(msg['FromUserName'], '当前玩家数量：' + str(len(game.get_player_list())))
                elif content == '玩家列表':
                    player_list_str = '当前玩家列表：\n'
                    for seat, player in enumerate(game.player_list):
                        player_list_str += str(seat) + '  ' + (player.get_player_nn()) + '\n'
                    send_message(msg['FromUserName'], player_list_str)
                elif content == '游戏状态':
                    send_message(msg['FromUserName'], '当前游戏状态为：' + str(game.get_game_status()))
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制加入':
                    search_result = msg['User'].search_member(msg['Content'].split()[1])
                    if len(search_result) == 1:
                        game.add_player(search_result[0]['UserName'], search_result[0]['NickName'])
                    else:
                        game.add_player(msg['Content'].split()[1], msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制离开':
                    game.del_player(msg['Content'].split()[1], msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制结算':
                    if game.get_game_status() == 2:
                        game.set_game_status(3)
                        game.night_settlement()
                    elif game.get_game_status() == 5:
                        game.set_game_status(6)
                        game.day_settlement()
                    elif game.get_game_status() == 7:
                        game.set_game_status(8)
                        game.day_settlement()
                elif msg["ActualNickName"] == 'INT.ZC' and content == '游戏列表':
                    send_message(msg['FromUserName'], '\n'.join(game.get_game_id() for game in GAME_LIST))
                break

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
    def private_op(msg):
        if len(GAME_LIST) == 1 and GAME_LIST[0].get_game_status() in [2, 3]:
            GAME_LIST[0].night_control(msg['FromUserName'], msg['Content'])

    itchat.run()


if __name__ == '__main__':
    main()






