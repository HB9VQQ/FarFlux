import tkinter as tk
from tkinter import messagebox
from tkinter.constants import DISABLED, E, N, NORMAL, S, VERTICAL, W

import json
import os
import sys

from farflux import connection_test, schedule_task

class App(tk.Tk):
    '''app controller definition'''
    def __init__(self, *args, **kwargs, ):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames = {}

        #   *****   CONTAINER   *****
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
       
        #   *****   FILE MENU   *****
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Status", command=lambda: self.show_frame(Landing))
        filemenu.add_command(label="Settings", command=lambda: self.show_frame(Settings))
        filemenu.add_command(label="About", command=lambda: self.show_frame(About))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit)
        tk.Tk.config(self, menu=menubar)

        #   *****   VIEWS   *****
        for view in [Landing, Settings, About]:
            frame = view(container, self)
            self.frames[view] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Landing)

    def show_frame(self, controller):
        '''frame controller'''
        frame = self.frames[controller]
        frame.tkraise()

#   *****   PAGES   *****
class Landing(tk.Frame):
    ''''''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.logs_path = f'C:/Users/{os.getlogin()}/AppData/Roaming/Afreet/Products/Faros/BeaconLogs'
        self.get_values()

        #   *****   WIDGETS   *****
        label = tk.Label(self, text="FarFlux Status")
        label.pack(pady=15)

        status_frame = tk.Frame(self, bg='#FFFFFF')
        status_frame.pack()

        logs_label = tk.Label(status_frame, text='Faros logs directory:', width=20, bg='#FFFFFF') 
        logs_label.grid(row=1, column=0, pady=3)
        self.logs_status = tk.Label(status_frame, width=20, bg='#FFFFFF',
                            text=['Available' if self.logs_available == True else 'Unavailable'],
                            fg=['green' if self.logs_available == True else 'red'])
        self.logs_status.grid(row=1, column=1, pady=3)

        db_label = tk.Label(status_frame, text='InfluxDB connection test:', width=20, bg='#FFFFFF') 
        db_label.grid(row=2, column=0, pady=3)
        self.db_status = tk.Label(status_frame,  width=20, bg='#FFFFFF',
                             text=['Successful' if self.db_connection[0] == 1 else 'Failed'],
                             fg=['green' if self.db_connection[0] == 1 else 'red'])
        self.db_status.grid(row=2, column=1, pady=3)

        refresh_btn = tk.Button(status_frame, text='Refresh', command=self.refresh)
        refresh_btn.grid(row=1, rowspan=2, column=2, padx=20)

        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(info_frame, orient=VERTICAL)
        scrollbar.grid(row=0, column=1, sticky=N+S+E)
        self.info_text = tk.Text(info_frame, width=65, height=6, yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.info_text.yview)
        self.info_text.insert(1.0, f'{self.status_message}')
        self.info_text.grid(row=0, column=0)

        self.schedule_button = tk.Button(info_frame, text='Schedule\nUpload Task', 
                                    command=self.schedule, width=20, state=self.status)
        self.schedule_button.grid(row=1, column=0, pady=10)

    #   *****   COMMAND FUNCTIONS   *****
    def check_db(self):
        ''''''
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as json_file:
                self.config = json.load(json_file)
            self.url = self.config['URL']
            self.org_id = self.config['ORG_ID']
            self.bucket = self.config['BUCKET']
            self.token = self.config['TOKEN']
            self.db_connection = connection_test(url=self.url, 
                                                 org_id=self.org_id, 
                                                 bucket=self.bucket, 
                                                 token=self.token)
        else:
            self.db_connection = (-1, 'Please provide InfluxDB settings:\nFile > Settings')
        return self.db_connection

    def refresh(self):
        ''''''
        self.get_values()
        self.logs_status.configure(text=['Available' if self.logs_available == True else 'Unavailable'],
                                fg=['green' if self.logs_available == True else 'red'])
        self.db_status.configure(text=['Successful' if self.db_connection[0] == 1 else 'Failed'],
                              fg=['green' if self.db_connection[0] == 1 else 'red'])
        self.schedule_button.configure(state=self.status)
        self.info_text.delete(1.0,'end')
        self.info_text.insert(1.0, self.status_message)
            
    def get_values(self):
        ''''''
        self.logs_available = True if os.path.exists(self.logs_path) else False
        self.db_connection = self.check_db()
        db_status = self.db_connection[0]
        db_message = self.db_connection[1]
        
        info_logs = f'Beacon logs directory not found:\n{self.logs_path}'

        if self.logs_available == False and db_status == 1:
            self.status = DISABLED
            self.status_message = info_logs
        elif self.logs_available == True and db_status != 1:
            self.status = DISABLED
            self.status_message = db_message
        elif self.logs_available == False and db_status != 1:
            self.status = DISABLED
            self.status_message = f'{info_logs}\n\n{db_message}'
        else:
            self.status = NORMAL
            self.status_message = 'Configuration complete!'
        
    def schedule(self):
        ''''''
        schedule_task()
        messagebox.showinfo("Upload Task Created", 
                            "Beacon data will be uploaded every 15 minutes.\n\nClosing application.")
        sys.exit()

