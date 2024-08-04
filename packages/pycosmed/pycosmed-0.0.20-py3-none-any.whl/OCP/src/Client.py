import socket
from functools import wraps
import xmltodict


# to carry out the tcp connection and send and recieve data
class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        self.socket.close()

    def send_xml(self, xml_data):
        self.socket.sendall(xml_data)
        response = self.receive_response()
        return response

    @staticmethod
    def _receive_as_dict(recieve):
        """a decorator that return a list of messages"""
        @wraps(recieve)
        def func(self):
            response = recieve(self).split(
                '<?xml version="1.0" encoding="utf-8" standalone="no"?>')
            if response[0] == '':
                response.remove('')
            if len(response) == 0 :
                return []
            elif response[0] == 'TimeOUT':
                return []

            messages = []
            for message in response:
                try:
                    messages.append(xmltodict.parse(message))
                except Exception as E:
                    print("recieved:", response, "end")
                    print(E)
                    print(response)
            return messages
        return func

    @_receive_as_dict
    def receive_response(self):
        """Receives a response with one or more messsages"""
        response = b""
        try:
            while True:
                part = self.socket.recv(1024)
                response += part

                if len(part) < 1024:
                    break

        except TimeoutError:
            return "TimeOUT"
        return response.decode("utf-8")
