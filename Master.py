import uuid
from enum import Enum
import itchat
import time
import random


class Game(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_status = 0
        self.game_type = 0
        self.player_list = []

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

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, player_list):
        self.player_list = player_list

    def add_player(self, player_id):
        self.player_list.append(player_id)

    def del_player(self, player_id):
        self.player_list.remove(player_id)


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

    def heal(self):
        self.set_player_healed(True)


class Player(object):
    def __init__(self, player_id, player_nn):
        self.player_id = player_id
        self.player_nn = player_nn
        self.player_seat = 0
        self.player_status = 0
        self.player_character = 0
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


CHARACTER6 = [Character.hhd, Character.jjs, Character.ys, Character.ss, Character.mfs, Character.sl]
CHARACTER7 = [Character.hhd, Character.jjs, Character.ys, Character.jc, Character.ss, Character.mfs, Character.sl]
GAME_LIST = []


# def settlement():
#     player_list = []
#     player = Player(0000)
#     player_list.append(player)
#     for player in player_list:
#
#         if player.get_player_character() is Character.jc:
#             jc_target = player.get_player_target()
#         if player.get_player_character() is Character.jjs:
#             jjs_target = player.get_player_target()
#         if player.get_player_character() is Character.ys:
#             ys_target = player.get_player_target()
#         if player.get_player_character() is Character.ss:
#             ss_target = player.get_player_target()
#         if player.get_player_character() is Character.sl:
#             sl_target = player.get_player_target()
#         if player.get_player_character() is Character.sm:
#             sm_target = player.get_player_target()
#         if player.get_player_character() is Character.em:
#             em_target = player.get_player_target()
#         if player.get_player_character() is Character.wy:
#             wy_target = player.get_player_target()
#         if player.get_player_character() is Character.jz:
#             jz_target = player.get_player_target()
#
#         if player.get_player_character() is Character.mfs:
#             mfs_target = player.get_player_target()
#             if mfs_target.get_player_hugged:
#                 pass
#             else:
#                 player.get_player_target().set_player_target(None)
#
#         if player.get_player_character() is Character.hhd:
#             hhd_target = player.get_player_target()
#             if mfs_target is Character.hhd:
#                 pass


def send_message(dest, content):
    time.sleep(0.2)
    print(content + ' is being sent to ' + dest)
    itchat.send(msg=content, toUserName=dest)


def create_game(group_id):
    game_already_exist = False
    for game in GAME_LIST:
        if game.get_game_id() == group_id:
            game_already_exist = True
    if not game_already_exist:
        game = Game(group_id)
        GAME_LIST.append(game)
        send_message(group_id, '游戏 ' + game.get_game_id() + ' 已创建')


def start_game(game, group_id):
    random.shuffle(game.get_player_list())
    game.set_player_list(game.get_player_list())
    send_message(group_id, '玩家名单：\n' + '\n'.join(
        player.get_player_nn() + '  ' + str(index + 1) for index, player in
        enumerate(game.get_player_list())) + '\n身份发放开始')
    if len(game.get_player_list()) == 7:
        random.shuffle(CHARACTER7)
        for index, player in enumerate(game.get_player_list()):
            player.name = CHARACTER7[index].name
            CHARACTER7[index].name.set_player_character(CHARACTER7[index].value)
            send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character())
    else:
        random.shuffle(CHARACTER6)
        for index, player in enumerate(game.get_player_list()):
            player.name = CHARACTER6[index].name
            player.set_player_character(CHARACTER6[index].value)
            send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character())
    game.set_game_status(1)
    send_message(group_id, '身份发放完成\n请私戳法官进行夜间行动')


def add_player(game, group_id, user_id, user_nn):
    if group_id == game.get_game_id():
        player_already_exist = False
        for player in game.get_player_list():
            if user_id == player.get_player_id():
                player_already_exist = True
        if player_already_exist:
            send_message(group_id, '@' + user_nn + '\u2005' + '您已加入游戏')
        else:
            game.add_player(Player(user_id, user_nn))
            send_message(group_id, '@' + user_nn + '\u2005' + '加入游戏')


def del_player(game, group_id, user_id, user_nn):
    if group_id == game.get_game_id():
        player_exist = False
        for player in game.get_player_list():
            if user_id == player.get_player_id():
                player_exist = True
        if not player_exist:
            send_message(group_id, '@' + user_nn + '\u2005' + '您还不是玩家')
        else:
            for player in game.get_player_list():
                if player.get_player_id() == user_id:
                    game.del_player(player)
            send_message(group_id, '@' + user_nn + '\u2005' + '离开游戏')


def main():
    itchat.auto_login(hotReload=True, enableCmdQR=False)
    group_chat_dict = itchat.search_chatrooms(name='HHDbot')
    for item in group_chat_dict:
        print(len(group_chat_dict))
        print(item)
    # itchat.send("机器人启动！！！！", toUserName="@@803d052409c5d1d19368552f05d39ee69340002deb9952993c92f2b03afcf8b2")

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
    def group_op(msg):
        print(msg)
        if msg['isAt']:
            content = msg['Content'].split()[2]
            if content == '创建游戏':
                create_game(msg['FromUserName'])
            for game in GAME_LIST:
                if game.get_game_id() == msg['FromUserName']:
                    if content == '开始游戏':
                        start_game(game, msg['FromUserName'])
                    elif content == '重发身份':
                        for player in game.get_player_list():
                            send_message(player.get_player_id(), '您的身份是：\n' + player.get_player_character())
                    elif content == '删除游戏':
                        GAME_LIST.remove(game)
                        send_message(msg['FromUserName'], '游戏 ' + game.game_id + ' 已删除')
                    elif content == '法官':
                        send_message(msg['ActualUserName'],  '\n'.join(player.get_player_nn() + '的身份是：' + player.get_player_character() for player in game.get_player_list()))
        for game in GAME_LIST:
            if msg['FromUserName'] == game.get_game_id() and game.get_game_status() == 0:
                content = msg['Content']
                if content == '加入':
                    add_player(game, msg['FromUserName'], msg['ActualUserName'], msg['ActualNickName'])
                elif content == '离开':
                    del_player(game, msg['FromUserName'], msg['ActualUserName'], msg['ActualNickName'])
                elif content == '玩家数量':
                    send_message(msg['FromUserName'], '当前玩家数量：' + str(len(game.get_player_list())))
                elif content == '玩家列表':
                    send_message(msg['FromUserName'], '\n'.join(player.get_player_nn() for player in game.get_player_list()))
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制添加':
                    add_player(game, msg['FromUserName'], msg['Content'].split()[3], msg['Content'].split()[3])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制移出':
                    del_player(game, msg['FromUserName'], msg['Content'].split()[3], msg['Content'].split()[3])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '游戏列表':
                    send_message(msg['FromUserName'], ' '.join(game.get_game_id() for game in GAME_LIST))

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
    def private_op(msg):
        if len(GAME_LIST) == 1 and GAME_LIST[0].get_game_status() == 1:
            for player in GAME_LIST[0].get_player_list():
                print(player.get_player_character())

    itchat.run()


if __name__ == '__main__':
    main()






