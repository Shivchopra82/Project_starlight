import speech_recognition as sr
import pyaudio
import pyttsx3
import pywhatkit
import pyjokes
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
from requests import get
import pyjokes
import pyautogui
from gnewsclient import gnewsclient
import operator
from pywikihow import search_wikihow
import psutil
import speedtest
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from ui_starlight import Ui_Starlight
import screen_brightness_control as sbc
import PyQt5.sip



#-------------------------------------------------nititalizing audio engine--------------------------------------------#
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 210)
########################################################################################################################


#----------------------------------------------defining the speak feature----------------------------------------------#
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
########################################################################################################################

#--------------------------------------------------MAIN FUNCTIONS------------------------------------------------------#
def wishme():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak('Good morning sir')
        print('Starlight: Good morning sir')

    elif hour>=12 and hour<16:
        speak('Good afternoon sir')
        print('Starlight: Good afternoon sir')

    else:
        speak('Good evening sir ')
        print('Starlight: Good evening sir')

    print('Starlight: I am starlight.')
    speak('I am starlight.')
    print('Starlight:  How can I help you?')
    speak(' How can I help you?')


def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)


def rand(i):
    return(random.randint(0,i))


def tell_jokes():
    joke = pyjokes.get_joke('en', 'neutral')
    speak(joke)
    print('Starlight: should i tell you one more...!!!')
    speak('should I tell you one more')
    command = take_command()
    if 'no' in command:
        print('Starlight: OK')
        speak('ok')
        repeat()
    elif ('yes' in command) or ('more' in command):
        print('Starlight: ok here is another one')
        speak('ok here is another one')
        tell_jokes()


def fetch_news(loc, top):

    client = gnewsclient.NewsClient(language='english',
                                    location=loc,
                                    topic=top,
                                    max_results=10)

    news_list = client.get_news()

    i = 1
    for item in news_list:
        n = item['title']
        n =n.split('-')
        n = n[0]
        print(f"Headline {i}: {n}")
        speak(n)
        print("")
        i += 1
########################################################################################################################


