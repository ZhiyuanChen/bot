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
        self.game_mode = 0  # 游戏类型 1：无转职禁言 2：无转职禁票 3：有转职禁言 4：有转职禁票
        self.player_list = []
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

    def get_alive_player(self):
        return self.alive_player

    def set_alive_player(self, alive_player):
        self.alive_player = alive_player

    def get_actioned_player(self):
        return self.actioned_player

    def set_actioned_player(self, actioned_player):
        self.actioned_player = actioned_player

    def get_mfs(self):
        for player in self.player_list:
            if player.get_player_character() == Character.mfs:
                return player

    def get_hhd(self):
        for player in self.player_list:
            if player.get_player_character() == Character.hhd:
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
            if player_id == player.player_id and player.status != 0:
                is_alive_player = True
                break
        if not is_alive_player:
            send_message(player_id, '\n'.join(player.player_nn + '的身份是：' + player.player_character for player in self.player_list))

    def start(self):
        random.shuffle(self.player_list)
        player_list_str = '玩家名单\n'
        for seat, player in enumerate(self.player_list):
            player.set_player_seat(seat + 1)
            player_list_str += str(player.get_player_seat()) + '  ' + (player.get_player_nn()) + '\n'
        send_message(self.game_id, player_list_str + '\n身份发放开始')
        if len(self.player_list) == 7:
            character_list = CHARACTER7
            self.game_mode = 3
        else:
            character_list = CHARACTER6
            self.game_mode = 2
        random.shuffle(character_list)
        for index, player in enumerate(self.player_list):
            player.name = character_list[index].name
            player.set_player_character(character_list[index])
            player.set_player_status(2)
            send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character().value)
        self.alive_player = len(self.player_list)
        self.game_status = 1
        send_message(self.game_id, '身份发放完成\n请私戳法官进行夜间行动')
        self.game_status = 2
        for player in self.player_list:
            send_message(player.get_player_id(), '请开始行动')

    def night_control(self, player_id, message):
        if self.game_status == 2:
            if self.actioned_player < self.alive_player:
                if message.split()[0] == '行动':
                    for player in self.player_list:
                        if player_id == player.get_player_id() and player.get_player_status() == 2:
                            available_target = False
                            for target_player in self.player_list:
                                if int(message.split()[1]) == target_player.get_player_seat():
                                    available_target = True
                                    break
                            if available_target:
                                self.night_action(player, int(message.split()[1]))
                            else:
                                send_message(player_id, '行动目标不正确')
                            break
                        else:
                            send_message(player_id, '您无法行动')
            if self.get_actioned_player() == self.get_alive_player():
                self.set_game_status(3)
                self.night_settlement()

    def night_action(self, player, target):
        for target_player in self.player_list:
            if target == target_player.get_player_seat():
                player.set_player_aims(target)
                player.set_player_target(target)
                player.set_player_status(3)
                self.actioned_player += 1
                break
        send_message(player.get_player_id(), '行动目标设置为：' + str(player.get_player_target()))

    def night_settlement(self):
        send_message(self.game_id, '夜间行动完成\n请等待法官结算')
        if self.get_mfs().get_player_target != self.get_hhd():
            pass


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
        self.player_target = None
        self.player_hugged = False
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

    def death(self):
        self.set_player_status(0)
        if self.get_player_character() in [Character.ss, Character.mfs, Character.sl]:
            return False
        return True

    def hug(self):
        if self.get_player_character() == Character.hhd:
            pass


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
                        del game
                        send_message(msg['FromUserName'], '游戏 ' + game.game_id + ' 已删除')
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
                if content == '重发身份':
                    for player in game.get_player_list():
                        send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character())
                elif content == '玩家数量':
                    send_message(msg['FromUserName'], '当前玩家数量：' + str(len(game.get_player_list())))
                elif content == '玩家列表':
                    send_message(msg['FromUserName'], '\n'.join(player.get_player_nn() for player in game.get_player_list()))
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制加入':
                    game.add_player(msg['Content'].split()[1], msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制离开':
                    game.del_player(msg['Content'].split()[1], msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制结算':
                    if game.get_game_status() == 2:
                        game.set_game_status(3)
                        game.night_settlement()

                elif msg["ActualNickName"] == 'INT.ZC' and content == '游戏列表':
                    send_message(msg['FromUserName'], '\n'.join(game.get_game_id() for game in GAME_LIST))
                break

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
    def private_op(msg):
        if len(GAME_LIST) == 1:
            GAME_LIST[0].night_control(msg['FromUserName'], msg['Content'])

    itchat.run()


if __name__ == '__main__':
    main()






