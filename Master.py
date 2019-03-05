import uuid
from enum import Enum
import itchat
import time
import random


class Game(object):
    def __init__(self):
        self.game_id = str(uuid.uuid1()).split('-')[0]
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
    def __init__(self, player_id):
        self.player_id = player_id
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
    print(content + ' is being sended to ' + dest)
    itchat.send(msg=content, toUserName=dest)


def main():
    CHARACTER = ['花蝴蝶', '狙击手', '医生', '杀手', '魔法师', '森林老人']
    game_list = []
    itchat.auto_login(hotReload=True, enableCmdQR=False)

    group_chat_dict = itchat.search_chatrooms(name='HHD')
    for item in group_chat_dict:
        print(len(group_chat_dict))
        print(item)
    # itchat.send("机器人启动！！！！", toUserName="@@803d052409c5d1d19368552f05d39ee69340002deb9952993c92f2b03afcf8b2")

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
    def text_reply(msg):
        print(msg)
        if msg['isAt'] and msg['FromUserName'] == '@@803d052409c5d1d19368552f05d39ee69340002deb9952993c92f2b03afcf8b2':
            content = msg['Content'].split()[2]
            if content == '创建游戏':
                game = Game()
                game_list.append(game)
                send_message(msg['FromUserName'], '游戏 ' + game.get_game_id() + ' 创建')
            elif len(content) == 8:
                for game in game_list:
                    if content == game.get_game_id():
                        player_already_exist = False
                        for player in game.get_player_list():
                            if msg["ActualNickName"] == player.get_player_id():
                                player_already_exist = True
                        if player_already_exist:
                            send_message(msg['FromUserName'], '@' + msg["ActualNickName"] + '\u2005' + '您已加入游戏' + game.get_game_id())
                        else:
                            game.add_player(Player(msg["ActualNickName"]))
                            send_message(msg['FromUserName'], '@' + msg["ActualNickName"] + '\u2005' + '加入游戏' + game.get_game_id())
                            send_message(msg['FromUserName'], '当前玩家人数：' + str(len(game.get_player_list())))
                    # else:
                    #     send_message(msg['FromUserName'], '游戏' + content + '不存在')
            elif msg["ActualNickName"] == 'INT.ZC' and content == '强制添加':
                for game in game_list:
                    if msg['Content'].split()[3] == game.get_game_id():
                        game.add_player(Player(msg['Content'].split()[4]))
                        send_message(msg['FromUserName'], msg["ActualNickName"] + ' 加入游戏' + game.get_game_id())
                        send_message(msg['FromUserName'], '当前玩家人数：' + str(len(game.get_player_list())))
                    # else:
                    #     send_message(msg['FromUserName'], '游戏' + content + '不存在')
            elif content == '删除游戏':
                for game in game_list:
                    if msg['Content'].split()[3] == game.get_game_id():
                        send_message(msg['FromUserName'], game.get_player_list())
            elif content == '玩家列表':
                for game in game_list:
                    if msg['Content'].split()[3] == game.get_game_id():
                        send_message(msg['FromUserName'], ' '.join(player.get_player_id() for player in game.get_player_list()))
            elif content == '游戏列表':
                temp = []
                for game in game_list:
                    temp.append(game.get_game_id())
                send_message(msg['FromUserName'], ' '.join(temp))
            elif content == '开始游戏':
                for game in game_list:
                    if msg['Content'].split()[3] == game.get_game_id():
                        send_message(msg['FromUserName'], ' '.join(player.get_player_id() for player in game.get_player_list()))
                        game.set_player_list(random.shuffle(game.get_player_list()))
                        send_message(msg['FromUserName'], ' '.join(player.get_player_id() for player in game.get_player_list()))
                        random.shuffle(CHARACTER)
                        send_message(msg['FromUserName'], ' '.join(CHARACTER))
                        game.set_game_status(1)
    itchat.run()


if __name__ == '__main__':
    main()






