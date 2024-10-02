import os
import subprocess
from PIL import Image

def generate_video_from_banner(banner_image_path, promo_text, output_video_path):
    try:
        banner = Image.open(banner_image_path).convert("RGBA")
        frames_dir = "static/output/frames"
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)

        for i in range(30):
            frame = banner.resize((int(banner.width * (1 + 0.01 * i)), int(banner.height * (1 + 0.01 * i))))
            frame_path = os.path.join(frames_dir, f"frame_{i}.png")
            frame.save(frame_path)

        video_output_path = os.path.join(output_video_path, "promo_video.mp4")
        ffmpeg_cmd = f"ffmpeg -y -framerate 30 -i {frames_dir}/frame_%d.png -c:v libx264 -r 30 -pix_fmt yuv420p {video_output_path}"
        subprocess.run(ffmpeg_cmd, shell=True)

        for file in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, file))

        return video_output_path
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
