import Connect
from tkinter import *
from tkinter.ttk import *

class Interface:
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("너의 편입은? Fly")
        self.canvas = Canvas(self.window, bg='white', width=1280, height=720)
        self.canvas.pack()

# ----------------------------------- 여긴 계열 선택 ----------------------------------------------
        self.canvas.create_text(40, 90, text="계열")
        self.line_select = Combobox(self.window)
        self.line_select['value'] = ("인문계열", "사회계열", "교육계열", "공학계열", "자연계열", "의약계열", "예체능계열")
        self.line_select.place(x=100, y=80)



#----------------------------------- 여긴 OO도 선택지역 ----------------------------------------------
        self.canvas.create_text(40, 130, text="지역-도")
        self.region_select = Combobox(self.window)
        self.region_select['value'] = ("서울특별시", "인천광역시", "부산광역시", "대전광역시", "대구광역시", "광주광역시", "울산광역시", "경기도",
                                       "충청북도", "충청남도", "경상북도", "경상남도", "강원도", "전라북도", "전라남도", "제주도")
        self.region_select.place(x=100,y=120)

#----------------------------------- 여긴 OO시 선택지역 ---------------------------------------------


# ----------------------------------- 여긴 학과 선택 ----------------------------------------------
        self.department_select = Combobox(self.window)
        list = [1,2,3,4,5]
        self.department_select['value'] = list # 학과를 xml로 로드해서 가져와야함 (리스트로 받는다)
        self.department_select.place(x=100, y=150)

        self.window.mainloop()

Interface()