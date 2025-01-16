import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os


class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("音频播放器")
        self.root.geometry("400x200")
        self.root.configure(bg="#f0f0f0")
        
        # 初始化pygame混音器
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        
        # 状态变量
        self.current_file = None
        self.is_playing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件名标签
        self.file_label = ttk.Label(
            main_frame, 
            text="未选择文件", 
            wraplength=350
        )
        self.file_label.pack(pady=20)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # 加载按钮
        self.load_button = ttk.Button(
            button_frame, 
            text="加载音频",
            command=self.load_audio
        )
        self.load_button.pack(side=tk.LEFT, padx=10)
        
        # 播放按钮
        self.play_button = ttk.Button(
            button_frame,
            text="播放",
            command=self.toggle_play
        )
        self.play_button.pack(side=tk.LEFT, padx=10)
        self.play_button["state"] = "disabled"
    
    def load_audio(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("MP3 文件", "*.mp3"), ("所有文件", "*.*")]
        )
        if file_path:
            # 停止当前播放
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.is_playing = False
            
            # 加载新文件
            self.current_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.play_button["state"] = "normal"
            self.play_button.config(text="播放")
            
            # 加载文件但不播放
            pygame.mixer.music.load(self.current_file)
    
    def toggle_play(self):
        if not self.is_playing:
            if self.current_file:
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_button.config(text="暂停")
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="播放")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop() 