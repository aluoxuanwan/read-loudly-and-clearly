from moviepy.editor import VideoFileClip

# 测试视频路径（可以是任意视频文件）
video_path = "fa1cd1ff-256b-4234-a8d9-be04bc500430_240p.mp4"

# 加载视频
video = VideoFileClip(video_path)

# 打印视频时长
print(f"视频时长: {video.duration} 秒")