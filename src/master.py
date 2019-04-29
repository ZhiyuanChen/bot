import random
import time
from game import Game, GameStatus
import itchat

GAME_LIST = []


def send_message(dest, content):
    time.sleep(0.3+random.random()/5)
    print(content + ' is being sent to ' + dest)
    try:
        itchat.send(msg=content, toUserName=dest)
    except TimeoutError:
        send_message(dest, content)


def create_game(group_id):
    for game in GAME_LIST:
        if game.game_id == group_id:
            send_message(group_id, '游戏 ' + game.game_id + ' 已存在')
            return
    game = Game(group_id)
    GAME_LIST.append(game)
    send_message(group_id, '游戏 ' + game.game_id + ' 已创建')


def main():
    itchat.auto_login(hotReload=True, enableCmdQR=2)

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
    def group_op(msg):
        print(msg)
        if msg['isAt']:
            content = msg['Content'].split()[2]
            if content == '创建游戏':
                create_game(msg['FromUserName'])
            for game in GAME_LIST:
                if game.game_id == msg['FromUserName']:
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
            if msg['FromUserName'] == game.game_id:
                content = msg['Content'].split()[0]
                if msg["ActualNickName"] == 'INT.ZC' and content == '强制加入':
                    search_result = msg['User'].search_member(msg['Content'].split()[1])
                    if len(search_result) == 1:
                        game.add_player(search_result[0]['UserName'], search_result[0]['NickName'])
                    else:
                        game.add_player(msg['Content'].split()[1], 'bot' + msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制离开':
                    game.del_player(msg['Content'].split()[1], msg['Content'].split()[1])
                elif msg["ActualNickName"] == 'INT.ZC' and content == '强制结算':
                    if game.game_status == GameStatus.action:
                        game.game_status = GameStatus.settlement
                        game.night_settlement()
                    elif game.game_status == GameStatus.vote_one:
                        game.game_status = GameStatus.count_one
                        game.day_settlement()
                    elif game.game_status == GameStatus.vote_two:
                        game.game_status = GameStatus.count_two
                        game.day_settlement()
                elif msg["ActualNickName"] == 'INT.ZC' and content == '游戏列表':
                    send_message(msg['FromUserName'], '\n'.join(game.game_id for game in GAME_LIST))
                if game.game_status == GameStatus.ready:
                    if content == '加入':
                        game.add_player(msg['ActualUserName'], msg['ActualNickName'])
                    elif content == '离开':
                        game.del_player(msg['ActualUserName'], msg['ActualNickName'])
                    elif content == '开始游戏':
                        game.start()
                elif content == '开始投票' and game.game_status == GameStatus.speech:
                    game.game_status = GameStatus.vote_one
                    send_message(msg['FromUserName'], '投票阶段开始')
                elif game.game_status in [GameStatus.vote_one, GameStatus.vote_two]:
                    game.day_control(msg['ActualUserName'], msg['Content'])
                if content == '重发身份' and game.game_status != GameStatus.ready:
                    for player in game.alive_player_set:
                        send_message(player.player_id, '您的身份是：\n' + player.player_character.value)
                elif content == '玩家数量':
                    send_message(msg['FromUserName'], '当前玩家数量：' + str(len(game.player_list)))
                elif content == '玩家列表':
                    if game.game_status == GameStatus.ready:
                        player_list_str = '当前玩家列表：\n'
                        for seat, player in enumerate(game.player_list):
                            player_list_str += str(seat + 1) + '  ' + player.player_nn + '\n'
                    else:
                        player_list_str = '当前存活玩家列表：\n'
                        for seat, player in enumerate(game.alive_player_set):
                            player_list_str += str(player.player_seat) + '  ' + player.player_nn + '\n'
                    send_message(msg['FromUserName'], player_list_str)
                elif content == '游戏状态':
                    send_message(msg['FromUserName'], '当前游戏状态为：' + game.game_status.value)
                elif content == '行动状态':
                    send_message(game.game_id, game.action_status())
                break

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
    def private_op(msg):
        if len(GAME_LIST) == 1 and GAME_LIST[0].game_status in [GameStatus.action, GameStatus.settlement]:
            GAME_LIST[0].night_control(msg['FromUserName'], msg['Content'])

    itchat.run()


if __name__ == '__main__':
    main()
