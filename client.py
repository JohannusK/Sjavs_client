import socket
import time
import threading
import queue
import sys
import random
from termcolor import colored

from cards import show_my_cards, place
from drawer import drawScreen

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

cmd_queue = queue.Queue()  # Queue to hold commands

names = ["Per", "Pól", "Hans", "Jakki", "Stólur", "Top hat", "Tróndur", "Jóhannus", "Telda"]
myname = random.choice(names)
playerId = -1
keep_running = True  # Control flag for threads


def send(tosend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(tosend.encode('utf-8'))
        return s.recv(1024).decode('utf-8')


interval = 0
def get_updates():
    global keep_running, interval, myname, playerId
    while keep_running:
        # Check if there are commands in the queue to send
        try:
            tosend = cmd_queue.get_nowait()
        except queue.Empty:
            tosend = f"GU{playerId}"  # Default message to get updates
        response = send(f"P{playerId} {tosend}")
        if response != "No new updates.":
            if 'hand: ' in response:
                tmp = show_my_cards(response)
                print(tmp)
            elif 'Current Players:' in response:
                if "Turn" in response:
                    playerTurn = response.split("\n")[0][6:]
                todraw = drawScreen(myname, playerId)
                for i, player in enumerate(response.split('\n')[1:-1]):
                    thisPlayername = player.split(',')[0][6:]
                    if "ID" in player:
                        if float(player.split(',')[1][14:-5]) > 0.5:
                            symbol = colored("✖", 'red')
                        else:
                            symbol = colored("✔", 'green')
                        playerNameForPrint = thisPlayername
                        if "Turn" in response:
                            if int(playerTurn) == i:
                                playerNameForPrint = colored(thisPlayername, 'red')
                        playerNameForPrint = playerNameForPrint + (" " * (10 - len(thisPlayername)))
                        tmp = playerNameForPrint + "│ " + symbol + "   │"
                        todraw = place(tmp, todraw, 61, 3+int(player[3]))



                print(todraw)
                #print(response)
                #if "Turn" in response:
                #    print(playerTurn)
            else:
                print(response)
        interval += 1
        if interval == 10:
            interval = 0
            cmd_queue.put("list players")

        time.sleep(0.1)  # Polling interval


def handle_user_input():
    global keep_running
    while keep_running:
        user_input = input()
        cmd_queue.put(user_input)
        if user_input.lower() == 'exit':
            break


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1:
        myname = sys.argv[1]
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
    else:
        print("😭")
        keep_running = False


