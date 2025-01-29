import tkinter as tk
import random
import time
from pynput.mouse import Controller
import threading

root = tk.Tk()
root.title("Erratic Human-like Mouse Movement with Pauses")
canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()

mouse_controller = Controller()

def human_like_mouse_move():
    last_x, last_y = 400, 300
    noise_factor = 5

    while True:
        move_x = random.uniform(-noise_factor, noise_factor)
        move_y = random.uniform(-noise_factor, noise_factor)
        
        new_x = last_x + move_x
        new_y = last_y + move_y
        
        new_x = max(0, min(800, new_x))
        new_y = max(0, min(600, new_y))

        mouse_controller.position = (new_x, new_y)

        canvas.create_line(last_x, last_y, new_x, new_y, fill='red', width=2)

        last_x, last_y = new_x, new_y

        time.sleep(random.uniform(0.2, 1.5))

mouse_thread = threading.Thread(target=human_like_mouse_move)
mouse_thread.daemon = True
mouse_thread.start()

root.mainloop()
