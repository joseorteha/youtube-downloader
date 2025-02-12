import tkinter as tk
from tkinter import ttk
import threading
import os
from click import progressbar
import yt_dlp

# Función para descargar el video
def download_video():
    video_url = entry.get()
    save_path = r"C:\Users\joseo\Documents\PROYECTOS 2024\Py"  # Reemplaza con la ruta donde deseas guardar el video
    try:
        # Configurar opciones para yt-dlp
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [on_progress],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'ffmpeg_location': r'C:\ffmpeg-7.1\bin',  # Especifica la ruta de ffmpeg
        }
        
        # Deshabilitar el botón de descarga
        button.config(state=tk.DISABLED)
        
        # Crear barra de progreso y etiqueta
        progress_label = tk.Label(window, text="Downloading...")
        progress_label.pack()
        progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
        progress_bar.pack()
        
        # Iniciar la descarga en un hilo separado
        download_thread = threading.Thread(target=perform_download, args=(video_url, ydl_opts, progress_bar))
        download_thread.start()
    except Exception as e:
        print("Error:", str(e))
        status_label.config(text="Error: " + str(e))

# Función para realizar la descarga en segundo plano
def perform_download(video_url, ydl_opts, progress_bar):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed!")
        status_label.config(text="Download completed!")
    except Exception as e:
        print("Error:", str(e))
        status_label.config(text="Error: " + str(e))
    finally:
        # Detener la barra de progreso
        progress_bar.stop()
        # Habilitar el botón de descarga
        button.config(state=tk.NORMAL)

# Función para mostrar el progreso de la descarga
def on_progress(d):
    if d['status'] == 'downloading':
        progress_percent = int(d['_percent_str'].replace('%', ''))
        window.after(0, update_progress, progressbar, progress_percent)

# Función para actualizar la barra de progreso en el hilo principal
def update_progress(progress_bar, progress_percent):
    progress_bar['value'] = progress_percent

# Crear la ventana principal
window = tk.Tk()
window.title("YouTube Video Downloader")

# Configurar las dimensiones de la ventana
window_width = 400
window_height = 250
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Crear la etiqueta y el campo de entrada
label = tk.Label(window, text="Enter YouTube video URL:")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Crear el botón de descarga
button = tk.Button(window, text="Download", command=download_video)
button.pack()

# Crear la etiqueta de estado
status_label = tk.Label(window, text="")
status_label.pack()

# Iniciar el bucle de eventos de Tkinter
window.mainloop()