  
import cv2
import numpy as np
import smtplib, ssl
import playsound
import threading

Alarm_Status = False
Email_Status = False
Fire_Reported = 0

def play_alarm_sound_function():
	while True:
		playsound.playsound('alarm.mp3',True)

def send_mail_function(receiver='dhanyamu55@gmail.com'):
        sender = 'xagent.amber@gmail.com'
        passwd = 'jpiupfucjtflepsd'

        context = ssl.create_default_context()

        server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=context)
        server.login(sender, passwd)
        message = f'Subject: Fire Detected\n\n We have detecetd unusual fire at Sadanam Kuamran College, Pathrippala..'
        try:
            server.sendmail(sender, receiver, message)
            print("Mail has send Successfully, Check your inbox!")
        except IndexError:
            print("Mail has not send due to unexpected issue. Please try again!")
        server.quit()


video = cv2.VideoCapture(0) # If you want to use webcam use Index like 0,1.
 
while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540)) 
 
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
 
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    
    no_red = cv2.countNonZero(mask)
    
    if int(no_red) > 15000:
        Fire_Reported = Fire_Reported + 1

    cv2.imshow("output", output)

    if Fire_Reported >= 1:
        if Alarm_Status == False:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True

        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
video.release()