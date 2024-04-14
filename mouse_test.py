from asciimatics.widgets import Frame, Layout, TextBox, Text
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.event import KeyboardEvent
from threading import Thread
from time import sleep
import socket
import queue
from cards import show_my_cards
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

cmd_queue = queue.Queue()  # Queue to hold commands

myname = "Trondur"
playerId = -1
keep_running = True  # Control flag for threads

def send(tosend):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(tosend.encode('utf-8'))
        return s.recv(1024).decode('utf-8')




class ScrollingFrame(Frame):
    def __init__(self, screen):
        super(ScrollingFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Scrolling Frame"
        )
        layout = Layout([4, 1], fill_frame=True)
        self.add_layout(layout)

        # Create the TextBox, specifying the height to fill the frame.
        self._scrolling_text_box = TextBox(screen.height // 2, as_string=True)
        self._scrolling_text_box2 = TextBox(screen.height, as_string=True)
        layout.add_widget(self._scrolling_text_box, 1)
        self.input_box = Text(label="Enter Command:", name="input_text")
        layout.add_widget(self.input_box, 0)
        layout.add_widget(self._scrolling_text_box2, 0)

        # Finalize the layout and reset the Frame
        self.fix()


    def update_scroll_content(self, new_content):
        # Set the TextBox value, which should auto-scroll if needed.
        self._scrolling_text_box.value = new_content

    def add_line(self, line):
        # Update the content with the new line
        new_content = self._scrolling_text_box.value + "\n" + str(line)
        self.update_scroll_content(new_content)

    def on_timer(self):
        # Get the last line number and add the next line.
        last_line = self._scrolling_text_box.value.split('\n')[-1]
        next_line = int(last_line) + 1 if last_line.isdigit() else 1
        self.add_line(next_line)
        # Restart the timer
        self.set_timer(1)

    def process_event(self, event):
        # Override the method to handle Enter key within the input box
        if isinstance(event, KeyboardEvent):
            if event.key_code in [10, 13]:  # Enter key
                # Call your function with the input text
                self.handle_command(self.input_box.value)
                # Clear the input box
                self.input_box.value = ""
                # Optional: Move to the next scene or perform other actions
                #raise NextScene("Main")
        # Pass other events to the base class
        return super(ScrollingFrame, self).process_event(event)

    def handle_command(self, command):
        # Handle the command here
        #print(f"Command entered: {command}")
        cmd_queue.put(command)
        # Example function call
        # process_command(command)


def demo(screen, old_scene):
    scenes = [Scene([ScrollingFrame(screen)], -1, name="Main")]
    screen.play(scenes, stop_on_resize=True, start_scene=old_scene, allow_int=True)


def updater(frame):
    counter = 1
    while True:
        frame.add_line(counter)
        counter += 1
        sleep(1)


def get_updates(frame):
    global keep_running
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
                frame.add_line(tmp)
            else:
                frame.add_line(response)
        sleep(0.1)  # Polling interval


def handle_user_input():
    global keep_running
    while keep_running:
        user_input = input()
        cmd_queue.put(user_input)
        if user_input.lower() == 'exit':
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        myname = sys.argv[1]

    screen = Screen.open()
    frame = ScrollingFrame(screen)
    # Start user input handling in a separate thread
    #input_thread = Thread(target=handle_user_input)
    #input_thread.start()

    response = send(f'Hallo, Eg eri {myname}')
    frame.add_line(f"Received {response}")

    frame.add_line(response[0])
    if response[0] == 'P':
        frame.add_line('yey!')
        playerId = response[1]
        update_thread = Thread(target=get_updates, args=(frame,))
        update_thread.daemon = True  # Daemonize the thread to close it when the main program exits
        update_thread.start()
        # Play the Scene
        last_scene = None
        try:
            while True:
                screen.play([Scene([frame], -1)], stop_on_resize=True, start_scene=last_scene)
        except ResizeScreenError as e:
            last_scene = e.scene
        finally:
            screen.close()
    else:
        frame.add_line("😭")
        keep_running = False



