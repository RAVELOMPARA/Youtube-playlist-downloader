import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox  # module nécessaire pour la boîte de dialogue
from pytube import Playlist


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Téléchargeur de playlist YouTube")
        self.create_widgets()

    def create_widgets(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Quitter", command=self.master.quit)

        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edition", menu=editmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=helpmenu)
        helpmenu.add_command(label="A propos", command=self.show_about)

        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        url_label = tk.Label(main_frame, text="URL de la playlist YouTube :")
        url_label.pack(side="left", padx=5)

        self.url_entry = tk.Entry(main_frame)
        self.url_entry.pack(side="left", padx=5)

        format_label = tk.Label(main_frame, text="Format de téléchargement :")
        format_label.pack(side="left", padx=5)

        self.format_var = tk.StringVar(value="mp4")
        self.format_options = ["mp4", "mp3"]
        format_dropdown = ttk.Combobox(main_frame, textvariable=self.format_var, values=self.format_options, state="readonly")
        format_dropdown.pack(side="left", padx=5)

        storage_label = tk.Label(main_frame, text="Emplacement de stockage :")
        storage_label.pack(side="left", padx=5)

        self.storage_path = tk.StringVar()
        storage_button = tk.Button(main_frame, text="Parcourir", command=self.select_storage_path)
        storage_button.pack(side="left", padx=5)

        download_button = tk.Button(main_frame, text="Télécharger", command=self.download_playlist)
        download_button.pack(side="left", padx=5)

        
        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(side="left", padx=5)

    def select_storage_path(self):
        path = filedialog.askdirectory()
        self.storage_path.set(path)

    def download_playlist(self):
        url = self.url_entry.get()
        playlist = Playlist(url)
        format = self.format_var.get()
        storage_path = self.storage_path.get()
        num_videos = len(playlist.video_urls)
        self.progress_bar.config(maximum=num_videos)
        for i, video_url in enumerate(playlist.video_urls, start=1):
            self.progress_bar['value'] = i
            self.master.update()
            video = playlist.videos[i - 1]
            video.streams.filter(file_extension=format).first().download(output_path=storage_path)
            print(f"{video.title} téléchargée. ({i}/{num_videos})")
        print("Toutes les vidéos de la playlist ont été téléchargées.")

    def show_about(self):
        messagebox.showinfo("A propos", "Ce programme a été réalisé par ...")

        
root = tk.Tk()
app = Application(master=root)
app.mainloop()
