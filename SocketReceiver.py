# import numpy
# import socket
# import _thread
#
#
# class SocketReceiver(object):
#     def __init__(self, controller):
#         self.controller = controller
#         self.signal = numpy.empty((0, self.controller.channels))
#         self.is_record = False
#         # Socket Establishment
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     def connect(self, host, port):
#         self.socket.connect((host, port))
#         self.socket.send(b'\r\n')
#         # Start Receiving In Parallel Thread
#         _thread.start_new_thread(self.receive, ())
#
#     def disconnect(self):
#         self.socket.close()
#
#     def start_record(self):
#         self.signal = numpy.empty((0, self.controller.channels))
#         self.is_record = True
#
#     def end_record(self):
#         self.is_record = False
#         # In Case Of Clash In The Middle of The if Condition
#         min_index = self.signal.shape[0] - 1
#         return self.signal[:min_index, :]
#
#     def receive(self):
#         while 1:
#             # Add Message To Previous Message
#             msg = self.socket.recv(1024).decode('utf-8')
#             # Split Message & Read First Part
#             msg = msg.split('\r\n')
#             data = numpy.fromstring(msg[0], dtype=numpy.float, sep=',')[2: -2]
#             if data.shape[0] == self.controller.channels and self.is_record:
#                 self.signal = numpy.append(self.signal, data.reshape(1, self.controller.channels), axis=0)
import time

import numpy
import socket
import _thread


class SocketReceiver:
    def __init__(self):
        # self.controller = controller
        print("GT")
        self.signal = numpy.empty((0, 14))
        # self.controller.channels))
        self.is_record = False
        # Socket Establishment
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))
        self.socket.send(b'\r\n')
        print("Connected")
        # Start Receiving In Parallel Thread
        _thread.start_new_thread(self.receive, ())

    def disconnect(self):
        self.socket.close()
        print("OK")

    def start_record(self):
        self.signal = numpy.empty((0, 14))
        # self.controller.channels))
        self.is_record = True

    def end_record(self):
        self.is_record = False
        # In Case Of Clash In The Middle of The if Condition
        min_index = self.signal.shape[0] - 1
        return self.signal[:min_index, :]

    def receive(self):
        while 1:
            # Add Message To Previous Message
            msg = self.socket.recv(1024).decode('utf-8')
            # Split Message & Read First Part
            msg = msg.split('\r\n')
            data = numpy.fromstring(msg[0], dtype=numpy.float, sep=',')[2: -2]
            if data.shape[0] == 14 and self.is_record:
                self.signal = numpy.append(self.signal, data.reshape(1, 14), axis=0)
            # print(data)


# s = SocketReceiver();
# s.connect('127.0.0.1', 54123)
# s.start_record()
# time.sleep(2)
# f = s.end_record()
# s.disconnect()
# print(f)
