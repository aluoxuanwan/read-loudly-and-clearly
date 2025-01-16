from moviepy.editor import VideoFileClip
import os

# 视频文件路径
video_path = r"D:\yolo\test\朗读\read-loudly-and-clearly\10050000-0aff-0242-1863-08da63928e02_240p.mp4"

# 获取视频文件名（不带扩展名）
video_name = os.path.splitext(os.path.basename(video_path))[0]

# 生成输出音频文件路径（与视频文件在同一目录下）
output_audio_path = os.path.join(
    os.path.dirname(video_path),  # 视频文件所在目录
    f"{video_name}.mp3"          # 使用视频文件名作为音频文件名
)

# 加载视频文件
video = VideoFileClip(video_path)

# 提取音频
audio = video.audio

# 保存音频为 MP3 文件
audio.write_audiofile(output_audio_path)

print(f"音频已提取并保存到: {output_audio_path}")