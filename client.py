import socket
import time
import threading
import queue


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

cmd_queue = queue.Queue()  # Queue to hold commands

myname = "Trondur"
playerId = -1

def send(tosend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(tosend.encode('utf-8'))
        return s.recv(1024).decode('utf-8')


def get_updates():
    while True:
        # Check if there are commands in the queue to send
        try:
            tosend = cmd_queue.get_nowait()
        except queue.Empty:
            tosend = f"GU{playerId}"  # Default message to get updates
        response = send(tosend)
        if response != "W":
            print(response)
        time.sleep(1)  # Polling interval


def handle_user_input():
    while True:
        user_input = input()
        cmd_queue.put(user_input)
        if user_input.lower() == 'exit':
            break


# Start user input handling in a separate thread
input_thread = threading.Thread(target=handle_user_input)
input_thread.start()

response = send(f'Hallo, Eg eri {myname}')
print(f"Received {response}")

print(response[0])
if response[0] == 'P':
    print('yey!')
    time.sleep(0.5)
    playerId = response[1]
    update_thread = threading.Thread(target=get_updates)
    update_thread.start()
