import Connect
from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter.ttk import *
import xml.etree.ElementTree as ET
import folium
import googlemaps

from cefpython3 import cefpython as cef
import sys
import threading


import urllib.request
import requests
from PIL import Image
from io import BytesIO

class Interface:
    line_list = []
    #country_list = []
    rect = [0, 0, 800, 720]
    stop_thread = False
    def sendmail(self):
        pass

    def __init__(self):
        #======= 구글 지도 api key ========
        self.__key = "AIzaSyDyJvpUNI8aZh0pPu-SRG-HBdDbxwyg4Tw"
        #==================================

        self.tem=  Connect.CarrerNetPassing()
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("너의 편입은? Fly")

        self.window.geometry("1280x720")
        self.bgimage = PhotoImage(file='resource\\bg.png') #<- 이미지를 마음에 드는걸로 바꾸면됨 :)
        self.canvas = Canvas(self.window, width=1280, height=720)
        self.canvas.create_image(0,0,anchor=NW, image=self.bgimage)
        self.canvas.place(x=0, y=0)
        self.temp_font=font.Font(size=10, weight='bold', family='italic')

        self.canvas.create_rectangle(0, 0, 240, 720, fill="gray65")

        self.canvas.create_rectangle(0, 0, 240, 30, fill="gray90")
        self.canvas.create_text(120, 15, text="검색 조건", font=self.temp_font)
# ----------------------------------- 여긴 계열 선택 ----------------------------------------------\
        self.canvas.create_rectangle(15, 45, 225, 75, fill="gray90", outline='white')
        self.brand = ["전체", "인문계열", "사회계열", "교육계열", "공학계열", "자연계열", "의약계열", "예체능계열"]
        self.str1 = StringVar()
        self.str1.trace('w', self.changeMajor)
        self.canvas.create_text(35, 60, text="계열",font=self.temp_font)
        self.line_select = Combobox(self.window, state='readonly', textvariable=self.str1, values=self.brand)
        self.line_select.place(x=55, y=50)

# ----------------------------------- 여긴 학과 선택 ----------------------------------------------
        self.canvas.create_rectangle(15, 85, 225, 115, fill="gray90", outline='white')
        self.canvas.create_text(35, 100, text="학과",font=self.temp_font)
        self.major_select = Combobox(self.window)
        self.major_select['value'] = self.line_list  # 학과를 xml로 로드해서 가져와야함 (리스트로 받는다)
        self.major_select.place(x=55, y=90)

#----------------------------------- 여긴 OO도 선택지역 ----------------------------------------------
        self.canvas.create_rectangle(15, 125, 225, 155, fill="gray90", outline='white')
        self.canvas.create_text(35, 140, text="지역",font=self.temp_font)
        self.area_select = Combobox(self.window)
        self.area_select['value'] = ("서울특별시", "인천광역시", "부산광역시", "대전광역시", "대구광역시", "광주광역시", "울산광역시", "경기도",
                                       "충청북도", "충청남도", "경상북도", "경상남도", "강원도", "전라북도", "전라남도", "제주도")
        self.area_select.place(x=55, y=130)


# ----------------------------------- 여긴 학과가 있는 대학 검색임 -------------------------------------------------
        self.show_resultButton = Button(self.window, text='검색', width=10, command=self.showSearchResult)
        self.show_resultButton.place(x=90, y=165)

        self.rst_university_list = []

# ----------------------------------- 여긴 대학교 선택 -------------------------------------------------
        self.canvas.create_rectangle(0, 200, 240, 230, fill="gray90")
        self.canvas.create_text(120, 215, text="검색 결과", font=self.temp_font)

        self.college_select = Listbox(self.window, selectmode='extended',bg='gray90')
        self.college_select.bind('<<ListboxSelect>>', self.click_item)
        self.college_select.place(x=15, y=245, width=210, height=445)

# -----------------------------------  선택 학교 정보창 -------------------------------------------------
        #openUniversityInfoWindow 에서 배치
        self.rst_canvas = Canvas(self.window, width=240, height=720)
        self.rst_canvas.create_rectangle(0, 0, 240, 720, fill="gray65")

        # rect (0,240) (240,135)에 학교 사진 넣을 예정
        self.close_univ_rstButton = Button(self.window, text='X',  width=3, command=self.closeUniversityInfoWindow)

        location_image = PhotoImage(file='resource\\location.png')
        globe_image=PhotoImage(file='resource\\globe.png')
        self.rst_canvas.create_image(10, 220, anchor=W, image=location_image)
        self.rst_canvas.create_image(10, 250, anchor=W, image=globe_image)


        self.rst_canvas.create_line(0, 0, 0, 730)
        self.rst_canvas.create_line(0, 135, 240, 135)
        self.rst_canvas.create_line(240, 0, 240, 730)

