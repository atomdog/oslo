#0MQ Communication Library
import time
import zmq

def formConnection():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    return(socket)

def ZMQ_Send(pack):
    socket = formConnection()
    socket.send(pack)

def ZMQ_Recv():
    socket = formConnection()
    message = socket.recv()
    return(message)
