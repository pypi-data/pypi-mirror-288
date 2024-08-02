import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp as youtube_dl
import os
import threading
import subprocess
import sys
from ttkthemes import ThemedTk

class YouTubeDownloaderApp:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("YouTube Downloader")
        self.root.geometry("400x400")
        
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#007BFF", foreground="black")
        style.configure("TLabel", background="#F0F0F0")
        style.configure("TEntry", padding=6, relief="flat")

        ttk.Label(self.root, text="Enter Video URL:").pack(pady=10, padx=10, anchor='w')
        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5, padx=10, anchor='w')

        ttk.Label(self.root, text="Select Output Path:").pack(pady=10, padx=10, anchor='w')
        self.output_path_entry = ttk.Entry(self.root, width=50)
        self.output_path_entry.pack(pady=5, padx=10, anchor='w')
        ttk.Button(self.root, text="Browse", command=self.select_path).pack(pady=10, padx=10, anchor='w')

        ttk.Label(self.root, text="Select Format:").pack(pady=10, padx=10, anchor='w')
        self.format_var = tk.StringVar(value='video')
        ttk.Radiobutton(self.root, text="Video", variable=self.format_var, value='video').pack(pady=5, padx=10, anchor='w')
        ttk.Radiobutton(self.root, text="Audio (MP3)", variable=self.format_var, value='audio').pack(pady=5, padx=10, anchor='w')

        ttk.Button(self.root, text="Download", command=self.start_download).pack(pady=20, padx=10, anchor='w')

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, path)

    def start_download(self):
        url = self.url_entry.get()
        path = self.output_path_entry.get()
        if not url or not path:
            messagebox.showwarning("Input Error", "Please enter both URL and output path.")
            return

        format_choice = self.format_var.get()
        if format_choice not in ['video', 'audio']:
            messagebox.showwarning("Format Error", "Please select a valid format.")
            return

        loading_dialog = tk.Toplevel(self.root)
        loading_dialog.title("Downloading")
        loading_dialog.geometry("300x150")
        loading_dialog.configure(bg='#2E3B4E')
        
        tk.Label(loading_dialog, text="Downloading... Please wait.", font=("Arial", 12), bg='#2E3B4E', fg='white').pack(pady=10)
        progress_var = tk.StringVar()
        progress_label = tk.Label(loading_dialog, textvariable=progress_var, font=("Arial", 10), bg='#2E3B4E', fg='white')
        progress_label.pack(pady=10)

        def update_progress(d):
            status = d.get('status', 'Downloading...')
            percent = d.get('percent', 0)
            if status == 'finished':
                progress_var.set('Download complete.')
            elif status == 'error':
                progress_var.set(f'Error: {d.get("error", "Unknown error")}')
            else:
                progress_var.set(f'{status}: {percent}%')

        def add_open_folder_button(file_path):
            open_folder_button = ttk.Button(loading_dialog, text="Show in Folder",
                                           command=lambda: open_folder(file_path))
            open_folder_button.pack(pady=10)

        download_func = self.download_video if format_choice == 'video' else self.download_audio
        threading.Thread(target=download_func, args=(url, path, update_progress, add_open_folder_button)).start()

    def download_video(self, url, path, progress_callback, open_folder_callback):
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: progress_callback(d)]
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(result)
            progress_callback({'status': 'finished'})
            open_folder_callback(file_path)
        except Exception as e:
            progress_callback({'status': 'error', 'error': str(e)})

    def download_audio(self, url, path, progress_callback, open_folder_callback):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [lambda d: progress_callback(d)]
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(result)
                file_path_mp3 = file_path.replace('.m4a', '.mp3')

                import time
                while not os.path.exists(file_path_mp3):
                    time.sleep(0.1)

                if os.path.exists(file_path_mp3):
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    progress_callback({'status': 'finished'})
                    open_folder_callback(file_path_mp3)
                else:
                    progress_callback({'status': 'error', 'error': 'MP3 file not found.'})
        except Exception as e:
            progress_callback({'status': 'error', 'error': str(e)})

def open_folder(file_path):
    try:
        if sys.platform == 'win32':
            os.startfile(os.path.dirname(file_path))
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', os.path.dirname(file_path)])
        else:
            subprocess.Popen(['xdg-open', os.path.dirname(file_path)])
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open folder: {str(e)}")
