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
from Screens.home_screen import home_screen
from Screens.main_screen import main_screen
from Screens.settings_screen import settings_screen
from global_var import *


class ParpadeatronApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(MAIN_TITLE_APP)
        self.root.geometry("400x320")
        self.root.configure(bg=COLOR_BG_WINDOW_BLUE)
        self.root.resizable(False, False)
        
        self.db = Database()
        self.start_time = None

        # Control variables
        self.is_running = False
        self.reminder_thread = None
        
        self.load_custom_font()
        self.center_window()
        self.setup_icon()
        
        
        self.show_main_screen()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_custom_font(self):
        try:
            #font_path = self.resource_path("Screens/Recursos/ARLRDBD.ttf")
            self.custom_font = tkFont.Font(family="Arial Rounded MT Bold", size=24)
        except Exception as e:
            print(f"Error al cargar la fuente: {e}")
            self.custom_font = tkFont.Font(family="Arial", size=24, weight="bold")

    # def resource_path(self, relative_path):
    #     try:
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #     return os.path.join(base_path, relative_path)

    def center_window(self):
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        current_width = self.root.winfo_width()
        current_high = self.root.winfo_height()

        x = (screen_width - current_width) // 2
        y = (screen_height - current_high) // 2
        self.root.geometry(f"{current_width}x{current_high}+{x}+{y}")

    def setup_icon(self):
        try:
            #icon_path = self.resource_path("Screens/Assets/icon_parpadeatron.ico")
            os.chdir(os.path.dirname(__file__))
            icon_path = "Screens/Assets/icon_parpadeatron.ico"
            if os.path.exists(icon_path):
                if sys.platform.startswith('win'):
                    self.root.iconbitmap(icon_path)
                else:
                    icon = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")

    def clean_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_logo(self, frame):
        try:
            #eye_image_path = self.resource_path("Screens/Assets/eye_title.png")
            os.chdir(os.path.dirname(__file__))
            eye_image = Image.open("Screens/Assets/eye_title.png")
            target_height = 80
            aspect_ratio = eye_image.width / eye_image.height
            target_width = int(target_height * aspect_ratio)
            eye_image = eye_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            self.eye_photo = ImageTk.PhotoImage(eye_image)
            tk.Label(frame, image=self.eye_photo, bg=COLOR_BG_WINDOW_BLUE).pack()
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            tk.Label(frame, text="👁️", font=('Arial', 48), bg=COLOR_BG_WINDOW_BLUE, fg='white').pack()

    def create_button(self, frame, text_btn, command_btn):
        button = tk.Button(
            frame,
            text=text_btn,
            command=command_btn,
            font=('Arial', 12, 'bold'),
            bg=COLOR_BUTTON_GREEN,
            fg='white',
            relief='flat',
            width=15,
            height=2,
            cursor='hand2'
        )
        button.pack(pady=10)

        return button
    
    

    def create_reminder_window(self):
        opacity = 0.35
        reminder = tk.Toplevel()
        reminder.overrideredirect(True)
        reminder.attributes('-alpha', opacity)
        reminder.configure(bg='lightgray')
        reminder.attributes('-topmost', True)
        
        screen_width = reminder.winfo_screenwidth()
        screen_height = reminder.winfo_screenheight()
        width = int(screen_width * 0.17)
        height = int(screen_height * 0.22)
        
        x = (screen_width - width) // 2
        y = screen_height - height - SCREEN_SPACING
        
        reminder.geometry(f"{width}x{height}+{x}+{y}")
        
        # GIF Frame
        reminder_frame = tk.Frame(reminder, bg='lightgray')
        reminder_frame.pack(expand=True)
        
        try:
            # Cargar el gif usando resource_path
            #gif_path = self.resource_path("Screens/Assets/eye.gif")
            os.chdir(os.path.dirname(__file__))
            gif = Image.open("Screens/Assets/eye.gif")
            
            # Calcular el tamaño máximo manteniendo la proporción
            max_size = min(width * 0.8, height * 0.8)
            aspect_ratio = gif.width / gif.height
            if aspect_ratio > 1:
                gif_width = int(max_size)
                gif_height = int(max_size / aspect_ratio)
            else:
                gif_height = int(max_size)
                gif_width = int(max_size * aspect_ratio)
            
            # Crear una lista para almacenar los frames
            self.frames = []
            total_duration = 3000  # 3 segundos en milisegundos
            
            try:
                # Contar el número total de frames
                frame_count = sum(1 for _ in ImageSequence.Iterator(gif))
                
                # Calcular el intervalo entre frames para que la animación dure 3 segundos
                self.frame_interval = total_duration // frame_count
                
                # Procesar cada frame
                for frame in ImageSequence.Iterator(gif):
                    frame = frame.resize((gif_width, gif_height), Image.Resampling.LANCZOS)
                    frame_tk = ImageTk.PhotoImage(frame)
                    self.frames.append(frame_tk)
            except Exception as e:
                print(f"Error procesando frames del gif: {e}")
            
            # Crear el label para mostrar el gif
            self.gif_label = tk.Label(reminder_frame, bg='lightgray')
            self.gif_label.pack()
            
            # Iniciar la animación
            self.animate_gif(0, reminder)
            
        except Exception as e:
            print(f"Error al cargar el gif: {e}")
            tk.Label(reminder_frame, text="👁️", font=('Arial', 48), bg='lightgray').pack()
        
        return reminder


    def animate_gif(self, frame_idx, reminder):
        if not reminder.winfo_exists():
            return
        
        if self.frames:  # Verificar que hay frames disponibles
            frame = self.frames[frame_idx]
            self.gif_label.configure(image=frame)
            next_frame = (frame_idx + 1) % len(self.frames)
            reminder.after(self.frame_interval, self.animate_gif, next_frame, reminder)

    def show_reminder(self):
        reminder = self.create_reminder_window()
        self.root.after(3000, reminder.destroy)

    def reminder_loop(self):
        while self.is_running:
            self.root.after(0, self.show_reminder)
            time.sleep(10)



    def on_closing(self):
        if self.is_running and self.start_time:
            total_time = datetime.now() - self.start_time
            str_time = str(timedelta(seconds=int(total_time.total_seconds())))
            self.db.register_time(str_time)
        
        self.is_running = False
        if self.reminder_thread:
            self.reminder_thread.join(timeout=1)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def show_home_screen(self):
        self.clean_window()
        home_screen(self)

    def show_main_screen(self):
        self.clean_window()
        main_screen(self)

    def show_settings_screen(self):
        self.clean_window()
        settings_screen(self)


if __name__ == "__main__":
    app = ParpadeatronApp()
    app.run()