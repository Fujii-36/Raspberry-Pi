import RPi.GPIO as GPIO
import webiopi
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SAVEDIR = '/home/pi/sensor'

# センサーピンの設定
GPIO_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

@webiopi.macro
def camera(no):
    #filename
    filename = SAVEDIR + '/camera_' + no + '.jpg'
    #taking photo
    command = 'fswebcam -r 320x240 -d /dev/video0 ' + filename
    #command = 'fswebcam -d /dev/video0 -r 320x240 image.jpg'  #写真を撮るためのコマンド
    os.system(command)
    #writing to disk cache
    os.system('sync')

@webiopi.macro
def CurrentTime():
    now = datetime.now()
    currenttime = (str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second))
    return currenttime

# メール設定
mail = ''
From_email = mail
To_email = mail  # 受信者のメールアドレス
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_pass = ''

# メール送信関数
def send_email():
    now = datetime.now()
    current_time =(str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second))
    message = "動きが検知されました.検知時間:" + current_time + "\n" + "http://172.22.34.102:8000/sensor.html"
    msg = MIMEText(message, 'plain')
    msg['Subject'] = '動きが検知されました。'
    msg['To'] = To_email
    msg['From'] = From_email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(From_email, smtp_pass)
        server.send_message(msg)
        server.quit()
        print("メールの送信に成功しました。メールを確認してください。")
    except Exception as e:
        print("メールの送信に失敗しました。:", str(e))

if __name__=='__main__':
    cnt1 = 0
    cnt2 = 0
    while True:
        # センサー感知
        if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
            cnt1 = cnt1 + 1
            cnt2 = 0
            print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "動きを感知しました。")
            if(cnt1 == 3):
                send_email()
        else:
            cnt2 = cnt2 + 1
            cnt1 = 0
            print(datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "なし")
            if(cnt2 == 6):
                break
        time.sleep(2)