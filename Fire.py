import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending

# To access xml file which includes positive and negative images of fire. (Trained images)
fire_cascade = cv2.CascadeClassifier('fire_detection.xml') 
                                                                    
# To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
vid = cv2.VideoCapture(0) 
runOnce = False 

def play_alarm_sound_function():
    # defined function to play alarm post fire detection using threading
    playsound.playsound('fire_Alarm.mp3',True) 
    # to play alarm # mp3 audio file is also provided with the code.
    print("Fire alarm end")


def send_mail_function():
    # defined function to send mail post fire detection using threading
    recipientmail = "201b052@juetguna.in" # recipients mail
    recipientmail = recipientmail.lower() # To lower case mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Senders mail ID and password
        server.login("anshikasoni909090@gmail.com", 'anshika@9889soni') 
        # recipients mail with mail message
        server.sendmail('201b052@juetguna.in', recipientmail, "Warning fire accident has been reported") 
        print("Alert mail sent sucesfully to {}".format(recipientmail))

        server.close()
        
    except Exception as e:
        print("error") #For error
		
while(True):

    Alarm_Status = False
    # Value in ret is True 
    # To read video frame
    ret, frame = vid.read() 
    # To convert frame into gray color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # to provide frame resolution
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    ## to highlight fire with square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() # To call mail thread
            runOnce = True

        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break