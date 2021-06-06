import telepot
import traceback
import sys
import University
import Major

# 봇 주소: https://t.me/kpu_fly_bot
# 봇 주소: https://t.me/kpu_fly_bot
# 봇 주소: https://t.me/kpu_fly_bot
# 봇 주소: https://t.me/kpu_fly_bot
# 봇 주소: https://t.me/kpu_fly_bot


class TelepotBot:
    def __init__(self):
        self.bot = telepot.Bot('1812538428:AAGarA_FAgTidwSM3orQWMLHz_Ow9UyniDg')
        self.bot.getMe()
        self.run()

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')
        if args[0] == '계열' and  len(args) ==1:
            print('try to 계열', args[1])

        elif args[0] == '학과' and  len(args) ==1:
            print('try to 계열학과', args[1])

        elif args[0] == '지역' and  len(args) ==1 :
            print('try to 지역', args[1])

        elif text.startswith('계열') and len(args) > 1:
            print('try to 계열 [계열이름]', args[1])

        elif text.startswith('학과') and len(args) > 1:
            print('try to 학과 [학과이름]', args[1])

        elif text.startswith('지역')and len(args) > 1:
            print('try to 지역 [지역이름]',args[1])

        else:
            self.sendMessage(chat_id, '모르는 명령어입니다.\n계열, 학과, 지역, 계열 [계열이름], 학과 [학과이름], 지역 [지역이름] 중 하나의 명령을 입력하세요.')

    def run(self):
        self.bot.message_loop(self.handle)


    def sendMessage(self, user, msg):
        try:
            self.bot.sendMessage(user, msg)
        except:
            traceback.print_exc(file=sys.stdout)


