import Connect
from tkinter import *
from tkinter import font
from tkinter.ttk import *
import xml.etree.ElementTree as ET
import folium
import googlemaps

import urllib.request
import requests
from PIL import Image
from io import BytesIO




class Interface():
    line_list = []
    college_list = []
    campus_name = []
    #country_list = []
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

        self.bgimage = PhotoImage(file='resource\\bg.png') #<- 이미지를 마음에 드는걸로 바꾸면됨 :)
        self.canvas = Canvas(self.window, width=1280, height=720)
        self.canvas.create_image(0,0,anchor=NW, image=self.bgimage)
        self.canvas.pack()


        self.canvas.create_line(300, 0, 300, 730)
        self.canvas.create_line(0, 250, 300, 250)
        #self.canvas.create_line(0, 350, 300, 350)

        self.canvas.create_line(500, 0, 500, 730)
        self.canvas.create_line(300, 150, 500, 150)

        self.canvas.create_line(300, 400, 500, 400)

        self.temp_font=font.Font(size=10,weight='bold', family='Consolas')
# ----------------------------------- 여긴 계열 선택 ----------------------------------------------\
        self.brand = ["전체", "인문계열", "사회계열", "교육계열", "공학계열", "자연계열", "의약계열", "예체능계열"]
        self.str1 = StringVar()
        self.str1.trace('w', self.changeMajor)
        self.canvas.create_text(40, 40, text="계열",font=self.temp_font)
        self.line_select = Combobox(self.window, state='readonly', textvariable=self.str1, values=self.brand)
        self.line_select.place(x=100, y=30)

# ----------------------------------- 여긴 학과 선택 ----------------------------------------------
        self.canvas.create_text(40, 80, text="학과",font=self.temp_font)
        self.str2 = StringVar()
        self.major_select = Combobox(self.window, state='readonly', textvariable=self.str2, value=self.line_list)
        self.major_select['value'] = self.line_list  # 학과를 xml로 로드해서 가져와야함 (리스트로 받는다)
        self.major_select.place(x=100, y=70)

#----------------------------------- 여긴 OO도 선택지역 ----------------------------------------------
        self.canvas.create_text(40, 120, text="지역-도",font=self.temp_font)
        self.area_select = Combobox(self.window)
        self.area_select['value'] = ("서울특별시", "인천광역시", "부산광역시", "대전광역시", "대구광역시", "광주광역시", "울산광역시", "경기도",
                                       "충청북도", "충청남도", "경상북도", "경상남도", "강원도", "전라북도", "전라남도", "제주도")
        self.area_select.place(x=100, y=110)

#----------------------------------- 여긴 OO시 선택지역 ---------------------------------------------
        self.canvas.create_text(40, 160, text="지역-시",font=self.temp_font)
        self.country_select = Combobox(self.window)
        self.country_select['value'] = None
        self.country_select.place(x=100, y=150)



#----------------------------------- 여긴 지도임 -------------------------------------------------

        # 지도 이미지 받아오게 하는 부분임....
        largura = 640
        alturaplus = 640
        final = Image.new("RGB", (largura, alturaplus))

        # 마지막 markers 만 표시됨
        # 세개의 marker 모두 표시됨.
        urlparams = urllib.parse.urlencode({'center': '한국산업기술대학교',
                                            'zoom': '16',
                                            'size': '%dx%d' % (1280, 1280),
                                            'maptype': 'ROADMAP',
                                            'markers': 'color:blue|label:S|37.3402849,126.7335076',
                                            'key': self.__key})
        url = 'https://maps.googleapis.com/maps/api/staticmap?' + urlparams

        r = requests.get(url)
        im = Image.open(BytesIO(r.content))
        final.paste(im)
        final.save("map.png", "png")

        image1 = Image.open('map.png')
        image1 = image1.resize((780,720))
        image1.save("map.png", "png")
        self.mapdata = PhotoImage(file='map.png')

        self.map_canvas = Canvas(self.window, width=780, height=720)
        self.map_canvas.create_image(0, 0, anchor=NW, image=self.mapdata, tags='map')
        self.map_canvas.place(x=500, y=0)


#----------------------------------- 이메일 버튼 -------------------------------------------------

        self.gmail_image = PhotoImage(file='resource\\gmail.png')
        self.gmailButton = Button(self.window, image=self.gmail_image, width=10,command=self.sendmail)
        self.gmailButton.place(x=1225, y=0)

# ----------------------------------- 여긴 학과가 있는 대학 검색임 -------------------------------------------------

        self.show_resultButton=Button(self.window,text='검색', width=10, command=self.showResult)
        self.show_resultButton.place(x=180, y=200)

        # 계열, 학과 탐색 예시 코드
        # 계열 및 학과가 완벽히 일치해야 검색이 가능합니다
        #self.tem.getUniversiryInfo('예체능계열','광고디자인과',"제주특별자치도")

# ----------------------------------- 여긴 대학교 선택 -------------------------------------------------
        self.college_select = Listbox(self.window, selectmode='extended')
        self.college_select.bind('<<ListboxSelect>>', self.click_item)
        self.college_select.place(x=0, y=250, width=300, height=480)

        self.window.mainloop()

    def click_item(self, event):
        selectedItem = self.college_select.curselection()
        if len(selectedItem) != 0:
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

    def showResult(self):
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
        self.college_list.clear()
        self.campus_name.clear()
        self.college_list, self.campus_name = self.tem.getUniversiryInfo(curr_line, curr_major, curr_area)
        k = self.college_select.size()
        for i in range(k):
            self.college_select.delete(i)

        for i in range(len(self.college_list)):
            self.college_select.insert(i, self.college_list[i])

        print(self.campus_name)

    def showMap(self, index):
        largura = 640
        alturaplus = 640
        final = Image.new("RGB", (largura, alturaplus))

        self.gmaps = googlemaps.Client(key=self.__key)
        geocode_result = self.gmaps.geocode(str(self.college_list[index]), language='ko')
        print(geocode_result)

        if len(geocode_result) != 0:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            addr = geocode_result[0]['formatted_address']
            urlparams = urllib.parse.urlencode({'center': self.college_list[index],
                                            'zoom': '16',
                                            'size': '%dx%d' % (1280, 1280),
                                            'maptype': 'ROADMAP',
                                            'markers': 'color:blue|label:S|' + str(lat) + "," + str(lng),
                                            'key': self.__key})
            url = 'https://maps.googleapis.com/maps/api/staticmap?' + urlparams

            r = requests.get(url)
            im = Image.open(BytesIO(r.content))
            final.paste(im)
            final.save("map.png", "png")

            image1 = Image.open('map.png')
            image1 = image1.resize((780, 720))
            image1.save("map.png", "png")
            self.mapdata = PhotoImage(file='map.png')
            self.map_canvas.delete('map')
            self.map_canvas.create_image(0, 0, anchor=NW, image=self.mapdata, tags='map')
            self.map_canvas.place(x=500, y=0)

            self.canvas.delete('college_info')
            self.canvas.create_text(400, 30, text=self.college_list[index], tags='college_info')
            self.canvas.create_text(400, 60, text=self.campus_name[index], tags='college_info')
            self.canvas.create_text(400, 100, anchor='center', width=180, text=addr, tags='college_info')
        else:
            pass

Interface()
