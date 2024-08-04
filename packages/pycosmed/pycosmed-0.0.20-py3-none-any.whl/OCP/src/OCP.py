import sys
from .Client import Client
from .Commander import Commander
# used to convert python dictionary to xml to be sent to omnia server
from dicttoxml2 import dicttoxml
from time import sleep # to create delay between different commands to allow the command to be executed properly
from functools import wraps


class OCP(Commander, Client):
    """Creates an OCP object that could be used to send commands and recieve response"""
    # Merge Commander and Client Class
    def __init__(self, root_node="OmniaXB", ip_address="127.0.0.1", port=44444):
        Client.__init__(self, host=ip_address, port=port)
        Commander.__init__(self, root_node=root_node)



if __name__ == "__main__":
    try:
        c = OCP(ip_address="127.0.0.1", port=44444, root_node="OmniaXB")
        c.connect()
        c.login("admin",'hcmlab')
        sleep(1)
        print(c.receive_response())
        sleep(5)
        print(c.enableRealTimeInfo())
        print(c.showOCPButton())
        for _ in range(100):
            print(c.receive_response())
    except:
        c.disconnect()
