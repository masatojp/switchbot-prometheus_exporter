#!/usr/bin/env python3

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
#from random import randrange
import time
from urllib.parse import parse_qs, urlparse
import threading

import json
import switchbot_sign

import json
import requests

from prometheus_client import start_http_server
from prometheus_client import Counter, Summary, Gauge, Enum

def data():

    while True:

        global humidity
        global temperature


        token = 'Switchbot_token' # copy and paste from the SwitchBot app V6.14 or later
        secret = 'Switchbot_secret' # copy and paste from the SwitchBot app V6.14 or later

        header = switchbot_sign.gensign(token, secret)
        # Get all device information in your switchbot hub
        #response_list = requests.get("https://api.switch-bot.com/v1.1/devices", headers=header)
        #devices  = json.loads(response_list.text)

        #print(devices)

        #机上温湿度計　取得
        response_desk_meter = requests.get("https://api.switch-bot.com/v1.1/devices/E92E62AE6867/status", headers=header)
        json_desk_meter      = json.loads(response_desk_meter.text)
        
        #print(json_desk_meter)

        temperature_desk    = json_desk_meter['body']['temperature']
        humidity_desk    = json_desk_meter['body']['humidity']
        
        #print(temperature_desk)
        #print(humidity_desk)


        #ベランダ温湿度計　取得
        #response_balcony_meter = requests.get("https://api.switch-bot.com/v1.1/devices/CD6140403915/status", headers=header)
        #json_balcony_meter      = json.loads(response_balcony_meter.text)
        
        #print(json_desk_meter)

        #temperature_balcony    = json_balcony_meter['body']['temperature']
        #humidity_balcony    = json_balcony_meter['body']['humidity']
        
        #print(temperature_balcony)
        #print(humidity_balcony)

        #鍵（上）　取得
        response_lock_upper = requests.get("https://api.switch-bot.com/v1.1/devices/C42E2A23CAF5/status", headers=header)
        json_lock_upper     = json.loads(response_lock_upper.text)
        
        print(json_lock_upper)

        lock_upper_lockState_text    = json_lock_upper['body']['lockState']
        lock_upper_doorState_text    = json_lock_upper['body']['doorState']
        
        print(lock_upper_lockState_text)
        print(lock_upper_doorState_text)

        
        #取得データの数値化（ロック状態）
        if lock_upper_lockState_text == "locked":
            lock_upper_lockState = 5
        elif lock_upper_lockState_text == "jammed":
            lock_upper_lockState = 4
        elif lock_upper_lockState_text == "locking":
            lock_upper_lockState = 3
        elif lock_upper_lockState_text == "unlocking":
            lock_upper_lockState = 2
        elif lock_upper_lockState_text == "unlocked":
            lock_upper_lockState = 1
        else:
            lock_upper_lockState = 0

        print(lock_upper_lockState)

        #取得データの数値化（ドア状態）
        if lock_upper_doorState_text == "closed":
            lock_upper_doorState = 2
        elif lock_upper_doorState_text == "opened":
            lock_upper_doorState = 1
        else:
            lock_upper_doorState = 0

        print(lock_upper_doorState)

        

        #鍵（下）　取得
        response_lock_lower = requests.get("https://api.switch-bot.com/v1.1/devices/D414B85C84DD/status", headers=header)
        json_lock_lower     = json.loads(response_lock_lower.text)
        
        print(json_lock_lower)

        lock_lower_lockState_text    = json_lock_lower['body']['lockState']
        lock_lower_doorState_text    = json_lock_lower['body']['doorState']
        
        print(lock_lower_lockState_text)
        print(lock_lower_doorState_text)

        #取得データの数値化（ロック状態）
        if lock_lower_lockState_text == "locked":
            lock_lower_lockState = 5
        elif lock_lower_lockState_text == "jammed":
            lock_lower_lockState = 4
        elif lock_lower_lockState_text == "locking":
            lock_lower_lockState = 3
        elif lock_lower_lockState_text == "unlocking":
            lock_lower_lockState = 2
        elif lock_lower_lockState_text == "unlocked":
            lock_lower_lockState = 1
        else:
            lock_lower_lockState = 0

        print(lock_lower_lockState)

        #取得データの数値化（ドア状態）
        if lock_lower_doorState_text == "closed":
            lock_lower_doorState = 2
        elif lock_lower_doorState_text == "opened":
            lock_lower_doorState = 1
        else:
            lock_lower_doorState = 0

        print(lock_lower_doorState)


        '''
        #SwitchBotAPI取得
        json_string = response.json()
        temperature = json.dumps(json_string["body"]["temperature"])
        humidity = json.dumps(json_string["body"]["humidity"])
        #デバッグ用print
        #print(humidity)
        #print(temperature)
        '''

        #prometheus用関数に設定
        humidity_gauge_desk.set(humidity_desk)
        temperature_gauge_desk.set(temperature_desk)

        #humidity_gauge_balcony.set(humidity_balcony)
        #temperature_gauge_balcony.set(temperature_balcony)

        lock_upper_lockState_gauge.set(lock_upper_lockState)
        lock_upper_doorState_gauge.set(lock_upper_doorState)

        lock_lower_lockState_gauge.set(lock_lower_lockState)
        lock_lower_doorState_gauge.set(lock_lower_doorState)

        #lock_upper_lockState_enum.state(lock_upper_lockState_text)
        #lock_upper_doorState_enum.state(lock_upper_doorState_text)

        #lock_lower_lockState_enum.state(lock_lower_lockState_text)
        #lock_lower_doorState_enum.state(lock_lower_doorState_text)
        
        time.sleep(17)
            
