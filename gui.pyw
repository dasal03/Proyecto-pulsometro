'''   
   Este programa es una GUI para la monitorización de los datos de un sensor de pulsos cardiacos, a través de la comunicación serial.
   Para ejecutarla es necesario instalar las librerias:
   - serial (pip install serial)
   - threading (pip install threading)
   - pandas (pip install pandas)

    Para ejecutar el programa es necesario conectar el Arduino a la PC y enviar datos por el puerto serial.
'''

from tkinter import *
import serial
import threading
import time
import csv
import pandas as pd

# Global variables
PROGRAM_NAME = "Pulsiometro"
PROGRAM_ICO = 'logo.ico'

class DataLogger:
    live_label_running = True
    text_content = []

    def __init__(self, root):
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.root.bg = "white"
        self.init_gui()

    def frame_creation(self):
        self.left_frame = Frame(root, bd=2, relief=SUNKEN, background="white")
        self.left_frame.pack(side=LEFT, fill=Y, expand=False)
        self.bottom_frame = Frame(
            root, bd=2, relief=SUNKEN, background="white")
        self.bottom_frame.pack(side=BOTTOM, fill=X, expand=False)
        self.right_frame = Frame(root, bd=2, relief=SUNKEN, background="white")
        self.right_frame.pack(side=RIGHT, fill='both', expand=True)

    def text_widget(self):
        self.live_text = Text(self.right_frame, height=15, width=40)
        self.live_text.pack(side=LEFT, fill='both', expand=True, padx=5)

    def get_data(self):
        filename = self.file_entry.get()+".csv"
        if filename != ".csv":
            try:
                ser = serial.Serial(self.com_entry.get())
                ser_bytes = ser.readline()
                decoded_bytes = str(
                    ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                data = decoded_bytes.split(str(self.split_entry.get()))
                feilds = []
                headers = ""

                for x in data:
                    feilds.append("Variable ")
                with open(filename, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile, lineterminator='\n')
                    csvwriter.writerow(feilds)
                    for pos in feilds:
                        headers + headers + str(pos)

                while True:
                    try:
                        ser_bytes = ser.readline()
                        decoded_bytes = str(
                            ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                        data = decoded_bytes.split(' ')
                        with open(filename, 'a') as csvfile:
                            csvwriter = csv.writer(
                                csvfile, lineterminator='\n')
                            csvwriter.writerow(data)
                            print("Data written to file")

                        self.live_text.insert(END, str(data) + "\n")
                        self.live_text.see(END)
                        print(data)

                        if DataLogger.live_label_running == False:
                            break
                    except:
                        print("No data")
                        break
            except:
                self.live_text.insert(END, "No data")
                DataLogger.live_label_running = False
                self.toggle_start()
        else:
            self.live_text.insert(END, "No data")
            DataLogger.live_label_running = False
            self.toggle_start()

    def get_data_thread(self):
        self.thread2 = threading.Thread(
            target=self.get_data, name="get_data_thread")
        self.thread2.daeamon = False
        self.thread2.start()

    def start_data(self):
        DataLogger.live_label_running = True
        self.get_data_thread()
        self.toggle_start()

    def pause_data(self):
        DataLogger.live_label_running = False
        self.toggle_start()

    def stop_data(self):
        DataLogger.live_label_running = False
        self.live_text_delete(1.0, END)
        self.toggle_start()

    def live_text_delete(self, start, end):
        self.live_text.delete(start, end)

    def toggle_start(self):
        if DataLogger.live_label_running == True:
            self.start_button.configure(state='disabled')
        else:
            self.start_button.configure(state='normal')

    def left_widgets(self):
        file_label = Label(self.left_frame, text="File Name:",
                           background='white').grid(row=0, column=0)
        self.file_entry = Entry(self.left_frame, justify='center', border=2)
        self.file_entry.grid(row=1, column=0)

        COM_label = Label(self.left_frame, text="COM Port:",
                          background='white').grid(row=2, column=0)
        self.com_entry = Entry(self.left_frame, justify='center', border=2)
        self.com_entry.grid(row=3, column=0)
        self.com_entry.insert(0, "COM3")

        split_label = Label(self.left_frame, text="Split at:",
                            background='white').grid(row=4, column=0)
        self.split_entry = Entry(self.left_frame, justify='center', border=2)
        self.split_entry.grid(row=5, column=0)
        self.split_entry.insert(0, " ")

    def bottom_buttons(self):
        self.start_button = Button(self.bottom_frame, text="Start", command=lambda: self.start_data(),
        background='green', fg='black', width=10)
        self.start_button.grid(row=3, column=0)

        self.pause_button = Button(self.bottom_frame, text="Pause", command=lambda: self.pause_data(),
        background='yellow', fg='black', width=10)
        self.pause_button.grid(row=3, column=1)

        self.stop_button = Button(self.bottom_frame, text="Stop", command=lambda: self.stop_data(), 
        background='red', fg='black', width=10)
        self.stop_button.grid(row=3, column=2)

    def init_gui(self):
        self.frame_creation()
        self.text_widget()
        self.left_widgets()
        self.bottom_buttons()


if __name__ == "__main__":
    root = Tk()
    root.iconbitmap(PROGRAM_ICO)
    root.geometry("500x300")
    root.resizable(width=False, height=False)
    DataLogger(root)
    root.mainloop()
