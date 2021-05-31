import socket
import time
import pytest


config = [
          {'name': 'rl_app', 'ip': 'localhost', 'port':'50000', 'enable': False},
          {'name': 'mtpwim', 'ip': 'localhost',  'port':'53000', 'enable': False},
          {'name': 'mtpwim1', 'ip': 'localhost',  'port':'51000', 'enable': False},
          {'name': 'mtpwim2', 'ip': 'localhost',  'port':'52000', 'enable': False},
          {'name': 'mtp_mysql', 'ip': 'localhost', 'port':'3306', 'enable': False},
          ]

timeout = 60 # seconds

class TestPorts:
    def testport(self):
        start = time.time()
        while time.time() - start < timeout:
            all_service_up = True
            for item in config:
                if item['enable'] == True:
                    continue

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((item['ip'],int(item['port'])))
                sock.close()
                if result == 0:
                   item['enable'] = True
                else:
                    all_service_up = False
            if all_service_up == True:
                break
            time.sleep(1)

        result = "OK"
        for item in config:
            if item['enable'] == True:
                continue
            else:
                result = "Problem"
                print ("Problem with service: " + item['name'] + " port: " + item['port'] + " is closed")
        if result == "OK":
            print ("OK")
        assert result == "OK"
