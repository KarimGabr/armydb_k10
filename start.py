import webbrowser
import time
import os
import threading


def open_browser ():
    url="http://localhost:8000/"
    #chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'
    #chrome = webbrowser.get(chrome_path)
    time.sleep(10)
    return webbrowser.open(url)

thread1 = threading.Thread(target=open_browser, name="thread1", args=())
thread1.start()
os.system("py manage.py runserver 0.0.0.0:8000")



