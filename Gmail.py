import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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