import socket
import os
import webbrowser
import time
import threading

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def open_browser ():
    url= y
    #chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'
    #chrome = webbrowser.get(chrome_path)
    time.sleep(10)
    return webbrowser.open(url)



x= get_ip()
x= str(x)
print(x)
y= "http://"+ x + ":8000"
thread1 = threading.Thread(target=open_browser, name="thread1", args=())
thread1.start()

os.system("py manage.py runserver" + " " + x ) 