#----------------------------------- 여긴 지도임 -------------------------------------------------

        # 지도 이미지 받아오게 하는 부분임....
        url = "https://www.google.co.kr/maps/@37.053745,125.6553969,5z?hl=ko"
        self.map_frame = tk.Frame(self.window, bg='blue', width=800, height=720)
        self.map_frame.place(x=480, y=0)
        self.thread = threading.Thread(target=self.test_thread, args=(self.map_frame,url))
        self.thread.start()

#----------------------------------- 이메일 버튼 -------------------------------------------------

        self.gmail_image = PhotoImage(file='resource\\gmail.png')
        self.gmailButton = Button(self.window, image=self.gmail_image, width=10,command=self.sendmail)
        self.gmailButton.place(x=1225, y=0)

        self.canvas.create_line(240, 0, 240, 730)

        self.canvas.create_line(0, 200, 240,200)




        self.window.mainloop()



    def click_item(self, event):
        selectedItem = self.college_select.curselection()
        if len(selectedItem) != 0:
            self.openUniversityInfoWindow(selectedItem[0])
            self.showMap(selectedItem[0])


    def changeMajor(self, index, value, op):
        self.temp = self.tem.getUniversiryInfo_line(self.line_select.current())
        tree = ET.ElementTree(ET.fromstring(self.temp))
        note = tree.iter('facilName')
        self.line_list.clear()
        for elt in tree.iter('facilName'):
            temp = [x for x in elt.text.split(',')]
            for i in temp:
                self.line_list.append(i)

        self.major_select['value'] = self.line_list

    def showSearchResult(self):

        if self.line_select.current() == -1:
            curr_line=''
        else:
            curr_line=self.line_select['value'][self.line_select.current()]
        if self.major_select.current() == -1:
            curr_major=''
        else:
            curr_major=self.major_select['value'][self.major_select.current()]
        if self.area_select.current() == -1:
            curr_area=''
        else:
            curr_area=self.area_select['value'][self.area_select.current()]

        self.rst_university_list.clear()
        self.rst_university_list=self.tem.getUniversiryInfo(curr_line, curr_major, curr_area)
        k = self.college_select.size()
        for i in range(k):
            self.college_select.delete(i)

        for i in range(len(self.rst_university_list)):
            self.college_select.insert(i, self.rst_university_list[i].getSchoolName())

        self.closeUniversityInfoWindow()


    def openUniversityInfoWindow(self,index):
        self.rst_canvas.delete('school_name')
        self.rst_canvas.delete('campus_name')
        self.rst_canvas.delete('area')
        self.rst_canvas.delete('school_URL')
        self.rst_canvas.create_text(35, 160, text=self.rst_university_list[index].getSchoolName(), font=self.temp_font,anchor=W,tags= 'school_name')
        self.rst_canvas.create_text(35, 190, text=self.rst_university_list[index].getCampusName(), font=self.temp_font,anchor=W,tags= 'campus_name')
        self.rst_canvas.create_text(35, 220, text=self.rst_university_list[index].getArea(), font=self.temp_font,anchor=W,tags= 'area')
        self.rst_canvas.create_text(35, 250, text=self.rst_university_list[index].getSchoolURL(), font=self.temp_font,anchor=W,tags= 'school_URL')
        self.rst_canvas.place(x=240, y=0)

        self.close_univ_rstButton.place(x=450,y=0)

    def closeUniversityInfoWindow(self):
        self.rst_canvas.place_forget()
        self.close_univ_rstButton.place_forget()


    def showMap(self, index):
        largura = 640
        alturaplus = 640
        final = Image.new("RGB", (largura, alturaplus))

        self.gmaps = googlemaps.Client(key=self.__key)
        geocode_result = self.gmaps.geocode(str(self.rst_university_list[index].getSchoolName()), language='ko')
        print(geocode_result)

        if len(geocode_result) != 0:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            addr = geocode_result[0]['formatted_address']
            urlparams = urllib.parse.urlencode({'center': self.rst_university_list[index].getSchoolName(),
                                            'zoom': '16',
                                            'size': '%dx%d' % (1280, 1280),
                                            'maptype': 'ROADMAP',
                                            'markers': 'color:blue|label:S|' + str(lat) + "," + str(lng),
                                            'key': self.__key})
            url = 'https://maps.googleapis.com/maps/api/staticmap?' + urlparams

        else:
            pass

    def test_thread(self, frame, url):
        sys.excepthook = cef.ExceptHook
        self.window_info = cef.WindowInfo(frame.winfo_id())
        self.window_info.SetAsChild(frame.winfo_id(), self.rect)
        cef.Initialize()
        browser = cef.CreateBrowserSync(self.window_info, url=url)
        cef.MessageLoop()


Interface()
