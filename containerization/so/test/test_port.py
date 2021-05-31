import socket
import time
import pytest


config = [
          {'name': 'so_app', 'ip': 'localhost', 'port':'8080', 'enable': False},
          {'name': 'so_mongo', 'ip': 'localhost', 'port':'27017', 'enable': False},
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
