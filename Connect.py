import http.client


class CarrerNetPassing:
    # 초기화 : 서버, Key / PlayerID, AccountID는 함수에서 받아옴.
    def __init__(self):
        self.__Server = "www.career.go.kr"
        self.__ApiKey = "fecd1f7f737539284f53c14621096584"

    def getUniversiryInfo(self,region):
        conn = http.client.HTTPConnection(self.__Server)
        conn.request("GET", "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=fecd1f7f737539284f53c14621096584&svcType=api&svcCode=MAJOR&contentType=xml&gubun=univ_list&subject=100394")
        rq = conn.getresponse()
        print(rq.status, rq.reason)
        respond_body = rq.read()
        print(respond_body.decode('utf-8'))

    def getUniversiryInfo_line(self, line): # 여기서 계열 선택시 xml 로드함
        conn = http.client.HTTPConnection(self.__Server)
        self.str = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=fecd1f7f737539284f53c14621096584&svcType=api&svcCode=MAJOR&contentType=xml&gubun=univ_list"
        if line == 0:
            conn.request("GET", self.str)
        else:
            line += 100390
            conn.request("GET", self.str+"&subject="+str(line))

        rq = conn.getresponse()
        print(rq.status, rq.reason)
        result = rq.read().decode('utf-8')

        return result

    def getRegionInfo(self, region):
        pass


CarrerNetPassing()