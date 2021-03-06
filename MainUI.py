import Connect
import CrawlImg
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

import Gmail
import time
from PIL import Image
from io import BytesIO

import urllib.request
import TelegramBot

import spam


thread = True
count = 0
search = False
urls = 'https://map.naver.com/'
class Interface:
    line_list = []
    now_url = ""
    #country_list = []
    rect = [0, 0, 1280, 720]
    stop_thread = False
    load_college = ''
    mail_college = ''
    college_url = ''
    map_url = ''

    def closeSendmail(self):
        self.mailFrame.place_forget()
        self.closeMail.place_forget()
        self.emaill.place_forget()
        self.emaillLabel.place_forget()
        self.sendButton.place_forget()


    def send(self):
        time.sleep(10)
        Gmail.MakeConcept(self.mail_college, self.rst_major_list[0], self.college_url, Entry.get(self.emaill))
        self.mailFrame.destroy()

    def ccc(self, event):
        self.emaillLabel['text'] = str(spam.send()) + str(Entry.get(self.emaill))
        self.emaillLabel.place(x=20,y=10)


    def sendmail(self):
        # email_send의 첫번째 인자 : 누가 보내는지
        # email_send의 두번째 인자 : 목적지 이메일 주소
        # email_send의 세번째 인자 : 이메일 제목
        # email_send의 네번째 인자 : 내용!
        #Gmail.email_send("", "", "요청하신 대학정보", "테스트중입니다.")
        self.mailFrame = Tk()
        self.mailFrame.geometry("200x100")
        self.emaillLabel = Label(self.mailFrame, text="이메일을 입력하세요")
        self.emaillLabel.place(x=40, y=10)
        self.emaill = Entry(self.mailFrame, text="이메일을 입력하세요")
        self.emaill.bind("<Key>", self.ccc)
        self.emaill.place(x=25, y=40)
        self.emaill.focus_set()
        self.browser.StopLoad()
        self.sendButton = Button(self.mailFrame, text="전송", command=self.send)
        self.sendButton.place(x=50, y=70)

        #Gmail.MakeConcept(self.mail_college, self.rst_major_list[0], self.college_url)

    def __init__(self):
        global search
        CrawlImg.onWebBrowser()
        #======= 구글 지도 api key ========
        self.__key = "AIzaSyDyJvpUNI8aZh0pPu-SRG-HBdDbxwyg4Tw"
        #==================================

        self.tem=  Connect.CarrerNetPassing()
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("너의 편입은? Fly")

        self.window.geometry("1280x720")
        self.canvas = Canvas(self.window, width=1280, height=720)
        self.canvas.place(x=0, y=0)
        self.temp_font=font.Font(size=10, weight='bold', family='italic')

        # UI 색상 변경 #
        self.title_color='SlateGray1'
        self.bg_color="gray65"
        self.box_color="gray90"


# ----------------------------------- 여긴 지도임 -------------------------------------------------

        # 지도 이미지 받아오게 하는 부분임....
        self.map_frame = tk.Frame(self.window, bg='white', width=1040, height=720)
        self.map_frame.place(x=240, y=0)

        self.thread = threading.Thread(target=self.test_thread, args=(self.map_frame, urls))
        self.thread.setDaemon(True)
        self.thread.start()


        self.mapButton = Button(self.window, text="지도",width=10, command=self.buttonMapUrlChange)
        self.collegeButton = Button(self.window, text="학교사이트",width=10, command=self.buttonCollegeUrlChange)

# ----------------------------------- 여긴 계열 선택 ----------------------------------------------\
        self.canvas.create_rectangle(0, 0, 240, 720, fill=self.bg_color)

        self.canvas.create_rectangle(0, 0, 240, 30, fill=self.title_color)
        self.canvas.create_text(120, 15, text="검색 조건", font=self.temp_font)

        self.canvas.create_rectangle(15, 45, 225, 75, fill=self.box_color, outline='white')
        self.brand = ["전체", "인문계열", "사회계열", "교육계열", "공학계열", "자연계열", "의약계열", "예체능계열"]
        self.str1 = StringVar()
        self.str1.trace('w', self.changeMajor)
        self.canvas.create_text(35, 60, text="계열",font=self.temp_font)
        self.line_select = Combobox(self.window, state='readonly', textvariable=self.str1, values=self.brand)
        self.line_select.place(x=55, y=50)

# ----------------------------------- 여긴 학과 선택 ----------------------------------------------
        self.canvas.create_rectangle(15, 85, 225, 115, fill=self.box_color, outline='white')
        self.canvas.create_text(35, 100, text="학과",font=self.temp_font)
        self.major_select = Combobox(self.window)
        self.major_select['value'] = self.line_list  # 학과를 xml로 로드해서 가져와야함 (리스트로 받는다)
        self.major_select.place(x=55, y=90)

