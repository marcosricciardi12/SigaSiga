import cv2
import time
import threading
import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

class VideoGenerator:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.video_writer = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.width, self.height))
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.stop_timer = False

    def generate_frame(self, team_local, team_visitor, points_local, points_visitor, time_left):
        frame = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(frame)

        # Dibujar los datos en la imagen
        draw.text((50, 50), f'Local: {team_local}', fill=(0, 0, 0))
        draw.text((50, 100), f'Visitor: {team_visitor}', fill=(0, 0, 0))
        draw.text((50, 150), f'Points Local: {points_local}', fill=(0, 0, 0))
        draw.text((50, 200), f'Points Visitor: {points_visitor}', fill=(0, 0, 0))
        draw.text((50, 250), f'Time Left: {time_left}', fill=(0, 0, 0))

        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        return frame

    def start_timer(self):
        while not self.stop_timer:
            # Actualizar los datos del cronómetro y generar el cuadro del video
            time_left = self.get_time_left()
            frame = self.generate_frame("Local Team", "Visitor Team", 10, 5, time_left)
            self.video_writer.write(frame)
            time.sleep(1)

    def start(self):
        self.stop_timer = False
        threading.Thread(target=self.start_timer).start()

    def stop(self):
        self.stop_timer = True
        self.video_writer.release()

    def get_time_left(self):
        # Aquí implementa la lógica para obtener el tiempo restante
        return "00:00"


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Video Generator')
        self.master.geometry('400x200')

        self.video_generator = None

        self.team_local_label = tk.Label(master, text="Local Team:")
        self.team_local_label.grid(row=0, column=0)
        self.team_local_entry = tk.Entry(master)
        self.team_local_entry.grid(row=0, column=1)

        self.team_visitor_label = tk.Label(master, text="Visitor Team:")
        self.team_visitor_label.grid(row=1, column=0)
        self.team_visitor_entry = tk.Entry(master)
        self.team_visitor_entry.grid(row=1, column=1)

        self.points_local_label = tk.Label(master, text="Points Local:")
        self.points_local_label.grid(row=2, column=0)
        self.points_local_value = tk.IntVar()
        self.points_local_value.set(0)
        self.points_local_display = tk.Label(master, textvariable=self.points_local_value)
        self.points_local_display.grid(row=2, column=1)
        self.points_local_add_button = tk.Button(master, text="+", command=self.add_points_local)
        self.points_local_add_button.grid(row=2, column=2)
        self.points_local_subtract_button = tk.Button(master, text="-", command=self.subtract_points_local)
        self.points_local_subtract_button.grid(row=2, column=3)

        self.points_visitor_label = tk.Label(master, text="Points Visitor:")
        self.points_visitor_label.grid(row=3, column=0)
        self.points_visitor_value = tk.IntVar()
        self.points_visitor_value.set(0)
        self.points_visitor_display = tk.Label(master, textvariable=self.points_visitor_value)
        self.points_visitor_display.grid(row=3, column=1)
        self.points_visitor_add_button = tk.Button(master, text="+", command=self.add_points_visitor)
        self.points_visitor_add_button.grid(row=3, column=2)
        self.points_visitor_subtract_button = tk.Button(master, text="-", command=self.subtract_points_visitor)
        self.points_visitor_subtract_button.grid(row=3, column=3)

        self.start_button = tk.Button(master, text="Start", command=self.start_video)
        self.start_button.grid(row=4, column=0)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_video)
        self.stop_button.grid(row=4, column=1)

    def add_points_local(self):
        self.points_local_value.set(self.points_local_value.get() + 1)

    def subtract_points_local(self):
        self.points_local_value.set(self.points_local_value.get() - 1)

    def add_points_visitor(self):
        self.points_visitor_value.set(self.points_visitor_value.get() + 1)

    def subtract_points_visitor(self):
        self.points_visitor_value.set(self.points_visitor_value.get() - 1)

    def start_video(self):
        self.video_generator = VideoGenerator(1280, 720, 30)
        self.video_generator.start()

    def stop_video(self):
        if self.video_generator:
            self.video_generator.stop()


def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()