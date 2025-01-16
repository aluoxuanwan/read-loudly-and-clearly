import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
from mutagen.mp3 import MP3


class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("音频播放器")
        self.root.geometry("400x250")
        self.root.configure(bg="#f0f0f0")
        
        # 初始化pygame混音器
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        
        # 状态变量
        self.current_file = None
        self.is_playing = False
        self.total_length = 0
        self.after_id = None
        self.dragging = False
        
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
        self.file_label.pack(pady=10)
        
        # 进度条框架
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.progress_var,
            command=self.on_progress_change
        )
        self.progress_bar.pack(fill=tk.X)
        
        # 绑定拖动事件
        self.progress_bar.bind("<ButtonPress-1>", self.start_drag)
        self.progress_bar.bind("<ButtonRelease-1>", self.end_drag)
        
        # 时间标签
        self.time_label = ttk.Label(
            progress_frame,
            text="00:00 / 00:00"
        )
        self.time_label.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
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
        
        # 开始更新进度
        self.update_progress()
    
    def format_time(self, seconds):
        """将秒数转换为 MM:SS 格式"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
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
            
            # 获取音频长度
            audio = MP3(file_path)
            self.total_length = audio.info.length
            self.progress_bar.configure(to=self.total_length)
            self.progress_var.set(0)
            self.time_label.config(
                text=f"00:00 / {self.format_time(self.total_length)}"
            )
            
            # 加载文件但不播放
            pygame.mixer.music.load(self.current_file)
            self.play_button["state"] = "normal"
            self.play_button.config(text="播放")
    
    def start_drag(self, event):
        """开始拖动进度条"""
        self.dragging = True
    
    def end_drag(self, event):
        """结束拖动进度条"""
        self.dragging = False
        if self.current_file:
            seek_time = self.progress_var.get()
            if self.is_playing:
                pygame.mixer.music.play(start=seek_time)
            else:
                pygame.mixer.music.play(start=seek_time)
                pygame.mixer.music.pause()
    
    def on_progress_change(self, value):
        """处理进度条拖动"""
        if self.current_file and not self.dragging:
            value = float(value)
            if abs(value - self.get_current_time()) > 1:
                pygame.mixer.music.play(start=value)
                if not self.is_playing:
                    pygame.mixer.music.pause()
    
    def get_current_time(self):
        """获取当前播放时间"""
        if not pygame.mixer.music.get_busy() or not self.is_playing:
            return 0
        return pygame.mixer.music.get_pos() / 1000.0
    
    def toggle_play(self):
        if not self.is_playing:
            if self.current_file:
                current_pos = self.progress_var.get()
                pygame.mixer.music.play(start=current_pos)
                self.is_playing = True
                self.play_button.config(text="暂停")
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="播放")
    
    def update_progress(self):
        """更新进度条和时间显示"""
        if self.current_file:
            current_time = self.get_current_time()
            if current_time >= 0:
                if not self.dragging:  # 仅在未拖动时更新进度条
                    self.progress_var.set(current_time)
                self.time_label.config(
                    text=f"{self.format_time(current_time)} / "
                         f"{self.format_time(self.total_length)}"
                )
        
        # 每100毫秒更新一次
        self.after_id = self.root.after(100, self.update_progress)
    
    def __del__(self):
        """清理资源"""
        try:
            if self.after_id:
                self.root.after_cancel(self.after_id)
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except (pygame.error, tk.TclError):
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()
