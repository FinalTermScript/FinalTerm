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
            print('try to 계열', args[0])
            line_list = "인문계열, 사회계열, 교육계열, 공학계열, 자연계열, 의약계열, 예체능계열"
            self.sendMessage(chat_id, line_list)


        elif args[0] == '학과' and  len(args) ==1:
            print('try to 계열학과', args[0])

        elif args[0] == '지역' and  len(args) ==1 :
            print('try to 지역', args[0])
            area_list = "서울특별시, 인천광역시, 부산광역시, 대전광역시, 대구광역시, 광주광역시, 울산광역시, 경기도, 충청북도, 충청남도, 경상북도, 경상남도, 강원도, 전라북도, 전라남도, 제주도"
            self.sendMessage(chat_id, area_list)

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


