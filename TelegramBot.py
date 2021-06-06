import telepot
import traceback
import sys
import Connect
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
        if args[0] == 'help' and  len(args) ==1:
            self.sendMessage(chat_id,
                             "계열목록, 학과목록 [계열이름], 지역목록\n학과 [계열이름] [학과이름] [지역이름]")

        elif args[0] == '계열목록' and  len(args) ==1:             #계열 리스트
            line_list = "인문계열, 사회계열, 교육계열, 공학계열, 자연계열, 의약계열, 예체능계열"
            self.sendMessage(chat_id, line_list)

        elif args[0] == '학과목록' and  len(args) > 1:           #학과 리스트(계열별)
            temp=Connect.CarrerNetPassing().getUniversiryInfo_line(args[1])
            if temp==False:
                self.sendMessage(chat_id, "없는 계열입니다.")
            else:
                major=""
                for i in range(len(temp)):
                    major+=temp[i]

                    if len(major)>380: #한 번에 너무 긴 메시지는 보낼 수 없음 -> 중간중간 끊어서 보냄
                        self.sendMessage(chat_id, major)
                        major=""
                        continue

                    if i != len(temp)-1:
                        major += ', '

                self.sendMessage(chat_id, major)

        elif args[0] == '지역목록' and  len(args) ==1 :           #지역 리스트
            area_list = "서울특별시, 인천광역시, 부산광역시, 대전광역시, 대구광역시, 광주광역시, 울산광역시, 경기도, 충청북도, 충청남도, 경상북도, 경상남도, 강원도, 전라북도, 전라남도, 제주도"
            self.sendMessage(chat_id, area_list)


        elif len(args) > 3 and (text.startswith('학과')):
            rst_major_list=[]
            rst_university_list = []

            if text.startswith('학과') :
                rst_major_list, rst_university_list = Connect.CarrerNetPassing().getUniversiryInfo(args[1], args[2], args[3])


            univ=''
            for i in range(len(rst_university_list)):
                univ += rst_university_list[i].getSchoolName()

                if len(univ) > 380:  # 한 번에 너무 긴 메시지는 보낼 수 없음 -> 중간중간 끊어서 보냄
                    self.sendMessage(chat_id, univ)
                    univ = ""
                    continue

                if i != len(rst_university_list) - 1:
                    univ += ', '

            self.sendMessage(chat_id, univ)

        else:
            self.sendMessage(chat_id, '모르는 명령어입니다.\n계열목록, 학과목록 [계열이름], 지역목록\n학과 [계열이름] [학과이름] [지역이름] 중 하나의 명령을 입력하세요.')

    def run(self):
        self.bot.message_loop(self.handle)


    def sendMessage(self, user, msg):
        try:
            self.bot.sendMessage(user, msg)
        except:
            traceback.print_exc(file=sys.stdout)