#----------------------------------- 여긴 OO도 선택지역 ----------------------------------------------
        self.canvas.create_rectangle(15, 125, 225, 155, fill=self.box_color, outline='white')
        self.canvas.create_text(35, 140, text="지역",font=self.temp_font)
        self.area_select = Combobox(self.window)
        self.area_select['value'] = ("서울특별시", "인천광역시", "부산광역시", "대전광역시", "대구광역시", "광주광역시", "울산광역시", "경기도",
                                       "충청북도", "충청남도", "경상북도", "경상남도", "강원도", "전라북도", "전라남도", "제주도")
        self.area_select.place(x=55, y=130)


# ----------------------------------- 여긴 학과가 있는 대학 검색임 -------------------------------------------------
        self.show_resultButton = Button(self.window, text='검색', width=10, command=self.showSearchResult)
        self.show_resultButton.place(x=90, y=165)

        self.rst_major_list=[]  #학과 검색시 학과 코드가 여러개 나올 수 있기 때문에 다 받아오긴 하지만 하나만 사용합니다
        self.rst_university_list = []

# ----------------------------------- 여긴 대학교 선택 -------------------------------------------------
        self.canvas.create_rectangle(0, 200, 240, 230, fill=self.title_color)
        self.canvas.create_text(120, 215, text="검색 결과", font=self.temp_font)

        self.college_select = Listbox(self.window, selectmode='extended',bg=self.box_color)
        self.college_select.bind('<<ListboxSelect>>', self.click_item)
        #self.college_select.bind('<Button-1>', self.urlLoad)
        self.college_select.place(x=15, y=245, width=210, height=445)

# -----------------------------------  선택 학교 정보창 -------------------------------------------------
        #openUniversityInfoWindow 에서 배치
        self.university_rst_canvas = Canvas(self.window, width=240, height=295)
        self.university_rst_canvas.create_rectangle(0, 0, 240, 295, fill=self.bg_color, outline='white')
        self.university_rst_canvas.create_rectangle(15, 150, 225, 280, fill=self.box_color, outline='white')

        self.close_rst_infoButton = Button(self.window, text='X', width=3, command=self.closeInfoWindow)

        location_image = PhotoImage(file='resource\\location.png')
        globe_image=PhotoImage(file='resource\\globe.png')
        self.university_rst_canvas.create_image(25, 230, anchor=W, image=location_image)
        self.university_rst_canvas.create_image(25, 260, anchor=W, image=globe_image)



        self.university_rst_canvas.create_line(0, 135, 240, 135)

# -----------------------------------  선택 학과 정보창 -------------------------------------------------
        self.major_rst_canvas = Canvas(self.window, width=240, height=720)
        self.major_rst_canvas.create_rectangle(0, 0, 240, 720, fill=self.bg_color, outline='white')

        self.major_rst_canvas.create_rectangle(0, 0, 240, 30, fill=self.title_color)
        self.major_rst_canvas.create_text(120, 15, text="학과 정보", font=self.temp_font)
        self.major_rst_canvas.create_rectangle(15,45, 225, 705, fill=self.box_color, outline='white')

        self.major_rst_canvas.create_line(25, 75, 215, 75,fill='gray80')
        self.major_rst_canvas.create_line(25, 255, 215, 255, fill='gray80')
        self.major_rst_canvas.create_line(25, 365, 215, 365, fill='gray80')
        self.major_rst_canvas.create_line(25, 485, 215, 485, fill='gray80')
        self.major_rst_canvas.create_line(25, 525, 215, 525, fill='gray80')
        #self.major_rst_canvas.create_line(25, 620, 215, 620, fill='gray80')