class Settings(tk.Frame):
    ''''''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.url_input = tk.StringVar()
        self.org_input = tk.StringVar()
        self.bucket_input = tk.StringVar()
        self.token_input = tk.StringVar()
        self.port_input = tk.IntVar()
        self.port_input.set(433)
        self.port_state = tk.IntVar()
        self.port_state.set(0)

        label = tk.Label(self, text="InfluxDB Settings")
        label.pack(pady=10)

        inner_frame = tk.Frame(self)
        inner_frame.pack()

        url_label = tk.Label(inner_frame, text="InfluxDB URL:", width=15, anchor=W) 
        url_label.grid(row=1, column=0, pady=10)
        self.url_entry = tk.Entry(inner_frame, width=70, textvariable=self.url_input)
        self.url_entry.grid(row=1,column=1, pady=10, columnspan=6)
        
        org_label = tk.Label(inner_frame, text="OrganizationID:", width=15, anchor=W)
        org_label.grid(row=2, column=0, pady=10)
        self.org_entry = tk.Entry(inner_frame, width=70, textvariable=self.org_input)
        self.org_entry.grid(row=2,column=1, pady=10, columnspan=6)

        bucket_label = tk.Label(inner_frame, text="Bucket:", width=15, anchor=W)
        bucket_label.grid(row=3, column=0, pady=10)
        self.bucket_entry = tk.Entry(inner_frame, width=70, textvariable=self.bucket_input)
        self.bucket_entry.grid(row=3,column=1, pady=10, columnspan=6)
        
        token_label = tk.Label(inner_frame, text="Token:", width=15, anchor=W)
        token_label.grid(row=4, column=0, pady=10)
        self.token_entry = tk.Entry(inner_frame, width=70, textvariable=self.token_input)
        self.token_entry.grid(row=4,column=1, pady=10, columnspan=6)

        self.port_check_btn = tk.Checkbutton(inner_frame, text="   Port:", width=12, anchor=W, 
                                             command=self.port_select, variable=self.port_state)
        self.port_check_btn.grid(row=5, column=0, pady=10)
        self.port_entry = tk.Entry(inner_frame, state=DISABLED, width=70, textvariable=self.port_input)
        self.port_entry.grid(row=5,column=1, pady=10, columnspan=6)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as json_file:
                self.config = json.load(json_file)
            self.url_entry.insert(0, self.config["URL"])
            self.org_entry.insert(0, self.config["ORG_ID"])
            self.bucket_entry.insert(0, self.config["BUCKET"])
            self.token_entry.insert(0, self.config["TOKEN"])
            if self.config["PORT"] == 433:
                self.port_input.set(self.config["PORT"])
                self.port_entry.configure(state=DISABLED)
                self.port_check_btn.deselect()
            else:
                self.port_input.set(self.config["PORT"])
                self.port_entry.configure(state=NORMAL)
                self.port_check_btn.select()
               
        self.apply_btn = tk.Button(inner_frame, text="Apply", command=lambda: self.apply(controller), 
                              width=15, state=DISABLED)
        self.apply_btn.grid(row=6,column=1, pady=5)
        self.apply_btn.after(500, self.refresh_apply)

        reset_btn = tk.Button(inner_frame, text="Reset", command=self.reset, width=15)
        reset_btn.grid(row=6,column=2, pady=5)
    
    def port_select(self):
        ''''''
        if self.port_state.get() == 1:
            if os.path.exists(CONFIG_FILE):
                self.port_input.set(self.config["PORT"])
            else:
                self.port_input.set(8086)
            self.port_entry.configure(state=NORMAL)
        else:
            self.port_input.set(433)
            self.port_entry.configure(state=DISABLED)

    def refresh_apply(self):
        '''
        '''
        a = self.url_entry.get()
        b = self.org_entry.get()
        c = self.bucket_entry.get()
        d = self.token_entry.get()
        self.apply_state = NORMAL if a and b and c and d != '' else DISABLED
        self.apply_btn.configure(state=self.apply_state)
        self.apply_btn.after(500, self.refresh_apply)

    def apply(self, controller):
        ''''''
        config = {
            "URL": self.url_input.get(),
            "ORG_ID": self.org_input.get(),
            "BUCKET": self.bucket_input.get(),
            "TOKEN": self.token_input.get(),
            "PORT": self.port_input.get()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        controller.show_frame(Landing)
        landing_page = controller.frames[Landing]
        landing_page.refresh()
        landing_page.tkraise()

    def reset(self):
        ''''''
        self.url_entry.delete(0,'end')
        self.org_entry.delete(0,'end')
        self.bucket_entry.delete(0,'end')
        self.token_entry.delete(0,'end')
        self.port_input.set(433)
        self.port_entry.configure(state=DISABLED)
        self.port_check_btn.deselect()
        try:
            os.remove(CONFIG_FILE)
        except FileNotFoundError:
            pass


class About(tk.Frame):
    ''''''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the about page.")
        label.pack(pady=10, padx=10)

#   *****   MAIN   *****
if __name__ == "__main__":
    if not os.path.exists(f'C:/Users/{os.getlogin()}/FarFlux'):
        os.mkdir(f'C:/Users/{os.getlogin()}/AppData/Roaming/FarFlux')
    CONFIG_FILE = f'C:/Users/{os.getlogin()}/AppData/Roaming/FarFlux/config.json'
    root=App()
    root.title('    FarFlux')
    root.wm_geometry("600x300")
    root.resizable(False, False)
    root.iconbitmap('radio_tower.ico')
    root.mainloop()