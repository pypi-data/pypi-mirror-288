""" Screensharing : Python module for sharing/casting your screen with others in realtime with fast & accurate casting.
 Works best when connected to same network
Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md
"""
import cv2
from mss import mss
import pyautogui
import socket
import numpy as np
from colorama import Fore

print(f"{Fore.RED}-------------------------Thanks for using our product-----------------------{Fore.WHITE}")


class server:
    """
        Main class of server. Handles loading and sending
        the screen inside the selected window.

        :keyword host:
            host ip address from the sender side
        :param port:
            it contains the port number which is used for sending file,
            if not it uses port-8080 as a default
        :param noofconn:
            it stands for number of connections
            default value is 1
    """

    def __init__(self,host,port=8080,noofconn=1):
        self.host=host
        self.port=port
        self.noofconn=noofconn

    def create(self):
        self.create_server(self.port,self.noofconn)

    def create_server(self,port,noofconn):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Socket successfully created")
        host=socket.gethostname()
        print("host name ->", host)
        server.bind((host,port))
        server.listen(noofconn)
        print("waiting for connections ....")
        server_client,addr=server.accept()
        print(addr,"connected sucessfully")
        print("list of devices --> ",server_client)
        self.sending(server,server_client,self.noofconn)

    def sending(self,server,server_client,noofconn):
        with server_client:
            while True:
                scr_width, scr_height=pyautogui.size()
                bounding_box = {'top': 0, 'left': 0, 'width':scr_width, 'height':scr_height}
                sct=mss()
                sct_img = sct.grab(bounding_box)
                frame=np.array(sct_img)

                # Encode the frame as a JPEG
                _, buffer = cv2.imencode('.jpeg', frame)
                frame_data = buffer.tobytes()

                # Send the frame size
                frame_size = len(frame_data)
                server_client.sendall(frame_size.to_bytes(4, byteorder='big'))
                # Send the frame data
                server_client.sendall(frame_data)


class server_receive:
    """
        Main class of server_receive. Handles loading received frames in
        the window.
        :keyword host:
            host ip address or name as per sender
        :param port:
            it contains the port number which is used for sending file,
            type: interger
            if not it uses port-8000 as a default
        :param display:
            it stands for output to be displayed or not
            type: boolean
            default value is True
    """

    def __init__(self,host,port=8000,display=True):
        self.host=host
        self.port=port
        self.display=display

    def connect(self):
        self.connect_rec(self.host,self.port)

    def connect_rec(self,host,port):
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        print("Connected to the Host")
        self.Recei(client)

    def Recei(self,client):
        cv2.namedWindow("Screen Share", cv2.WINDOW_AUTOSIZE)
        while True:
            frame_size = client.recv(4)
            if not frame_size:
                break
            frame_size = int.from_bytes(frame_size, byteorder='big')
            # Receive the frame data
            frame_data=b''
            while len(frame_data) < frame_size:
                packet = client.recv(frame_size - len(frame_data))
                if not packet:
                    break
                frame_data += packet

            if not frame_data:
                break

            # Decode the frame data
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Adjust size if necessary

            # Display the frame
            cv2.imshow("Screen Share", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