humidity_gauge_desk = Gauge('my_home_living_humidity_switchbot', 'My Home Living humidity by SwitchBot')
temperature_gauge_desk = Gauge('my_home_living_temperature_switchbot', 'My Home Living temperature by SwitchBot')

#humidity_gauge_balcony = Gauge('my_home_balcony_humidity_switchbot', 'My Home Balcony humidity by SwitchBot')
#temperature_gauge_balcony = Gauge('my_home_balcony_temperature_switchbot', 'My Home Balcony temperature by SwitchBot')

lock_upper_lockState_gauge = Gauge('my_home_lock_upper_lockstate_switchbot', 'My Home Lock Upper LockState by SwitchBot')
lock_upper_doorState_gauge = Gauge('my_home_lock_upper_doorstate_switchbot', 'My Home Lock Upper DoorState by SwitchBot')

lock_lower_lockState_gauge = Gauge('my_home_lock_lower_lockstate_switchbot', 'My Home Lock Lower LockState by SwitchBot')
lock_lower_doorState_gauge = Gauge('my_home_lock_lower_doorstate_switchbot', 'My Home Lock Lower DoorState by SwitchBot')

#lock_upper_lockState_enum = Enum('my_home_lock_upper_lockstate_switchbot', 'My Home Lock Upper LockState by SwitchBot',states=['locked', 'jammed', 'locking','unlocking', 'unlocked'])
#lock_upper_doorState_enum = Enum('my_home_lock_upper_doorstate_switchbot', 'My Home Lock Upper DoorState by SwitchBot',states=['closed', 'opened'])

#lock_lower_lockState_enum = Enum('my_home_lock_lower_lockstate_switchbot', 'My Home Lock Lower LockState by SwitchBot',states=['locked', 'jammed', 'locking','unlocking', 'unlocked'])
#lock_lower_doorState_enum = Enum('my_home_lock_lower_doorstate_switchbot', 'My Home Lock Lower DoorState by SwitchBot',states=['closed', 'opened'])

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path.endswith('/error'):
            raise Exception('Error')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Hello World!! from {self.path} as GET'.encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path.endswith('/error'):
            raise Exception('Error')

        content_length = int(self.headers['content-length'])
        body = self.rfile.read(content_length).decode('utf-8')

        print(f'body = {body}')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Hello World!! from {self.path} as POST'.encode('utf-8'))

if __name__ == '__main__':
    thread_1 = threading.Thread(target=data)
    thread_1.start()
    start_http_server(8000)

    with ThreadingHTTPServer(('0.0.0.0', 8080), MyHTTPRequestHandler) as server:
        print(f'[{datetime.now()}] Server startup.')
        server.serve_forever()
