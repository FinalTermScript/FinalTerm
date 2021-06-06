import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, copy
from email.mime.image import MIMEImage
from string import Template


def email_send(from_email, to_email, title='', content=''):

    if from_email and to_email :
        print('이메일 전송')
        smtp = smtplib.SMTP('smtp.gmail.com', 25)
        smtp.ehlo()  # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('아이디', '비밀번호')

        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(content, "html", _charset="utf8"))
        msg['Subject'] = title
        msg['To'] = to_email

        # (보내는메일, 받는메일, 전송내용)
        smtp.sendmail(from_email, to_email, msg.as_string())
        smtp.quit()


class EmailHTMLImageContent:
    """e메일에 담길 이미지가 포함된 컨텐츠"""

    def __init__(self, str_subject, str_image_file_name, str_cid_name, template, template_params):
        """이미지파일(str_image_file_name), 컨텐츠ID(str_cid_name)사용된 string template과 딕셔너리형 template_params받아 MIME 메시지를 만든다"""
        assert isinstance(template, Template)
        assert isinstance(template_params, dict)
        self.msg = MIMEMultipart()

        # e메일 제목을 설정한다
        self.msg['Subject'] = str_subject  # e메일 제목을 설정한다

        # e메일 본문을 설정한다
        str_msg = template.safe_substitute(**template_params)  # ${변수} 치환하며 문자열 만든다
        mime_msg = MIMEText(str_msg, 'html')  # MIME HTML 문자열을 만든다
        self.msg.attach(mime_msg)

        # e메일 본문에 이미지를 임베딩한다
        assert template.template.find("cid:" + str_cid_name) >= 0, 'template must have cid for embedded image.'
        assert os.path.isfile(str_image_file_name), 'image file does not exist.'
        with open(str_image_file_name, 'rb') as img_file:
            mime_img = MIMEImage(img_file.read())
            mime_img.add_header('Content-ID', '<' + str_cid_name + '>')
        self.msg.attach(mime_img)

    def get_message(self, str_from_email_addr, str_to_eamil_addrs):
        """발신자, 수신자리스트를 이용하여 보낼메시지를 만든다 """
        mm = copy.deepcopy(self.msg)
        mm['From'] = str_from_email_addr  # 발신자
        mm['To'] = ",".join(str_to_eamil_addrs)  # 수신자리스트
        return mm


class EmailSender:
    """e메일 발송자"""

    def __init__(self, str_host, num_port=25):
        """호스트와 포트번호로 SMTP로 연결한다 """
        self.str_host = str_host
        self.num_port = num_port
        self.ss = smtplib.SMTP(host=str_host, port=num_port)
        # SMTP인증이 필요하면 아래 주석을 해제하세요.
        self.ss.starttls()
        self.ss.login('kwb010712@gmail.com', 'q1w2e3r411!!') # 메일서버에 연결한 계정과 비밀번호

    def send_message(self, emailContent, str_from_email_addr, str_to_eamil_addrs):
        """e메일을 발송한다 """
        cc = emailContent.get_message(str_from_email_addr, str_to_eamil_addrs)
        self.ss.send_message(cc, from_addr=str_from_email_addr, to_addrs=str_to_eamil_addrs)
        del cc

def MakeConcept(college_name, RST, url):
    str_subject = '요청하신 대학 정보 입니다. with FLY'
    template = Template("<html>:"
                                "<head></head>"
                                "<body>"
                                    "<img src=""cid:my_image1""><br>"
                                    "학교 : "+str(college_name)+"<br>"
                                    "학교 사이트 :"+str(url)+"<br>"
                                    "학과 이름 :"+str(RST.getMajor())+"<br>"
                                    "세부 학과 :"+str(RST.getDepartment())+"<br>"
                                    "주요 과목 :"+str(RST.getMainSubject())+"<br>"
                                    "연관 직업 :"+str(RST.getJob())+"<br>"
                                    "취업률 :"+str(RST.getEmployment())+"<br>"
                                    "평균 월급 :"+str(RST.getSalary())+"<br>"
                                "</body>"
                            "</html>")
    template_params = {'NAME': 'Son'}
    str_image_file_name = 'resource\\school_img.png'
    str_cid_name = 'my_image1'
    emailHTMLImageContent = EmailHTMLImageContent(str_subject, str_image_file_name, str_cid_name, template, template_params)

    str_from_email_addr = 'kwb010712@gmail.com'  # 발신자
    str_to_email_addrs = 'kwb010712@naver.com' # 수신자리스트
    Tp = EmailSender("smtp.gmail.com")
    Tp.send_message(emailHTMLImageContent, str_from_email_addr, str_to_email_addrs)
