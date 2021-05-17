import Connect
from tkinter import *
from tkinter.ttk import *
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump, ElementTree

class Interface:
    def changeValue(self, index, value, op):
        b_index = self.line_select.current()
        self.temp = self.tem.getUniversiryInfo_line(b_index)


    def __init__(self):
        #======= 임시로 생성한 리스트 ========
        self.line_list = []

        #==================================
        self.tem = Connect.CarrerNetPassing()
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("너의 편입은? Fly")
        self.canvas = Canvas(self.window, bg='white', width=1280, height=720)
        self.canvas.pack()

# ----------------------------------- 여긴 계열 선택 ----------------------------------------------\
        self.brand = ["전체", "인문계열", "사회계열", "교육계열", "공학계열", "자연계열", "의약계열", "예체능계열"]
        self.str1 = StringVar()
        self.str1.trace('w', self.changeValue)
        self.canvas.create_text(40, 40, text="계열")
        self.line_select = Combobox(self.window, state='readonly', textvariable=self.str1, values=self.brand)
        self.line_select.place(x=100, y=30)



#----------------------------------- 여긴 OO도 선택지역 ----------------------------------------------
        self.canvas.create_text(40, 80, text="지역-도")
        self.region_select = Combobox(self.window)
        self.region_select['value'] = ("서울특별시", "인천광역시", "부산광역시", "대전광역시", "대구광역시", "광주광역시", "울산광역시", "경기도",
                                       "충청북도", "충청남도", "경상북도", "경상남도", "강원도", "전라북도", "전라남도", "제주도")
        self.region_select.place(x=100,y=70)

#----------------------------------- 여긴 OO시 선택지역 ---------------------------------------------
        self.canvas.create_text(40, 120, text="지역-시")
        self.country_select = Combobox(self.window)
        self.country_select['value'] = None

        self.country_select.place(x=100, y=110)

# ----------------------------------- 여긴 학과 선택 ----------------------------------------------
        self.canvas.create_text(40, 160, text="학과")
        self.department_select = Combobox(self.window)
        list = [1,2,3,4,5]
        self.department_select['value'] = self.line_list # 학과를 xml로 로드해서 가져와야함 (리스트로 받는다)
        self.department_select.place(x=100, y=150)

        self.window.mainloop()


Connect.CarrerNetPassing()
Interface()