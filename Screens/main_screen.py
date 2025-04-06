import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from PIL import Image, ImageTk, ImageSequence
import sys
from pathlib import Path
import os
from tkinter import font
import tkinter.font as tkFont
from Database.database import Database
from datetime import datetime, timedelta
from global_var import * 

def main_screen(app):
    
    current_width = app.root.winfo_width()
    app.root.geometry(f"{current_width}x{300}")
    app.center_window()

    main_frame = tk.Frame(app.root, bg=COLOR_BG_WINDOW_BLUE)
    main_frame.pack(expand=True, fill='both', padx=10, pady=10)

    app.show_logo(main_frame)

    tk.Label(
        main_frame, 
        text="Parpadeatron", 
        font=app.custom_font, 
        fg='white', 
        bg=COLOR_BG_WINDOW_BLUE
    ).pack(pady=10)

    last_use_time = app.db.get_last_time()
    use_label = tk.Label(
        main_frame, 
        text=f"Last time of use: {last_use_time}", 
        font=('Arial', 12), 
        fg='white', 
        bg=COLOR_BG_WINDOW_BLUE 
    )
    use_label.pack(pady=(10,10))

    toggle_button = app.create_button(
        main_frame, 
        "Start", 
        lambda: toggle_reminder(toggle_button, use_label)
    )
    toggle_button.bind('<Enter>', lambda event: on_enter(toggle_button))
    toggle_button.bind('<Leave>', lambda event: on_leave(toggle_button))
    
    toggle_button.pack(side="top", padx=5, pady=(10, 5))

    def toggle_reminder(toggle_button, use_label):
        if not app.is_running:
            app.is_running = True
            app.start_time = datetime.now()
            toggle_button.config(
                text="Stop", 
                bg= COLOR_BUTTON_RED
            )
            app.reminder_thread = threading.Thread(target=app.reminder_loop)
            app.reminder_thread.daemon = True
            app.reminder_thread.start()
        else:
            app.is_running = False
            toggle_button.config(
                text="Start", 
                bg= COLOR_BUTTON_GREEN
            )
            if app.start_time:
                total_time = datetime.now() - app.start_time
                str_time = str(timedelta(seconds=int(total_time.total_seconds())))
                app.db.register_time(str_time)
                use_label.config(text=f"Last time of use: {str_time}")
                app.start_time = None
    
    def on_enter(button):
        if button['text'] == "Stop":
            button['bg'] = COLOR_BUTTON_RED_HOVER
        else:
            button['bg'] = COLOR_BUTTON_GREEN_HOVER

    def on_leave(button):
        if button['text'] == "Stop":
            button['bg'] = COLOR_BUTTON_RED
        else:
            button['bg'] = COLOR_BUTTON_GREEN

    





    