# ----------------------------------- 취업률 그래프 -----------------------------------
        self.major_rst_canvas.create_line(30, 590, 210, 590)
        self.major_rst_canvas.create_line(30, 590, 30, 600)  # 0
        self.major_rst_canvas.create_line(75, 590, 75, 600)  # 25
        self.major_rst_canvas.create_line(120, 590, 120, 600)  # 50
        self.major_rst_canvas.create_line(165, 590, 165, 600)  # 75
        self.major_rst_canvas.create_line(210, 590, 210, 600)  # 100

        self.temp_mini_font = font.Font(size=8, family='italic')
        self.major_rst_canvas.create_text(30, 605, text="0", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(75, 605, text="25", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(120, 605, text="50", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(165, 605, text="75", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(210, 605, text="100", anchor=N, font=self.temp_mini_font)

# ----------------------------------- 남녀 성비 그래프 -----------------------------------
        self.major_rst_canvas.create_line(30, 680, 210, 680)
        self.major_rst_canvas.create_line(30, 680, 30, 690)#0
        self.major_rst_canvas.create_line(75, 680, 75, 690)#25
        self.major_rst_canvas.create_line(120, 680, 120, 690)#50
        self.major_rst_canvas.create_line(165, 680, 165, 690)#75
        self.major_rst_canvas.create_line(210, 680, 210, 690)#100

        self.temp_mini_font = font.Font(size=8, family='italic')
        self.major_rst_canvas.create_text(30, 695, text="0", anchor=N,font=self.temp_mini_font)
        self.major_rst_canvas.create_text(75, 695, text="25", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(120, 695, text="50", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(165, 695, text="75", anchor=N, font=self.temp_mini_font)
        self.major_rst_canvas.create_text(210, 695, text="100", anchor=N, font=self.temp_mini_font)

#----------------------------------- 이메일 버튼 -------------------------------------------------

        self.gmail_image = PhotoImage(file='resource\\gmail.png')
        self.gmailButton = Button(self.window, image=self.gmail_image, width=10,command=self.sendmail)
        self.gmailButton.place(x=1225, y=0)

        self.canvas.create_line(240, 0, 240, 730)

        self.canvas.create_line(0, 200, 240,200)

        self.mapButton.place(x=1145, y=0)
        self.collegeButton.place(x=1145, y=24)

# ----------------------------------- 텔레그렘 -------------------------------------------------
        self.bot=TelegramBot.TelepotBot()

        self.window.mainloop()



    def click_item(self, event):
        selectedItem = self.college_select.curselection()
        if len(selectedItem) != 0:
            self.mail_college = ''
            self.load_college = self.rst_university_list[selectedItem[0]].getSchoolName()
            CrawlImg.crawl(self.rst_university_list[selectedItem[0]].getSchoolName())
            self.mail_college = self.rst_university_list[selectedItem[0]].getSchoolName()
            self.openInfoWindow(selectedItem[0])
        self.urlLoad()
            #self.showMap(selectedItem[0])

    def changeMajor(self, index, value, op):
        self.major_select['value'] = self.tem.getUniversiryInfo_line(self.brand[self.line_select.current()])

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


        self.rst_major_list.clear()
        self.rst_university_list.clear()
        self.rst_major_list, self.rst_university_list=self.tem.getUniversiryInfo(curr_line, curr_major, curr_area)
        print(self.rst_major_list, self.rst_university_list)
        k = self.college_select.size()
        for i in range(k):
            self.college_select.delete(i)

        for i in range(len(self.rst_university_list)):
            self.college_select.insert(i, self.rst_university_list[i].getSchoolName())

        self.closeUniversityInfoWindow()


    def openUniversityInfoWindow(self,index):
        self.university_rst_canvas.delete('school_img')
        self.school_image = PhotoImage(file='resource\\school_img.png')
        self.university_rst_canvas.create_image(0, 0, anchor=NW, image=self.school_image, tags='school_img')

        self.university_rst_canvas.delete('school_name')
        self.university_rst_canvas.delete('campus_name')
        self.university_rst_canvas.delete('area')
        self.university_rst_canvas.delete('school_URL')
        self.university_rst_canvas.create_text(50, 170, text=self.rst_university_list[index].getSchoolName(), font=self.temp_font, anchor=W, tags='school_name')
        self.university_rst_canvas.create_text(50, 200, text=self.rst_university_list[index].getCampusName(), font=self.temp_font, anchor=W, tags='campus_name')
        self.university_rst_canvas.create_text(50, 230, text=self.rst_university_list[index].getArea(), font=self.temp_font, anchor=W, tags='area')
        self.university_rst_canvas.create_text(50, 260, text=self.rst_university_list[index].getSchoolURL(), font=self.temp_font, anchor=W, tags='school_URL')
        self.college_url = ''
        self.college_url = self.rst_university_list[index].getSchoolURL()
        if self.major_select.current() != -1:
            self.university_rst_canvas.place(x=480, y=0)
            self.close_rst_infoButton.place(x=690, y=0)
        else:
            self.university_rst_canvas.place(x=240, y=0)
            self.close_rst_infoButton.place(x=450, y=0)

    def closeUniversityInfoWindow(self):
        self.university_rst_canvas.place_forget()
        self.close_rst_infoButton.place_forget()

    def openMajorInfoWindow(self):
        self.major_rst_canvas.delete('major')
        self.major_rst_canvas.delete('department_title')
        self.major_rst_canvas.delete('department')
        self.major_rst_canvas.delete('main_subject_title')
        self.major_rst_canvas.delete('main_subject')
        self.major_rst_canvas.delete('job_title')
        self.major_rst_canvas.delete('job')
        self.major_rst_canvas.delete('employment')
        self.major_rst_canvas.delete('salary')
        self.major_rst_canvas.delete('gender')
        self.major_rst_canvas.delete('graph_gender_male')
        self.major_rst_canvas.delete('graph_gender_female')
        self.major_rst_canvas.delete('employment_perent')
        self.major_rst_canvas.delete('graph_gender_female')
        self.major_rst_canvas.delete('employment_percent_text')

        self.major_rst_canvas.create_text(25, 55, text="학과 이름: "+self.rst_major_list[0].getMajor(),font=self.temp_font, anchor=NW, width=190, tags='major')

        self.major_rst_canvas.create_text(25, 85, text="세부 학과: ",font=self.temp_font, anchor=NW, width=190, tags='department_title')
        self.major_rst_canvas.create_text(35, 105, text=self.rst_major_list[0].getDepartment(), font=self.temp_font, anchor=NW,width=190,tags='department')
        self.major_rst_canvas.create_text(25, 265, text="주요 과목: ", font=self.temp_font, anchor=NW, width=190,
                                          tags='main_subject_title')
        self.major_rst_canvas.create_text(35, 285, text=self.rst_major_list[0].getMainSubject(), font=self.temp_font,
                                          anchor=NW, width=190, tags='main_subject')
        self.major_rst_canvas.create_text(25, 375, text="연관 직업: ", font=self.temp_font, anchor=NW, width=190,
                                          tags='job_title')
        self.major_rst_canvas.create_text(35, 395, text=self.rst_major_list[0].getJob(), font=self.temp_font,
                                          anchor=NW, width=190, tags='job')
        self.major_rst_canvas.create_text(25, 495, text="평균 월급: " + self.rst_major_list[0].getSalary()+'만원',
                                          font=self.temp_font, anchor=NW, width=190, tags='salary')

        self.major_rst_canvas.create_text(25, 535, text="취업률: ", font=self.temp_font, anchor=NW, width=190, tags='employment')
        employment_perent=float(self.rst_major_list[0].getEmployment())
        self.major_rst_canvas.create_rectangle(30, 560, 30 + (210 - 30) / 100.0 * employment_perent, 580, fill='blue',
                                               tag='employment_perent')
        self.major_rst_canvas.create_text(30 + (210 - 30) / 100.0 * employment_perent + 10 , 560, text=str(employment_perent) + '%', font=self.temp_font, anchor=NW, width=190, tags='employment_percent_text')


        self.major_rst_canvas.create_text(25, 625, text="남녀 성비: ", font=self.temp_font, anchor=NW, width=190, tags='gender')
        male_percent = float(self.rst_major_list[0].getMalePercent())
        self.major_rst_canvas.create_rectangle(30, 650, 30+ (210-30)/100.0 * male_percent, 670, fill='blue',tag='graph_gender_male')
        self.major_rst_canvas.create_rectangle(30 + (210 - 30) / 100.0 * male_percent, 650, 210, 670, fill='red',tag='graph_gender_female')

        self.major_rst_canvas.place(x=240, y=0)

    def closeMajorInfoWindow(self):
        self.major_rst_canvas.place_forget()

    def openInfoWindow(self,index):
        self.openUniversityInfoWindow(index)
        if self.major_select.current() != -1:
            self.openMajorInfoWindow()

    def closeInfoWindow(self):
        self.closeUniversityInfoWindow()
        self.closeMajorInfoWindow()

    def test_thread(self, frame, url):
        global thread, urls

        sys.excepthook = cef.ExceptHook
        self.window_info = cef.WindowInfo(frame.winfo_id())
        self.window_info.SetAsChild(frame.winfo_id(), self.rect)
        cef.Initialize()
        self.browser = cef.CreateBrowserSync(self.window_info, url=url)
        cef.MessageLoop()

    def buttonMapUrlChange(self):
        self.browser.LoadUrl(self.map_url)

    def buttonCollegeUrlChange(self):
        self.browser.LoadUrl(self.college_url)

    def urlLoad(self):
        global urls
        url = 'https://map.naver.com/v5/search/' + str(self.load_college)
        self.map_url = url
        self.browser.StopLoad()
        self.now_url = url
        self.browser.LoadUrl(url)
        if url != urls:
            self.browser.StopLoad()
            urls = url
            self.browser.LoadUrl(url)




Interface()
cef.Shutdown()
CrawlImg.closeDriver()