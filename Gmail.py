import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"
senderAddr = 'kwb010712@gmail.com'
recipientAddr = 'kwb010712@naver.com'
def SetHost():
    pass

def reciptAddr(string):
    recipientAddr = string

def sendMessage(rst):
    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "원하시던 대학 학과 정보 입니다!"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("본인이메일적고테스트", "********")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

sendMessage(1)