#-----------------------------------------------------MAIN THREAD------------------------------------------------------#


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.executing()



    #------------------------------------------------------TAKE COMMAND----------------------------------------------------#
    def take_command(self):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Starlight is listening...")
            listener.pause_threshold = 1
            voice = listener.listen(source, timeout=4,  phrase_time_limit=7)
        try:
            print('Recognizing...')
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            if 'starlight' in command:
                command = command.replace('starlight', '')

        except Exception as e :
            print('Starlight: Sorry sir I cannot understand')
            speak('sorry sir I cannot understand')
            repeat()
            pass
        return command
    ########################################################################################################################


    #--------------------------------------------INITIALIZING STARLIGHT PROGRAM---------------------------------------------#
    def run_starlight(self):
        wishme()
        self.main()


    def repeat(self):
        print('Starlight: Anything else you want sir')
        speak('Anything else you want sir')
        self.main()
    ########################################################################################################################


    #--------------------------------------------------STARLIGHT SKELETON--------------------------------------------------#
    def main(self):
        self.command = self.take_command()

        if ('play music' in self.command) or ('play some music' in self.command) or ('play songs' in self.command) or ('play song' in self.command):
            music_dir = 'F:\\songs'
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            speak('playing')
            os.startfile(os.path.join(music_dir, rd))


        elif ('play'in self.command) or ('play video of' in self.command):
            self.command = self.command.replace('play video of', '')
            self.command = self.command.replace('play', '')
            self.command = self.command.replace('on youtube', '')
            # print(self.command)
            speak('playing')
            print('playing' + self.command )
            pywhatkit.playonyt(self.command)


        elif 'wikipedia' in self.command:
            try:
                self.command = self.command.replace('wikipedia', '')
                self.command = self.command.replace('search', '')
                speak('searching wikipedia')
                info = wikipedia.summary(self.command, 2)
                print(info)
                speak(info)
                self.repeat()
            except Exception as e:
                print('Starlight: sir there is some error in searching the wikipedia')
                speak('sir there is some error in searching the wikipedia')
                self.repeat()


        elif 'who is' in self.command:
            try:
                search = self.command.replace('who is', '')
                info = wikipedia.summary(search, 2)
                speak('I found something on wikipedia')
                print(info)
                speak(info)
                self.repeat()
            except Exception as e:
                print("Starlight: Sir i don't know about this")
                speak('Sir i dont know about this ')
                self.repeat()



        elif 'time' in self.command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak('The time is' + time)
            self.repeat()


        elif ('day is today' in self.command) or ('day today' in self.command):
            tellDay()
            self.repeat()


        elif ('calculation' in self.command) or ('calculate' in self.command):
            print('Starlight: Ok sir what you want to calculate, Example 5 plus 5')
            speak('ok sir what you want to calculate, Example 5 plus 5')
            self.query = self.take_command()
            self.query = self.query.replace('calculate', '')
            self.query = self.query.replace('evaluate', '')
            self.query = self.query.replace('solve', '')
            def identify_operator_fn(op):

                return {
                    '+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    'divide' : operator.__truediv__,
                    'divided' : operator.__truediv__,
                    '/': operator.__truediv__
                    }[op]
            def evaluate_expression(var_1, operator, var_2):
                var_1, var_2 = int(var_1), int(var_2)
                return identify_operator_fn(operator)(var_1, var_2)
            try:
                print(f'Starlight: Your answer is: {evaluate_expression(*(query.split()))}')
                speak(evaluate_expression(*(query.split())))
            except:
                if ('divided' in query) or ('divide'in query):
                    query = query.split()
                    var_1 = query[0]
                    var_2 = query[-1]
                    ans = operator.__truediv__(var_1, var_2)
                    print(ans)
                else:
                    pass
            self.repeat()


    ########################################################################################################################









    #--------------------------------------------------APPLICATION OPENING-------------------------------------------------#
        elif 'notepad' in self.command:
            speak('opening notepad')
            os.system('notepad.exe')
            self.repeat()


        elif 'word' in self.command:
            speak('opening ms word')
            path = "C:\\Program Files\\Microsoft Office\\root\Office16\\WINWORD.EXE"
            os.startfile(path)
            self.repeat()


        elif 'excel' in self.command:
            speak('opening ms excel')
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(path)
            self.repeat()


        elif ('power point' in self.command) or ('powerpoint' in self.command):
            speak('Opening power point ')
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
            os.startfile(path)
            self.repeat()


        elif ('open command prompt' in self.command) or ('open cmd' in self.command):
            speak('opening cmd')
            os.system("start cmd")
            self.repeat()


        elif 'open camera' in self.command:
            speak('opening camera')
            speak('press q for exit')
            vid = cv2.VideoCapture(0)
            while True:
                ret, frame = vid.read()
                cv2.imshow('webcam', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            vid.release()
            cv2.destroyAllWindows()


        ########################################################################################################################




        # -------------------------------------------------SEARCHING ON INTERNET------------------------------------------------#


        elif ('open youtube' in self.command) or ('youtube' in self.command):
            print('Starlight: opening')
            speak('opening')
            webbrowser.open('www.youtube.com')
            self.repeat()


        elif ('open facebook' in self.command) or ('facebook' in self.command):
            print('Starlight: opening')
            speak('Opening')
            webbrowser.open('www.facebook.com')
            self.repeat()


        elif ('open instagram' in  self.command) or ('instagram' in self.command):
            print('Starlight: opening')
            speak('Opening')
            webbrowser.open('www.instagram.com')
            self.repeat()


        elif ('open stack overflow' in self.command) or ('stack overflow' in self.command):
            print('Starlight: opening')
            speak('opening')
            webbrowser.open('www.stackoverflow.com')
            self.repeat()


        elif ('open google' in self.command) or ('google' in self.command):
            speak('sir what should I search on google')
            self.query_2 = self.take_command()
            self.query_2 = self.query_2.replace('search', '')
            webbrowser.open(self.query_2)
            self.repeat()


        elif ('open whatsapp' in self.command) or ('whatsapp' in self.command):
            print('Starlight: opening')
            speak('opening')
            webbrowser.open('www.whatsapp.com')
            self.repeat()


        elif ('open github' in self.command) or ('github' in self.command):
            print('Starlight: opening')
            speak('opening')
            webbrowser.open('www.github.com')
            self.repeat()


        elif ('open ignou' in self.command) or ('ignou website' in self.command):
            print('Starlight: opening ignou')
            speak('opening ignou')
            webbrowser.open('www.ignou.ac.in')
            self.repeat()


        elif ('in chrome' in self.command) or ('in google chrome' in self.command):
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('.com', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('of', '')
            web = 'www.'+self.command+'.com'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.com' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('.com', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('of', '')
            web = 'www.'+self.command+'.com'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.ac.in' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.ac.in', '')
            web = 'www.'+self.command+'.ac.in'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.nic.in' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.nic.in', '')
            web = 'www.'+self.command+'.nic.in'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.in' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.in', '')
            web = 'www.'+self.command+'.in'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.org' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.org', '')
            web = 'www.'+self.command+'.org'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.net' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.net', '')
            web = 'www.'+self.command+'.net'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.edu' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.edu', '')
            web = 'www.'+self.command+'.edu'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif ('open' in self.command) and ('.gov' in self.command):
            print('Starlight: opening')
            speak('opening')
            self.command = self.command.replace('in chrome', '')
            self.command = self.command.replace('of', '')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('website', '')
            self.command = self.command.replace('open', '')
            self.command = self.command.replace('.gov', '')
            web = 'www.'+self.command+'.gov'
            web = web.replace(' ', '')
            webbrowser.open(web)
            self.repeat()


        elif 'search' in self.command:
            print('Starlight: ok sir weight')
            speak('ok sir weight')
            self.command = self.command.replace('search', '')
            self.command = self.command.replace('about', '')
            self.command = self.command.replace('on google', '')
            webbrowser.open(self.command)
            self.repeat()


        elif ('jokes' in self.command) or ('joke' in self.command):
            tell_jokes()


        elif 'news' in self.command:
            print('Starlight: Sir of which country you want to listen the news')
            speak('sir of which country you want to listen the news')
            self.country = self.take_command()
            print('Starlight: And of which topic you want to listen the news')
            speak('And of which topic you want to listen the news')
            self.topic = self.take_command()
            print('Starlight: OK sir')
            speak('ok sir')
            print('Starlight: Please wait I am fetching the news')
            speak('please wait I am fetching the news')
            print('Starlight: This may take some time')
            speak('this may take some time')
            fetch_news(self.country, self.topic)
            self.repeat()


        elif 'headlines' in self.command:
            print('Starlight: Sir of which country you want to listen the headlines')
            speak('sir of which country you want to listen the headlines')
            self.country = self.take_command()
            print('Starlight: And of which topic you want to listen the headlines')
            speak('And of which topic you want to listen the headlines')
            self.topic = self.take_command()
            print('Starlight: OK sir')
            speak('ok sir')
            print('Starlight: Please wait I am fetching the headlines')
            speak('please wait I am fetching the headlines')
            print('Starlight: This may take some time')
            speak('this may take some time')
            fetch_news(self.country, self.topic)
            self.repeat()


        elif 'how to' in self.command:
            try:
                max_results = 1
                ans = search_wikihow(self.command, max_results)
                assert len(ans) == 1
                print(ans[0])
                # speak(ans[0])
                print(ans[0].summary)
                speak(ans[0].summary)
                self.repeat()
            except Exception as e:
                print("Starlight: Sorry sir I don/'t know about that")
                speak("Sorry sir I don't know about that")
                self.repeat()


        elif ('speed test' in self.command) or ('internet speed' in self.command) or ('network speed' in self.command):
            print('Starlight: ok sir,wait')
            speak('ok sir, wait')
            print('Starlight: Let me check')
            speak('Let me check')
            print('Starlight: This may take some time')
            speak('this may take sometime')
            print('running speed test.....')
            speed = speedtest.Speedtest()
            print("Starlight:Getting best server")
            speed.get_best_server()
            down = int(speed.download())
            up = int(speed.upload())
            d_speed_kb = int(down/1024)
            d_speed_mb = int(d_speed_kb/1024)
            u_speed_kb = int(up/1024)
            u_speed_mb = int(u_speed_kb/1024)
            print(f'Starlight: Your network has {d_speed_mb} megabits per second of download speed and {u_speed_mb} megabits per second of upload speed')
            speak(f'Your network has {d_speed_mb} megabits per second of download speed and {u_speed_mb} megabits per second of upload speed')
            self.repeat()





    ########################################################################################################################






    #------------------------------------LOGICS USING KEYBOARD BUTTONS BY AUTOGUI MODULE-----------------------------------#
        elif ('switch window' in self.command) or ('switch the window' in self.command):
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.sleep(1)
            pyautogui.keyUp('alt')
            self.repeat()


        elif 'screenshot' in self.command:
            print('Starlight: taking screenshot')
            speak('taking screeshot')
            im1 = pyautogui.screenshot()
            im1.save('my_screenshot.png')
            self.repeat()


        elif 'task manager' in self.command:
            print('Starlight: Opening task manager')
            speak('opening task manager')
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('shift')
            pyautogui.press('esc')
            pyautogui.keyUp('shift')
            pyautogui.keyUp('ctrl')
            self.repeat()


        elif 'desktop screen' in self.command:
            print('Starlight: As you wish sir')
            speak('as you wish sir')
            pyautogui.keyDown('win')
            pyautogui.press('d')
            pyautogui.keyUp('win')
            self.repeat()


        elif 'close this window' in self.command:
            print('Starlight: closing')
            speak('closing')
            pyautogui.keyDown('alt')
            pyautogui.press('f4')
            pyautogui.keyUp('alt')
            self.repeat()


        elif 'open settings' in self.command:
            print('Starlight: opening')
            speak('opening')
            pyautogui.keyDown('win')
            pyautogui.press('i')
            pyautogui.keyUp('win')
            self.repeat()


        elif ('notification area' in self.command) or ('action center' in self.command):
            print('Starlight: Opening')
            speak('opening')
            pyautogui.keyDown('win')
            pyautogui.press('a')
            pyautogui.keyUp('win')
            self.repeat()


        elif ('volume up' in self.command) or ('increase volume' in self.command) or ('increase sound' in self.command):
            print('Starlight: Sir how much you want to increase the volume')
            speak('Sir how much you want to increase the volume')
            self.level = self.take_command()
            self.level = self.level.replace('levels', '')
            self.level = self.level.replace('points', '')
            self.level = self.level.replace('level', '')
            self.level = self.level.replace('percent', '')
            self.level = self.level.replace('point', '')
            self.level = int(self.level)
            i = self.level // 2
            j = 0
            for j in range(0, i):
                pyautogui.press('volumeup')
            self.repeat()


        elif ('volume down' in self.command) or ('decrease volume' in self.command) or ('decrease sound' in self.command):
            print('Starlight: Sir how much you want to decrease the volume')
            speak('Sir how much you want to decrease the volume')
            self.level = self.take_command()
            self.level = self.level.replace('levels', '')
            self.level = self.level.replace('points', '')
            self.level = self.level.replace('level', '')
            self.level = self.level.replace('percent', '')
            self.level = self.level.replace('point', '')
            self.level = int(self.level)
            i = self.level // 2
            j = 0
            for j in range(0, i):
                pyautogui.press('volumedown')
            self.repeat()


        elif ('volume mute' in self.command) or ('mute volume' in self.command) or ('silent system' in self.command):
            print('Starlight: ok sir')
            speak('ok sir')
            pyautogui.press('volumemute')
            self.repeat()


        elif ('volume unmute' in self.command) or ('unmute volume' in self.command) or ('open system sound' in self.command) or ('unmute system' in self.command):
            print('Starlight: ok sir')
            speak('ok sir')
            pyautogui.press('volumeup')
            self.repeat()


    ########################################################################################################################



    #-----------------------------------------------SCREEN BRIGHTNESS CONTROL-----------------------------------------------#

        elif ('increase brightness' in self.command) or ('display brighter' in self.command):
            print('Starlight: sir how much should I increase brightness')
            speak('sir how much should I increase brightness')
            self.value = self.take_command()
            self.value = self.value.replace('increase', '')
            self.value = self.value.replace('percent', '')
            self.value = self.value.replace('%', '')
            bright = self.value.split()
            i = bright[0]
            i = '+'+i
            sbc.set_brightness(i)
            self.repeat()


        elif ('decrease brightness' in self.command) or ('display darker' in self.command) or ('display dim' in self.command):
            print('Starlight: sir how much should I reduce brightness')
            speak('sir how much should I reduce brightness')
            self.value = self.take_command()
            self.value = self.value.replace('decrease', '')
            self.value = self.value.replace('reduce', '')
            self.value = self.value.replace('percent', '')
            self.value = self.value.replace('%', '')
            dark = self.value.split()
            i = dark[0]
            i = '-'+i
            sbc.set_brightness(i)
            self.repeat()


        elif 'set brightness' in self.command:
            self.command = self.command.replace('%', '')
            self.command = self.command.replace('percent', '')
            value = self.command.split()
            i = value[-1]
            sbc.set_brightness(i)
            self.repeat()


    ########################################################################################################################


    #----------------------------------------------------LOGIC USING IP----------------------------------------------------#
        elif ('my ip' in self.command) or ('my device ip' in self.command):
            ip = get('https://api.ipify.org').text
            print(f'Starlight: your IP address is {ip}')
            speak(f'your IP address is {ip}')
            self.repeat()



        elif ('where we are' in self.command) or ('current location' in self.command) or ('my location' in self.command):
            print('Starlight: wait sir let me check')
            speak('wait sir let me check')
            try:
                ip = get('https://api.ipify.org').text
                url = 'https://get.geojs.io/v1/ip/geo/'+ip+'.json'
                geo_requests = get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                state = geo_data['region']
                country = geo_data['country']
                # latitude = geo_data['latitude']
                # longitude = geo_data['longitude']
                print(f'Starlight: Sir I am no sure, but I think we are somewhere near {city} of state {state} of country {country}')
                speak(f'Sir I am not sure, but I think we are somewhere near {city} of state {state} of country {country}')
                self.repeat()

            except Exception as e:
                print('Starlight: Sorry sir due to network issue I am not able to find the location where we are')
                speak('Sorry sir due to network issue I am not able to find the location where we are')
                self.repeat()
                pass


    ########################################################################################################################



    #------------------------------------------------BASIC SYSTEM FUNCTIONS------------------------------------------------#

        elif ('shutdown computer' in self.command) or ('shutdown pc' in self.command) or ('shutdown system' in self.command) or ('shut down pc' in self.command) or ('shut down system' in self.command):
            print('Starlight: system shutdown initiated')
            speak('system shutdown initiated in ten seconds')
            pywhatkit.shutdown(time=10)
            self.repeat()


        elif ('cancel shutdown' in self.command) or ('cancel shut down' in self.command):
            print('Starlight: cancelling shutdown')
            speak('cancelling shut down')
            pywhatkit.cancelShutdown()


        elif ('restart computer' in self.command) or ('restart pc' in self.command) or ('restart system' in self.command):
            print('Starlight: system restart initiated')
            speak('system restart initiated')
            os.system("shutdown /r /t 1")



        elif ('system on sleep' in self.command) or ('pc on sleep' in self.command) or ('computer on sleep' in self.command):
            print('Starlight: putting system on sleep')
            speak('putting system on sleep')
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


        elif ('how much power left' in self.command) or ('how much power we have' in self.command) or ('battery' in self.command) or ('how much power do we have' in self.command):
            battery = psutil.sensors_battery()
            percentage = battery.percent
            print(f'Starlight: Sir you have {percentage} percentage of battery left')
            speak(f'Sir you have {percentage} percentage of battery left')
            self.repeat()





    ########################################################################################################################


    #-------------------------------------------------INTERACTIVE ACTIONS--------------------------------------------------#

        elif  ('what you can do' in self.command) or ('what can you do' in self.command):
            print('Starlight: sir I am a personal aassistant created to help doing some basic and some tricky computer')
            speak('sir I am a personal aassistant created to help doing some basic and some tricky things on computer')
            print('Starlight: I can do basic things like searching google, playing music on youtube, playing songs, giving details on persons and things etc.')
            speak('I can do basic things like searching google, playing music on youtube, playing songs, giving details on persons and things etc.')
            print('Starlight: Also I can do some tricky things like finding your ip address, giving you location, telling you jokes, sending message on your behalf')
            speak('Also I can do some tricky things like finding your ip address, giving you location, telling you jokes, sending message on your behalf')
            print('Starlight: You can try yourself by giving a command')
            speak('you can try yourself by giving a command')
            self.main()


        elif ('no' in self.command) or ('go to sleep' in self.command) or ('take rest' in self.command) or ('shut up' in self.command) or ('nothing' in self.command):
            ans = ['ok', 'as you wish sir', 'fine', 'sure']
            reply = ans[rand(len(ans) - 1)]
            print(f'Starlight: {reply}')
            speak(reply)
            sleep_greet = ['you can call me when you need', 'ok sir I am going to sleep', 'sir, just say wake up when you need me']
            sleep_reply = sleep_greet[rand(len(sleep_greet)-1)]
            print(f'Starlight: {sleep_reply}')
            speak(sleep_reply)
            pass


        elif 'hello' in self.command:
            print('Assistant: Hello sir')
            speak('Hello sir')
            print('Assistant: How can I help you')
            speak('How can I help you')
            self.main()


        elif ('yes' in self.command):
            print('Starlight: ok,what you want sir')
            speak('ok, what you want sir')
            self.main()


    ########################################################################################################################

    #------------------------------------------OTHER VIRTUAL ASSISTANT KNOWLEDGE-------------------------------------------#

        elif 'alexa' in self.command:
            ans = ['Alexa is a great friend of mine', 'Alexa is the virtual assistant made by amazon', 'I met Alexa on the internet and I must say she is very intelligent', ' It seems like I had listen name Alexa berfore']
            reply = ans[rand(len(ans)-1)]
            print(f'Starlight: {reply}')
            speak(reply)
            self.repeat()


        elif 'siri' in self.command:
            ans = ['Siri is the virtual assistant created by apple', 'Siri is my best friend', 'I met Siri on the internet and we became friends']
            reply = ans[rand(len(ans)-1)]
            print(f'Starlight: {reply}')
            speak(reply)
            self.repeat()

        elif 'google assistant' in self.command:
            ans = ['Google assistant is the vitual assistant created for android operating system', 'Google assistant is one of the great friend of mine']
            reply = ans[rand(len(ans)-1)]
            print(f'Starlight: {reply}')
            speak(reply)


        elif ('close yourself' in self.command) in ('goodbye' in self.command):
            speak('ok sir')
            sys.exit()


        else:
            print('Starlight: Sir I am currently not able to help you with you request')
            speak('Sir I am currently not able to help you with you request')
            self.repeat()

    ########################################################################################################################

    def hot_word(self):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Starlight is listening...")
            listener.pause_threshold = 2
            voice = listener.listen(source, phrase_time_limit=7)
        try:
            print('Recognizing...')
            hot_key = listener.recognize_google(voice)
            hot_key = hot_key.lower()
            print(hot_key)
            if 'starlight' in hot_key:
                hot_key = hot_key.replace('starlight', '')

        except Exception as e:
            return 'none'
        return hot_key


    def executing(self):
        speak('Allow me to introduce myself, I am starlight. A system artificial intelligence and I am here to assist you in the variety of task as best I can. 24 hours a day 7 days a week. Callibrating all resouces, system is now fullu operational. Just say wakeup starlight and i will be there to help you')

        while True:
            self.key = self.hot_word()
            if ('wake up' in self.key) or ('get up' in self.key) or ('wakeup' in self.key) or ('getup' in self.key) or ('help me' in self.key):
                self.run_starlight()
            elif ('good bye' in self.key) or ('goodbye' in self.key) or('kill yourself' in self.key) or ('close yourself' in self.key):
                speak('goodbye sir take care')
                sys.exit()

startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Starlight()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("Screenshot (31).png")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        # self.u3i.movie = QtGui.QMovie("Screenshot (311).png")
        # self.ui.label_3.setMovie(self.ui.movie)
        # self.ui.movie.start()
        # self.ui.movie = QtGui.QMovie("Screenshot (311).png")
        # self.ui.label_4.setMovie(self.ui.movie)
        # self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)
        startExecution.start()

    def showtime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText(label_date)

app = QApplication(sys.argv)
main = Main()
main.show()
# exit(app.exec_())
sys.exit(app.exec_())















# run_starlight()

#------------------------------------------------------MAIN PROGRAM----------------------------------------------------#
# if __name__ == '__main__':
#     def hot_word():
#         listener = sr.Recognizer()
#         with sr.Microphone() as source:
#             listener.adjust_for_ambient_noise(source)
#             print("Starlight is listening...")
#             listener.pause_threshold = 2
#             voice = listener.listen(source, phrase_time_limit=7)
#         try:
#             print('Recognizing...')
#             hot_key = listener.recognize_google(voice)
#             hot_key = hot_key.lower()
#             print(hot_key)
#             if 'starlight' in hot_key:
#                 hot_key = hot_key.replace('starlight', '')
#
#         except Exception as e :
#             return 'none'
#         return hot_key
#     while True:
#         key = vVvccccccccccchot_word()
#         if ('wake up' in key) or ('get up' in key) or ('wakeup' in key) or ('getup' in key) or ('help me' in key):
#             run_starlight()
#         elif ('good bye' in key) or ('close yourself' in key):
#             sys.exit()

