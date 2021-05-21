import http.client
import xml.etree.ElementTree as ET

class CarrerNetPassing:
    # 초기화 : 서버, Key / PlayerID, AccountID는 함수에서 받아옴.
    def __init__(self):
        self.__Server = "www.career.go.kr"
        self.__ApiKey = "fecd1f7f737539284f53c14621096584"

    def getUniversiryInfo(self, line_to_find, major_to_find, region_to_find): #매개변수는 string으로 전달
        rst_university_list = []

        conn = http.client.HTTPConnection(self.__Server)
        URL = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=fecd1f7f737539284f53c14621096584&svcType=api&svcCode=MAJOR&contentType=xml&gubun=univ_list"
        if (line_to_find=='' ) and (major_to_find != ''): #계열 미선택시 학과 선택 불가능
            pass
        else:
            i_line_to_find=0
            if line_to_find=='인문계열':
                i_line_to_find=100391
            elif line_to_find=='사회계열':
                i_line_to_find = 100392
            elif line_to_find == '교육계열':
                i_line_to_find = 100393
            elif line_to_find == '공학계열':
                i_line_to_find = 100394
            elif line_to_find == '자연계열':
                i_line_to_find = 100395
            elif line_to_find == '의약계열':
                i_line_to_find = 100396
            elif line_to_find == '예체능계열':
                i_line_to_find = 100397
            URL += "&subject=" + str(i_line_to_find)

            conn.request("GET", URL)
            rq = conn.getresponse()
            strXml = rq.read().decode('utf-8')
            #print(strXml)

            major_seq_list = []
            tree = ET.ElementTree(ET.fromstring(strXml))
            universityElements = tree.iter("content")  # return list type
            # 학과 검색시 ( 계열, 지역 상관없이 무조건 )

            # 학과가 해당하는 학과코드를 탐색
            # (한 학과가 두 개의 학과코드에 포함되어 있는 경우가 있음)
            for university in universityElements:
                major_list = university.find("facilName")
                for major in major_list.text.split(','):
                    if (major_to_find != '') and (major != major_to_find):
                        continue
                    major_seq = university.find("majorSeq").text
                    major_seq_list.append(major_seq)
                    print(major)
                    print("major_seq: ", major_seq)



            # 탐색한 학과코드로 재요청
            rst_university_name_list = []
            result = []
            for i in major_seq_list:
                for j in self.getUniversiryInfoByMajorSeq(i):
                    # 학교가 중복으로 나올 수 있으므로 학교 이름으로 중복 방지 ( 타 캠퍼스는 다른 학교로 취급)
                    if [j.find("schoolName").text, j.find("campus_nm").text] not in rst_university_name_list:
                        if (region_to_find != '')and (j.find('area').text != region_to_find):  # 지역 검색시
                            continue
                        rst_university_list.append(j)
                        rst_university_name_list.append([j.find("schoolName").text, j.find("campus_nm").text])

            for i in rst_university_list:
                print()
                print(i.find("area").text)
                print(i.find("schoolURL").text)
                print(i.find("campus_nm").text)
                print(i.find("schoolName").text)
                print()
                result.append(i.find("schoolName").text)

        print(result)
        return result




    def getUniversiryInfoByMajorSeq(self, major_seq):  #getUniversiryInfo함수 내에서만 사용  # int로 매개변수 전달
        rst_university_list=[]
        conn = http.client.HTTPConnection(self.__Server)
        base_URL = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=fecd1f7f737539284f53c14621096584&svcType=api&svcCode=MAJOR_VIEW&contentType=xml&gubun=univ_list&majorSeq="
        URL = base_URL + str(major_seq)

        conn.request("GET", URL)
        rq = conn.getresponse()
        strXml = rq.read().decode('utf-8')
        #print(strXml)

        tree = ET.ElementTree(ET.fromstring(strXml))
        universityElements = tree.iter("university")
        for university_list in universityElements:
            for university in university_list.iter("content"):
                rst_university_list.append(university)
                # 학교 이름 출력 테스트 코드
                #print(university.find("schoolName").text)

        return rst_university_list  # Element의 list를 return





    def getUniversiryInfo_line(self, line): # 여기서 계열 선택시 xml 로드함
        conn = http.client.HTTPConnection(self.__Server)
        self.str = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=fecd1f7f737539284f53c14621096584&svcType=api&svcCode=MAJOR&contentType=xml&gubun=univ_list"
        if line == 0:
            conn.request("GET", self.str)
        else:
            line += 100390
            conn.request("GET", self.str+"&subject="+str(line))

        rq = conn.getresponse()
        result = rq.read().decode('utf-8')
        #print(result)
        return result



    def getRegionInfo(self, region):
        pass


CarrerNetPassing()