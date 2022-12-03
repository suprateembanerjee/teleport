import cv2
import numpy as np
import socket
import sys
import pickle
import picamera2
import time
import libcamera

camera = picamera2.Picamera2()
camera.configure(camera.create_video_configuration({'size':(640,480)}, transform=libcamera.Transform(vflip=True, hflip=True)))
encoder = picamera2.encoders.H264Encoder(1000000)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.1.22',8888))
    sock.listen()
    
    camera.encoder = encoder
    
    print('Before Accept')
    conn,addr = sock.accept()
    print('Accepted')
    
    stream = conn.makefile('wb')
    camera.encoder.output = picamera2.outputs.FileOutput(stream)
    camera.start_encoder()
    camera.start()
    while conn:
        pass

camera.stop()
camera.stop_encoder()
conn.close()
