# This code will run on the publisher camera, it will send video to cache server
# Lets import the libraries

import socket, cv2, pickle, struct
import imutils
import cv2


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Get the old state of the SO_REUSEADDR option
old_state = server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) 


# Enable the SO_REUSEADDR option
server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
new_state = server_socket.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
#print ("New sock state:",new_state)

                                     
host_name  = socket.gethostname()
host_ip = '192.168.43.101' # Enter the Drone IP address
print('HOST IP:',host_ip)
port = 9997
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

def start_video_stream():
	client_socket,addr = server_socket.accept()
	camera = True
	if camera == True:
		vid = cv2.VideoCapture(0)
	else:
		vid = cv2.VideoCapture('videos/boat.mp4')
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			while(vid.isOpened()):
				img,frame = vid.read()

				frame  = imutils.resize(frame,width=320)
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				cv2.imshow("TRANSMITTING TO CACHE SERVER",frame)
				key = cv2.waitKey(1) & 0xFF
				if key ==ord('q'):
					client_socket.close()
					break

	except Exception as e:
		print(f"CACHE SERVER {addr} DISCONNECTED")
		pass

while True:
	start_video_stream()

