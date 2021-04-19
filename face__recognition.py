import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
import cv2
import face_recognition
import os
import time
import pyttsx3
import speech_recognition as sr
from selenium import webdriver


list_of_images = []
encode_list = []
face_loc_list = []
list_of_Test_images = []
encode_Test_list = []
face_loc_Test_list = []

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            talk("Please say the password")
            listener.pause_threshold = 1
            listener.energy_threshold = 100000
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

    except:
        pass
    return command


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Face Recognition'
        self.left = 500
        self.top = 500
        self.width = 400
        self.height = 250
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('diaphragm.ico'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Store ID', self)
        button.setToolTip('This is an example button')
        button.move(150, 150)
        button.clicked.connect(self.StoreData)
        button2 = QPushButton('Recognise', self)
        button2.move(150, 70)
        button2.clicked.connect(self.Detect)
        self.show()

    @pyqtSlot()
    def StoreData(self):

        password = take_command()
        if password == "pacific":
            talk("Welcome")
            time.sleep(2)
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("Taking Data")
            img_counter = 0
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("Taking Data", frame)

                k = cv2.waitKey(1)
                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k % 256 == 32:
                    # SPACE pressed
                    img_name = "Data{}.png".format(img_counter)
                    cv2.imwrite(f"C:/Users/Snehi Kaushik/PycharmProjects/new_project/images/{img_name}", frame)
                    img_counter += 1

            cam.release()
            cv2.destroyAllWindows()
            time.sleep(2)
            talk("Thank you for your patience. Your id has been stored.")
        else:
            talk("Wrong password")
        Start()

    @pyqtSlot()
    def Detect(self):
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Detecting")
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Detection", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "capture{}.png".format(img_counter)
                cv2.imwrite(f"C:/Users/Snehi Kaushik/PycharmProjects/new_project/Test_images/{img_name}", frame)
                img_counter += 1

        cam.release()
        cv2.destroyAllWindows()
        Start()


def Start():
    base_path = 'C:/Users/Snehi Kaushik/PycharmProjects/new_project/images'
    for entry in os.listdir(base_path):
        if os.path.isfile(os.path.join(base_path, entry)):
            list_of_images.append(entry)

    print(list_of_images)

    for i in list_of_images:
        img1 = face_recognition.load_image_file(f'C:/Users/Snehi Kaushik/PycharmProjects/new_project/images/{i}')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        faceLoc = face_recognition.face_locations(img1)[0]
        encodeImg = face_recognition.face_encodings(img1)[0]
        face_loc_list.append(faceLoc)
        encode_list.append(encodeImg)
        cv2.rectangle(img1, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    base_path_2 = 'C:/Users/Snehi Kaushik/PycharmProjects/new_project/Test_images'
    for files in os.listdir(base_path_2):
        if os.path.isfile(os.path.join(base_path_2, files)):
            list_of_Test_images.append(files)

    print(list_of_Test_images)

    for i in list_of_Test_images:
        img_Test = face_recognition.load_image_file(
            f'C:/Users/Snehi Kaushik/PycharmProjects/new_project/Test_images/{i}')
        img_Test = cv2.cvtColor(img_Test, cv2.COLOR_BGR2RGB)
        faceLocTest = face_recognition.face_locations(img_Test)[0]
        encodeTest = face_recognition.face_encodings(img_Test)[0]
        face_loc_Test_list.append(faceLocTest)
        encode_Test_list.append(encodeTest)
        cv2.rectangle(img_Test, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

    # Checking weather your face matches with the data stored
    var = 0
    for i in encode_list:
        for x in encode_Test_list:
            results = face_recognition.compare_faces([i], x)
            facedis = face_recognition.face_distance([i], x)
            a = f'{results}'
            if a == '[True]':
                var = 1
                talk("Hey, your face has been recognised. welcome to your instagram account")
                chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe"

                driver = webdriver.Chrome(chrome_driver_path)

                driver.maximize_window()

                # reaching target website
                driver.get("https://www.instagram.com/")
                time.sleep(2)
                email = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
                email.send_keys("INSTAGRAM_USERNAME")

                password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
                password.send_keys("INSTAGRAM PASSWORD")

                login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')
                login.click()

    # If you are not identified
    if var == 0:
        talk("Sorry but you don't have the authority to enter ")
    # removing all the files from Test_images folder as they are of no use now
    for i in list_of_Test_images:
        os.chdir('C:/Users/Snehi Kaushik/PycharmProjects/new_project/Test_images')
        os.remove(f'{i}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())